from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

import numpy as np
import torch


EPS = 1e-7


@dataclass
class ConfusionCounts:
    tp: int = 0
    fp: int = 0
    tn: int = 0
    fn: int = 0

    def add(self, other: "ConfusionCounts") -> None:
        self.tp += other.tp
        self.fp += other.fp
        self.tn += other.tn
        self.fn += other.fn

    def as_dict(self) -> dict[str, int]:
        return {"tp": self.tp, "fp": self.fp, "tn": self.tn, "fn": self.fn}


def _safe_div(numerator: float, denominator: float, empty_value: float = 0.0) -> float:
    if denominator == 0:
        return empty_value
    return float(numerator / denominator)


def counts_from_binary(pred: np.ndarray, target: np.ndarray) -> ConfusionCounts:
    pred_bool = pred.astype(bool)
    target_bool = target.astype(bool)
    return ConfusionCounts(
        tp=int(np.logical_and(pred_bool, target_bool).sum()),
        fp=int(np.logical_and(pred_bool, ~target_bool).sum()),
        tn=int(np.logical_and(~pred_bool, ~target_bool).sum()),
        fn=int(np.logical_and(~pred_bool, target_bool).sum()),
    )


def counts_from_tensors(probs: torch.Tensor, targets: torch.Tensor, threshold: float = 0.5) -> ConfusionCounts:
    pred = (probs.detach().cpu().numpy() >= threshold).astype(np.uint8)
    target = (targets.detach().cpu().numpy() > 0.5).astype(np.uint8)
    return counts_from_binary(pred, target)


def metrics_from_counts(counts: ConfusionCounts) -> dict[str, float]:
    tp, fp, tn, fn = counts.tp, counts.fp, counts.tn, counts.fn
    both_empty = (tp + fp + fn) == 0
    return {
        "dice": 1.0 if both_empty else _safe_div(2 * tp, 2 * tp + fp + fn),
        "iou": 1.0 if both_empty else _safe_div(tp, tp + fp + fn),
        "precision": _safe_div(tp, tp + fp, empty_value=1.0),
        "recall": _safe_div(tp, tp + fn, empty_value=1.0),
        "specificity": _safe_div(tn, tn + fp, empty_value=1.0),
        "pixel_accuracy": _safe_div(tp + tn, tp + fp + tn + fn, empty_value=1.0),
    }


def per_image_metrics(pred: np.ndarray, target: np.ndarray, sample_id: str) -> dict[str, Any]:
    counts = counts_from_binary(pred, target)
    metrics = metrics_from_counts(counts)
    target_empty = int((target > 0).sum()) == 0
    pred_empty = int((pred > 0).sum()) == 0
    return {
        "sample_id": sample_id,
        **counts.as_dict(),
        **metrics,
        "target_empty": target_empty,
        "prediction_empty": pred_empty,
        "both_empty": target_empty and pred_empty,
        "wall_pixels": int((target > 0).sum()),
        "predicted_wall_pixels": int((pred > 0).sum()),
        "wall_fraction": float((target > 0).mean()),
    }


def summarize_macro(rows: list[dict[str, Any]], include_both_empty: bool = True) -> dict[str, Any]:
    selected = rows if include_both_empty else [r for r in rows if not r.get("both_empty", False)]
    out: dict[str, Any] = {"sample_count": len(selected), "include_both_empty": include_both_empty}
    for key in ["dice", "iou", "precision", "recall", "specificity", "pixel_accuracy"]:
        values = np.array([float(r[key]) for r in selected], dtype=np.float64)
        if values.size == 0:
            out.update({f"{key}_mean": None, f"{key}_median": None, f"{key}_std": None, f"{key}_min": None, f"{key}_max": None})
        else:
            out.update(
                {
                    f"{key}_mean": float(values.mean()),
                    f"{key}_median": float(np.median(values)),
                    f"{key}_std": float(values.std(ddof=0)),
                    f"{key}_min": float(values.min()),
                    f"{key}_max": float(values.max()),
                }
            )
    return out


def bootstrap_ci(
    values: Iterable[float],
    seed: int = 123,
    n_bootstrap: int = 2000,
    confidence: float = 0.95,
) -> dict[str, float | int | None]:
    arr = np.array(list(values), dtype=np.float64)
    if arr.size == 0:
        return {"seed": seed, "n_bootstrap": n_bootstrap, "low": None, "high": None}
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(n_bootstrap):
        sample = rng.choice(arr, size=arr.size, replace=True)
        means.append(sample.mean())
    alpha = 1.0 - confidence
    low, high = np.quantile(np.array(means), [alpha / 2, 1 - alpha / 2])
    return {"seed": seed, "n_bootstrap": n_bootstrap, "low": float(low), "high": float(high)}


