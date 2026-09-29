#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import shlex
import subprocess
import time
from pathlib import Path
import sys
from typing import Any

import torch
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitunet_cubicasa.audit import audit_multiclass_split
from mitunet_cubicasa.dataset import CubiCasaMultiClassDataset, CubiCasaWallDataset, audit_source_resolutions, prepare_dataset
from mitunet_cubicasa.engine import (
    evaluate_model,
    evaluate_model_multiclass,
    save_evaluation_outputs,
    save_multiclass_evaluation_outputs,
    save_training_curves,
    threshold_search,
    train_one_epoch,
    train_one_epoch_multiclass,
)
from mitunet_cubicasa.losses import AsymmetricTverskyLoss, MultiHeadSegmentationLoss
from mitunet_cubicasa.model import build_mitunet, load_matching_weights, load_model_from_checkpoint
from mitunet_cubicasa.ontology import (
    ICON_CLASSES,
    MASK_SCHEMA_VERSION,
    TASK_BINARY_WALL,
    TASK_CUBICASA_MULTICLASS,
    deterministic_palette,
    enabled_structure_classes,
    mapping_hash,
    mapping_payload,
)
from mitunet_cubicasa.observability import (
    is_metric_improved,
    make_training_log_row,
    metric_mode,
    save_observability_plots,
    save_training_summary,
    validate_early_stopping_metric,
    write_training_log,
)
from mitunet_cubicasa.utils import (
    collect_environment,
    detect_device,
    load_yaml,
    read_csv_rows,
    save_json,
    save_yaml,
    seed_everything,
    setup_logging,
    timestamp,
    write_csv,
)
from mitunet_cubicasa.transforms import validate_experiment_image_size


DEFAULTS: dict[str, Any] = {
    "experiment_root": "experiments/cubicasa5k_mitunet",
    "cache_dir": "artifacts/cubicasa5k_wall_cache",
    "epochs": 30,
    "batch_size": 4,
    "image_size": 512,
    "resize_mode": "letterbox",
    "optimizer": "adam",
    "lr": 1e-4,
    "weight_decay": 0.0,
    "tversky_alpha": 0.6,
    "tversky_beta": 0.4,
    "threshold": 0.5,
    "seed": 42,
    "num_workers": 4,
    "amp": True,
    "gradient_accumulation_steps": 1,
    "grad_clip": None,
    "early_stopping_patience": 8,
    "early_stopping_metric": "val_iou",
    "early_stopping_min_delta": 0.0,
    "scheduler_patience": 3,
    "encoder_weights": "imagenet",
    "subtract_openings": False,
    "preview_count": 20,
    "threshold_search": True,
    "bootstrap_seed": 123,
    "reports_root": "reports/training_runs",
    "task_mode": TASK_BINARY_WALL,
    "include_optional_structure": False,
    "init_checkpoint": None,
    "structure_ce_weight": 1.0,
    "structure_dice_weight": 1.0,
    "icon_ce_weight": 1.0,
    "icon_dice_weight": 1.0,
    "structure_task_weight": 1.0,
    "icon_task_weight": 1.0,
    "use_recommended_ce_weights": True,
    "required_structure_classes": ["wall"],
    "required_icon_classes": ["window", "door"],
}


HISTORY_FIELDS = [
    "epoch",
    "train_loss",
    "val_loss",
    "val_dice",
    "val_iou",
    "learning_rate",
    "learning_rate_group_0",
    "lr",
    "epoch_time_seconds",
    "train_time_seconds",
    "validation_time_seconds",
    "peak_gpu_memory_allocated_mb",
    "peak_gpu_memory_reserved_mb",
    "physical_batch_size",
    "gradient_accumulation_steps",
    "effective_batch_size",
    "seconds_elapsed",
    "checkpoint_path",
    "best_checkpoint",
    "structure_ce",
    "structure_dice_loss",
    "structure_loss",
    "icon_ce",
    "icon_dice_loss",
    "icon_loss",
    "wall_dice",
    "wall_iou",
    "window_dice",
    "window_iou",
    "door_dice",
    "door_iou",
    "appliance_dice",
    "appliance_iou",
]


def resolve_image_size_config(cfg: dict[str, Any], cli_input_size: int | None = None) -> dict[str, Any]:
    cfg = dict(cfg)
    image_size = cfg.get("image_size")
    legacy_input_size = cfg.get("input_size")
    if cli_input_size is not None:
        if image_size is not None and int(image_size) != int(cli_input_size):
            raise ValueError(f"Conflicting --input-size={cli_input_size} and image_size={image_size}")
        image_size = cli_input_size
    if image_size is None:
        image_size = legacy_input_size if legacy_input_size is not None else DEFAULTS["image_size"]
    if legacy_input_size is not None and int(legacy_input_size) != int(image_size):
        raise ValueError(f"Conflicting config values: image_size={image_size} and input_size={legacy_input_size}")
    cfg["image_size"] = int(image_size)
    cfg["input_size"] = int(image_size)
    return cfg


def _command_line() -> str:
    return " ".join(shlex.quote(arg) for arg in [sys.executable, *sys.argv])


def _git_state() -> dict[str, Any]:
    def run_git(args: list[str]) -> str | None:
        try:
            return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
        except Exception:
            return None

    return {
        "commit": run_git(["rev-parse", "HEAD"]),
        "changed_files": (run_git(["status", "--short"]) or "").splitlines(),
    }


def _file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _manifest_checksums(manifest_paths: dict[str, Path]) -> dict[str, dict[str, Any]]:
    checksums: dict[str, dict[str, Any]] = {}
    for split, path in manifest_paths.items():
        with path.open("r", encoding="utf-8") as f:
            sample_count = max(0, sum(1 for _ in f) - 1)
        checksums[split] = {
            "path": str(path),
            "sha256": _file_sha256(path),
            "sample_count": sample_count,
        }
    return checksums


def _write_environment_text(environment: dict[str, Any], path: Path) -> None:
    lines = [
        f"python: {environment.get('python')}",
        f"python_executable: {environment.get('python_executable')}",
        f"platform: {environment.get('platform')}",
        f"cwd: {environment.get('cwd')}",
    ]
    device = environment.get("device", {})
    if isinstance(device, dict):
        lines.extend(
            [
                f"torch_version: {device.get('torch_version')}",
                f"cuda_version: {device.get('cuda_version')}",
                f"cuda_available: {device.get('cuda_available')}",
                f"selected_device: {device.get('selected_device')}",
                f"gpu_model: {device.get('gpu_model')}",
                f"gpu_vram_total_bytes: {device.get('gpu_vram_total_bytes')}",
            ]
        )
    packages = environment.get("packages", {})
    if isinstance(packages, dict):
        lines.append("packages:")
        lines.extend(f"  {name}: {version}" for name, version in sorted(packages.items()))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _metric_definitions(cfg: dict[str, Any], early_stopping_metric: str) -> dict[str, Any]:
    return {
        "dice_formula": "2 * TP / (2 * TP + FP + FN); defined as 1.0 when prediction and target are both empty",
        "iou_formula": "TP / (TP + FP + FN); defined as 1.0 when prediction and target are both empty",
        "epsilon": 1e-7,
        "threshold_or_postprocessing": f"binary sigmoid probabilities thresholded at {cfg['threshold']}; optional validation threshold search selects by micro Dice then micro IoU",
        "historical_validation_threshold": 0.5,
        "metric_reduction": "dataset-level micro aggregation of TP/FP/TN/FN for val_dice and val_iou",
        "macro_reporting": "per-image macro summaries are also saved for evaluation outputs",
        "background_included": "background pixels contribute to TN, specificity, and pixel accuracy but not Dice/IoU numerator or denominator except through FP/FN",
        "loss": "AsymmetricTverskyLoss on raw logits",
        "loss_reduction": "per-sample Tversky loss averaged across the batch; epoch losses are sample-weighted averages",
        "checkpoint_selection_rule": f"best checkpoint selected by {early_stopping_metric}",
    }


