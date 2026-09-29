from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image
from torch.utils.data import DataLoader
from tqdm import tqdm

from .metrics import (
    ConfusionCounts,
    bootstrap_ci,
    confusion_matrix_from_arrays,
    metrics_from_counts,
    metrics_from_confusion_matrix,
    per_image_metrics,
    summarize_macro,
    threshold_grid,
)
from .ontology import ICON_CLASSES, IGNORE_INDEX, deterministic_palette, enabled_structure_classes
from .utils import progress_disabled, save_json, write_csv


def batch_to_device(batch: dict[str, Any], device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
    return batch["image"].to(device, non_blocking=True), batch["mask"].to(device, non_blocking=True)


def batch_to_device_multiclass(batch: dict[str, Any], device: torch.device) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
    return batch["image"].to(device, non_blocking=True), {
        "structure": batch["structure_mask"].to(device, non_blocking=True).long(),
        "icons": batch["icon_mask"].to(device, non_blocking=True).long(),
    }


def _component_accumulator() -> dict[str, float]:
    return {
        "loss": 0.0,
        "structure_ce": 0.0,
        "structure_dice_loss": 0.0,
        "structure_loss": 0.0,
        "icon_ce": 0.0,
        "icon_dice_loss": 0.0,
        "icon_loss": 0.0,
    }


def _average_components(total: dict[str, float], samples: int) -> dict[str, float]:
    return {key: value / max(1, samples) for key, value in total.items()}


def _validate_multiclass_outputs(outputs: dict[str, torch.Tensor], sample_ids: list[str] | tuple[str, ...]) -> None:
    for name, logits in outputs.items():
        if logits.ndim != 4:
            raise ValueError(f"{name} logits must be [B,C,H,W], got {tuple(logits.shape)}")
        if not torch.isfinite(logits).all():
            raise FloatingPointError(f"Non-finite {name} logits for samples={list(sample_ids)}")


def train_one_epoch(
    model: torch.nn.Module,
    loader: DataLoader,
    criterion: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    amp_enabled: bool = False,
    grad_clip: float | None = None,
    gradient_accumulation_steps: int = 1,
) -> float:
    model.train()
    total_loss = 0.0
    total_samples = 0
    gradient_accumulation_steps = max(1, int(gradient_accumulation_steps))
    scaler = torch.amp.GradScaler("cuda", enabled=amp_enabled)
    optimizer.zero_grad(set_to_none=True)
    loader_length = len(loader)
    for step, batch in enumerate(tqdm(loader, desc="train", leave=False, disable=progress_disabled()), start=1):
        images, masks = batch_to_device(batch, device)
        with torch.amp.autocast(device_type="cuda", enabled=amp_enabled):
            logits = model(images)
            loss = criterion(logits, masks)
        if not torch.isfinite(loss):
            raise FloatingPointError(f"Non-finite training loss: {loss.item()}")
        batch_size = int(images.shape[0])
        total_loss += float(loss.detach().cpu().item()) * batch_size
        total_samples += batch_size
        scaler.scale(loss / gradient_accumulation_steps).backward()
        should_step = step % gradient_accumulation_steps == 0 or step == loader_length
        if should_step:
            if grad_clip is not None and grad_clip > 0:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad(set_to_none=True)
    return total_loss / max(1, total_samples)


def train_one_epoch_multiclass(
    model: torch.nn.Module,
    loader: DataLoader,
    criterion: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
    amp_enabled: bool = False,
    grad_clip: float | None = None,
    gradient_accumulation_steps: int = 1,
) -> dict[str, float]:
    model.train()
    totals = _component_accumulator()
    total_samples = 0
    gradient_accumulation_steps = max(1, int(gradient_accumulation_steps))
    scaler = torch.amp.GradScaler("cuda", enabled=amp_enabled)
    optimizer.zero_grad(set_to_none=True)
    loader_length = len(loader)
    for step, batch in enumerate(tqdm(loader, desc="train", leave=False, disable=progress_disabled()), start=1):
        images, targets = batch_to_device_multiclass(batch, device)
        with torch.amp.autocast(device_type="cuda", enabled=amp_enabled):
            outputs = model(images)
            _validate_multiclass_outputs(outputs, batch["sample_id"])
            losses = criterion(outputs, targets)
            loss = losses["loss"]
        if not torch.isfinite(loss):
            raise FloatingPointError(f"Non-finite training loss for samples={list(batch['sample_id'])}: {loss.item()}")
        batch_size = int(images.shape[0])
        for key in totals:
            totals[key] += float(losses[key].detach().cpu().item()) * batch_size
        total_samples += batch_size
        scaler.scale(loss / gradient_accumulation_steps).backward()
        should_step = step % gradient_accumulation_steps == 0 or step == loader_length
        if should_step:
            if grad_clip is not None and grad_clip > 0:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad(set_to_none=True)
    return _average_components(totals, total_samples)


def _unnormalize_image(image_tensor: torch.Tensor) -> np.ndarray:
    mean = torch.tensor([0.485, 0.456, 0.406], dtype=image_tensor.dtype).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225], dtype=image_tensor.dtype).view(3, 1, 1)
    image = image_tensor.detach().cpu() * std + mean
    image = image.clamp(0, 1).permute(1, 2, 0).numpy()
    return (image * 255).astype(np.uint8)