def threshold_grid(start: float = 0.10, stop: float = 0.90, step: float = 0.05) -> list[float]:
    count = int(round((stop - start) / step)) + 1
    return [round(start + i * step, 2) for i in range(count)]


def confusion_matrix_from_arrays(
    pred: np.ndarray,
    target: np.ndarray,
    num_classes: int,
    ignore_index: int = 255,
) -> np.ndarray:
    pred_flat = pred.reshape(-1).astype(np.int64)
    target_flat = target.reshape(-1).astype(np.int64)
    valid = target_flat != ignore_index
    valid &= target_flat >= 0
    valid &= target_flat < num_classes
    valid &= pred_flat >= 0
    valid &= pred_flat < num_classes
    encoded = num_classes * target_flat[valid] + pred_flat[valid]
    counts = np.bincount(encoded, minlength=num_classes * num_classes)
    return counts.reshape(num_classes, num_classes).astype(np.int64)


def confusion_matrix_from_tensors(
    logits: torch.Tensor,
    targets: torch.Tensor,
    ignore_index: int = 255,
) -> np.ndarray:
    pred = torch.argmax(logits.detach(), dim=1).cpu().numpy()
    target = targets.detach().cpu().numpy()
    return confusion_matrix_from_arrays(pred, target, int(logits.shape[1]), ignore_index=ignore_index)


def _none_mean(values: list[float | None]) -> float | None:
    selected = [float(v) for v in values if v is not None]
    if not selected:
        return None
    return float(np.mean(selected))


def metrics_from_confusion_matrix(confusion: np.ndarray, class_names: list[str]) -> dict[str, Any]:
    confusion = confusion.astype(np.int64)
    num_classes = int(confusion.shape[0])
    total = int(confusion.sum())
    per_class = []
    ious_for_fw = []
    supports_for_fw = []
    for idx in range(num_classes):
        tp = int(confusion[idx, idx])
        fp = int(confusion[:, idx].sum() - tp)
        fn = int(confusion[idx, :].sum() - tp)
        support = int(confusion[idx, :].sum())
        pred_support = int(confusion[:, idx].sum())
        active = support + pred_support > 0
        precision = _safe_div(tp, tp + fp) if active and (tp + fp) > 0 else None
        recall = _safe_div(tp, tp + fn) if support > 0 else None
        dice = _safe_div(2 * tp, 2 * tp + fp + fn) if active else None
        iou = _safe_div(tp, tp + fp + fn) if active else None
        per_class.append(
            {
                "class_id": idx,
                "class_name": class_names[idx] if idx < len(class_names) else str(idx),
                "true_positives": tp,
                "false_positives": fp,
                "false_negatives": fn,
                "pixel_support": support,
                "predicted_pixels": pred_support,
                "precision": precision,
                "recall": recall,
                "dice": dice,
                "iou": iou,
                "zero_support": support == 0,
            }
        )
        if support > 0 and iou is not None:
            supports_for_fw.append(support)
            ious_for_fw.append(iou)
    dice_values = [row["dice"] for row in per_class]
    iou_values = [row["iou"] for row in per_class]
    dice_no_bg = [row["dice"] for row in per_class[1:]]
    iou_no_bg = [row["iou"] for row in per_class[1:]]
    fw_iou = None
    if supports_for_fw and sum(supports_for_fw) > 0:
        fw_iou = float(np.average(np.asarray(ious_for_fw, dtype=np.float64), weights=np.asarray(supports_for_fw, dtype=np.float64)))
    return {
        "confusion_matrix": confusion.tolist(),
        "per_class": per_class,
        "macro_dice_including_background": _none_mean(dice_values),
        "macro_iou_including_background": _none_mean(iou_values),
        "macro_dice_excluding_background": _none_mean(dice_no_bg),
        "macro_iou_excluding_background": _none_mean(iou_no_bg),
        "frequency_weighted_iou": fw_iou,
        "pixel_accuracy": _safe_div(float(np.trace(confusion)), total) if total else None,
        "total_pixels": total,
    }