def _gpu_peak_mb(device: torch.device) -> tuple[float | None, float | None]:
    if device.type != "cuda":
        return None, None
    return (
        float(torch.cuda.max_memory_allocated(device) / (1024**2)),
        float(torch.cuda.max_memory_reserved(device) / (1024**2)),
    )


def _make_summary_writer(exp_dir: Path, enabled: bool) -> Any | None:
    if not enabled:
        return None
    try:
        from torch.utils.tensorboard import SummaryWriter
    except Exception:
        return None
    return SummaryWriter(log_dir=str(exp_dir / "tensorboard"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train MitUNet on local CubiCasa5K binary wall masks.")
    parser.add_argument("--data-root", default="/home/pmharris/dev/cubicasa5k_data")
    parser.add_argument("--config", default="configs/cubicasa5k_mitunet.yaml")
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--run-name", default=None)
    parser.add_argument("--cache-dir", default=None)
    parser.add_argument("--floortrans-root", default=None)
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=None)
    parser.add_argument("--image-size", type=int, default=None)
    parser.add_argument("--input-size", type=int, default=None)
    parser.add_argument("--resize-mode", choices=["letterbox", "direct"], default=None)
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--weight-decay", type=float, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--num-workers", type=int, default=None)
    parser.add_argument("--encoder-weights", default=None)
    parser.add_argument("--grad-clip", type=float, default=None)
    parser.add_argument("--early-stopping-patience", type=int, default=None)
    parser.add_argument("--early-stopping-metric", choices=["val_iou", "val_loss"], default=None)
    parser.add_argument("--early-stopping-min-delta", type=float, default=None)
    parser.add_argument("--reports-root", default=None)
    parser.add_argument("--task-mode", choices=[TASK_BINARY_WALL, TASK_CUBICASA_MULTICLASS], default=None)
    parser.add_argument("--init-checkpoint", default=None)
    parser.add_argument("--limit-train", type=int, default=None)
    parser.add_argument("--limit-val", type=int, default=None)
    parser.add_argument("--limit-test", type=int, default=None)
    parser.add_argument("--resume", action="store_true", help="Resume an existing run directory from last_model.pth.")
    parser.add_argument("--no-amp", action="store_true")
    parser.add_argument("--no-augment", action="store_true")
    parser.add_argument("--no-threshold-search", action="store_true")
    parser.add_argument("--subtract-openings", action="store_true")
    parser.add_argument("--allow-invalid-over-1pct", action="store_true")
    return parser.parse_args()


def build_config(args: argparse.Namespace) -> dict[str, Any]:
    cfg = dict(DEFAULTS)
    config_path = Path(args.config)
    if config_path.exists():
        cfg.update(load_yaml(config_path))
    overrides = {
        "experiment_root": args.output_root,
        "cache_dir": args.cache_dir,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "gradient_accumulation_steps": args.gradient_accumulation_steps,
        "image_size": args.image_size,
        "resize_mode": args.resize_mode,
        "lr": args.lr,
        "weight_decay": args.weight_decay,
        "seed": args.seed,
        "num_workers": args.num_workers,
        "encoder_weights": args.encoder_weights,
        "grad_clip": args.grad_clip,
        "early_stopping_patience": args.early_stopping_patience,
        "early_stopping_metric": args.early_stopping_metric,
        "early_stopping_min_delta": args.early_stopping_min_delta,
        "reports_root": args.reports_root,
        "task_mode": args.task_mode,
        "init_checkpoint": args.init_checkpoint,
    }
    for key, value in overrides.items():
        if value is not None:
            cfg[key] = value
    if args.no_amp:
        cfg["amp"] = False
    if args.no_threshold_search:
        cfg["threshold_search"] = False
    if args.subtract_openings:
        cfg["subtract_openings"] = True
    cfg["augment"] = not args.no_augment
    cfg["limit_train"] = args.limit_train
    cfg["limit_val"] = args.limit_val
    cfg["limit_test"] = args.limit_test
    cfg["data_root"] = args.data_root
    cfg["config_path"] = str(config_path)
    if cfg.get("task_mode") not in {TASK_BINARY_WALL, TASK_CUBICASA_MULTICLASS}:
        raise ValueError(f"Unsupported task_mode={cfg.get('task_mode')!r}")
    cfg = resolve_image_size_config(cfg, cli_input_size=args.input_size)
    validate_experiment_image_size(int(cfg["image_size"]))
    return cfg


def make_loader(dataset: CubiCasaWallDataset, batch_size: int, num_workers: int, device: torch.device, shuffle: bool) -> DataLoader:
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=device.type == "cuda",
        drop_last=False,
    )


def save_checkpoint(
    path: Path,
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.ReduceLROnPlateau,
    epoch: int,
    best_validation: dict[str, Any],
    architecture: dict[str, Any],
    preprocessing: dict[str, Any],
    threshold: float,
    cfg: dict[str, Any],
    environment: dict[str, Any],
    validation_metrics: dict[str, Any] | None = None,
) -> None:
    payload = {
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
        "scheduler_state": scheduler.state_dict(),
        "epoch": epoch,
        "best_validation": best_validation,
        "architecture": architecture,
        "preprocessing": preprocessing,
        "threshold": threshold,
        "random_seed": cfg["seed"],
        "config": cfg,
        "environment": environment,
        "validation_metrics": validation_metrics,
    }
    if cfg.get("task_mode") == TASK_CUBICASA_MULTICLASS:
        payload.update(
            {
                "task_mode": TASK_CUBICASA_MULTICLASS,
                "structure_class_names": cfg.get("structure_class_names"),
                "icon_class_names": cfg.get("icon_class_names"),
                "mask_schema_version": MASK_SCHEMA_VERSION,
                "mapping_hash": cfg.get("mapping_hash"),
                "class_mapping": cfg.get("class_mapping"),
                "checkpoint_note": "Binary output heads cannot be reused directly; encoder/decoder weights may initialize matching multiclass modules.",
            }
        )
    torch.save(payload, path)


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, str) and value.strip().lower() in {"", "none", "null", "nan", "na", "n/a"}:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _load_existing_history(path: Path, max_epoch: int) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for row in read_csv_rows(path):
        epoch = _as_float(row.get("epoch"))
        if epoch is not None and int(epoch) <= max_epoch:
            rows.append(row)
    return rows


def _float_list(value: Any) -> list[float] | None:
    if value is None:
        return None
    if isinstance(value, str) and value.strip().lower() in {"", "none", "null"}:
        return None
    return [float(v) for v in value]


