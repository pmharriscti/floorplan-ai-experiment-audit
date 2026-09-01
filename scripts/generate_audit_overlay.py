#!/usr/bin/env python3
"""Generate small visual QA evidence for the audited floor-plan experiments.

The script reads verified historical manifests, checkpoints, metrics, saved
overlays, and probability maps. It writes only curated QA samples into this
audit repository and performs no training.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont


AUDIT_ROOT = Path(__file__).resolve().parents[1]
MITUNET_ROOT = Path("/home/pmharris/dev/mitunet")
PHASE1_ROOT = Path(
    "/mnt/e/AI_Team/mitunet/phase1_wall_structure/experiments/"
    "mitunet_phase1_wall_region_centerline_junctions_20260807_163622_UTC"
)
PHASE2_ROOT = Path(
    "/mnt/e/AI_Team/mitunet/phase2_wall_boundary_door_openings/experiments/"
    "mitunet_phase2_wall_boundary_door_openings_20260810_200219_UTC"
)

os.environ.setdefault("NO_ALBUMENTATIONS_UPDATE", "1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-codex")
sys.path.insert(0, str(MITUNET_ROOT))
os.chdir(MITUNET_ROOT)

from mitunet_cubicasa.dataset import CubiCasaWallDataset  # noqa: E402
from mitunet_cubicasa.metrics import counts_from_binary, metrics_from_counts  # noqa: E402
from mitunet_cubicasa.model import load_model_from_checkpoint  # noqa: E402
from mitunet_cubicasa.wall_structure_dataset import (  # noqa: E402
    CubiCasaWallStructureDataset,
    CubiCasaWallStructurePhase2Dataset,
)
from mitunet_cubicasa.wall_structure_metrics import points_from_heatmap  # noqa: E402
from mitunet_cubicasa.wall_structure_model import (  # noqa: E402
    CENTERLINE_LOGITS,
    DOOR_OPENING_LOGITS,
    JUNCTION_LOGITS,
    WALL_BOUNDARY_LOGITS,
    WALL_REGION_LOGITS,
    load_wall_structure_checkpoint,
)


IMAGENET_MEAN = np.asarray((0.485, 0.456, 0.406), dtype=np.float32)
IMAGENET_STD = np.asarray((0.229, 0.224, 0.225), dtype=np.float32)

SAMPLES = [
    {
        "sample_id": "high_quality_architectural/333",
        "role": "typical_clean_validation_case",
        "reason": "Shared validation sample with solid wall-region performance across the inspected runs.",
    },
    {
        "sample_id": "high_quality_architectural/3015",
        "role": "strong_high_resolution_case",
        "reason": "Shared validation sample where the 1024 px global model shows a clear wall-region gain.",
    },
    {
        "sample_id": "high_quality_architectural/5559",
        "role": "difficult_failure_case",
        "reason": "Shared validation sample with visibly lower wall-region and structural metrics.",
    },
]

PHASE1_THRESHOLDS = {
    "wall_region": 0.05,
    "centerline": 0.95,
    "junction": 0.85,
    "junction_nms_radius": 3,
}

PHASE2_THRESHOLDS = {
    "wall_region": 0.05,
    "centerline": 0.95,
    "junction": 0.9,
    "junction_nms_radius": 2,
    "wall_boundary": 0.95,
    "door_opening": 0.85,
    "door_min_component_area": 1,
}


@dataclass(frozen=True)
class BinaryExperiment:
    experiment_id: str
    name: str
    audit_dir: Path
    source_run_dir: Path
    manifest_csv: Path
    checkpoint_path: Path
    metrics_csv: Path
    historical_overlay_dir: Path
    image_size: int
    threshold: float
    provenance_note: str
    checkpoint_sha256: str | None = None
    metrics_filter: dict[str, str] | None = None
    extra_source_files: tuple[Path, ...] = ()


@dataclass(frozen=True)
class StructuralExperiment:
    experiment_id: str
    name: str
    audit_dir: Path
    source_run_dir: Path
    manifest_csv: Path
    checkpoint_path: Path | None
    checkpoint_sha256: str | None
    checkpoint_sha256_status: str
    image_size: int
    thresholds: dict[str, float | int]
    metrics_csvs: dict[str, Path]
    historical_target_qa_dir: Path


BINARY_EXPERIMENTS = [
    BinaryExperiment(
        experiment_id="01_binary_mitunet",
        name="Binary MitUNet baseline",
        audit_dir=AUDIT_ROOT / "experiments/01_binary_mitunet",
        source_run_dir=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu",
        manifest_csv=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu/val_manifest.csv",
        checkpoint_path=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu/best_model.pth",
        metrics_csv=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu/per_image_validation_metrics.csv",
        historical_overlay_dir=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu/validation_prediction_overlays",
        image_size=512,
        threshold=0.1,
        provenance_note="Prediction mask regenerated for audit by inference from the verified baseline checkpoint.",
        checkpoint_sha256="fb9665056aa06057a571f247882ba5d32abde297215f2ae94d210759f540b72f",
    ),
    BinaryExperiment(
        experiment_id="02_hybrid_tiling",
        name="Hybrid tiling / 1024 global-patch sweep",
        audit_dir=AUDIT_ROOT / "experiments/02_hybrid_tiling",
        source_run_dir=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024",
        manifest_csv=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/val_manifest.csv",
        checkpoint_path=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/best_model.pth",
        metrics_csv=MITUNET_ROOT
        / "reports/binary_wall_hybrid_global_patch/20260723T021006Z/val_fusion_weights_per_image_metrics.csv",
        historical_overlay_dir=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/validation_prediction_overlays",
        image_size=1024,
        threshold=0.5,
        provenance_note=(
            "Prediction mask regenerated from the verified 1024 px global checkpoint. "
            "This represents the locked hybrid selection because the selected fusion used "
            "global_weight=1.0 and patch_weight=0.0."
        ),
        checkpoint_sha256="42cad015bf894e6afe11011424b7ed88c49a1512f81593f14df5b228d65a3910",
        metrics_filter={
            "method": "hybrid",
            "crop_size": "1024",
            "overlap": "0.5",
            "blending": "gaussian",
            "global_weight": "1.0",
        },
        extra_source_files=(
            MITUNET_ROOT / "reports/binary_wall_hybrid_global_patch/20260723T021006Z/locked_validation_selection.json",
            MITUNET_ROOT / "reports/binary_wall_hybrid_global_patch/20260723T021006Z/val_crop1024_overlap0.5_gaussian_gw1_summary.json",
            Path("/mnt/e/AI_Team/mitunet/experiments/binary_wall_hybrid_global_patch/20260723T021043Z/experiment_manifest.json"),
        ),
    ),
    BinaryExperiment(
        experiment_id="03_deeplabv3",
        name="DeepLabV3-ResNet50 comparator",
        audit_dir=AUDIT_ROOT / "experiments/03_deeplabv3",
        source_run_dir=Path(
            "/mnt/e/AI_Team/mitunet/experiments/cubicasa5k_deeplabv3_resnet50/"
            "deeplabv3_resnet50_wall_512_imagenet_aux_seed42_20260805T154529Z"
        ),
        manifest_csv=Path(
            "/mnt/e/AI_Team/mitunet/experiments/cubicasa5k_deeplabv3_resnet50/"
            "deeplabv3_resnet50_wall_512_imagenet_aux_seed42_20260805T154529Z/val_manifest.csv"
        ),
        checkpoint_path=Path(
            "/mnt/e/AI_Team/mitunet/experiments/cubicasa5k_deeplabv3_resnet50/"
            "deeplabv3_resnet50_wall_512_imagenet_aux_seed42_20260805T154529Z/best_model.pth"
        ),
        metrics_csv=Path(
            "/mnt/e/AI_Team/mitunet/experiments/cubicasa5k_deeplabv3_resnet50/"
            "deeplabv3_resnet50_wall_512_imagenet_aux_seed42_20260805T154529Z/per_image_validation_metrics.csv"
        ),
        historical_overlay_dir=Path(
            "/mnt/e/AI_Team/mitunet/experiments/cubicasa5k_deeplabv3_resnet50/"
            "deeplabv3_resnet50_wall_512_imagenet_aux_seed42_20260805T154529Z/validation_prediction_overlays"
        ),
        image_size=512,
        threshold=0.5,
        provenance_note="Prediction mask regenerated for audit by inference from the verified DeepLabV3 checkpoint.",
        checkpoint_sha256="c1da3cccf9d06c1e7f0023ee04797493452c8bd031de5bd0125d9cb4230d11d8",
    ),
    BinaryExperiment(
        experiment_id="06_binary_mitunet_1024",
        name="Binary MitUNet 1024 px global",
        audit_dir=AUDIT_ROOT / "experiments/06_binary_mitunet_1024",
        source_run_dir=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024",
        manifest_csv=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/val_manifest.csv",
        checkpoint_path=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/best_model.pth",
        metrics_csv=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/per_image_validation_metrics.csv",
        historical_overlay_dir=MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/validation_prediction_overlays",
        image_size=1024,
        threshold=0.1,
        provenance_note=(
            "Prediction mask regenerated for audit by inference from the verified 1024 px global MitUNet "
            "checkpoint at the run-selected threshold."
        ),
        checkpoint_sha256="42cad015bf894e6afe11011424b7ed88c49a1512f81593f14df5b228d65a3910",
        extra_source_files=(
            MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/summary.json",
            MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/metrics.json",
            MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/threshold_search.csv",
            MITUNET_ROOT / "experiments/cubicasa5k_mitunet/full_gpu_1024/run_config_resolved.yaml",
        ),
    ),
]

PHASE1_EXPERIMENT = StructuralExperiment(
    experiment_id="04_phase1_wall_structure",
    name="Phase 1 wall structure",
    audit_dir=AUDIT_ROOT / "experiments/04_phase1_wall_structure",
    source_run_dir=PHASE1_ROOT,
    manifest_csv=PHASE1_ROOT / "metrics/label_statistics.csv",
    checkpoint_path=PHASE1_ROOT / "checkpoints/best_structural_score.pth",
    checkpoint_sha256=None,
    checkpoint_sha256_status="deferred_in_source_checkpoint_manifest",
    image_size=512,
    thresholds=PHASE1_THRESHOLDS,
    metrics_csvs={
        "centerline": PHASE1_ROOT / "metrics/per_image_centerline_metrics.csv",
        "junction": PHASE1_ROOT / "metrics/per_image_junction_metrics.csv",
        "graph": PHASE1_ROOT / "metrics/per_image_graph_metrics.csv",
    },
    historical_target_qa_dir=PHASE1_ROOT / "overlays/target_qa",
)

PHASE2_EXPERIMENT = StructuralExperiment(
    experiment_id="05_phase2_boundary_openings",
    name="Phase 2 boundary and door/openings",
    audit_dir=AUDIT_ROOT / "experiments/05_phase2_boundary_openings",
    source_run_dir=PHASE2_ROOT,
    manifest_csv=PHASE2_ROOT / "metrics/label_statistics.csv",
    checkpoint_path=PHASE2_ROOT / "checkpoints/best_phase2_structural_score.pth",
    checkpoint_sha256=None,
    checkpoint_sha256_status="deferred_in_source_checkpoint_manifest",
    image_size=512,
    thresholds=PHASE2_THRESHOLDS,
    metrics_csvs={
        "combined": PHASE2_ROOT / "metrics/per_image_metrics.csv",
        "boundary": PHASE2_ROOT / "metrics/boundary_metrics.csv",
        "door_opening": PHASE2_ROOT / "metrics/door_opening_metrics.csv",
        "graph": PHASE2_ROOT / "metrics/graph_metrics.csv",
    },
    historical_target_qa_dir=PHASE2_ROOT / "overlays/target_qa",
)


def safe_id(sample_id: str) -> str:
    return sample_id.strip("/").replace("/", "__")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_value(value: str | None) -> Any:
    if value is None or value == "":
        return None
    if value in {"True", "False"}:
        return value == "True"
    for parser in (int, float):
        try:
            return parser(value)
        except ValueError:
            pass
    return value


def parsed_row(row: dict[str, str] | None) -> dict[str, Any]:
    return {key: parse_value(value) for key, value in (row or {}).items()}


def row_by_sample(path: Path) -> dict[str, dict[str, str]]:
    return {row["sample_id"]: row for row in read_csv_rows(path)}


def metric_row(path: Path, sample_id: str, filters: dict[str, str] | None = None) -> dict[str, Any]:
    for row in read_csv_rows(path):
        if row.get("sample_id") != sample_id:
            continue
        if filters and any(str(row.get(key)) != expected for key, expected in filters.items()):
            continue
        return parsed_row(row)
    return {}


def binary_mask(array: np.ndarray) -> np.ndarray:
    out = (np.asarray(array) > 0).astype(np.uint8)
    if out.ndim != 2:
        raise ValueError(f"Expected [H,W] binary mask, got {out.shape}")
    return out


def mask_stats(mask: np.ndarray) -> dict[str, Any]:
    values = sorted(int(v) for v in np.unique(mask).tolist())
    if not set(values).issubset({0, 1, 255}):
        raise ValueError(f"Mask contains non-binary values: {values}")
    normalized = binary_mask(mask)
    return {
        "shape": [int(normalized.shape[0]), int(normalized.shape[1])],
        "unique_values": values,
        "positive_pixels": int(normalized.sum()),
        "positive_fraction": float(normalized.mean()),
    }


def unnormalize_image(image_tensor: torch.Tensor) -> np.ndarray:
    array = image_tensor.detach().cpu().float().numpy()
    if array.ndim != 3:
        raise ValueError(f"Expected CHW tensor, got {array.shape}")
    array = np.transpose(array, (1, 2, 0))
    array = (array * IMAGENET_STD + IMAGENET_MEAN) * 255.0
    return np.clip(np.rint(array), 0, 255).astype(np.uint8)


def primary_binary_logits(outputs: torch.Tensor | dict[str, torch.Tensor]) -> torch.Tensor:
    if isinstance(outputs, torch.Tensor):
        return outputs
    for key in ("out", "logits", "mask", "prediction"):
        value = outputs.get(key)
        if isinstance(value, torch.Tensor):
            return value
    raise KeyError("Binary model output dictionary did not contain primary logits.")


def tensor_mask(value: torch.Tensor | np.ndarray) -> np.ndarray:
    if isinstance(value, torch.Tensor):
        value = value.detach().cpu().numpy()
    value = np.asarray(value)
    if value.ndim == 3 and value.shape[0] == 1:
        value = value[0]
    return binary_mask(value)


def save_rgb(path: Path, array: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.asarray(array, dtype=np.uint8), mode="RGB").save(path)


def save_mask(path: Path, mask: np.ndarray) -> None:
    mask = binary_mask(mask)
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray((mask * 255).astype(np.uint8), mode="L").save(path)


def save_error_overlay(path: Path, source: np.ndarray, gt: np.ndarray, pred: np.ndarray) -> None:
    gt = binary_mask(gt).astype(bool)
    pred = binary_mask(pred).astype(bool)
    base = Image.fromarray(np.asarray(source, dtype=np.uint8), mode="RGB").convert("RGBA")
    color = np.zeros((gt.shape[0], gt.shape[1], 4), dtype=np.uint8)
    color[np.logical_and(gt, pred)] = (0, 170, 90, 130)
    color[np.logical_and(~gt, pred)] = (230, 55, 55, 150)
    color[np.logical_and(gt, ~pred)] = (45, 115, 230, 160)
    overlay = Image.alpha_composite(base, Image.fromarray(color, mode="RGBA")).convert("RGB")
    path.parent.mkdir(parents=True, exist_ok=True)
    overlay.save(path)


def render_points(points: list[dict[str, Any]], shape: tuple[int, int], radius: int = 4) -> np.ndarray:
    canvas = Image.new("L", (int(shape[1]), int(shape[0])), 0)
    draw = ImageDraw.Draw(canvas)
    for point in points:
        x = int(round(float(point["x"])))
        y = int(round(float(point["y"])))
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=255)
    return (np.asarray(canvas, dtype=np.uint8) > 0).astype(np.uint8)


def find_dataset_index(dataset: Any, sample_id: str) -> int:
    for idx, row in enumerate(dataset.rows):
        if row["sample_id"] == sample_id:
            return idx
    raise KeyError(f"{sample_id} not found in dataset.")


def copy_or_mark(src: Path | None, dst: Path, unavailable_text: str) -> dict[str, Any]:
    if src is None or not src.exists():
        marker = dst.with_suffix(".NOT_YET_AVAILABLE.txt")
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(unavailable_text + "\n", encoding="utf-8")
        return {"status": "NOT_YET_AVAILABLE", "audit_path": str(marker.relative_to(AUDIT_ROOT))}
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {
        "status": "VERIFIED",
        "source_path": str(src),
        "source_sha256": sha256_file(src),
        "audit_path": str(dst.relative_to(AUDIT_ROOT)),
        "audit_sha256": sha256_file(dst),
    }


def find_historical_prediction_overlay(exp: BinaryExperiment, sample_id: str) -> Path | None:
    matches = sorted(exp.historical_overlay_dir.glob(f"*_{safe_id(sample_id)}.jpg"))
    return matches[0] if matches else None


def find_historical_target_qa(root: Path, sample_id: str) -> Path | None:
    matches = sorted(root.rglob(f"{safe_id(sample_id)}.png"))
    random_val = [path for path in matches if "/random_val/" in str(path)]
    return (random_val or matches or [None])[0]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_binary_model(checkpoint_path: Path, device: torch.device) -> torch.nn.Module:
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    result = load_model_from_checkpoint(checkpoint, map_location=device)
    result.model.eval()
    return result.model


def load_phase1_model(checkpoint_path: Path, device: torch.device) -> torch.nn.Module:
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    result = load_wall_structure_checkpoint(checkpoint, map_location=device)
    result.model.eval()
    return result.model


def binary_probability(model: torch.nn.Module, image_tensor: torch.Tensor, device: torch.device) -> np.ndarray:
    with torch.no_grad():
        logits = primary_binary_logits(model(image_tensor.unsqueeze(0).to(device)))
        probability = torch.sigmoid(logits)[0, 0].detach().cpu().numpy()
    if probability.ndim != 2:
        raise ValueError(f"Expected [H,W] probability, got {probability.shape}")
    return probability


def phase1_probabilities(model: torch.nn.Module, image_tensor: torch.Tensor, device: torch.device) -> dict[str, np.ndarray]:
    with torch.no_grad():
        outputs = model(image_tensor.unsqueeze(0).to(device))
    return {
        "wall_region": torch.sigmoid(outputs[WALL_REGION_LOGITS])[0, 0].detach().cpu().numpy(),
        "centerline": torch.sigmoid(outputs[CENTERLINE_LOGITS])[0, 0].detach().cpu().numpy(),
        "junction": torch.sigmoid(outputs[JUNCTION_LOGITS])[0, 0].detach().cpu().numpy(),
    }


def threshold_door(probability: np.ndarray, threshold: float, min_area: int) -> np.ndarray:
    mask = (np.asarray(probability) >= float(threshold)).astype(np.uint8)
    if int(min_area) <= 1:
        return mask
    from scipy import ndimage as ndi

    labels, count = ndi.label(mask, structure=np.ones((3, 3), dtype=bool))
    out = np.zeros_like(mask)
    for idx in range(1, int(count) + 1):
        comp = labels == idx
        if int(comp.sum()) >= int(min_area):
            out[comp] = 1
    return out


def file_records(paths: dict[str, Path], skip_sha256_names: set[str] | None = None) -> dict[str, dict[str, Any]]:
    records = {}
    skip_sha256_names = skip_sha256_names or set()
    for name, path in paths.items():
        records[name] = {
            "path": str(path),
            "exists": path.exists(),
            "sha256": None if name in skip_sha256_names or not path.exists() else sha256_file(path),
            "sha256_status": "skipped_large_artifact" if name in skip_sha256_names and path.exists() else None,
        }
    return records


def recomputed_binary_metrics(pred: np.ndarray, gt: np.ndarray) -> dict[str, Any]:
    counts = counts_from_binary(binary_mask(pred), binary_mask(gt))
    computed = metrics_from_counts(counts)
    return {
        "iou": computed["iou"],
        "dice": computed["dice"],
        "precision": computed["precision"],
        "recall": computed["recall"],
        "tp": counts.tp,
        "fp": counts.fp,
        "tn": counts.tn,
        "fn": counts.fn,
    }


def make_contact_sheet(
    qa_root: Path,
    sample_dirs: list[Path],
    columns: list[tuple[str, str]],
    *,
    output_name: str = "contact_sheet.png",
) -> Path:
    thumb_w = 220
    label_h = 26
    sample_label_h = 30
    gutter = 10
    width = len(columns) * thumb_w + (len(columns) + 1) * gutter
    row_h = sample_label_h + label_h + thumb_w + gutter
    height = gutter + len(sample_dirs) * row_h
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    y = gutter
    for sample_dir in sample_dirs:
        metadata = json.loads((sample_dir / "metadata.json").read_text(encoding="utf-8"))
        draw.text((gutter, y), f"{metadata['sample_id']} ({metadata['sample_role']})", fill=(20, 20, 20), font=font)
        y += sample_label_h
        for col, (filename, title) in enumerate(columns):
            x = gutter + col * (thumb_w + gutter)
            draw.text((x, y), title, fill=(20, 20, 20), font=font)
            image = Image.open(sample_dir / filename).convert("RGB")
            resample = Image.Resampling.NEAREST if "mask" in filename else Image.Resampling.LANCZOS
            image.thumbnail((thumb_w, thumb_w), resample)
            panel = Image.new("RGB", (thumb_w, thumb_w), (245, 245, 245))
            panel.paste(image, ((thumb_w - image.width) // 2, (thumb_w - image.height) // 2))
            sheet.paste(panel, (x, y + label_h))
        y += label_h + thumb_w + gutter
    out = qa_root / output_name
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    return out


def write_binary_qa_readme(exp: BinaryExperiment, samples_meta: list[dict[str, Any]], contact_sheet: Path) -> None:
    rows = []
    for meta in samples_meta:
        metrics = meta["per_image_metrics_from_source_csv"]
        rows.append(
            "| "
            + " | ".join(
                [
                    meta["sample_id"],
                    meta["sample_role"],
                    f"{metrics.get('iou'):.6f}" if isinstance(metrics.get("iou"), float) else str(metrics.get("iou")),
                    f"{metrics.get('dice'):.6f}" if isinstance(metrics.get("dice"), float) else str(metrics.get("dice")),
                    f"[metadata]({safe_id(meta['sample_id'])}/metadata.json)",
                    f"[overlay]({safe_id(meta['sample_id'])}/overlay_wall_errors.png)",
                ]
            )
            + " |"
        )
    readme = "\n".join(
        [
            f"# Visual QA - {exp.name}",
            "",
            "This directory contains three curated validation samples for visual audit. Predictions were regenerated by inference from the verified checkpoint and source validation manifest; no training was run.",
            "",
            f"Contact sheet: [contact_sheet.png]({contact_sheet.name})",
            "",
            "Overlay palette: green = true positive, red = false positive, blue = false negative.",
            "",
            "| Sample | Role | Source IoU | Source Dice | Metadata | Overlay |",
            "| --- | --- | ---: | ---: | --- | --- |",
            *rows,
            "",
            "Each sample folder includes `source.png`, `ground_truth_wall_mask.png`, `prediction_wall_mask.png`, `overlay_wall_errors.png`, `historical_validation_overlay.jpg`, and `metadata.json`.",
            "",
        ]
    )
    (exp.audit_dir / "qa/README.md").write_text(readme, encoding="utf-8")


def write_structural_qa_readme(exp: StructuralExperiment, samples_meta: list[dict[str, Any]], contact_sheet: Path) -> None:
    rows = []
    for meta in samples_meta:
        metrics = meta["per_image_metrics_from_source_csvs"]
        if exp.experiment_id == "04_phase1_wall_structure":
            center = (metrics.get("centerline") or {}).get("cldice")
            junction = (metrics.get("junction") or {}).get("junction_f1_5px")
            metric_text = f"centerline clDice {center:.6f}; junction F1@5 {junction:.6f}"
        else:
            combined = metrics.get("combined") or {}
            metric_text = (
                f"wall IoU {combined.get('wall_region_iou'):.6f}; "
                f"boundary F1@2 {combined.get('boundary_f1_2px'):.6f}; "
                f"door F1 {combined.get('door_opening_object_f1'):.6f}"
            )
        rows.append(
            "| "
            + " | ".join(
                [
                    meta["sample_id"],
                    meta["sample_role"],
                    metric_text,
                    f"[metadata]({safe_id(meta['sample_id'])}/metadata.json)",
                    f"[overlay]({safe_id(meta['sample_id'])}/{meta['primary_overlay']})",
                ]
            )
            + " |"
        )
    readme = "\n".join(
        [
            f"# Visual QA - {exp.name}",
            "",
            "This directory contains three curated validation samples for visual audit. Structural predictions come from verified historical checkpoints or saved probability maps; no training was run.",
            "",
            f"Contact sheet: [contact_sheet.png]({contact_sheet.name})",
            "",
            "Overlay palette: green = true positive, red = false positive, blue = false negative.",
            "",
            "| Sample | Role | Source Metrics | Metadata | Primary Overlay |",
            "| --- | --- | --- | --- | --- |",
            *rows,
            "",
            "Each sample folder includes a source image, target masks, prediction masks, overlays, historical target QA where available, and `metadata.json`.",
            "",
        ]
    )
    (exp.audit_dir / "qa/README.md").write_text(readme, encoding="utf-8")


def generate_binary_experiment(exp: BinaryExperiment, device: torch.device) -> dict[str, Any]:
    qa_root = exp.audit_dir / "qa"
    qa_root.mkdir(parents=True, exist_ok=True)
    dataset = CubiCasaWallDataset(
        exp.manifest_csv,
        "val",
        image_size=exp.image_size,
        resize_mode="letterbox",
        augment=False,
    )
    manifest_by_id = row_by_sample(exp.manifest_csv)
    checkpoint_sha = exp.checkpoint_sha256 or sha256_file(exp.checkpoint_path)
    model = load_binary_model(exp.checkpoint_path, device)
    sample_dirs: list[Path] = []
    samples_meta: list[dict[str, Any]] = []
    for sample in SAMPLES:
        sample_id = sample["sample_id"]
        item = dataset[find_dataset_index(dataset, sample_id)]
        source = unnormalize_image(item["image"])
        gt = tensor_mask(item["mask"])
        probability = binary_probability(model, item["image"], device)
        pred = (probability >= exp.threshold).astype(np.uint8)
        sample_dir = qa_root / safe_id(sample_id)
        save_rgb(sample_dir / "source.png", source)
        save_mask(sample_dir / "ground_truth_wall_mask.png", gt)
        save_mask(sample_dir / "prediction_wall_mask.png", pred)
        save_error_overlay(sample_dir / "overlay_wall_errors.png", source, gt, pred)
        historical = copy_or_mark(
            find_historical_prediction_overlay(exp, sample_id),
            sample_dir / "historical_validation_overlay.jpg",
            "Historical validation prediction overlay was not found in the source overlay directory.",
        )
        metric = metric_row(exp.metrics_csv, sample_id, exp.metrics_filter)
        source_paths = {
            "manifest_csv": exp.manifest_csv,
            "metrics_csv": exp.metrics_csv,
            "checkpoint": exp.checkpoint_path,
            "source_image": Path(str(item["image_path"])),
            "source_wall_mask": Path(str(item["mask_path"])),
        }
        metadata = {
            "experiment_id": exp.experiment_id,
            "experiment_name": exp.name,
            "sample_id": sample_id,
            "sample_role": sample["role"],
            "selection_reason": sample["reason"],
            "split": "val",
            "visual_evidence_status": "VERIFIED",
            "source_run_directory": str(exp.source_run_dir),
            "manifest_row": manifest_by_id.get(sample_id, {}),
            "checkpoint": {"path": str(exp.checkpoint_path), "sha256": checkpoint_sha},
            "threshold": exp.threshold,
            "image_size": exp.image_size,
            "prediction_provenance": exp.provenance_note,
            "source_files": file_records(source_paths, skip_sha256_names={"checkpoint"}),
            "extra_source_files": file_records({path.name: path for path in exp.extra_source_files}),
            "per_image_metrics_from_source_csv": metric,
            "per_image_metrics_recomputed_from_saved_masks": recomputed_binary_metrics(pred, gt),
            "assets": {
                "source": "source.png",
                "ground_truth_wall_mask": "ground_truth_wall_mask.png",
                "prediction_wall_mask": "prediction_wall_mask.png",
                "overlay_wall_errors": "overlay_wall_errors.png",
                "historical_validation_overlay": historical,
            },
            "mask_integrity": {
                "ground_truth_wall_mask": mask_stats(gt),
                "prediction_wall_mask": mask_stats(pred),
            },
            "generation": {
                "script": "scripts/generate_audit_overlay.py",
                "source_image_policy": "Letterboxed validation image regenerated from the source manifest and saved as a review copy.",
                "mask_resize_policy": "Nearest-neighbor mask handling inherited from the validation dataset transform.",
                "overlay_palette": {"true_positive": "green", "false_positive": "red", "false_negative": "blue"},
                "no_training_performed": True,
                "historical_directories_modified": False,
            },
        }
        write_json(sample_dir / "metadata.json", metadata)
        sample_dirs.append(sample_dir)
        samples_meta.append(metadata)
    contact = make_contact_sheet(
        qa_root,
        sample_dirs,
        [
            ("source.png", "Source"),
            ("ground_truth_wall_mask.png", "GT wall"),
            ("prediction_wall_mask.png", "Pred wall"),
            ("overlay_wall_errors.png", "Overlay"),
        ],
    )
    write_binary_qa_readme(exp, samples_meta, contact)
    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return {
        "experiment_id": exp.experiment_id,
        "sample_count": len(samples_meta),
        "qa_root": str(qa_root.relative_to(AUDIT_ROOT)),
        "contact_sheet": str(contact.relative_to(AUDIT_ROOT)),
    }


def generate_phase1(exp: StructuralExperiment, device: torch.device) -> dict[str, Any]:
    qa_root = exp.audit_dir / "qa"
    qa_root.mkdir(parents=True, exist_ok=True)
    dataset = CubiCasaWallStructureDataset(
        exp.manifest_csv,
        "val",
        image_size=exp.image_size,
        resize_mode="letterbox",
        augment=False,
    )
    manifest_by_id = row_by_sample(exp.manifest_csv)
    checkpoint_path = exp.checkpoint_path
    if checkpoint_path is None:
        raise ValueError("Phase 1 generation requires a checkpoint.")
    checkpoint_sha = exp.checkpoint_sha256
    model = load_phase1_model(checkpoint_path, device)
    sample_dirs: list[Path] = []
    samples_meta: list[dict[str, Any]] = []
    for sample in SAMPLES:
        sample_id = sample["sample_id"]
        item = dataset[find_dataset_index(dataset, sample_id)]
        source = unnormalize_image(item["image"])
        probs = phase1_probabilities(model, item["image"], device)
        wall_gt = tensor_mask(item["wall_region_mask"])
        wall_pred = (probs["wall_region"] >= float(exp.thresholds["wall_region"])).astype(np.uint8)
        center_gt = tensor_mask(item["raw_centerline_mask"])
        center_pred = (probs["centerline"] >= float(exp.thresholds["centerline"])).astype(np.uint8)
        target_points = json.loads(item["junctions_json"])
        predicted_points = points_from_heatmap(
            probs["junction"],
            threshold=float(exp.thresholds["junction"]),
            nms_radius=int(exp.thresholds["junction_nms_radius"]),
        )
        junction_gt = render_points(target_points, wall_gt.shape)
        junction_pred = render_points(predicted_points, wall_gt.shape)
        sample_dir = qa_root / safe_id(sample_id)
        save_rgb(sample_dir / "source.png", source)
        save_mask(sample_dir / "ground_truth_wall_region_mask.png", wall_gt)
        save_mask(sample_dir / "prediction_wall_region_mask.png", wall_pred)
        save_error_overlay(sample_dir / "overlay_wall_region_errors.png", source, wall_gt, wall_pred)
        save_mask(sample_dir / "ground_truth_centerline_mask.png", center_gt)
        save_mask(sample_dir / "prediction_centerline_mask.png", center_pred)
        save_error_overlay(sample_dir / "overlay_centerline_errors.png", source, center_gt, center_pred)
        save_mask(sample_dir / "ground_truth_junction_mask.png", junction_gt)
        save_mask(sample_dir / "prediction_junction_mask.png", junction_pred)
        save_error_overlay(sample_dir / "overlay_junction_errors.png", source, junction_gt, junction_pred)
        historical = copy_or_mark(
            find_historical_target_qa(exp.historical_target_qa_dir, sample_id),
            sample_dir / "historical_target_qa.png",
            "Historical target QA composite was not found for this sample.",
        )
        metric_rows = {name: metric_row(path, sample_id) for name, path in exp.metrics_csvs.items()}
        source_paths = {
            "manifest_csv": exp.manifest_csv,
            "checkpoint": checkpoint_path,
            "source_image": Path(str(item["image_path"])),
            "source_wall_mask": Path(str(item["mask_path"])),
            "wall_region_mask": Path(str(item["wall_region_mask_path"])),
            "raw_centerline_mask": Path(str(item["raw_centerline_mask_path"])),
            "centerline_training_mask": Path(str(item["centerline_training_mask_path"])),
            "junction_mask": Path(str(item["junction_mask_path"])),
            "junction_metadata": Path(str(item["junction_metadata_path"])),
        }
        metadata = {
            "experiment_id": exp.experiment_id,
            "experiment_name": exp.name,
            "sample_id": sample_id,
            "sample_role": sample["role"],
            "selection_reason": sample["reason"],
            "split": "val",
            "visual_evidence_status": "VERIFIED",
            "source_run_directory": str(exp.source_run_dir),
            "manifest_row": manifest_by_id.get(sample_id, {}),
            "checkpoint": {
                "path": str(checkpoint_path),
                "sha256": checkpoint_sha,
                "sha256_status": exp.checkpoint_sha256_status,
            },
            "thresholds": exp.thresholds,
            "image_size": exp.image_size,
            "prediction_provenance": "Predictions regenerated for audit by inference from the verified Phase 1 structural checkpoint.",
            "source_files": file_records(source_paths, skip_sha256_names={"checkpoint"}),
            "per_image_metrics_from_source_csvs": metric_rows,
            "per_image_metrics_recomputed_from_saved_masks": {
                "wall_region": recomputed_binary_metrics(wall_pred, wall_gt),
                "centerline_pixel": recomputed_binary_metrics(center_pred, center_gt),
                "junction_rendered_points": recomputed_binary_metrics(junction_pred, junction_gt),
            },
            "assets": {
                "source": "source.png",
                "ground_truth_wall_region_mask": "ground_truth_wall_region_mask.png",
                "prediction_wall_region_mask": "prediction_wall_region_mask.png",
                "overlay_wall_region_errors": "overlay_wall_region_errors.png",
                "ground_truth_centerline_mask": "ground_truth_centerline_mask.png",
                "prediction_centerline_mask": "prediction_centerline_mask.png",
                "overlay_centerline_errors": "overlay_centerline_errors.png",
                "ground_truth_junction_mask": "ground_truth_junction_mask.png",
                "prediction_junction_mask": "prediction_junction_mask.png",
                "overlay_junction_errors": "overlay_junction_errors.png",
                "historical_target_qa": historical,
            },
            "junction_visualization": {
                "target_point_count": len(target_points),
                "predicted_point_count": len(predicted_points),
                "point_render_radius_px": 4,
                "source_metric_policy": "Historical junction metrics use point matching; saved masks render those points for visual inspection.",
            },
            "mask_integrity": {
                "ground_truth_wall_region_mask": mask_stats(wall_gt),
                "prediction_wall_region_mask": mask_stats(wall_pred),
                "ground_truth_centerline_mask": mask_stats(center_gt),
                "prediction_centerline_mask": mask_stats(center_pred),
                "ground_truth_junction_mask": mask_stats(junction_gt),
                "prediction_junction_mask": mask_stats(junction_pred),
            },
            "generation": {
                "script": "scripts/generate_audit_overlay.py",
                "source_image_policy": "Letterboxed validation image regenerated from the source manifest and saved as a review copy.",
                "mask_resize_policy": "Nearest-neighbor mask handling inherited from the Phase 1 validation dataset transform.",
                "overlay_palette": {"true_positive": "green", "false_positive": "red", "false_negative": "blue"},
                "no_training_performed": True,
                "historical_directories_modified": False,
            },
            "primary_overlay": "overlay_wall_region_errors.png",
        }
        write_json(sample_dir / "metadata.json", metadata)
        sample_dirs.append(sample_dir)
        samples_meta.append(metadata)
    contact = make_contact_sheet(
        qa_root,
        sample_dirs,
        [
            ("source.png", "Source"),
            ("overlay_wall_region_errors.png", "Wall region"),
            ("overlay_centerline_errors.png", "Centerline"),
            ("overlay_junction_errors.png", "Junction"),
        ],
    )
    write_structural_qa_readme(exp, samples_meta, contact)
    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return {
        "experiment_id": exp.experiment_id,
        "sample_count": len(samples_meta),
        "qa_root": str(qa_root.relative_to(AUDIT_ROOT)),
        "contact_sheet": str(contact.relative_to(AUDIT_ROOT)),
    }


def generate_phase2(exp: StructuralExperiment) -> dict[str, Any]:
    qa_root = exp.audit_dir / "qa"
    qa_root.mkdir(parents=True, exist_ok=True)
    dataset = CubiCasaWallStructurePhase2Dataset(
        exp.manifest_csv,
        "val",
        image_size=exp.image_size,
        resize_mode="letterbox",
        augment=False,
    )
    manifest_by_id = row_by_sample(exp.manifest_csv)
    sample_dirs: list[Path] = []
    samples_meta: list[dict[str, Any]] = []
    checkpoint_record = (
        {
            "path": str(exp.checkpoint_path),
            "sha256": exp.checkpoint_sha256,
            "sha256_status": exp.checkpoint_sha256_status,
        }
        if exp.checkpoint_path is not None and exp.checkpoint_path.exists()
        else {"path": None, "sha256": None}
    )
    for sample in SAMPLES:
        sample_id = sample["sample_id"]
        item = dataset[find_dataset_index(dataset, sample_id)]
        source = unnormalize_image(item["image"])
        probability_path = exp.source_run_dir / "probability_maps/val" / f"{safe_id(sample_id)}.npz"
        with np.load(probability_path) as data:
            probs = {key: np.asarray(data[key], dtype=np.float32) for key in data.files}
        wall_gt = tensor_mask(item["wall_region_mask"])
        wall_pred = (probs["wall_region"] >= float(exp.thresholds["wall_region"])).astype(np.uint8)
        center_gt = tensor_mask(item["raw_centerline_mask"])
        center_pred = (probs["centerline"] >= float(exp.thresholds["centerline"])).astype(np.uint8)
        target_points = json.loads(item["junctions_json"])
        predicted_points = points_from_heatmap(
            probs["junction"],
            threshold=float(exp.thresholds["junction"]),
            nms_radius=int(exp.thresholds["junction_nms_radius"]),
        )
        junction_gt = render_points(target_points, wall_gt.shape)
        junction_pred = render_points(predicted_points, wall_gt.shape)
        boundary_gt = tensor_mask(item["raw_wall_boundary_mask"])
        boundary_pred = (probs["wall_boundary"] >= float(exp.thresholds["wall_boundary"])).astype(np.uint8)
        door_gt = tensor_mask(item["raw_door_opening_mask"])
        door_pred = threshold_door(
            probs["door_opening"],
            threshold=float(exp.thresholds["door_opening"]),
            min_area=int(exp.thresholds["door_min_component_area"]),
        )
        sample_dir = qa_root / safe_id(sample_id)
        save_rgb(sample_dir / "source.png", source)
        save_mask(sample_dir / "ground_truth_wall_region_mask.png", wall_gt)
        save_mask(sample_dir / "prediction_wall_region_mask.png", wall_pred)
        save_error_overlay(sample_dir / "overlay_wall_region_errors.png", source, wall_gt, wall_pred)
        save_mask(sample_dir / "ground_truth_centerline_mask.png", center_gt)
        save_mask(sample_dir / "prediction_centerline_mask.png", center_pred)
        save_error_overlay(sample_dir / "overlay_centerline_errors.png", source, center_gt, center_pred)
        save_mask(sample_dir / "ground_truth_junction_mask.png", junction_gt)
        save_mask(sample_dir / "prediction_junction_mask.png", junction_pred)
        save_error_overlay(sample_dir / "overlay_junction_errors.png", source, junction_gt, junction_pred)
        save_mask(sample_dir / "ground_truth_wall_boundary_mask.png", boundary_gt)
        save_mask(sample_dir / "prediction_wall_boundary_mask.png", boundary_pred)
        save_error_overlay(sample_dir / "overlay_wall_boundary_errors.png", source, boundary_gt, boundary_pred)
        save_mask(sample_dir / "ground_truth_door_opening_mask.png", door_gt)
        save_mask(sample_dir / "prediction_door_opening_mask.png", door_pred)
        save_error_overlay(sample_dir / "overlay_door_opening_errors.png", source, door_gt, door_pred)
        historical = copy_or_mark(
            find_historical_target_qa(exp.historical_target_qa_dir, sample_id),
            sample_dir / "historical_target_qa.png",
            "Historical target QA composite was not found for this sample.",
        )
        metric_rows = {name: metric_row(path, sample_id) for name, path in exp.metrics_csvs.items()}
        source_paths = {
            "manifest_csv": exp.manifest_csv,
            "probability_map": probability_path,
            "source_image": Path(str(item["image_path"])),
            "source_wall_mask": Path(str(item["mask_path"])),
            "wall_region_mask": Path(str(item["wall_region_mask_path"])),
            "raw_centerline_mask": Path(str(item["raw_centerline_mask_path"])),
            "junction_mask": Path(str(item["junction_mask_path"])),
            "wall_boundary_raw_mask": Path(str(item["wall_boundary_raw_mask_path"])),
            "door_opening_raw_mask": Path(str(item["door_opening_raw_mask_path"])),
            "door_opening_metadata": Path(str(item["door_opening_metadata_path"])),
        }
        metadata = {
            "experiment_id": exp.experiment_id,
            "experiment_name": exp.name,
            "sample_id": sample_id,
            "sample_role": sample["role"],
            "selection_reason": sample["reason"],
            "split": "val",
            "visual_evidence_status": "VERIFIED",
            "source_run_directory": str(exp.source_run_dir),
            "manifest_row": manifest_by_id.get(sample_id, {}),
            "checkpoint": checkpoint_record,
            "thresholds": exp.thresholds,
            "image_size": exp.image_size,
            "prediction_provenance": "Prediction masks derived from the historical saved Phase 2 validation probability map.",
            "probability_map": {
                "path": str(probability_path),
                "sha256": sha256_file(probability_path),
                "keys": sorted(probs),
                "dtype_on_disk": "float16",
            },
            "source_files": file_records(source_paths),
            "per_image_metrics_from_source_csvs": metric_rows,
            "per_image_metrics_recomputed_from_saved_masks": {
                "wall_region": recomputed_binary_metrics(wall_pred, wall_gt),
                "centerline_pixel": recomputed_binary_metrics(center_pred, center_gt),
                "junction_rendered_points": recomputed_binary_metrics(junction_pred, junction_gt),
                "wall_boundary": recomputed_binary_metrics(boundary_pred, boundary_gt),
                "door_opening_pixel": recomputed_binary_metrics(door_pred, door_gt),
            },
            "assets": {
                "source": "source.png",
                "ground_truth_wall_region_mask": "ground_truth_wall_region_mask.png",
                "prediction_wall_region_mask": "prediction_wall_region_mask.png",
                "overlay_wall_region_errors": "overlay_wall_region_errors.png",
                "ground_truth_centerline_mask": "ground_truth_centerline_mask.png",
                "prediction_centerline_mask": "prediction_centerline_mask.png",
                "overlay_centerline_errors": "overlay_centerline_errors.png",
                "ground_truth_junction_mask": "ground_truth_junction_mask.png",
                "prediction_junction_mask": "prediction_junction_mask.png",
                "overlay_junction_errors": "overlay_junction_errors.png",
                "ground_truth_wall_boundary_mask": "ground_truth_wall_boundary_mask.png",
                "prediction_wall_boundary_mask": "prediction_wall_boundary_mask.png",
                "overlay_wall_boundary_errors": "overlay_wall_boundary_errors.png",
                "ground_truth_door_opening_mask": "ground_truth_door_opening_mask.png",
                "prediction_door_opening_mask": "prediction_door_opening_mask.png",
                "overlay_door_opening_errors": "overlay_door_opening_errors.png",
                "historical_target_qa": historical,
            },
            "junction_visualization": {
                "target_point_count": len(target_points),
                "predicted_point_count": len(predicted_points),
                "point_render_radius_px": 4,
                "source_metric_policy": "Historical junction metrics use point matching; saved masks render those points for visual inspection.",
            },
            "mask_integrity": {
                "ground_truth_wall_region_mask": mask_stats(wall_gt),
                "prediction_wall_region_mask": mask_stats(wall_pred),
                "ground_truth_centerline_mask": mask_stats(center_gt),
                "prediction_centerline_mask": mask_stats(center_pred),
                "ground_truth_junction_mask": mask_stats(junction_gt),
                "prediction_junction_mask": mask_stats(junction_pred),
                "ground_truth_wall_boundary_mask": mask_stats(boundary_gt),
                "prediction_wall_boundary_mask": mask_stats(boundary_pred),
                "ground_truth_door_opening_mask": mask_stats(door_gt),
                "prediction_door_opening_mask": mask_stats(door_pred),
            },
            "generation": {
                "script": "scripts/generate_audit_overlay.py",
                "source_image_policy": "Letterboxed validation image regenerated from the source manifest and saved as a review copy.",
                "mask_resize_policy": "Nearest-neighbor mask handling inherited from the Phase 2 validation dataset transform.",
                "overlay_palette": {"true_positive": "green", "false_positive": "red", "false_negative": "blue"},
                "no_training_performed": True,
                "historical_directories_modified": False,
            },
            "primary_overlay": "overlay_wall_boundary_errors.png",
        }
        write_json(sample_dir / "metadata.json", metadata)
        sample_dirs.append(sample_dir)
        samples_meta.append(metadata)
    contact = make_contact_sheet(
        qa_root,
        sample_dirs,
        [
            ("source.png", "Source"),
            ("overlay_wall_region_errors.png", "Wall region"),
            ("overlay_wall_boundary_errors.png", "Boundary"),
            ("overlay_door_opening_errors.png", "Door/opening"),
        ],
    )
    write_structural_qa_readme(exp, samples_meta, contact)
    return {
        "experiment_id": exp.experiment_id,
        "sample_count": len(samples_meta),
        "qa_root": str(qa_root.relative_to(AUDIT_ROOT)),
        "contact_sheet": str(contact.relative_to(AUDIT_ROOT)),
    }


def write_shared_comparison(summary: dict[str, Any]) -> None:
    out = AUDIT_ROOT / "docs/visual_comparisons/shared_validation_samples.md"
    experiments = sorted(item["experiment_id"] for item in summary["experiments"])
    experiment_labels = [experiment.split("_", 1)[0] for experiment in experiments]
    lines = [
        "# Shared Validation Samples",
        "",
        "The visual QA pass uses the same three validation sample identities across all audited experiments.",
        "",
        "| " + " | ".join(["Sample", "Role", *experiment_labels]) + " |",
        "| " + " | ".join(["---", "---", *(["---"] * len(experiment_labels))]) + " |",
    ]
    for sample in SAMPLES:
        sid = safe_id(sample["sample_id"])
        links = [f"[metadata](../../experiments/{exp}/qa/{sid}/metadata.json)" for exp in experiments]
        lines.append("| " + " | ".join([sample["sample_id"], sample["role"], *links]) + " |")
    lines.extend(
        [
            "",
            "Direct visual comparison should account for task differences: experiments 01, 03, and 06 are standalone binary wall-region models, experiment 02 is the hybrid/global-patch evaluation using the 1024 checkpoint, Phase 1 adds centerline and junction heads, and Phase 2 adds wall-boundary and door-opening heads.",
            "",
        ]
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    summary: dict[str, Any] = {
        "visual_qa_scope": "six_audited_experiments",
        "samples": SAMPLES,
        "device": str(device),
        "experiments": [],
        "no_training_performed": True,
    }
    for exp in BINARY_EXPERIMENTS:
        summary["experiments"].append(generate_binary_experiment(exp, device))
    summary["experiments"].append(generate_phase1(PHASE1_EXPERIMENT, device))
    summary["experiments"].append(generate_phase2(PHASE2_EXPERIMENT))
    summary["experiments"].sort(key=lambda item: item["experiment_id"])
    write_json(AUDIT_ROOT / "docs/visual_qa_generation_summary.json", summary)
    write_shared_comparison(summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
