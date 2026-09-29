from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset
from tqdm import tqdm

from .cubicasa_parser import NativeSample, detect_layout, rasterize_multiclass_masks, rasterize_wall_mask, resolve_native_dataset
from .ontology import (
    ICON_CLASSES,
    IGNORE_INDEX,
    MASK_SCHEMA_VERSION,
    TASK_BINARY_WALL,
    TASK_CUBICASA_MULTICLASS,
    deterministic_palette,
    enabled_structure_classes,
    mapping_hash,
    mapping_payload,
    validate_indexed_mask_values,
)
from .transforms import build_transform
from .utils import ensure_dir, progress_disabled, read_csv_rows, save_json, write_csv


CACHE_VERSION = 1
MANIFEST_FIELDS = [
    "split",
    "sample_id",
    "image_path",
    "annotation_path",
    "mask_path",
    "original_width",
    "original_height",
    "wall_pixels",
    "wall_fraction",
]
INVALID_FIELDS = ["split", "sample_id", "image_path", "annotation_path", "reason"]
SOURCE_RESOLUTION_AUDIT_FIELDS = [
    "split",
    "sample_id",
    "image_path",
    "file_name",
    "source_image_type",
    "original_width",
    "original_height",
    "minimum_dimension",
    "maximum_dimension",
    "either_dimension_exceeds_512",
    "either_dimension_reaches_1024",
    "both_dimensions_reach_1024",
]
MULTICLASS_MANIFEST_FIELDS = [
    "split",
    "sample_id",
    "image_path",
    "annotation_path",
    "structure_mask_path",
    "icon_mask_path",
    "original_width",
    "original_height",
    "structure_non_background_pixels",
    "icon_non_empty_pixels",
    "mask_schema_version",
    "mapping_hash",
]


@dataclass(frozen=True)
class PreparedDataset:
    layout: dict[str, Any]
    dataset_root: Path
    split_files: dict[str, Path]
    manifest_paths: dict[str, Path]
    invalid_samples_path: Path
    dataset_summary_path: Path
    summary: dict[str, Any]


def _safe_cache_name(sample_id: str) -> str:
    return sample_id.strip("/").replace("/", "__")