def _save_multiclass_per_class(epoch: int, val_eval: dict[str, Any], exp_dir: Path) -> None:
    rows = []
    for head in ["structure", "icons"]:
        for row in val_eval[head]["per_class"]:
            rows.append({"epoch": epoch, "head": head, **row})
    write_csv(rows, exp_dir / f"validation_epoch_{epoch:03d}_per_class_metrics.csv")


def run_multiclass_training_attempt(cfg: dict[str, Any], exp_dir: Path, batch_size: int, logger: Any, *, resume: bool = False) -> dict[str, Any]:
    seed_notes = seed_everything(int(cfg["seed"]))
    device, device_info = detect_device()
    amp_enabled = bool(cfg["amp"] and device.type == "cuda")
    gradient_accumulation_steps = max(1, int(cfg.get("gradient_accumulation_steps", 1)))
    effective_batch_size = batch_size * gradient_accumulation_steps
    include_optional_structure = bool(cfg.get("include_optional_structure", False))
    structure_classes = enabled_structure_classes(include_optional_structure)
    icon_classes = ICON_CLASSES
    structure_names = [item.name for item in structure_classes]
    icon_names = [item.name for item in icon_classes]
    class_mapping = mapping_payload(include_optional_structure)
    map_hash = mapping_hash(include_optional_structure)

    environment = collect_environment(device_info)
    environment["determinism_notes"] = seed_notes
    environment["amp_active"] = amp_enabled
    environment["physical_batch_size"] = batch_size
    environment["gradient_accumulation_steps"] = gradient_accumulation_steps
    environment["effective_batch_size"] = effective_batch_size
    save_json(environment, exp_dir / "environment.json")
    _write_environment_text(environment, exp_dir / "environment.txt")
    (exp_dir / "command.txt").write_text(_command_line() + "\n", encoding="utf-8")
    save_json(_git_state(), exp_dir / "git_state.json")
    save_json(class_mapping, exp_dir / "class_mapping.json")
    save_json(
        {
            "structure": deterministic_palette(structure_classes),
            "icons": deterministic_palette(icon_classes),
            "unified_export": {
                "lossy": True,
                "priority": "icons/openings > structural classes > background",
                "note": "The unified mask cannot represent overlapping structure and icon labels.",
            },
        },
        exp_dir / "palette.json",
    )

    prepared = prepare_dataset(
        data_root=cfg["data_root"],
        output_dir=exp_dir,
        cache_dir=cfg["cache_dir"],
        floortrans_root=cfg.get("floortrans_root"),
        subtract_openings=False,
        preview_count=int(cfg["preview_count"]),
        allow_invalid_over_1pct=bool(cfg.get("allow_invalid_over_1pct", False)),
        task_mode=TASK_CUBICASA_MULTICLASS,
        include_optional_structure=include_optional_structure,
    )
    audit = audit_multiclass_split(
        data_root=cfg["data_root"],
        output_dir=exp_dir,
        split="train",
        floortrans_root=cfg.get("floortrans_root"),
        include_optional_structure=include_optional_structure,
        required_structure_classes=list(cfg.get("required_structure_classes") or []),
        required_icon_classes=list(cfg.get("required_icon_classes") or []),
    )
    source_resolution_summary = audit_source_resolutions(prepared.manifest_paths, exp_dir)
    manifest_checksums = _manifest_checksums(prepared.manifest_paths)
    save_json(manifest_checksums, exp_dir / "manifest_checksums.json")

    train_ds = CubiCasaMultiClassDataset(
        prepared.manifest_paths["train"],
        "train",
        image_size=int(cfg["image_size"]),
        resize_mode=str(cfg["resize_mode"]),
        augment=bool(cfg["augment"]),
        limit=cfg.get("limit_train"),
        include_optional_structure=include_optional_structure,
    )
    val_ds = CubiCasaMultiClassDataset(
        prepared.manifest_paths["val"],
        "val",
        image_size=int(cfg["image_size"]),
        resize_mode=str(cfg["resize_mode"]),
        augment=False,
        limit=cfg.get("limit_val"),
        include_optional_structure=include_optional_structure,
    )
    test_ds = CubiCasaMultiClassDataset(
        prepared.manifest_paths["test"],
        "test",
        image_size=int(cfg["image_size"]),
        resize_mode=str(cfg["resize_mode"]),
        augment=False,
        limit=cfg.get("limit_test"),
        include_optional_structure=include_optional_structure,
    )
    train_loader = make_loader(train_ds, batch_size, int(cfg["num_workers"]), device, shuffle=True)
    val_loader = make_loader(val_ds, batch_size, int(cfg["num_workers"]), device, shuffle=False)
    test_loader = make_loader(test_ds, batch_size, int(cfg["num_workers"]), device, shuffle=False)

    build = build_mitunet(
        encoder_weights=cfg["encoder_weights"],
        task_mode=TASK_CUBICASA_MULTICLASS,
        include_optional_structure=include_optional_structure,
    )
    model = build.model.to(device)
    if build.pretrained_error:
        logger.info("Pretrained encoder weights were not loaded: %s", build.pretrained_error)
    logger.info("Pretrained encoder loaded: %s", build.pretrained_loaded)
    if cfg.get("init_checkpoint"):
        init_checkpoint = torch.load(cfg["init_checkpoint"], map_location="cpu", weights_only=False)
        init_state = init_checkpoint.get("model_state") or init_checkpoint.get("model")
        if init_state is None:
            raise KeyError("Initialization checkpoint does not contain 'model_state' or 'model'")
        load_report = load_matching_weights(model, init_state)
        save_json(load_report, exp_dir / "init_checkpoint_load_report.json")
        logger.info(
            "initialized from %s: loaded=%s missing=%s unexpected=%s shape_mismatch=%s",
            cfg["init_checkpoint"],
            len(load_report["loaded_keys"]),
            load_report["missing_keys"],
            load_report["unexpected_keys"],
            load_report["skipped_shape_mismatch_keys"],
        )

    recommended = audit["recommended_ce_weights"]
    structure_class_weights = _float_list(cfg.get("structure_class_weights"))
    icon_class_weights = _float_list(cfg.get("icon_class_weights"))
    if bool(cfg.get("use_recommended_ce_weights", True)):
        structure_class_weights = structure_class_weights or recommended["structure"]
        icon_class_weights = icon_class_weights or recommended["icons"]
    save_json(
        {
            "structure": structure_class_weights,
            "icons": icon_class_weights,
            "source": "audit recommended inverse-log-frequency" if bool(cfg.get("use_recommended_ce_weights", True)) else "configuration",
        },
        exp_dir / "class_weights.json",
    )
    criterion = MultiHeadSegmentationLoss(
        structure_ce_weight=float(cfg["structure_ce_weight"]),
        structure_dice_weight=float(cfg["structure_dice_weight"]),
        icon_ce_weight=float(cfg["icon_ce_weight"]),
        icon_dice_weight=float(cfg["icon_dice_weight"]),
        structure_task_weight=float(cfg["structure_task_weight"]),
        icon_task_weight=float(cfg["icon_task_weight"]),
        structure_class_weights=structure_class_weights,
        icon_class_weights=icon_class_weights,
    ).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=float(cfg["lr"]), weight_decay=float(cfg["weight_decay"]))
    early_stopping_metric = "val_iou"
    early_stopping_min_delta = float(cfg.get("early_stopping_min_delta", 0.0))
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=0.5,
        patience=int(cfg["scheduler_patience"]),
    )
    preprocessing = {
        "image_size": int(cfg["image_size"]),
        "input_size": int(cfg["image_size"]),
        "resize_mode": cfg["resize_mode"],
        "normalize": "imagenet",
        "mask_interpolation": "nearest",
        "image_interpolation": "bilinear",
        "task_mode": TASK_CUBICASA_MULTICLASS,
    }
    cfg.update(
        {
            "task_mode": TASK_CUBICASA_MULTICLASS,
            "image_size": int(cfg["image_size"]),
            "input_size": int(cfg["image_size"]),
            "physical_batch_size": batch_size,
            "gradient_accumulation_steps": gradient_accumulation_steps,
            "effective_batch_size": effective_batch_size,
            "amp_active": amp_enabled,
            "pretrained_encoder_loaded": build.pretrained_loaded,
            "pretrained_encoder_error": build.pretrained_error,
            "manifest_checksums": manifest_checksums,
            "source_resolution_summary": source_resolution_summary,
            "git": _git_state(),
            "class_mapping": class_mapping,
            "mapping_hash": map_hash,
            "mask_schema_version": MASK_SCHEMA_VERSION,
            "structure_class_names": structure_names,
            "icon_class_names": icon_names,
            "class_distribution_audit": {
                "json": str(exp_dir / "train_class_distribution_audit.json"),
                "csv": str(exp_dir / "train_class_distribution_audit.csv"),
            },
            "class_weights": {"structure": structure_class_weights, "icons": icon_class_weights},
        }
    )
    save_yaml(cfg, exp_dir / "config.yaml")
    save_yaml(cfg, exp_dir / "run_config_resolved.yaml")
    save_json(
        {
            "dice_formula": "multiclass soft Dice masks ignore_index pixels and averages present classes in each batch",
            "metric_reduction": "epoch-level confusion-matrix accumulation",
            "checkpoint_selection_rule": "best_model.pth selected by validation macro IoU excluding background/empty across both heads",
            "best_wall_checkpoint": "best_wall_model.pth selected by validation wall IoU",
        },
        exp_dir / "metric_definitions.json",
    )

    history: list[dict[str, Any]] = []
    observability_history: list[dict[str, Any]] = []
    best = {"dice": -1.0, "iou": -1.0, "loss": None, "epoch": 0, "metric": early_stopping_metric, "score": None}
    best_wall = {"iou": -1.0, "dice": None, "epoch": 0}
    best_score: float | None = None
    patience_left = int(cfg["early_stopping_patience"])
    history_csv = exp_dir / "history.csv"
    legacy_history_csv = exp_dir / "training_history.csv"
    report_dir = Path(str(cfg.get("reports_root", "reports/training_runs"))) / exp_dir.name
    training_log_csv = report_dir / "training_log.csv"
    writer = _make_summary_writer(exp_dir, enabled=True)
    start_epoch = 1

    if resume:
        resume_checkpoint_path = exp_dir / "last_model.pth"
        if not resume_checkpoint_path.exists():
            raise FileNotFoundError(f"Cannot resume: missing {resume_checkpoint_path}")
        checkpoint = torch.load(resume_checkpoint_path, map_location="cpu", weights_only=False)
        checkpoint_cfg = checkpoint.get("config", {})
        for key in ["image_size", "resize_mode", "seed", "task_mode", "mapping_hash"]:
            if key in checkpoint_cfg and str(checkpoint_cfg[key]) != str(cfg.get(key)):
                raise ValueError(f"Cannot resume with changed {key}: checkpoint={checkpoint_cfg[key]!r}, current={cfg.get(key)!r}")
        model.load_state_dict(checkpoint["model_state"])
        optimizer.load_state_dict(checkpoint["optimizer_state"])
        scheduler.load_state_dict(checkpoint["scheduler_state"])
        completed_epoch = int(checkpoint.get("epoch", 0))
        start_epoch = completed_epoch + 1
        best = checkpoint.get("best_validation", best)
        best_score = _as_float(best.get("score"))
        best_wall = checkpoint.get("best_wall_validation", best_wall)
        history = _load_existing_history(history_csv, completed_epoch)
        patience_left = max(0, int(cfg["early_stopping_patience"]) - max(0, completed_epoch - int(best.get("epoch", completed_epoch) or 0)))
        logger.info("resuming multiclass run from %s at epoch %s/%s", resume_checkpoint_path, start_epoch, cfg["epochs"])

    start = time.time() - (_as_float(history[-1].get("seconds_elapsed")) if history else 0.0)
    for epoch in range(start_epoch, int(cfg["epochs"]) + 1):
        logger.info("Epoch %s/%s", epoch, cfg["epochs"])
        epoch_start = time.time()
        if device.type == "cuda":
            torch.cuda.reset_peak_memory_stats(device)
        lr_groups = [float(group["lr"]) for group in optimizer.param_groups]
        learning_rate = lr_groups[0]
        train_start = time.time()
        train_components = train_one_epoch_multiclass(
            model,
            train_loader,
            criterion,
            optimizer,
            device,
            amp_enabled=amp_enabled,
            grad_clip=cfg.get("grad_clip"),
            gradient_accumulation_steps=gradient_accumulation_steps,
        )
        train_time_seconds = time.time() - train_start
        validation_start = time.time()
        val_eval = evaluate_model_multiclass(
            model,
            val_loader,
            device,
            criterion=criterion,
            amp_enabled=amp_enabled,
            include_optional_structure=include_optional_structure,
        )
        validation_time_seconds = time.time() - validation_start
        _save_multiclass_per_class(epoch, val_eval, exp_dir)
        val_loss = float(val_eval["loss"])
        val_dice = float(val_eval["macro_dice_excluding_background"] or 0.0)
        val_iou = float(val_eval["macro_iou_excluding_background"] or 0.0)
        wall_iou = float(val_eval["wall_iou"] or 0.0)
        wall_dice = float(val_eval["wall_dice"] or 0.0)
        early_stopping_score = val_iou
        is_best = is_metric_improved(
            early_stopping_score,
            best_score,
            early_stopping_metric,
            min_delta=early_stopping_min_delta,
        )
        is_best_wall = wall_iou > float(best_wall.get("iou", -1.0))
        scheduler.step(early_stopping_score)
        seconds_elapsed = round(time.time() - start, 2)
        epoch_time_seconds = time.time() - epoch_start
        peak_allocated_mb, peak_reserved_mb = _gpu_peak_mb(device)
        row = {
            "epoch": epoch,
            "train_loss": train_components["loss"],
            "val_loss": val_loss,
            "val_dice": val_dice,
            "val_iou": val_iou,
            "learning_rate": learning_rate,
            "learning_rate_group_0": lr_groups[0],
            "lr": learning_rate,
            "epoch_time_seconds": epoch_time_seconds,
            "train_time_seconds": train_time_seconds,
            "validation_time_seconds": validation_time_seconds,
            "peak_gpu_memory_allocated_mb": peak_allocated_mb,
            "peak_gpu_memory_reserved_mb": peak_reserved_mb,
            "physical_batch_size": batch_size,
            "gradient_accumulation_steps": gradient_accumulation_steps,
            "effective_batch_size": effective_batch_size,
            "seconds_elapsed": seconds_elapsed,
            "checkpoint_path": str(exp_dir / ("best_model.pth" if is_best else "last_model.pth")),
            "best_checkpoint": is_best,
            "structure_ce": train_components["structure_ce"],
            "structure_dice_loss": train_components["structure_dice_loss"],
            "structure_loss": train_components["structure_loss"],
            "icon_ce": train_components["icon_ce"],
            "icon_dice_loss": train_components["icon_dice_loss"],
            "icon_loss": train_components["icon_loss"],
            "wall_dice": wall_dice,
            "wall_iou": wall_iou,
            "window_dice": val_eval["window_dice"],
            "window_iou": val_eval["window_iou"],
            "door_dice": val_eval["door_dice"],
            "door_iou": val_eval["door_iou"],
            "appliance_dice": val_eval["appliance_dice"],
            "appliance_iou": val_eval["appliance_iou"],
        }
        if is_best:
            best = {
                "dice": val_dice,
                "iou": val_iou,
                "loss": val_loss,
                "epoch": epoch,
                "metric": early_stopping_metric,
                "score": early_stopping_score,
            }
            best_score = early_stopping_score
            patience_left = int(cfg["early_stopping_patience"])
            save_checkpoint(
                exp_dir / "best_model.pth",
                model,
                optimizer,
                scheduler,
                epoch,
                best,
                build.architecture,
                preprocessing,
                float(cfg["threshold"]),
                {**cfg, "best_wall_validation": best_wall},
                environment,
                validation_metrics=val_eval,
            )
            logger.info("saved best_model.pth")
        else:
            patience_left -= 1
        if is_best_wall:
            best_wall = {"iou": wall_iou, "dice": wall_dice, "epoch": epoch}
            save_checkpoint(
                exp_dir / "best_wall_model.pth",
                model,
                optimizer,
                scheduler,
                epoch,
                best,
                build.architecture,
                preprocessing,
                float(cfg["threshold"]),
                {**cfg, "best_wall_validation": best_wall},
                environment,
                validation_metrics=val_eval,
            )
            logger.info("saved best_wall_model.pth")
        save_checkpoint(
            exp_dir / "last_model.pth",
            model,
            optimizer,
            scheduler,
            epoch,
            {**best, "best_wall_validation": best_wall},
            build.architecture,
            preprocessing,
            float(cfg["threshold"]),
            {**cfg, "best_wall_validation": best_wall},
            environment,
            validation_metrics=val_eval,
        )
        history.append(row)
        write_csv(history, history_csv, HISTORY_FIELDS)
        write_csv(history, legacy_history_csv, HISTORY_FIELDS)
        observability_history.append(
            make_training_log_row(
                epoch=epoch,
                train_loss=train_components["loss"],
                val_loss=val_loss,
                val_dice=val_dice,
                val_iou=val_iou,
                learning_rate=learning_rate,
                checkpoint_path=row["checkpoint_path"],
                best_checkpoint=is_best,
                seconds_elapsed=seconds_elapsed,
                epoch_time_seconds=epoch_time_seconds,
                train_time_seconds=train_time_seconds,
                validation_time_seconds=validation_time_seconds,
                peak_gpu_memory_allocated_mb=peak_allocated_mb,
                peak_gpu_memory_reserved_mb=peak_reserved_mb,
                learning_rate_group_0=lr_groups[0],
                dice_loss=train_components["structure_dice_loss"] + train_components["icon_dice_loss"],
            )
        )
        write_training_log(observability_history, training_log_csv)
        if writer is not None:
            writer.add_scalar("Loss/train", train_components["loss"], epoch)
            writer.add_scalar("Loss/validation", val_loss, epoch)
            writer.add_scalar("Metrics/validation_macro_dice_ex_bg", val_dice, epoch)
            writer.add_scalar("Metrics/validation_macro_iou_ex_bg", val_iou, epoch)
            writer.add_scalar("Metrics/wall_iou", wall_iou, epoch)
            writer.add_scalar("LearningRate/group_0", learning_rate, epoch)
            writer.flush()
        logger.info(
            "epoch=%s train_loss=%.6f val_loss=%.6f val_macro_iou_ex_bg=%.6f wall_iou=%.6f best=%s best_wall=%s",
            epoch,
            train_components["loss"],
            val_loss,
            val_iou,
            wall_iou,
            is_best,
            is_best_wall,
        )
        if patience_left <= 0:
            logger.info("early stopping triggered on validation macro IoU excluding background")
            break

    if writer is not None:
        writer.close()
    save_training_curves(history_csv, exp_dir / "training_curves.png")
    save_observability_plots(observability_history, exp_dir / "plots")
    save_observability_plots(observability_history, report_dir / "plots")
    save_training_summary(
        observability_history,
        report_dir / "summary.md",
        run_id=exp_dir.name,
        source_run_dir=exp_dir,
        early_stopping_metric=early_stopping_metric,
    )

    checkpoint_path = exp_dir / "best_model.pth"
    if checkpoint_path.exists():
        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
        loaded = load_model_from_checkpoint(checkpoint, map_location=device)
        model = loaded.model.eval()
    test_eval = evaluate_model_multiclass(
        model,
        test_loader,
        device,
        amp_enabled=amp_enabled,
        overlay_dir=exp_dir / "test_prediction_panels",
        max_overlays=20,
        include_optional_structure=include_optional_structure,
    )
    val_overlay_eval = evaluate_model_multiclass(
        model,
        val_loader,
        device,
        amp_enabled=amp_enabled,
        overlay_dir=exp_dir / "validation_prediction_panels",
        max_overlays=20,
        include_optional_structure=include_optional_structure,
    )
    save_multiclass_evaluation_outputs(test_eval, exp_dir, "test")
    save_multiclass_evaluation_outputs(val_overlay_eval, exp_dir, "validation")
    main_metrics = {
        "best_epoch": best["epoch"],
        "best_validation_macro_iou_excluding_background": best["iou"],
        "best_wall_validation": best_wall,
        "test": test_eval,
        "dataset_summary": prepared.summary,
    }
    save_json(main_metrics, exp_dir / "metrics.json")
    save_json(
        {
            "run_dir": str(exp_dir),
            "task_mode": TASK_CUBICASA_MULTICLASS,
            "image_size": int(cfg["image_size"]),
            "epochs_completed": len(history),
            "best_checkpoint_path": str(exp_dir / "best_model.pth"),
            "best_wall_checkpoint_path": str(exp_dir / "best_wall_model.pth"),
            "last_checkpoint_path": str(exp_dir / "last_model.pth"),
            "checkpoint_selection_metric": "validation macro IoU excluding background/empty",
            "best_epoch": best["epoch"],
            "best_validation_macro_iou_excluding_background": best["iou"],
            "best_wall_validation": best_wall,
            "mapping_hash": map_hash,
            "mask_schema_version": MASK_SCHEMA_VERSION,
            "class_distribution_audit": cfg["class_distribution_audit"],
            "physical_batch_size": batch_size,
            "gradient_accumulation_steps": gradient_accumulation_steps,
            "effective_batch_size": effective_batch_size,
            "amp_active": amp_enabled,
            "source_resolution_summary": source_resolution_summary,
            "manifest_checksums": manifest_checksums,
            "environment": environment,
            "command": _command_line(),
        },
        exp_dir / "summary.json",
    )
    return {
        "exp_dir": str(exp_dir),
        "best": best,
        "best_wall": best_wall,
        "test_eval": test_eval,
        "environment": environment,
        "epochs_completed": len(history),
    }