def save_prediction_overlay(
    image_tensor: torch.Tensor,
    target: np.ndarray,
    pred: np.ndarray,
    path: str | Path,
) -> None:
    image = Image.fromarray(_unnormalize_image(image_tensor)).convert("RGBA")
    target_layer = Image.new("RGBA", image.size, (0, 190, 80, 0))
    pred_layer = Image.new("RGBA", image.size, (235, 50, 50, 0))
    target_alpha = (target.astype(np.uint8) > 0).astype(np.uint8) * 95
    pred_alpha = (pred.astype(np.uint8) > 0).astype(np.uint8) * 95
    target_layer.putalpha(Image.fromarray(target_alpha, mode="L"))
    pred_layer.putalpha(Image.fromarray(pred_alpha, mode="L"))
    out = Image.alpha_composite(Image.alpha_composite(image, target_layer), pred_layer)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    out.convert("RGB").save(path)


def _colorize_indexed(mask: np.ndarray, palette: dict[str, list[int]], class_names: list[str]) -> np.ndarray:
    out = np.zeros((*mask.shape, 3), dtype=np.uint8)
    for idx, name in enumerate(class_names):
        out[mask == idx] = np.asarray(palette[name], dtype=np.uint8)
    return out


def _overlay_indexed(image: np.ndarray, mask: np.ndarray, palette: dict[str, list[int]], class_names: list[str], alpha: float = 0.42) -> np.ndarray:
    color = _colorize_indexed(mask, palette, class_names)
    fg = mask > 0
    out = image.copy().astype(np.float32)
    out[fg] = (1.0 - alpha) * out[fg] + alpha * color[fg].astype(np.float32)
    return np.clip(out, 0, 255).astype(np.uint8)


def make_unified_export(structure: np.ndarray, icons: np.ndarray) -> np.ndarray:
    unified = structure.copy()
    unified[icons > 0] = icons[icons > 0] + 64
    return unified.astype(np.uint8)


def save_multiclass_prediction_panel(
    image_tensor: torch.Tensor,
    gt_structure: np.ndarray,
    pred_structure: np.ndarray,
    gt_icons: np.ndarray,
    pred_icons: np.ndarray,
    path: str | Path,
    include_optional_structure: bool = False,
) -> None:
    image = _unnormalize_image(image_tensor)
    structure_names = [item.name for item in enabled_structure_classes(include_optional_structure)]
    icon_names = [item.name for item in ICON_CLASSES]
    structure_palette = deterministic_palette(enabled_structure_classes(include_optional_structure))
    icon_palette = deterministic_palette(ICON_CLASSES)
    panels = [
        ("input", image),
        ("gt structure", _colorize_indexed(gt_structure, structure_palette, structure_names)),
        ("pred structure", _colorize_indexed(pred_structure, structure_palette, structure_names)),
        ("gt icons", _colorize_indexed(gt_icons, icon_palette, icon_names)),
        ("pred icons", _colorize_indexed(pred_icons, icon_palette, icon_names)),
        ("structure overlay", _overlay_indexed(image, pred_structure, structure_palette, structure_names)),
        ("icon overlay", _overlay_indexed(image, pred_icons, icon_palette, icon_names)),
        ("unified preview", _colorize_indexed((make_unified_export(pred_structure, pred_icons) > 0).astype(np.uint8), {"background": [0, 0, 0], "preview": [255, 210, 70]}, ["background", "preview"])),
    ]
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for ax, (title, panel) in zip(axes.reshape(-1), panels):
        ax.imshow(panel)
        ax.set_title(title)
        ax.axis("off")
    legend_lines = []
    legend_lines.extend(f"S{idx}: {name}" for idx, name in enumerate(structure_names) if idx > 0)
    legend_lines.extend(f"I{idx}: {name}" for idx, name in enumerate(icon_names) if idx > 0)
    fig.text(0.5, 0.02, " | ".join(legend_lines), ha="center", va="bottom", fontsize=8)
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=140)
    plt.close(fig)


