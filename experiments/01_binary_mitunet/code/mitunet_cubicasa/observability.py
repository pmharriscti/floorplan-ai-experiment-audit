from __future__ import annotations

import csv
import math
import os
from datetime import datetime
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", "/tmp/mitunet_matplotlib")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator


TRAINING_LOG_FIELDS = [
    "epoch",
    "train_loss",
    "val_loss",
    "bce_loss",
    "dice_loss",
    "val_dice",
    "val_iou",
    "boundary_iou",
    "learning_rate",
    "learning_rate_group_0",
    "checkpoint_path",
    "best_checkpoint",
    "seconds_elapsed",
    "epoch_time_seconds",
    "train_time_seconds",
    "validation_time_seconds",
    "peak_gpu_memory_allocated_mb",
    "peak_gpu_memory_reserved_mb",
]

EARLY_STOPPING_METRICS = {"val_iou": "max", "val_loss": "min"}


def validate_early_stopping_metric(metric: str) -> str:
    if metric not in EARLY_STOPPING_METRICS:
        choices = ", ".join(sorted(EARLY_STOPPING_METRICS))
        raise ValueError(f"Unsupported early stopping metric {metric!r}; choose one of: {choices}")
    return metric


def metric_mode(metric: str) -> str:
    return EARLY_STOPPING_METRICS[validate_early_stopping_metric(metric)]


def is_metric_improved(value: float, best_value: float | None, metric: str, min_delta: float = 0.0) -> bool:
    mode = metric_mode(metric)
    if best_value is None:
        return True
    if mode == "min":
        return value < best_value - min_delta
    return value > best_value + min_delta


def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_training_log(rows: list[dict[str, Any]], path: str | Path) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TRAINING_LOG_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: _csv_value(row.get(field)) for field in TRAINING_LOG_FIELDS})


def make_training_log_row(
    *,
    epoch: int,
    train_loss: float,
    val_loss: float,
    val_dice: float,
    val_iou: float,
    learning_rate: float,
    checkpoint_path: str | Path,
    best_checkpoint: bool,
    seconds_elapsed: float | None = None,
    epoch_time_seconds: float | None = None,
    train_time_seconds: float | None = None,
    validation_time_seconds: float | None = None,
    peak_gpu_memory_allocated_mb: float | None = None,
    peak_gpu_memory_reserved_mb: float | None = None,
    learning_rate_group_0: float | None = None,
    bce_loss: float | None = None,
    dice_loss: float | None = None,
    boundary_iou: float | None = None,
) -> dict[str, Any]:
    return {
        "epoch": epoch,
        "train_loss": train_loss,
        "val_loss": val_loss,
        "bce_loss": bce_loss,
        "dice_loss": dice_loss,
        "val_dice": val_dice,
        "val_iou": val_iou,
        "boundary_iou": boundary_iou,
        "learning_rate": learning_rate,
        "learning_rate_group_0": learning_rate if learning_rate_group_0 is None else learning_rate_group_0,
        "checkpoint_path": str(Path(checkpoint_path).resolve()),
        "best_checkpoint": bool(best_checkpoint),
        "seconds_elapsed": seconds_elapsed,
        "epoch_time_seconds": epoch_time_seconds,
        "train_time_seconds": train_time_seconds,
        "validation_time_seconds": validation_time_seconds,
        "peak_gpu_memory_allocated_mb": peak_gpu_memory_allocated_mb,
        "peak_gpu_memory_reserved_mb": peak_gpu_memory_reserved_mb,
    }