def run_training_attempt(cfg: dict[str, Any], exp_dir: Path, batch_size: int, logger: Any, *, resume: bool = False) -> dict[str, Any]:
    if cfg.get("task_mode") == TASK_CUBICASA_MULTICLASS:
        return run_multiclass_training_attempt(cfg, exp_dir, batch_size, logger, resume=resume)
    seed_notes = seed_everything(int(cfg["seed"]))
    device, device_info = detect_device()
    amp_enabled = bool(cfg["amp"] and device.type == "cuda")
    gradient_accumulation_steps = max(1, int(cfg.get("gradient_accumulation_steps", 1)))
    effective_batch_size = batch_size * gradient_accumulation_steps
    environment = collect_environment(device_info)
    environment["determinism_notes"] = seed_notes
    environment["amp_active"] = amp_enabled
    environment["physical_batch_size"] = batch_size
    environment["gradient_accumulation_steps"] = gradient_accumulation_steps
    environment["effective_batch_size"] = effective_batch_size
    save_json(environment, exp_dir / "environment.json")
    _write_environment_text(environment, exp_dir / "environment.txt")
    (exp_dir / "command.txt").write_text(_command_line() + "\n", encoding="utf-8")
    save_json(_git_state(), exp_dir / "git_state.json")

    prepared = prepare_dataset(
        data_root=cfg["data_root"],
        output_dir=exp_dir,
        cache_dir=cfg["cache_dir"],
        floortrans_root=cfg.get("floortrans_root"),
        subtract_openings=bool(cfg["subtract_openings"]),
        preview_count=int(cfg["preview_count"]),
        allow_invalid_over_1pct=bool(cfg.get("allow_invalid_over_1pct", False)),
    )
    source_resolution_summary = audit_source_resolutions(prepared.manifest_paths, exp_dir)
    manifest_checksums = _manifest_checksums(prepared.manifest_paths)
    save_json(manifest_checksums, exp_dir / "manifest_checksums.json")

    train_ds = CubiCasaWallDataset(
        prepared.manifest_paths["train"],
        "train",
        image_size=int(cfg["image_size"]),
        resize_mode=str(cfg["resize_mode"]),
        augment=bool(cfg["augment"]),
        limit=cfg.get("limit_train"),
    )
    val_ds = CubiCasaWallDataset(
        prepared.manifest_paths["val"],
        "val",
        image_size=int(cfg["image_size"]),
        resize_mode=str(cfg["resize_mode"]),
        augment=False,
        limit=cfg.get("limit_val"),
    )
    test_ds = CubiCasaWallDataset(
        prepared.manifest_paths["test"],
        "test",
        image_size=int(cfg["image_size"]),
        resize_mode=str(cfg["resize_mode"]),
        augment=False,
        limit=cfg.get("limit_test"),
    )
    train_loader = make_loader(train_ds, batch_size, int(cfg["num_workers"]), device, shuffle=True)
    val_loader = make_loader(val_ds, batch_size, int(cfg["num_workers"]), device, shuffle=False)
    test_loader = make_loader(test_ds, batch_size, int(cfg["num_workers"]), device, shuffle=False)

    build = build_mitunet(encoder_weights=cfg["encoder_weights"])
    model = build.model.to(device)
    if build.pretrained_error:
        logger.info("Pretrained encoder weights were not loaded: %s", build.pretrained_error)
    logger.info("Pretrained encoder loaded: %s", build.pretrained_loaded)

    criterion = AsymmetricTverskyLoss(alpha=float(cfg["tversky_alpha"]), beta=float(cfg["tversky_beta"]))
    optimizer = torch.optim.Adam(model.parameters(), lr=float(cfg["lr"]), weight_decay=float(cfg["weight_decay"]))
    early_stopping_metric = validate_early_stopping_metric(str(cfg.get("early_stopping_metric", "val_iou")))
    early_stopping_min_delta = float(cfg.get("early_stopping_min_delta", 0.0))
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode=metric_mode(early_stopping_metric),
        factor=0.5,
        patience=int(cfg["scheduler_patience"]),
    )

    preprocessing = {
        "image_size": int(cfg["image_size"]),
        "input_size": int(cfg["image_size"]),
        "resize_mode": cfg["resize_mode"],
        "normalize": "imagenet",
        "mask_interpolation": "nearest",
        "image_interpolation": "bilinear",
        "subtract_openings": bool(cfg["subtract_openings"]),
    }
    cfg["image_size"] = int(cfg["image_size"])
    cfg["input_size"] = int(cfg["image_size"])
    cfg["physical_batch_size"] = batch_size
    cfg["gradient_accumulation_steps"] = gradient_accumulation_steps
    cfg["effective_batch_size"] = effective_batch_size
    cfg["amp_active"] = amp_enabled
    cfg["pretrained_encoder_loaded"] = build.pretrained_loaded
    cfg["pretrained_encoder_error"] = build.pretrained_error
    cfg["manifest_checksums"] = manifest_checksums
    cfg["source_resolution_summary"] = source_resolution_summary
    cfg["git"] = _git_state()
    save_yaml(cfg, exp_dir / "config.yaml")
    save_yaml(cfg, exp_dir / "run_config_resolved.yaml")

    history: list[dict[str, Any]] = []
    observability_history: list[dict[str, Any]] = []
    best = {"dice": -1.0, "iou": -1.0, "loss": None, "epoch": 0, "metric": early_stopping_metric, "score": None}
    best_score: float | None = None
    patience_left = int(cfg["early_stopping_patience"])
    history_csv = exp_dir / "history.csv"
    legacy_history_csv = exp_dir / "training_history.csv"
    report_dir = Path(str(cfg.get("reports_root", "reports/training_runs"))) / exp_dir.name
    training_log_csv = report_dir / "training_log.csv"
    save_json(_metric_definitions(cfg, early_stopping_metric), exp_dir / "metric_definitions.json")
    writer = _make_summary_writer(exp_dir, enabled=True)

    start_epoch = 1
    if resume:
        resume_checkpoint_path = exp_dir / "last_model.pth"
        if not resume_checkpoint_path.exists():
            raise FileNotFoundError(f"Cannot resume: missing {resume_checkpoint_path}")
        checkpoint = torch.load(resume_checkpoint_path, map_location="cpu", weights_only=False)
        checkpoint_cfg = checkpoint.get("config", {})
        for key in ["image_size", "resize_mode", "seed", "threshold", "tversky_alpha", "tversky_beta"]:
            if key in checkpoint_cfg and str(checkpoint_cfg[key]) != str(cfg.get(key)):
                raise ValueError(f"Cannot resume with changed {key}: checkpoint={checkpoint_cfg[key]!r}, current={cfg.get(key)!r}")
        model.load_state_dict(checkpoint["model_state"])
        optimizer.load_state_dict(checkpoint["optimizer_state"])
        scheduler.load_state_dict(checkpoint["scheduler_state"])
        completed_epoch = int(checkpoint.get("epoch", 0))
        if completed_epoch >= int(cfg["epochs"]):
            logger.info("resume checkpoint already completed epoch %s/%s", completed_epoch, cfg["epochs"])
        start_epoch = completed_epoch + 1
        best = checkpoint.get("best_validation", best)
        best_score = _as_float(best.get("score"))
        if best_score is None:
            best_score = _as_float(best.get("iou" if early_stopping_metric == "val_iou" else "loss"))
        best_epoch = int(best.get("epoch", completed_epoch) or 0)
        patience_left = max(0, int(cfg["early_stopping_patience"]) - max(0, completed_epoch - best_epoch))
        history = _load_existing_history(history_csv, completed_epoch)
        observability_history = _load_existing_history(training_log_csv, completed_epoch)
        if not observability_history:
            observability_history = [
                make_training_log_row(
                    epoch=int(_as_float(row.get("epoch")) or 0),
                    train_loss=float(_as_float(row.get("train_loss")) or 0.0),
                    val_loss=float(_as_float(row.get("val_loss")) or 0.0),
                    val_dice=float(_as_float(row.get("val_dice")) or 0.0),
                    val_iou=float(_as_float(row.get("val_iou")) or 0.0),
                    learning_rate=float(_as_float(row.get("learning_rate")) or _as_float(row.get("lr")) or 0.0),
                    checkpoint_path=row.get("checkpoint_path") or exp_dir / "last_model.pth",
                    best_checkpoint=_as_bool(row.get("best_checkpoint")),
                    seconds_elapsed=_as_float(row.get("seconds_elapsed")),
                    epoch_time_seconds=_as_float(row.get("epoch_time_seconds")),
                    train_time_seconds=_as_float(row.get("train_time_seconds")),
                    validation_time_seconds=_as_float(row.get("validation_time_seconds")),
                    peak_gpu_memory_allocated_mb=_as_float(row.get("peak_gpu_memory_allocated_mb")),
                    peak_gpu_memory_reserved_mb=_as_float(row.get("peak_gpu_memory_reserved_mb")),
                    learning_rate_group_0=_as_float(row.get("learning_rate_group_0")),
                )
                for row in history
            ]
        logger.info("resuming from %s at epoch %s/%s", resume_checkpoint_path, start_epoch, cfg["epochs"])

    prior_elapsed = _as_float(history[-1].get("seconds_elapsed")) if history else None
    start = time.time() - (prior_elapsed or 0.0)
    for epoch in range(start_epoch, int(cfg["epochs"]) + 1):
        logger.info("Epoch %s/%s", epoch, cfg["epochs"])
        epoch_start = time.time()
        if device.type == "cuda":
            torch.cuda.reset_peak_memory_stats(device)
        lr_groups = [float(group["lr"]) for group in optimizer.param_groups]
        learning_rate = lr_groups[0]
        train_start = time.time()
        train_loss = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
            device,
            amp_enabled=amp_enabled,
            grad_clip=cfg.get("grad_clip"),
            gradient_accumulation_steps=gradient_accumulation_steps,
        )
        train_time_seconds = time.time() - train_start
        validation_start = time.time()
        val_eval = evaluate_model(model, val_loader, device, thresholds=[0.5], criterion=criterion, amp_enabled=amp_enabled)
        validation_time_seconds = time.time() - validation_start
        val_metrics = val_eval[0.5]
        val_dice = float(val_metrics["micro"]["dice"])
        val_iou = float(val_metrics["micro"]["iou"])
        val_loss = float(val_metrics["loss"])
        early_stopping_score = val_iou if early_stopping_metric == "val_iou" else val_loss
        is_best = is_metric_improved(
            early_stopping_score,
            best_score,
            early_stopping_metric,
            min_delta=early_stopping_min_delta,
        )
        checkpoint_path = exp_dir / ("best_model.pth" if is_best else "last_model.pth")
        scheduler.step(early_stopping_score)
        seconds_elapsed = round(time.time() - start, 2)
        epoch_time_seconds = time.time() - epoch_start
        peak_allocated_mb, peak_reserved_mb = _gpu_peak_mb(device)
        row = {
            "epoch": epoch,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "val_dice": val_dice,
            "val_iou": val_iou,
            "learning_rate": learning_rate,
            "learning_rate_group_0": lr_groups[0],
            "lr": learning_rate,
            "epoch_time_seconds": epoch_time_seconds,
            "train_time_seconds": train_time_seconds,
            "validation_time_seconds": validation_time_seconds,
            "peak_gpu_memory_allocated_mb": peak_allocated_mb,
            "peak_gpu_memory_reserved_mb": peak_reserved_mb,
            "physical_batch_size": batch_size,
            "gradient_accumulation_steps": gradient_accumulation_steps,
            "effective_batch_size": effective_batch_size,
            "seconds_elapsed": seconds_elapsed,
            "checkpoint_path": str(checkpoint_path),
            "best_checkpoint": is_best,
        }
        if is_best:
            best = {
                "dice": val_dice,
                "iou": val_iou,
                "loss": val_loss,
                "epoch": epoch,
                "metric": early_stopping_metric,
                "score": early_stopping_score,
            }
            best_score = early_stopping_score
            patience_left = int(cfg["early_stopping_patience"])
            save_checkpoint(
                exp_dir / "best_model.pth",
                model,
                optimizer,
                scheduler,
                epoch,
                best,
                build.architecture,
                preprocessing,
                float(cfg["threshold"]),
                cfg,
                environment,
            )
            logger.info("saved best_model.pth")
        else:
            patience_left -= 1
        save_checkpoint(
            exp_dir / "last_model.pth",
            model,
            optimizer,
            scheduler,
            epoch,
            best,
            build.architecture,
            preprocessing,
            float(cfg["threshold"]),
            cfg,
            environment,
        )
        history.append(row)
        write_csv(history, history_csv, HISTORY_FIELDS)
        write_csv(history, legacy_history_csv, HISTORY_FIELDS)
        observability_history.append(
            make_training_log_row(
                epoch=epoch,
                train_loss=train_loss,
                val_loss=val_loss,
                val_dice=val_dice,
                val_iou=val_iou,
                learning_rate=learning_rate,
                checkpoint_path=checkpoint_path,
                best_checkpoint=is_best,
                seconds_elapsed=seconds_elapsed,
                epoch_time_seconds=epoch_time_seconds,
                train_time_seconds=train_time_seconds,
                validation_time_seconds=validation_time_seconds,
                peak_gpu_memory_allocated_mb=peak_allocated_mb,
                peak_gpu_memory_reserved_mb=peak_reserved_mb,
                learning_rate_group_0=lr_groups[0],
            )
        )
        write_training_log(observability_history, training_log_csv)
        if writer is not None:
            writer.add_scalar("Loss/train", train_loss, epoch)
            writer.add_scalar("Loss/validation", val_loss, epoch)
            writer.add_scalar("Metrics/validation_dice", val_dice, epoch)
            writer.add_scalar("Metrics/validation_iou", val_iou, epoch)
            writer.add_scalar("LearningRate/group_0", learning_rate, epoch)
            if peak_allocated_mb is not None:
                writer.add_scalar("System/peak_gpu_memory_mb", peak_allocated_mb, epoch)
            writer.add_scalar("Time/epoch_seconds", epoch_time_seconds, epoch)
            writer.flush()
        logger.info(
            "epoch=%s train_loss=%.6f val_loss=%.6f val_dice=%.6f val_iou=%.6f %s=%.6f best=%s",
            epoch,
            train_loss,
            val_loss,
            val_dice,
            val_iou,
            early_stopping_metric,
            early_stopping_score,
            is_best,
        )
        if patience_left <= 0:
            logger.info("early stopping triggered on %s", early_stopping_metric)
            break

    if writer is not None:
        writer.close()
    save_training_curves(history_csv, exp_dir / "training_curves.png")
    save_observability_plots(observability_history, exp_dir / "plots")
    save_observability_plots(observability_history, report_dir / "plots")
    save_training_summary(
        observability_history,
        report_dir / "summary.md",
        run_id=exp_dir.name,
        source_run_dir=exp_dir,
        early_stopping_metric=early_stopping_metric,
    )

    checkpoint = torch.load(exp_dir / "best_model.pth", map_location=device, weights_only=False)
    loaded = load_model_from_checkpoint(checkpoint, map_location=device)
    model = loaded.model
    model.eval()

    selected_threshold = float(cfg["threshold"])
    threshold_rows: list[dict[str, Any]] = []
    if bool(cfg["threshold_search"]):
        selected_threshold, threshold_rows, _ = threshold_search(model, val_loader, device, amp_enabled=amp_enabled)
        write_csv(threshold_rows, exp_dir / "threshold_search.csv")
        logger.info("validation-selected threshold: %.2f", selected_threshold)
    else:
        write_csv([], exp_dir / "threshold_search.csv", ["threshold", "micro_dice", "micro_iou", "macro_dice_mean", "macro_iou_mean"])

    checkpoint["threshold"] = selected_threshold
    torch.save(checkpoint, exp_dir / "best_model.pth")
    thresholds = sorted(set([0.5, selected_threshold]))
    test_eval = evaluate_model(
        model,
        test_loader,
        device,
        thresholds=thresholds,
        amp_enabled=amp_enabled,
        overlay_dir=exp_dir / "test_prediction_overlays",
        overlay_threshold=selected_threshold,
        max_overlays=20,
    )
    val_overlay_eval = evaluate_model(
        model,
        val_loader,
        device,
        thresholds=[selected_threshold],
        amp_enabled=amp_enabled,
        overlay_dir=exp_dir / "validation_prediction_overlays",
        overlay_threshold=selected_threshold,
        max_overlays=20,
    )
    save_evaluation_outputs(test_eval, exp_dir, "test")
    save_evaluation_outputs(val_overlay_eval, exp_dir, "validation")

    main_metrics = {
        "best_epoch": best["epoch"],
        "best_validation_dice": best["dice"],
        "best_validation_iou": best["iou"],
        "validation_selected_threshold": selected_threshold,
        "test": {f"{threshold:.2f}": {k: v for k, v in result.items() if k != "per_image"} for threshold, result in test_eval.items()},
        "dataset_summary": prepared.summary,
    }
    save_json(main_metrics, exp_dir / "metrics.json")
    summary = {
        "run_dir": str(exp_dir),
        "image_size": int(cfg["image_size"]),
        "epochs_completed": len(history),
        "best_checkpoint_path": str(exp_dir / "best_model.pth"),
        "last_checkpoint_path": str(exp_dir / "last_model.pth"),
        "checkpoint_selection_metric": early_stopping_metric,
        "best_epoch": best["epoch"],
        "best_validation_dice": best["dice"],
        "best_validation_iou": best["iou"],
        "selected_threshold": selected_threshold,
        "physical_batch_size": batch_size,
        "gradient_accumulation_steps": gradient_accumulation_steps,
        "effective_batch_size": effective_batch_size,
        "amp_active": amp_enabled,
        "source_resolution_summary": source_resolution_summary,
        "manifest_checksums": manifest_checksums,
        "environment": environment,
        "command": _command_line(),
    }
    save_json(summary, exp_dir / "summary.json")
    save_json({f"{t:.2f}": {k: test_eval[t]["micro"][k] for k in ["tp", "fp", "tn", "fn"]} for t in test_eval}, exp_dir / "confusion_counts.json")
    summary_rows = []
    for threshold, result in test_eval.items():
        summary_rows.append(
            {
                "split": "test",
                "threshold": threshold,
                "micro_dice": result["micro"]["dice"],
                "micro_iou": result["micro"]["iou"],
                "macro_dice_mean": result["macro"]["dice_mean"],
                "macro_iou_mean": result["macro"]["iou_mean"],
                "precision": result["micro"]["precision"],
                "recall": result["micro"]["recall"],
                "specificity": result["micro"]["specificity"],
                "pixel_accuracy": result["micro"]["pixel_accuracy"],
            }
        )
    write_csv(summary_rows, exp_dir / "metrics_summary.csv")
    return {
        "exp_dir": str(exp_dir),
        "best": best,
        "selected_threshold": selected_threshold,
        "test_eval": test_eval,
        "environment": environment,
        "epochs_completed": len(history),
    }