def evaluate_model(
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    thresholds: list[float] | None = None,
    criterion: torch.nn.Module | None = None,
    amp_enabled: bool = False,
    overlay_dir: str | Path | None = None,
    overlay_threshold: float = 0.5,
    max_overlays: int = 20,
) -> dict[float, dict[str, Any]]:
    thresholds = thresholds or [0.5]
    model.eval()
    counts = {threshold: ConfusionCounts() for threshold in thresholds}
    per_threshold_rows: dict[float, list[dict[str, Any]]] = {threshold: [] for threshold in thresholds}
    total_loss = 0.0
    total_loss_samples = 0
    overlay_count = 0
    with torch.no_grad():
        for batch in tqdm(loader, desc="eval", leave=False, disable=progress_disabled()):
            images, masks = batch_to_device(batch, device)
            with torch.amp.autocast(device_type="cuda", enabled=amp_enabled):
                logits = model(images)
                if criterion is not None:
                    loss = criterion(logits, masks)
                    batch_size = int(images.shape[0])
                    total_loss += float(loss.detach().cpu().item()) * batch_size
                    total_loss_samples += batch_size
            probs = torch.sigmoid(logits).detach().cpu().numpy()
            targets = (masks.detach().cpu().numpy() > 0.5).astype(np.uint8)
            for bidx, sample_id in enumerate(batch["sample_id"]):
                target = targets[bidx, 0]
                prob = probs[bidx, 0]
                for threshold in thresholds:
                    pred = (prob >= threshold).astype(np.uint8)
                    row = per_image_metrics(pred, target, sample_id)
                    row["threshold"] = threshold
                    per_threshold_rows[threshold].append(row)
                    counts[threshold].add(
                        ConfusionCounts(
                            tp=int(row["tp"]),
                            fp=int(row["fp"]),
                            tn=int(row["tn"]),
                            fn=int(row["fn"]),
                        )
                    )
                if overlay_dir is not None and overlay_count < max_overlays:
                    pred = (prob >= overlay_threshold).astype(np.uint8)
                    safe_id = str(sample_id).strip("/").replace("/", "__")
                    save_prediction_overlay(images[bidx].detach().cpu(), target, pred, Path(overlay_dir) / f"{overlay_count:03d}_{safe_id}.jpg")
                    overlay_count += 1
    out: dict[float, dict[str, Any]] = {}
    for threshold in thresholds:
        rows = per_threshold_rows[threshold]
        micro = {**counts[threshold].as_dict(), **metrics_from_counts(counts[threshold])}
        total_pixels = counts[threshold].tp + counts[threshold].fp + counts[threshold].tn + counts[threshold].fn
        micro["wall_pixel_prevalence"] = float((counts[threshold].tp + counts[threshold].fn) / total_pixels) if total_pixels else 0.0
        dice_values = [float(row["dice"]) for row in rows]
        iou_values = [float(row["iou"]) for row in rows]
        out[threshold] = {
            "threshold": threshold,
            "loss": total_loss / max(1, total_loss_samples) if criterion is not None else None,
            "micro": micro,
            "macro": summarize_macro(rows, include_both_empty=True),
            "macro_excluding_both_empty": summarize_macro(rows, include_both_empty=False),
            "empty_ground_truth_masks": sum(1 for row in rows if row["target_empty"]),
            "empty_predictions": sum(1 for row in rows if row["prediction_empty"]),
            "both_empty_policy": "Dice=1 and IoU=1 when prediction and target are both empty.",
            "bootstrap_ci": {
                "macro_dice": bootstrap_ci(dice_values),
                "macro_iou": bootstrap_ci(iou_values),
            },
            "per_image": rows,
        }
    return out