def _file_fingerprint(path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {"path": str(path), "size": stat.st_size, "mtime_ns": stat.st_mtime_ns}


def _mask_paths(cache_dir: Path, sample: NativeSample) -> tuple[Path, Path]:
    name = _safe_cache_name(sample.sample_id)
    return cache_dir / "masks" / f"{name}.png", cache_dir / "metadata" / f"{name}.json"


def _multiclass_mask_paths(cache_dir: Path, sample: NativeSample, include_optional_structure: bool) -> tuple[Path, Path, Path]:
    name = _safe_cache_name(sample.sample_id)
    schema_dir = cache_dir / f"{MASK_SCHEMA_VERSION}_{mapping_hash(include_optional_structure)[:12]}"
    return (
        schema_dir / "structure_masks" / f"{name}.png",
        schema_dir / "icon_masks" / f"{name}.png",
        schema_dir / "metadata" / f"{name}.json",
    )


def _cache_valid(meta_path: Path, image_path: Path, svg_path: Path, settings: dict[str, Any], width: int, height: int) -> bool:
    if not meta_path.exists():
        return False
    try:
        with meta_path.open("r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception:
        return False
    expected = {
        "cache_version": CACHE_VERSION,
        "image": _file_fingerprint(image_path),
        "annotation": _file_fingerprint(svg_path),
        "settings": settings,
        "width": width,
        "height": height,
    }
    return all(meta.get(k) == v for k, v in expected.items())


def _load_or_create_mask(
    sample: NativeSample,
    cache_dir: Path,
    data_root: Path,
    floortrans_root: str | Path | None,
    subtract_openings: bool,
) -> tuple[Path, int, float, dict[str, Any], int, int]:
    with Image.open(sample.image_path) as image:
        width, height = image.size
    mask_path, meta_path = _mask_paths(cache_dir, sample)
    settings = {
        "image_file": sample.image_path.name,
        "subtract_openings": subtract_openings,
        "target": "binary_wall",
    }
    if not (mask_path.exists() and _cache_valid(meta_path, sample.image_path, sample.annotation_path, settings, width, height)):
        mask, parser_meta = rasterize_wall_mask(
            sample.annotation_path,
            height=height,
            width=width,
            data_root=data_root,
            floortrans_root=floortrans_root,
            subtract_openings=subtract_openings,
        )
        mask_path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(mask.astype(np.uint8), mode="L").save(mask_path)
        metadata = {
            "cache_version": CACHE_VERSION,
            "sample_id": sample.sample_id,
            "image": _file_fingerprint(sample.image_path),
            "annotation": _file_fingerprint(sample.annotation_path),
            "settings": settings,
            "width": width,
            "height": height,
            "parser": parser_meta,
        }
        with meta_path.open("w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, sort_keys=True)
            f.write("\n")
    mask = np.array(Image.open(mask_path).convert("L"), dtype=np.uint8)
    mask = (mask > 0).astype(np.uint8)
    if mask.shape != (height, width):
        raise ValueError(f"Mask/image shape mismatch for {sample.sample_id}: mask={mask.shape} image={(height, width)}")
    unique = np.unique(mask)
    if not set(unique.tolist()).issubset({0, 1}):
        raise ValueError(f"Mask is not binary for {sample.sample_id}: {unique.tolist()}")
    wall_pixels = int(mask.sum())
    return mask_path, wall_pixels, float(mask.mean()), {"unique": unique.tolist()}, width, height


def _load_or_create_multiclass_masks(
    sample: NativeSample,
    cache_dir: Path,
    data_root: Path,
    floortrans_root: str | Path | None,
    include_optional_structure: bool = False,
) -> tuple[Path, Path, int, int, dict[str, Any], int, int]:
    with Image.open(sample.image_path) as image:
        width, height = image.size
    structure_path, icon_path, meta_path = _multiclass_mask_paths(cache_dir, sample, include_optional_structure)
    settings = {
        "image_file": sample.image_path.name,
        "target": TASK_CUBICASA_MULTICLASS,
        "mask_schema_version": MASK_SCHEMA_VERSION,
        "mapping_hash": mapping_hash(include_optional_structure),
        "include_optional_structure": include_optional_structure,
    }
    cache_ok = (
        structure_path.exists()
        and icon_path.exists()
        and _cache_valid(meta_path, sample.image_path, sample.annotation_path, settings, width, height)
    )
    if not cache_ok:
        structure_mask, icon_mask, parser_meta = rasterize_multiclass_masks(
            sample.annotation_path,
            height=height,
            width=width,
            data_root=data_root,
            floortrans_root=floortrans_root,
            include_optional_structure=include_optional_structure,
        )
        structure_path.parent.mkdir(parents=True, exist_ok=True)
        icon_path.parent.mkdir(parents=True, exist_ok=True)
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(structure_mask.astype(np.uint8), mode="L").save(structure_path)
        Image.fromarray(icon_mask.astype(np.uint8), mode="L").save(icon_path)
        metadata = {
            "cache_version": CACHE_VERSION,
            "sample_id": sample.sample_id,
            "image": _file_fingerprint(sample.image_path),
            "annotation": _file_fingerprint(sample.annotation_path),
            "settings": settings,
            "width": width,
            "height": height,
            "parser": parser_meta,
        }
        with meta_path.open("w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, sort_keys=True)
            f.write("\n")

    structure = np.array(Image.open(structure_path).convert("L"), dtype=np.uint8)
    icons = np.array(Image.open(icon_path).convert("L"), dtype=np.uint8)
    if structure.shape != (height, width) or icons.shape != (height, width):
        raise ValueError(
            f"Mask/image shape mismatch for {sample.sample_id}: "
            f"structure={structure.shape} icons={icons.shape} image={(height, width)}"
        )
    structure_class_count = len(enabled_structure_classes(include_optional_structure))
    icon_class_count = len(ICON_CLASSES)
    validate_indexed_mask_values(set(int(v) for v in np.unique(structure)), structure_class_count)
    validate_indexed_mask_values(set(int(v) for v in np.unique(icons)), icon_class_count)
    structure_pixels = int((structure > 0).sum())
    icon_pixels = int((icons > 0).sum())
    metadata = {
        "structure_unique": np.unique(structure).astype(int).tolist(),
        "icon_unique": np.unique(icons).astype(int).tolist(),
        "mapping_hash": settings["mapping_hash"],
        "mask_schema_version": MASK_SCHEMA_VERSION,
    }
    return structure_path, icon_path, structure_pixels, icon_pixels, metadata, width, height


def _save_overlay(image_path: Path, mask_path: Path, out_path: Path, max_dim: int = 1024) -> None:
    image = Image.open(image_path).convert("RGB")
    mask = Image.open(mask_path).convert("L")
    if image.size != mask.size:
        raise ValueError(f"Overlay shape mismatch: {image_path} and {mask_path}")
    scale = min(1.0, max_dim / max(image.size))
    if scale < 1.0:
        new_size = (max(1, int(image.width * scale)), max(1, int(image.height * scale)))
        image = image.resize(new_size, Image.Resampling.BILINEAR)
        mask = mask.resize(new_size, Image.Resampling.NEAREST)
    overlay = Image.new("RGBA", image.size, (255, 0, 0, 0))
    alpha = np.array(mask, dtype=np.uint8)
    alpha = (alpha > 0).astype(np.uint8) * 110
    overlay.putalpha(Image.fromarray(alpha, mode="L"))
    composed = Image.alpha_composite(image.convert("RGBA"), overlay)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    composed.convert("RGB").save(out_path)


def _save_multiclass_preview(
    image_path: Path,
    structure_path: Path,
    icon_path: Path,
    out_path: Path,
    include_optional_structure: bool,
    max_dim: int = 1024,
) -> None:
    image = Image.open(image_path).convert("RGBA")
    structure = Image.open(structure_path).convert("L")
    icons = Image.open(icon_path).convert("L")
    if image.size != structure.size or image.size != icons.size:
        raise ValueError(f"Overlay shape mismatch: {image_path}, {structure_path}, {icon_path}")
    scale = min(1.0, max_dim / max(image.size))
    if scale < 1.0:
        new_size = (max(1, int(image.width * scale)), max(1, int(image.height * scale)))
        image = image.resize(new_size, Image.Resampling.BILINEAR)
        structure = structure.resize(new_size, Image.Resampling.NEAREST)
        icons = icons.resize(new_size, Image.Resampling.NEAREST)
    structure_arr = np.array(structure, dtype=np.uint8)
    icon_arr = np.array(icons, dtype=np.uint8)
    structure_palette = deterministic_palette(enabled_structure_classes(include_optional_structure))
    icon_palette = deterministic_palette(ICON_CLASSES)
    rgb = np.zeros((image.height, image.width, 4), dtype=np.uint8)
    structure_names = [item.name for item in enabled_structure_classes(include_optional_structure)]
    icon_names = [item.name for item in ICON_CLASSES]
    for idx, name in enumerate(structure_names):
        if idx == 0:
            continue
        rgb[structure_arr == idx, :3] = structure_palette[name]
        rgb[structure_arr == idx, 3] = 95
    for idx, name in enumerate(icon_names):
        if idx == 0:
            continue
        rgb[icon_arr == idx, :3] = icon_palette[name]
        rgb[icon_arr == idx, 3] = 135
    overlay = Image.fromarray(rgb, mode="RGBA")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    Image.alpha_composite(image, overlay).convert("RGB").save(out_path)


def _preview_plan(manifests: dict[str, list[dict[str, Any]]], total: int) -> list[dict[str, Any]]:
    if total <= 0:
        return []
    selected: list[dict[str, Any]] = []
    splits = [s for s in ["train", "val", "test"] if manifests.get(s)]
    base = max(1, total // max(1, len(splits)))
    for split in splits:
        rows = manifests[split]
        count = min(base, len(rows))
        if count == 0:
            continue
        idxs = np.linspace(0, len(rows) - 1, count, dtype=int)
        selected.extend(rows[int(i)] for i in idxs)
    remaining = total - len(selected)
    if remaining > 0:
        all_rows = [row for split in splits for row in manifests[split]]
        for row in all_rows:
            if remaining <= 0:
                break
            if row not in selected:
                selected.append(row)
                remaining -= 1
    return selected[:total]


def prepare_dataset(
    data_root: str | Path,
    output_dir: str | Path,
    cache_dir: str | Path = "artifacts/cubicasa5k_wall_cache",
    floortrans_root: str | Path | None = None,
    subtract_openings: bool = False,
    preview_count: int = 20,
    allow_invalid_over_1pct: bool = False,
    verbose: bool = True,
    task_mode: str = TASK_BINARY_WALL,
    include_optional_structure: bool = False,
) -> PreparedDataset:
    data_root = Path(data_root)
    output_dir = ensure_dir(output_dir)
    cache_dir = ensure_dir(cache_dir)
    layout = detect_layout(data_root)
    if not layout["native_cubicasa"]:
        raise ValueError(f"Detected layout is not native CubiCasa5K with model.svg and {layout}")
    native = resolve_native_dataset(data_root)
    if task_mode not in {TASK_BINARY_WALL, TASK_CUBICASA_MULTICLASS}:
        raise ValueError(f"Unsupported task_mode={task_mode!r}")
    manifests: dict[str, list[dict[str, Any]]] = {"train": [], "val": [], "test": []}
    invalid: list[dict[str, Any]] = []
    split_counts = {split: len(samples) for split, samples in native.samples.items()}

    for split, samples in native.samples.items():
        iterator = tqdm(samples, desc=f"validate {split}", disable=not verbose or progress_disabled())
        for sample in iterator:
            try:
                if not sample.folder.exists():
                    raise FileNotFoundError(f"Missing sample folder: {sample.folder}")
                if not sample.image_path.exists():
                    raise FileNotFoundError(f"Missing image: {sample.image_path}")
                if not sample.annotation_path.exists():
                    raise FileNotFoundError(f"Missing SVG annotation: {sample.annotation_path}")
                if task_mode == TASK_BINARY_WALL:
                    mask_path, wall_pixels, wall_fraction, _, width, height = _load_or_create_mask(
                        sample,
                        cache_dir=cache_dir,
                        data_root=data_root,
                        floortrans_root=floortrans_root,
                        subtract_openings=subtract_openings,
                    )
                    manifests[split].append(
                        {
                            "split": split,
                            "sample_id": sample.sample_id,
                            "image_path": str(sample.image_path),
                            "annotation_path": str(sample.annotation_path),
                            "mask_path": str(mask_path),
                            "original_width": width,
                            "original_height": height,
                            "wall_pixels": wall_pixels,
                            "wall_fraction": wall_fraction,
                        }
                    )
                else:
                    structure_path, icon_path, structure_pixels, icon_pixels, mask_meta, width, height = _load_or_create_multiclass_masks(
                        sample,
                        cache_dir=cache_dir,
                        data_root=data_root,
                        floortrans_root=floortrans_root,
                        include_optional_structure=include_optional_structure,
                    )
                    manifests[split].append(
                        {
                            "split": split,
                            "sample_id": sample.sample_id,
                            "image_path": str(sample.image_path),
                            "annotation_path": str(sample.annotation_path),
                            "structure_mask_path": str(structure_path),
                            "icon_mask_path": str(icon_path),
                            "original_width": width,
                            "original_height": height,
                            "structure_non_background_pixels": structure_pixels,
                            "icon_non_empty_pixels": icon_pixels,
                            "mask_schema_version": mask_meta["mask_schema_version"],
                            "mapping_hash": mask_meta["mapping_hash"],
                        }
                    )
            except Exception as exc:
                invalid.append(
                    {
                        "split": split,
                        "sample_id": sample.sample_id,
                        "image_path": str(sample.image_path),
                        "annotation_path": str(sample.annotation_path),
                        "reason": str(exc),
                    }
                )

    for split, count in split_counts.items():
        split_invalid = sum(1 for row in invalid if row["split"] == split)
        if count and split_invalid / count > 0.01 and not allow_invalid_over_1pct:
            invalid_path = output_dir / "invalid_samples.csv"
            write_csv(invalid, invalid_path, INVALID_FIELDS)
            raise RuntimeError(
                f"{split} has {split_invalid}/{count} invalid samples (>1%). "
                f"See {invalid_path}. Use --allow-invalid-over-1pct to continue."
            )

    manifest_paths = {}
    for split, rows in manifests.items():
        path = output_dir / f"{split}_manifest.csv"
        write_csv(rows, path, MULTICLASS_MANIFEST_FIELDS if task_mode == TASK_CUBICASA_MULTICLASS else MANIFEST_FIELDS)
        manifest_paths[split] = path
    invalid_samples_path = output_dir / "invalid_samples.csv"
    write_csv(invalid, invalid_samples_path, INVALID_FIELDS)

    summary_splits = {}
    for split, rows in manifests.items():
        total_pixels = sum(int(r["original_width"]) * int(r["original_height"]) for r in rows)
        if task_mode == TASK_BINARY_WALL:
            wall_pixels = sum(int(r["wall_pixels"]) for r in rows)
            empty_masks = sum(1 for r in rows if int(r["wall_pixels"]) == 0)
            summary_splits[split] = {
                "resolved_samples": split_counts.get(split, 0),
                "valid_samples": len(rows),
                "invalid_samples": sum(1 for row in invalid if row["split"] == split),
                "empty_masks": empty_masks,
                "wall_pixels": wall_pixels,
                "total_pixels": total_pixels,
                "wall_pixel_prevalence": float(wall_pixels / total_pixels) if total_pixels else 0.0,
            }
        else:
            structure_pixels = sum(int(r["structure_non_background_pixels"]) for r in rows)
            icon_pixels = sum(int(r["icon_non_empty_pixels"]) for r in rows)
            summary_splits[split] = {
                "resolved_samples": split_counts.get(split, 0),
                "valid_samples": len(rows),
                "invalid_samples": sum(1 for row in invalid if row["split"] == split),
                "empty_structure_masks": sum(1 for r in rows if int(r["structure_non_background_pixels"]) == 0),
                "empty_icon_masks": sum(1 for r in rows if int(r["icon_non_empty_pixels"]) == 0),
                "structure_non_background_pixels": structure_pixels,
                "icon_non_empty_pixels": icon_pixels,
                "total_pixels": total_pixels,
                "structure_pixel_prevalence": float(structure_pixels / total_pixels) if total_pixels else 0.0,
                "icon_pixel_prevalence": float(icon_pixels / total_pixels) if total_pixels else 0.0,
            }

    previews = _preview_plan(manifests, preview_count)
    preview_dir = output_dir / "mask_overlays"
    for i, row in enumerate(previews):
        name = _safe_cache_name(str(row["sample_id"]))
        if task_mode == TASK_BINARY_WALL:
            _save_overlay(Path(row["image_path"]), Path(row["mask_path"]), preview_dir / f"{i:03d}_{row['split']}_{name}.jpg")
        else:
            _save_multiclass_preview(
                Path(row["image_path"]),
                Path(row["structure_mask_path"]),
                Path(row["icon_mask_path"]),
                preview_dir / f"{i:03d}_{row['split']}_{name}.jpg",
                include_optional_structure=include_optional_structure,
            )

    summary = {
        "layout": layout,
        "dataset_root": str(native.dataset_root),
        "split_files": {k: str(v) for k, v in native.split_files.items()},
        "image_file": "F1_scaled.png",
        "target": (
            "binary wall mask from native SVG Wall polygons"
            if task_mode == TASK_BINARY_WALL
            else "two-head multiclass targets from native SVG: structure_mask and icon_mask"
        ),
        "task_mode": task_mode,
        "wall_mapping": "floortrans.loaders.house.rooms_selected['Wall'] == 2",
        "doors_windows_policy": "Doors/windows are not subtracted from native SVG wall targets by default.",
        "splits": summary_splits,
        "cache_dir": str(cache_dir),
        "preview_dir": str(preview_dir),
    }
    if task_mode == TASK_CUBICASA_MULTICLASS:
        summary["class_mapping"] = mapping_payload(include_optional_structure)
        summary["mapping_hash"] = mapping_hash(include_optional_structure)
        summary["mask_schema_version"] = MASK_SCHEMA_VERSION
    dataset_summary_path = output_dir / "dataset_summary.json"
    save_json(summary, dataset_summary_path)
    return PreparedDataset(
        layout=layout,
        dataset_root=native.dataset_root,
        split_files=native.split_files,
        manifest_paths=manifest_paths,
        invalid_samples_path=invalid_samples_path,
        dataset_summary_path=dataset_summary_path,
        summary=summary,
    )


def audit_source_resolutions(
    manifest_paths: dict[str, str | Path],
    output_dir: str | Path,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for split in ["train", "val", "test"]:
        manifest_path = manifest_paths.get(split)
        if manifest_path is None:
            continue
        for row in read_csv_rows(manifest_path):
            width = int(row["original_width"])
            height = int(row["original_height"])
            image_path = Path(row["image_path"])
            rows.append(
                {
                    "split": split,
                    "sample_id": row["sample_id"],
                    "image_path": str(image_path),
                    "file_name": image_path.name,
                    "source_image_type": image_path.name,
                    "original_width": width,
                    "original_height": height,
                    "minimum_dimension": min(width, height),
                    "maximum_dimension": max(width, height),
                    "either_dimension_exceeds_512": width > 512 or height > 512,
                    "either_dimension_reaches_1024": width >= 1024 or height >= 1024,
                    "both_dimensions_reach_1024": min(width, height) >= 1024,
                }
            )

    total = len(rows)
    dims = Counter((int(row["original_width"]), int(row["original_height"])) for row in rows)
    above_512 = sum(1 for row in rows if row["either_dimension_exceeds_512"])
    reaches_1024 = sum(1 for row in rows if row["either_dimension_reaches_1024"])
    both_reach_1024 = sum(1 for row in rows if row["both_dimensions_reach_1024"])
    summary = {
        "total_image_count": total,
        "most_common_source_dimensions": [
            {"width": width, "height": height, "count": count}
            for (width, height), count in dims.most_common(25)
        ],
        "count_with_either_dimension_above_512": above_512,
        "percentage_with_useful_detail_above_512": float(above_512 / total) if total else 0.0,
        "count_with_either_dimension_at_or_above_1024": reaches_1024,
        "percentage_with_useful_detail_at_or_above_1024": float(reaches_1024 / total) if total else 0.0,
        "count_with_both_dimensions_at_or_above_1024": both_reach_1024,
        "percentage_with_both_dimensions_at_or_above_1024": float(both_reach_1024 / total) if total else 0.0,
        "source_image_type_counts": dict(Counter(str(row["source_image_type"]) for row in rows)),
        "interpretation": (
            "The audit uses native manifest original_width/original_height. "
            "A 1024 run can only exploit detail where the aligned source image has sufficient native pixels."
        ),
    }
    output_dir = Path(output_dir)
    write_csv(rows, output_dir / "source_resolution_audit.csv", SOURCE_RESOLUTION_AUDIT_FIELDS)
    save_json({"summary": summary, "rows": rows}, output_dir / "source_resolution_audit.json")
    return summary


class CubiCasaWallDataset(Dataset):
    def __init__(
        self,
        manifest_csv: str | Path,
        split: str,
        image_size: int = 512,
        resize_mode: str = "letterbox",
        augment: bool = True,
        limit: int | None = None,
    ):
        rows = read_csv_rows(manifest_csv)
        self.rows = [row for row in rows if row["split"] == split]
        if limit is not None:
            self.rows = self.rows[:limit]
        if not self.rows:
            raise ValueError(f"No rows for split={split} in {manifest_csv}")
        self.split = split
        self.transform = build_transform(split, image_size, resize_mode, augment=augment)

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> dict[str, Any]:
        row = self.rows[index]
        image = np.array(Image.open(row["image_path"]).convert("RGB"), dtype=np.uint8)
        mask = np.array(Image.open(row["mask_path"]).convert("L"), dtype=np.uint8)
        mask = (mask > 0).astype(np.uint8)
        if image.shape[:2] != mask.shape:
            raise ValueError(f"Image/mask mismatch for {row['sample_id']}: {image.shape[:2]} vs {mask.shape}")
        augmented = self.transform(image=image, mask=mask)
        image_tensor = augmented["image"].float()
        mask_tensor = augmented["mask"]
        if mask_tensor.ndim == 2:
            mask_tensor = mask_tensor.unsqueeze(0)
        mask_tensor = (mask_tensor > 0).float()
        return {
            "image": image_tensor,
            "mask": mask_tensor,
            "sample_id": row["sample_id"],
            "image_path": row["image_path"],
            "mask_path": row["mask_path"],
            "original_size": torch.tensor([int(row["original_height"]), int(row["original_width"])]),
        }


class CubiCasaMultiClassDataset(Dataset):
    def __init__(
        self,
        manifest_csv: str | Path,
        split: str,
        image_size: int = 512,
        resize_mode: str = "letterbox",
        augment: bool = True,
        limit: int | None = None,
        include_optional_structure: bool = False,
        debug: bool = False,
    ):
        rows = read_csv_rows(manifest_csv)
        self.rows = [row for row in rows if row["split"] == split]
        if limit is not None:
            self.rows = self.rows[:limit]
        if not self.rows:
            raise ValueError(f"No rows for split={split} in {manifest_csv}")
        self.split = split
        self.include_optional_structure = include_optional_structure
        self.structure_classes = enabled_structure_classes(include_optional_structure)
        self.icon_classes = ICON_CLASSES
        self.debug = debug or split in {"val", "test"}
        self.transform = build_transform(
            split,
            image_size,
            resize_mode,
            augment=augment,
            additional_mask_names=["icon_mask"],
        )

    def __len__(self) -> int:
        return len(self.rows)

    def _validate_mask(self, tensor: torch.Tensor, name: str, num_classes: int, sample_id: str) -> None:
        if tensor.ndim != 2:
            raise ValueError(f"{name} must be [H, W] for {sample_id}; got shape={tuple(tensor.shape)}")
        if tensor.dtype != torch.long:
            raise TypeError(f"{name} must be torch.long for {sample_id}; got dtype={tensor.dtype}")
        values = set(int(v) for v in tensor.unique().tolist())
        validate_indexed_mask_values(values, num_classes, ignore_index=IGNORE_INDEX)

    def __getitem__(self, index: int) -> dict[str, Any]:
        row = self.rows[index]
        image = np.array(Image.open(row["image_path"]).convert("RGB"), dtype=np.uint8)
        structure_mask = np.array(Image.open(row["structure_mask_path"]).convert("L"), dtype=np.uint8)
        icon_mask = np.array(Image.open(row["icon_mask_path"]).convert("L"), dtype=np.uint8)
        if image.shape[:2] != structure_mask.shape or image.shape[:2] != icon_mask.shape:
            raise ValueError(
                f"Image/mask mismatch for {row['sample_id']}: "
                f"image={image.shape[:2]} structure={structure_mask.shape} icon={icon_mask.shape}"
            )
        augmented = self.transform(image=image, mask=structure_mask, icon_mask=icon_mask)
        image_tensor = augmented["image"].float()
        structure_tensor = augmented["mask"].long()
        icon_tensor = augmented["icon_mask"].long()
        if structure_tensor.ndim == 3 and structure_tensor.shape[0] == 1:
            structure_tensor = structure_tensor.squeeze(0)
        if icon_tensor.ndim == 3 and icon_tensor.shape[0] == 1:
            icon_tensor = icon_tensor.squeeze(0)
        if self.debug:
            self._validate_mask(structure_tensor, "structure_mask", len(self.structure_classes), row["sample_id"])
            self._validate_mask(icon_tensor, "icon_mask", len(self.icon_classes), row["sample_id"])
        return {
            "image": image_tensor,
            "structure_mask": structure_tensor,
            "icon_mask": icon_tensor,
            "sample_id": row["sample_id"],
            "image_path": row["image_path"],
            "annotation_path": row["annotation_path"],
            "structure_mask_path": row["structure_mask_path"],
            "icon_mask_path": row["icon_mask_path"],
            "original_size": torch.tensor([int(row["original_height"]), int(row["original_width"])]),
        }
