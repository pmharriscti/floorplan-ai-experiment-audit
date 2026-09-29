from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from tqdm import tqdm

from .cubicasa_parser import resolve_native_dataset, rasterize_multiclass_masks
from .ontology import (
    ICON_CLASSES,
    TASK_CUBICASA_MULTICLASS,
    class_names,
    enabled_structure_classes,
    mapping_hash,
    mapping_payload,
)
from .utils import progress_disabled, save_json


AUDIT_FIELDS = [
    "head",
    "raw_svg_class_name",
    "target_grouped_class",
    "object_count",
    "image_count",
    "pixel_count",
    "percentage_of_target_pixels",
    "unmapped_class_count",
    "malformed_polygon_count",
]


def _write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=AUDIT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in AUDIT_FIELDS})


def recommended_ce_weights(pixel_counts: list[int], cap: float = 10.0) -> list[float]:
    counts = np.asarray(pixel_counts, dtype=np.float64)
    total = float(counts.sum())
    if total <= 0:
        return [1.0 for _ in pixel_counts]
    freqs = counts / total
    weights = 1.0 / np.log(1.02 + np.maximum(freqs, 1e-12))
    weights = np.clip(weights, 0.05, cap)
    weights = weights / np.mean(weights)
    return [float(round(v, 6)) for v in weights.tolist()]


def audit_multiclass_split(
    data_root: str | Path,
    output_dir: str | Path,
    split: str = "train",
    floortrans_root: str | Path | None = None,
    include_optional_structure: bool = False,
    required_structure_classes: list[str] | None = None,
    required_icon_classes: list[str] | None = None,
    verbose: bool = True,
) -> dict[str, Any]:
    native = resolve_native_dataset(data_root)
    if split not in native.samples:
        raise ValueError(f"Unknown split={split!r}; expected one of {sorted(native.samples)}")
    structure_classes = enabled_structure_classes(include_optional_structure)
    structure_names = class_names(structure_classes)
    icon_names = class_names(ICON_CLASSES)
    structure_pixel_counts = np.zeros(len(structure_names), dtype=np.int64)
    icon_pixel_counts = np.zeros(len(icon_names), dtype=np.int64)
    grouped: dict[tuple[str, str, str], dict[str, Any]] = {}
    image_sets: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    total_unmapped = 0
    total_malformed = 0

    samples = native.samples[split]
    iterator = tqdm(samples, desc=f"audit {split}", disable=not verbose or progress_disabled())
    for sample in iterator:
        with Image.open(sample.image_path) as image:
            width, height = image.size
        structure_mask, icon_mask, meta = rasterize_multiclass_masks(
            sample.annotation_path,
            height=height,
            width=width,
            data_root=data_root,
            floortrans_root=floortrans_root,
            include_optional_structure=include_optional_structure,
        )
        structure_pixel_counts += np.bincount(structure_mask.reshape(-1), minlength=len(structure_names))[: len(structure_names)]
        icon_pixel_counts += np.bincount(icon_mask.reshape(-1), minlength=len(icon_names))[: len(icon_names)]
        total_unmapped += int(meta.get("unmapped_class_count", 0))
        total_malformed += int(meta.get("malformed_polygon_count", 0))
        for record in meta.get("records", []):
            raw = str(record["raw_svg_class_name"])
            head = str(record["head"])
            target = str(record.get("target_grouped_class") or "UNMAPPED")
            key = (head, raw, target)
            row = grouped.setdefault(
                key,
                {
                    "head": head,
                    "raw_svg_class_name": raw,
                    "target_grouped_class": target,
                    "object_count": 0,
                    "image_count": 0,
                    "pixel_count": 0,
                    "unmapped_class_count": 0,
                    "malformed_polygon_count": 0,
                },
            )
            row["object_count"] += 1
            row["pixel_count"] += int(record.get("pixel_count", 0))
            row["unmapped_class_count"] += int(bool(record.get("unmapped", False)))
            row["malformed_polygon_count"] += int(bool(record.get("malformed", False)))
            image_sets[key].add(sample.sample_id)

    structure_target_pixels = int(structure_pixel_counts[1:].sum())
    icon_target_pixels = int(icon_pixel_counts[1:].sum())
    rows = []
    for key, row in sorted(grouped.items(), key=lambda item: (item[0][0], item[0][2], item[0][1])):
        head = row["head"]
        denom = structure_target_pixels if head == "structure" else icon_target_pixels
        out = dict(row)
        out["image_count"] = len(image_sets[key])
        out["percentage_of_target_pixels"] = float(out["pixel_count"] / denom) if denom else 0.0
        rows.append(out)

    required_structure_classes = required_structure_classes or []
    required_icon_classes = required_icon_classes or []
    missing_required = []
    for name in required_structure_classes:
        if name not in structure_names:
            missing_required.append({"head": "structure", "class_name": name, "reason": "not_enabled"})
            continue
        if int(structure_pixel_counts[structure_names.index(name)]) == 0:
            missing_required.append({"head": "structure", "class_name": name, "reason": "zero_training_pixels"})
    for name in required_icon_classes:
        if name not in icon_names:
            missing_required.append({"head": "icons", "class_name": name, "reason": "not_enabled"})
            continue
        if int(icon_pixel_counts[icon_names.index(name)]) == 0:
            missing_required.append({"head": "icons", "class_name": name, "reason": "zero_training_pixels"})
    if missing_required:
        raise RuntimeError(f"Configured required classes are unavailable in {split}: {missing_required}")
    if total_unmapped:
        raise RuntimeError(f"Found {total_unmapped} unmapped SVG classes in {split}; refusing to map them to background.")

    output_dir = Path(output_dir)
    csv_path = output_dir / f"{split}_class_distribution_audit.csv"
    json_path = output_dir / f"{split}_class_distribution_audit.json"
    _write_csv(rows, csv_path)
    payload = {
        "task_mode": TASK_CUBICASA_MULTICLASS,
        "split": split,
        "sample_count": len(samples),
        "mapping_hash": mapping_hash(include_optional_structure),
        "class_mapping": mapping_payload(include_optional_structure),
        "structure_class_names": structure_names,
        "icon_class_names": icon_names,
        "structure_pixel_counts": {name: int(structure_pixel_counts[idx]) for idx, name in enumerate(structure_names)},
        "icon_pixel_counts": {name: int(icon_pixel_counts[idx]) for idx, name in enumerate(icon_names)},
        "recommended_ce_weights": {
            "structure": recommended_ce_weights(structure_pixel_counts.tolist()),
            "icons": recommended_ce_weights(icon_pixel_counts.tolist()),
            "method": "inverse-log-frequency normalized to mean 1 and capped before normalization",
        },
        "unmapped_class_count": total_unmapped,
        "malformed_polygon_count": total_malformed,
        "rows": rows,
        "csv_path": str(csv_path),
    }
    save_json(payload, json_path)
    return payload