def evaluate_model_multiclass(
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    criterion: torch.nn.Module | None = None,
    amp_enabled: bool = False,
    overlay_dir: str | Path | None = None,
    max_overlays: int = 20,
    include_optional_structure: bool = False,
) -> dict[str, Any]:
    model.eval()
    structure_names = [item.name for item in enabled_structure_classes(include_optional_structure)]
    icon_names = [item.name for item in ICON_CLASSES]
    structure_confusion = np.zeros((len(structure_names), len(structure_names)), dtype=np.int64)
    icon_confusion = np.zeros((len(icon_names), len(icon_names)), dtype=np.int64)
    totals = _component_accumulator()
    total_loss_samples = 0
    overlay_count = 0
    with torch.no_grad():
        for batch in tqdm(loader, desc="eval", leave=False, disable=progress_disabled()):
            images, targets = batch_to_device_multiclass(batch, device)
            with torch.amp.autocast(device_type="cuda", enabled=amp_enabled):
                outputs = model(images)
                _validate_multiclass_outputs(outputs, batch["sample_id"])
                if criterion is not None:
                    losses = criterion(outputs, targets)
                    loss = losses["loss"]
                    if not torch.isfinite(loss):
                        raise FloatingPointError(f"Non-finite validation loss for samples={list(batch['sample_id'])}: {loss.item()}")
                    batch_size = int(images.shape[0])
                    for key in totals:
                        totals[key] += float(losses[key].detach().cpu().item()) * batch_size
                    total_loss_samples += batch_size
            structure_pred = torch.argmax(outputs["structure"], dim=1).detach().cpu().numpy().astype(np.uint8)
            icon_pred = torch.argmax(outputs["icons"], dim=1).detach().cpu().numpy().astype(np.uint8)
            structure_target = targets["structure"].detach().cpu().numpy().astype(np.uint8)
            icon_target = targets["icons"].detach().cpu().numpy().astype(np.uint8)
            for bidx, sample_id in enumerate(batch["sample_id"]):
                structure_confusion += confusion_matrix_from_arrays(
                    structure_pred[bidx],
                    structure_target[bidx],
                    len(structure_names),
                    ignore_index=IGNORE_INDEX,
                )
                icon_confusion += confusion_matrix_from_arrays(
                    icon_pred[bidx],
                    icon_target[bidx],
                    len(icon_names),
                    ignore_index=IGNORE_INDEX,
                )
                if overlay_dir is not None and overlay_count < max_overlays:
                    safe_id = str(sample_id).strip("/").replace("/", "__")
                    save_multiclass_prediction_panel(
                        images[bidx].detach().cpu(),
                        structure_target[bidx],
                        structure_pred[bidx],
                        icon_target[bidx],
                        icon_pred[bidx],
                        Path(overlay_dir) / f"{overlay_count:03d}_{safe_id}.jpg",
                        include_optional_structure=include_optional_structure,
                    )
                    overlay_count += 1
    structure_metrics = metrics_from_confusion_matrix(structure_confusion, structure_names)
    icon_metrics = metrics_from_confusion_matrix(icon_confusion, icon_names)
    loss_components = _average_components(totals, total_loss_samples) if criterion is not None else {}
    macro_iou_values = [
        value
        for value in [
            structure_metrics["macro_iou_excluding_background"],
            icon_metrics["macro_iou_excluding_background"],
        ]
        if value is not None
    ]
    macro_dice_values = [
        value
        for value in [
            structure_metrics["macro_dice_excluding_background"],
            icon_metrics["macro_dice_excluding_background"],
        ]
        if value is not None
    ]
    return {
        "loss": loss_components.get("loss"),
        "loss_components": loss_components,
        "structure": structure_metrics,
        "icons": icon_metrics,
        "macro_iou_excluding_background": float(np.mean(macro_iou_values)) if macro_iou_values else None,
        "macro_dice_excluding_background": float(np.mean(macro_dice_values)) if macro_dice_values else None,
        "wall_iou": _class_metric(structure_metrics, "wall", "iou"),
        "wall_dice": _class_metric(structure_metrics, "wall", "dice"),
        "window_iou": _class_metric(icon_metrics, "window", "iou"),
        "window_dice": _class_metric(icon_metrics, "window", "dice"),
        "door_iou": _class_metric(icon_metrics, "door", "iou"),
        "door_dice": _class_metric(icon_metrics, "door", "dice"),
        "appliance_iou": _class_metric(icon_metrics, "appliance", "iou"),
        "appliance_dice": _class_metric(icon_metrics, "appliance", "dice"),
    }