def normalize_training_history_rows(
    rows: list[dict[str, Any]],
    run_dir: str | Path,
    early_stopping_metric: str = "val_iou",
    min_delta: float = 0.0,
) -> list[dict[str, Any]]:
    validate_early_stopping_metric(early_stopping_metric)
    run_dir = Path(run_dir)
    best_value: float | None = None
    normalized: list[dict[str, Any]] = []
    for source in rows:
        epoch = int(_required_float(source, "epoch"))
        train_loss = _required_float(source, "train_loss")
        val_loss = _required_float(source, "val_loss")
        val_dice = _required_float(source, "val_dice")
        val_iou = _required_float(source, "val_iou")
        learning_rate = _first_float(source, ["learning_rate", "lr"])
        if learning_rate is None:
            raise KeyError("Training history is missing learning_rate/lr")
        metric_value = val_iou if early_stopping_metric == "val_iou" else val_loss
        best_checkpoint = is_metric_improved(metric_value, best_value, early_stopping_metric, min_delta=min_delta)
        if best_checkpoint:
            best_value = metric_value
        checkpoint_path = source.get("checkpoint_path")
        if not checkpoint_path:
            checkpoint_path = run_dir / ("best_model.pth" if best_checkpoint else "last_model.pth")
        normalized.append(
            make_training_log_row(
                epoch=epoch,
                train_loss=train_loss,
                val_loss=val_loss,
                bce_loss=_first_float(source, ["bce_loss"]),
                dice_loss=_first_float(source, ["dice_loss"]),
                val_dice=val_dice,
                val_iou=val_iou,
                boundary_iou=_first_float(source, ["boundary_iou"]),
                learning_rate=learning_rate,
                checkpoint_path=checkpoint_path,
                best_checkpoint=_as_bool(source.get("best_checkpoint"), best_checkpoint),
                seconds_elapsed=_first_float(source, ["seconds_elapsed", "seconds"]),
                epoch_time_seconds=_first_float(source, ["epoch_time_seconds"]),
                train_time_seconds=_first_float(source, ["train_time_seconds"]),
                validation_time_seconds=_first_float(source, ["validation_time_seconds"]),
                peak_gpu_memory_allocated_mb=_first_float(source, ["peak_gpu_memory_allocated_mb"]),
                peak_gpu_memory_reserved_mb=_first_float(source, ["peak_gpu_memory_reserved_mb"]),
                learning_rate_group_0=_first_float(source, ["learning_rate_group_0", "learning_rate", "lr"]),
            )
        )
    return normalized


def save_observability_plots(rows: list[dict[str, Any]], plots_dir: str | Path) -> list[Path]:
    plots_dir = Path(plots_dir)
    plots_dir.mkdir(parents=True, exist_ok=True)
    if not rows:
        return []
    written: list[Path] = []
    epochs = [_required_float(row, "epoch") for row in rows]

    written.append(
        _save_plot(
            plots_dir / "train_loss_vs_val_loss.png",
            "Loss",
            "loss",
            epochs,
            [
                ("train_loss", _series(rows, "train_loss")),
                ("val_loss", _series(rows, "val_loss")),
            ],
        )
    )
    written.append(
        _save_plot(
            plots_dir / "val_dice_vs_val_iou.png",
            "Validation Dice and IoU",
            "score",
            epochs,
            [
                ("val_dice", _series(rows, "val_dice")),
                ("val_iou", _series(rows, "val_iou")),
            ],
        )
    )
    written.append(
        _save_plot(
            plots_dir / "learning_rate.png",
            "Learning Rate",
            "learning_rate",
            epochs,
            [("learning_rate", _series(rows, "learning_rate"))],
        )
    )
    component_series = [
        ("total_loss", _series(rows, "total_loss")),
        ("bce_loss", _series(rows, "bce_loss")),
        ("dice_loss", _series(rows, "dice_loss")),
    ]
    component_series = [(label, values) for label, values in component_series if any(math.isfinite(v) for v in values)]
    if len(component_series) >= 2:
        written.append(_save_plot(plots_dir / "loss_components.png", "Loss Components", "loss", epochs, component_series))
    return written