def main() -> None:
    args = parse_args()
    cfg = build_config(args)
    cfg["floortrans_root"] = args.floortrans_root
    cfg["allow_invalid_over_1pct"] = args.allow_invalid_over_1pct
    if args.run_name:
        run_name = args.run_name
    elif cfg.get("task_mode") == TASK_CUBICASA_MULTICLASS:
        run_name = f"mitunet_cubicasa_multiclass_{MASK_SCHEMA_VERSION}_{timestamp()}"
    else:
        run_name = timestamp()
    exp_root = Path(cfg["experiment_root"])
    exp_dir = exp_root / run_name
    if exp_dir.exists() and not args.resume:
        exp_dir = exp_root / f"{run_name}_{timestamp()}"
    exp_dir.mkdir(parents=True, exist_ok=args.resume)
    logger = setup_logging(exp_dir / "run.log")
    logger.info("experiment directory: %s", exp_dir)
    if args.resume:
        logger.info("resume requested")

    requested = int(cfg["batch_size"])
    candidates = []
    for value in [requested, 2, 1]:
        if value <= requested and value not in candidates:
            candidates.append(value)
    last_exc: Exception | None = None
    for batch_size in candidates:
        try:
            result = run_training_attempt(cfg, exp_dir, batch_size, logger, resume=args.resume)
            logger.info("training complete: %s", result["exp_dir"])
            return
        except RuntimeError as exc:
            last_exc = exc
            message = str(exc).lower()
            if "out of memory" in message and batch_size != candidates[-1]:
                logger.warning("OOM at batch size %s; retrying with smaller batch size", batch_size)
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                continue
            raise
    if last_exc is not None:
        raise last_exc


if __name__ == "__main__":
    main()
