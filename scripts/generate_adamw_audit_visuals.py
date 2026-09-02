#!/usr/bin/env python3
"""Copy small AdamW visual QA artifacts into the audit repository.

This script uses only historical outputs from the 512 px AdamW optimizer
experiment. It performs no training and no inference.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


AUDIT_ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT_ID = "07_mitunet_512_adamw"
EXPERIMENT_NAME = "MitUNet 512 AdamW optimizer comparator"
SOURCE_ROOT = Path(
    "/mnt/e/test/_folder/floorplan_ai/experiments/"
    "mitunet_cubicasa5k_512_adamw/20260901_134158"
)
AUDIT_DIR = AUDIT_ROOT / "experiments" / EXPERIMENT_ID
QA_ROOT = AUDIT_DIR / "qa"
PLOTS_ROOT = AUDIT_DIR / "plots"


def safe_id(sample_id: str) -> str:
    return sample_id.strip("/").replace("/", "__")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def row_by_sample(path: Path) -> dict[str, dict[str, str]]:
    return {row["sample_id"]: row for row in read_csv_rows(path)}


def metric_row(path: Path, sample_id: str, threshold: float) -> dict[str, Any]:
    expected = str(threshold)
    for row in read_csv_rows(path):
        if row.get("sample_id") == sample_id and str(row.get("threshold")) == expected:
            return parsed_row(row)
    return {}


def copy_record(src: Path, dst: Path) -> dict[str, Any]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {
        "source_path": str(src),
        "source_sha256": sha256_file(src),
        "audit_path": str(dst.relative_to(AUDIT_ROOT)),
        "audit_sha256": sha256_file(dst),
    }


def file_record(path: Path, *, skip_sha256: bool = False) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": path.exists(),
        "sha256": None if skip_sha256 or not path.exists() else sha256_file(path),
        "sha256_status": "skipped_large_artifact" if skip_sha256 and path.exists() else None,
    }


def mask_stats(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("L")
    values = sorted(set(image.getdata()))
    positive = sum(1 for value in image.getdata() if value > 0)
    width, height = image.size
    return {
        "mode": image.mode,
        "shape": [height, width],
        "unique_values": values,
        "positive_pixels": positive,
        "positive_fraction": positive / float(width * height),
    }


def make_contact_sheet(samples: list[dict[str, Any]]) -> Path:
    thumb_w = 300
    thumb_h = 200
    label_h = 34
    gutter = 12
    columns = 3
    rows = (len(samples) + columns - 1) // columns
    width = columns * thumb_w + (columns + 1) * gutter
    height = rows * (label_h + thumb_h + gutter) + gutter
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, sample in enumerate(samples):
        row = index // columns
        col = index % columns
        x = gutter + col * (thumb_w + gutter)
        y = gutter + row * (label_h + thumb_h + gutter)
        label = f"{sample['category']}: {sample['sample_id']}"
        draw.text((x, y), label, fill=(20, 20, 20), font=font)
        image = Image.open(QA_ROOT / safe_id(sample["sample_id"]) / "comparison_adam_vs_adamw.png").convert("RGB")
        image.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        panel = Image.new("RGB", (thumb_w, thumb_h), (245, 245, 245))
        panel.paste(image, ((thumb_w - image.width) // 2, (thumb_h - image.height) // 2))
        sheet.paste(panel, (x, y + label_h))
    out = QA_ROOT / "contact_sheet.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    return out


def markdown_row(sample: dict[str, Any]) -> str:
    sample_dir = safe_id(sample["sample_id"])
    delta = sample["adamw_iou"] - sample["adam_iou"]
    return (
        f"| {sample['category']} | {sample['sample_id']} | "
        f"{sample['adam_iou']:.6f} | {sample['adamw_iou']:.6f} | {delta:+.6f} | "
        f"[metadata]({sample_dir}/metadata.json) | "
        f"[comparison]({sample_dir}/comparison_adam_vs_adamw.png) |"
    )


def write_qa_readme(samples: list[dict[str, Any]], contact_sheet: Path) -> None:
    lines = [
        f"# Visual QA - {EXPERIMENT_NAME}",
        "",
        "This directory contains six representative test samples copied from the historical Adam-vs-AdamW comparison artifacts. No training or inference was run for this audit copy.",
        "",
        f"Contact sheet: [contact_sheet.png]({contact_sheet.name})",
        "",
        "| Role | Sample | Adam IoU | AdamW IoU | AdamW minus Adam IoU | Metadata | Comparison |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
        *[markdown_row(sample) for sample in samples],
        "",
        "Each sample folder includes `source.png`, `ground_truth_wall_mask.png`, `adam_prediction_wall_mask.png`, `adamw_prediction_wall_mask.png`, `adamw_prediction_overlay.png`, `ground_truth_wall_overlay.png`, `comparison_adam_vs_adamw.png`, and `metadata.json`.",
        "",
    ]
    (QA_ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_visual_comparison_doc(samples: list[dict[str, Any]]) -> None:
    out = AUDIT_ROOT / "docs" / "visual_comparisons" / "adamw_optimizer_samples.md"
    lines = [
        "# AdamW Optimizer Visual Samples",
        "",
        "These representative test samples come from the historical Adam-vs-AdamW comparison artifacts for experiment `07_mitunet_512_adamw`.",
        "",
        "| Role | Sample | Adam Dice | AdamW Dice | AdamW minus Adam Dice | Adam IoU | AdamW IoU | AdamW minus Adam IoU | Comparison |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for sample in samples:
        sid = safe_id(sample["sample_id"])
        dice_delta = sample["adamw_dice"] - sample["adam_dice"]
        iou_delta = sample["adamw_iou"] - sample["adam_iou"]
        lines.append(
            f"| {sample['category']} | {sample['sample_id']} | "
            f"{sample['adam_dice']:.6f} | {sample['adamw_dice']:.6f} | {dice_delta:+.6f} | "
            f"{sample['adam_iou']:.6f} | {sample['adamw_iou']:.6f} | {iou_delta:+.6f} | "
            f"[comparison](../../experiments/{EXPERIMENT_ID}/qa/{sid}/comparison_adam_vs_adamw.png) |"
        )
    lines.extend(
        [
            "",
            "The experiment-level outcome should be read from the official metrics JSON: AdamW improved precision slightly but reduced recall enough to lower held-out test IoU and Dice versus the Adam control.",
            "",
        ]
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    comparison_path = SOURCE_ROOT / "evaluation/visual_comparison_index.json"
    representative_csv = SOURCE_ROOT / "evaluation/representative_samples.csv"
    per_image_csv = SOURCE_ROOT / "evaluation/per_image_test_metrics.csv"
    manifest_csv = SOURCE_ROOT / "test_manifest.csv"
    comparisons = json.loads(comparison_path.read_text(encoding="utf-8"))["comparisons"]
    manifest = row_by_sample(manifest_csv)

    copied_samples: list[dict[str, Any]] = []
    for sample in comparisons:
        sample_id = sample["sample_id"]
        sample_slug = safe_id(sample_id)
        sample_dir = QA_ROOT / sample_slug
        pred_dir = SOURCE_ROOT / "predictions" / sample_slug
        composite = SOURCE_ROOT / "overlays/adam_vs_adamw" / f"{sample['category']}__{sample_slug}.png"
        assets = {
            "comparison_adam_vs_adamw": copy_record(composite, sample_dir / "comparison_adam_vs_adamw.png"),
            "source": copy_record(pred_dir / "original.png", sample_dir / "source.png"),
            "ground_truth_wall_mask": copy_record(pred_dir / "target.png", sample_dir / "ground_truth_wall_mask.png"),
            "adam_prediction_wall_mask": copy_record(pred_dir / "adam_prediction.png", sample_dir / "adam_prediction_wall_mask.png"),
            "adamw_prediction_wall_mask": copy_record(pred_dir / "adamw_prediction.png", sample_dir / "adamw_prediction_wall_mask.png"),
            "adamw_prediction_overlay": copy_record(pred_dir / "adamw_prediction_overlay.png", sample_dir / "adamw_prediction_overlay.png"),
            "ground_truth_wall_overlay": copy_record(pred_dir / "target_overlay.png", sample_dir / "ground_truth_wall_overlay.png"),
        }
        metadata = {
            "experiment_id": EXPERIMENT_ID,
            "experiment_name": EXPERIMENT_NAME,
            "sample_id": sample_id,
            "sample_role": sample["category"],
            "split": "test",
            "visual_evidence_status": "VERIFIED",
            "source_run_directory": str(SOURCE_ROOT),
            "manifest_row": manifest.get(sample_id, {}),
            "thresholds": {
                "adam_control_wall": sample["adam_threshold"],
                "adamw_experiment_wall": sample["adamw_threshold"],
            },
            "image_size": 512,
            "prediction_provenance": "Copied from historical Adam-vs-AdamW evaluation artifacts; no inference was run during audit packaging.",
            "visual_comparison_metrics": sample,
            "per_image_adamw_metrics_from_source_csv": metric_row(per_image_csv, sample_id, sample["adamw_threshold"]),
            "source_files": {
                "visual_comparison_index": file_record(comparison_path),
                "representative_samples_csv": file_record(representative_csv),
                "per_image_test_metrics_csv": file_record(per_image_csv),
                "test_manifest_csv": file_record(manifest_csv),
                "best_checkpoint": file_record(SOURCE_ROOT / "checkpoints/best_model.pth", skip_sha256=True),
            },
            "assets": assets,
            "mask_integrity": {
                "ground_truth_wall_mask": mask_stats(sample_dir / "ground_truth_wall_mask.png"),
                "adam_prediction_wall_mask": mask_stats(sample_dir / "adam_prediction_wall_mask.png"),
                "adamw_prediction_wall_mask": mask_stats(sample_dir / "adamw_prediction_wall_mask.png"),
            },
            "generation": {
                "script": "scripts/generate_adamw_audit_visuals.py",
                "source_image_policy": "Historical 512 px evaluation copy from the AdamW run.",
                "mask_policy": "Historical 512 px target and prediction PNGs copied from the AdamW run.",
                "no_training_performed": True,
                "no_inference_performed": True,
                "historical_directories_modified": False,
            },
        }
        (sample_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        copied_samples.append(sample)

    contact_sheet = make_contact_sheet(copied_samples)
    write_qa_readme(copied_samples, contact_sheet)
    write_visual_comparison_doc(copied_samples)

    PLOTS_ROOT.mkdir(parents=True, exist_ok=True)
    training_plot = copy_record(SOURCE_ROOT / "logs/training_curves.png", PLOTS_ROOT / "training_curves.png")
    (PLOTS_ROOT / "README.md").write_text(
        "\n".join(
            [
                f"# Training Plot - {EXPERIMENT_NAME}",
                "",
                "This small PNG was copied from the historical run logs.",
                "",
                "- [training_curves.png](training_curves.png)",
                "",
            ]
        ),
        encoding="utf-8",
    )

    summary = {
        "experiment_id": EXPERIMENT_ID,
        "visual_qa_scope": "adamw_optimizer_comparison",
        "source_run_directory": str(SOURCE_ROOT),
        "qa_root": str(QA_ROOT.relative_to(AUDIT_ROOT)),
        "plots_root": str(PLOTS_ROOT.relative_to(AUDIT_ROOT)),
        "contact_sheet": str(contact_sheet.relative_to(AUDIT_ROOT)),
        "training_plot": training_plot,
        "sample_count": len(copied_samples),
        "samples": copied_samples,
        "no_training_performed": True,
        "no_inference_performed": True,
    }
    summary_path = AUDIT_ROOT / "docs" / "visual_comparisons" / "adamw_optimizer_visual_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