def save_training_summary(
    rows: list[dict[str, Any]],
    path: str | Path,
    *,
    run_id: str,
    source_run_dir: str | Path | None = None,
    early_stopping_metric: str = "val_iou",
) -> dict[str, Any]:
    validate_early_stopping_metric(early_stopping_metric)
    if not rows:
        raise ValueError("Cannot summarize an empty training log")
    analysis = analyze_training_run(rows)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    source_label = str(source_run_dir) if source_run_dir is not None else "not recorded"
    best_iou = analysis["best_iou"]
    best_loss = analysis["best_loss"]
    final = rows[-1]
    lines = [
        f"# Training Run Summary: {run_id}",
        "",
        f"- Source run: `{source_label}`",
        f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Epochs logged: {len(rows)}",
        f"- Early stopping metric: `{early_stopping_metric}`",
        "",
        "## Best Epochs",
        "",
        "| Criterion | Epoch | Train loss | Val loss | Val Dice | Val IoU |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        _summary_table_row("Best validation IoU", best_iou),
        _summary_table_row("Best validation loss", best_loss),
        "",
        "## Observability Checks",
        "",
        "| Check | Result | Evidence |",
        "| --- | --- | --- |",
        f"| Overfitting occurred | {_yes_no(analysis['overfitting']['occurred'])} | {analysis['overfitting']['evidence']} |",
        f"| Training plateaued | {_yes_no(analysis['plateau']['occurred'])} | {analysis['plateau']['evidence']} |",
        f"| Learning rate looked unstable | {_yes_no(analysis['lr_unstable']['occurred'])} | {analysis['lr_unstable']['evidence']} |",
        "",
        "## Metric Guardrail",
        "",
        (
            "Lower training loss alone is not counted as success. "
            "The selected checkpoint should be judged by validation Dice/IoU, and the final epoch is only better if validation quality also improves."
        ),
        "",
        "## Final Epoch",
        "",
        (
            f"Epoch {int(_required_float(final, 'epoch'))}: train loss {_fmt(_as_float(final.get('train_loss')))}, "
            f"validation loss {_fmt(_as_float(final.get('val_loss')))}, validation Dice {_fmt(_as_float(final.get('val_dice')))}, "
            f"validation IoU {_fmt(_as_float(final.get('val_iou')))}, learning rate {_fmt(_as_float(final.get('learning_rate')))}."
        ),
        "",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    return analysis


def save_training_observability_outputs(
    history_rows: list[dict[str, Any]],
    *,
    report_dir: str | Path,
    run_id: str,
    source_run_dir: str | Path | None = None,
    early_stopping_metric: str = "val_iou",
    min_delta: float = 0.0,
) -> dict[str, Any]:
    source_for_checkpoints = source_run_dir or report_dir
    rows = normalize_training_history_rows(
        history_rows,
        source_for_checkpoints,
        early_stopping_metric=early_stopping_metric,
        min_delta=min_delta,
    )
    report_dir = Path(report_dir)
    training_log = report_dir / "training_log.csv"
    write_training_log(rows, training_log)
    plots = save_observability_plots(rows, report_dir / "plots")
    analysis = save_training_summary(
        rows,
        report_dir / "summary.md",
        run_id=run_id,
        source_run_dir=source_run_dir,
        early_stopping_metric=early_stopping_metric,
    )
    return {
        "training_log": training_log,
        "plots": plots,
        "summary": report_dir / "summary.md",
        "analysis": analysis,
    }


def analyze_training_run(rows: list[dict[str, Any]]) -> dict[str, Any]:
    best_iou = max((row for row in rows if _as_float(row.get("val_iou")) is not None), key=lambda row: _as_float(row.get("val_iou")) or -math.inf)
    best_loss = min((row for row in rows if _as_float(row.get("val_loss")) is not None), key=lambda row: _as_float(row.get("val_loss")) or math.inf)
    return {
        "best_iou": best_iou,
        "best_loss": best_loss,
        "overfitting": _detect_overfitting(rows, best_iou, best_loss),
        "plateau": _detect_plateau(rows, best_iou),
        "lr_unstable": _detect_lr_instability(rows),
    }


def _detect_overfitting(rows: list[dict[str, Any]], best_iou: dict[str, Any], best_loss: dict[str, Any]) -> dict[str, Any]:
    if len(rows) < 6:
        return {"occurred": False, "evidence": "Too few epochs for a reliable overfitting signal."}
    final = rows[-1]
    best_iou_epoch = int(_required_float(best_iou, "epoch"))
    final_epoch = int(_required_float(final, "epoch"))
    train_best = _as_float(best_iou.get("train_loss"))
    train_final = _as_float(final.get("train_loss"))
    iou_best = _as_float(best_iou.get("val_iou"))
    iou_final = _as_float(final.get("val_iou"))
    loss_best = _as_float(best_loss.get("val_loss"))
    loss_final = _as_float(final.get("val_loss"))
    if None in {train_best, train_final, iou_best, iou_final, loss_best, loss_final} or train_best == 0:
        return {"occurred": False, "evidence": "Required train/validation metrics were unavailable."}
    train_drop = (train_best - train_final) / abs(train_best)
    iou_drop = iou_best - iou_final
    loss_increase = (loss_final - loss_best) / abs(loss_best) if loss_best else 0.0
    stale_best = best_iou_epoch <= final_epoch - 3
    occurred = stale_best and train_drop > 0.01 and (iou_drop > 0.005 or loss_increase > 0.02)
    if occurred:
        evidence = (
            f"Validation IoU peaked at epoch {best_iou_epoch} and later fell by {_fmt(iou_drop)} while train loss kept decreasing "
            f"({_fmt(train_drop * 100)}% after the peak)."
        )
    else:
        evidence = (
            f"Best validation IoU was epoch {best_iou_epoch} of {final_epoch}; final IoU changed by {_fmt(iou_final - iou_best)} "
            f"from that peak while train loss changed by {_fmt(train_drop * 100)}%."
        )
    return {"occurred": occurred, "evidence": evidence}


def _detect_plateau(rows: list[dict[str, Any]], best_iou: dict[str, Any]) -> dict[str, Any]:
    if len(rows) < 8:
        return {"occurred": False, "evidence": "Too few epochs for a reliable plateau signal."}
    final_epoch = int(_required_float(rows[-1], "epoch"))
    best_iou_epoch = int(_required_float(best_iou, "epoch"))
    window = min(5, len(rows))
    recent = rows[-window:]
    recent_ious = [_as_float(row.get("val_iou")) for row in recent]
    recent_ious = [value for value in recent_ious if value is not None]
    if not recent_ious:
        return {"occurred": False, "evidence": "Validation IoU was unavailable in the recent window."}
    recent_span = max(recent_ious) - min(recent_ious)
    no_recent_best = best_iou_epoch <= final_epoch - window
    occurred = no_recent_best and recent_span < 0.002
    if occurred:
        evidence = f"No new validation IoU best in the last {window} epochs; recent IoU varied by only {_fmt(recent_span)}."
    else:
        evidence = f"Validation IoU reached its run best at epoch {best_iou_epoch}; recent IoU span was {_fmt(recent_span)}."
    return {"occurred": occurred, "evidence": evidence}


def _detect_lr_instability(rows: list[dict[str, Any]]) -> dict[str, Any]:
    lrs = [_as_float(row.get("learning_rate")) for row in rows]
    lrs = [value for value in lrs if value is not None]
    if len(lrs) < 2:
        return {"occurred": False, "evidence": "Only one learning rate value was logged."}
    changes = [curr - prev for prev, curr in zip(lrs, lrs[1:]) if not math.isclose(prev, curr, rel_tol=1e-9, abs_tol=1e-12)]
    increases = [change for change in changes if change > 0]
    nonzero_signs = [1 if change > 0 else -1 for change in changes]
    reversals = sum(1 for prev, curr in zip(nonzero_signs, nonzero_signs[1:]) if prev != curr)
    min_lr = min(lrs)
    ratio = max(lrs) / min_lr if min_lr > 0 else math.inf
    occurred = bool(increases) or reversals > 0 or len(changes) > max(4, len(lrs) // 3) or ratio > 100.0
    if occurred:
        evidence = f"Logged LR sequence had {len(increases)} increases, {reversals} direction reversals, and max/min ratio {_fmt(ratio)}."
    else:
        unique = []
        for lr in lrs:
            if not unique or not math.isclose(unique[-1], lr, rel_tol=1e-9, abs_tol=1e-12):
                unique.append(lr)
        evidence = f"Learning rate changed monotonically through {', '.join(_fmt(value) for value in unique)}."
    return {"occurred": occurred, "evidence": evidence}


def _save_plot(path: Path, title: str, ylabel: str, epochs: list[float], series: list[tuple[str, list[float]]]) -> Path:
    fig, ax = plt.subplots(figsize=(10.8, 6.0))
    for label, values in series:
        ax.plot(epochs, values, marker="o", linewidth=1.8, markersize=4, label=label)
    ax.set_title(title)
    ax.set_xlabel("epoch")
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if ylabel == "learning_rate":
        ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _pos: f"{value:.6f}"))
    ax.grid(True, alpha=0.35)
    legend_loc = "lower right" if "Dice" in title or "IoU" in title else "upper right"
    ax.legend(loc=legend_loc)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def _series(rows: list[dict[str, Any]], key: str) -> list[float]:
    values = []
    for row in rows:
        value = _as_float(row.get(key))
        values.append(value if value is not None else math.nan)
    return values


def _summary_table_row(label: str, row: dict[str, Any]) -> str:
    return (
        f"| {label} | {int(_required_float(row, 'epoch'))} | {_fmt(_as_float(row.get('train_loss')))} | "
        f"{_fmt(_as_float(row.get('val_loss')))} | {_fmt(_as_float(row.get('val_dice')))} | {_fmt(_as_float(row.get('val_iou')))} |"
    )


def _csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float) and not math.isfinite(value):
        return ""
    return value


def _required_float(row: dict[str, Any], key: str) -> float:
    value = _as_float(row.get(key))
    if value is None:
        raise KeyError(f"Missing numeric field: {key}")
    return value


def _first_float(row: dict[str, Any], keys: list[str]) -> float | None:
    for key in keys:
        value = _as_float(row.get(key))
        if value is not None:
            return value
    return None


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, str) and value.strip().lower() in {"", "none", "null", "nan", "na", "n/a"}:
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _fmt(value: float | None) -> str:
    if value is None:
        return "NA"
    if abs(value) >= 100:
        return f"{value:.2f}"
    if abs(value) >= 1:
        return f"{value:.4f}"
    return f"{value:.6g}"


def _yes_no(value: bool) -> str:
    return "Yes" if value else "No"