def _class_metric(metrics: dict[str, Any], class_name: str, metric_name: str) -> float | None:
    for row in metrics["per_class"]:
        if row["class_name"] == class_name:
            return row.get(metric_name)
    return None


def save_multiclass_evaluation_outputs(results: dict[str, Any], output_dir: str | Path, prefix: str) -> None:
    output_dir = Path(output_dir)
    save_json(results, output_dir / f"{prefix}_multiclass_metrics.json")
    rows = []
    for head in ["structure", "icons"]:
        for row in results[head]["per_class"]:
            rows.append({"head": head, **row})
    write_csv(rows, output_dir / f"{prefix}_per_class_metrics.csv")


def select_best_threshold(results: dict[float, dict[str, Any]]) -> float:
    best_threshold = 0.5
    best_pair = (-math.inf, -math.inf)
    for threshold, result in results.items():
        pair = (float(result["micro"]["dice"]), float(result["micro"]["iou"]))
        if pair > best_pair:
            best_pair = pair
            best_threshold = threshold
    return best_threshold


def threshold_search(
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    amp_enabled: bool = False,
) -> tuple[float, list[dict[str, Any]], dict[float, dict[str, Any]]]:
    thresholds = threshold_grid()
    results = evaluate_model(model, loader, device, thresholds=thresholds, amp_enabled=amp_enabled)
    rows = []
    for threshold in thresholds:
        result = results[threshold]
        rows.append(
            {
                "threshold": threshold,
                "micro_dice": result["micro"]["dice"],
                "micro_iou": result["micro"]["iou"],
                "macro_dice_mean": result["macro"]["dice_mean"],
                "macro_iou_mean": result["macro"]["iou_mean"],
            }
        )
    return select_best_threshold(results), rows, results


def save_training_curves(history_csv: str | Path, out_path: str | Path) -> None:
    rows = []
    with Path(history_csv).open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return
    epochs = [int(row["epoch"]) for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(epochs, [float(row["train_loss"]) for row in rows], label="train")
    axes[0].plot(epochs, [float(row["val_loss"]) for row in rows], label="val")
    axes[0].set_xlabel("epoch")
    axes[0].set_ylabel("loss")
    axes[0].legend()
    axes[1].plot(epochs, [float(row["val_dice"]) for row in rows], label="dice")
    axes[1].plot(epochs, [float(row["val_iou"]) for row in rows], label="iou")
    axes[1].set_xlabel("epoch")
    axes[1].legend()
    fig.tight_layout()
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def save_evaluation_outputs(
    results: dict[float, dict[str, Any]],
    output_dir: str | Path,
    prefix: str,
) -> None:
    output_dir = Path(output_dir)
    serializable = {}
    summary_rows = []
    per_image_rows = []
    confusion = {}
    for threshold, result in results.items():
        key = f"{threshold:.2f}"
        per_image = result["per_image"]
        serializable[key] = {k: v for k, v in result.items() if k != "per_image"}
        confusion[key] = {k: result["micro"][k] for k in ["tp", "fp", "tn", "fn"]}
        summary_rows.append(
            {
                "threshold": threshold,
                "micro_dice": result["micro"]["dice"],
                "micro_iou": result["micro"]["iou"],
                "macro_dice_mean": result["macro"]["dice_mean"],
                "macro_iou_mean": result["macro"]["iou_mean"],
                "precision": result["micro"]["precision"],
                "recall": result["micro"]["recall"],
                "specificity": result["micro"]["specificity"],
                "pixel_accuracy": result["micro"]["pixel_accuracy"],
                "empty_ground_truth_masks": result["empty_ground_truth_masks"],
                "empty_predictions": result["empty_predictions"],
            }
        )
        per_image_rows.extend(per_image)
    save_json(serializable, output_dir / f"{prefix}_metrics.json")
    save_json(confusion, output_dir / f"{prefix}_confusion_counts.json")
    write_csv(summary_rows, output_dir / f"{prefix}_metrics_summary.csv")
    write_csv(per_image_rows, output_dir / f"per_image_{prefix}_metrics.csv")
