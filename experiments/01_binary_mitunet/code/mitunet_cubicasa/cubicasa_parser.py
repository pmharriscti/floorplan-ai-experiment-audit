from __future__ import annotations

import hashlib
import io
import re
import sys
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.dom import minidom

import numpy as np
from svgpathtools import parse_path

from .ontology import (
    ICON_CLASSES,
    ICON_SOURCE_TO_TARGET,
    MASK_SCHEMA_VERSION,
    STRUCTURE_SOURCE_TO_TARGET,
    enabled_structure_classes,
    fixed_furniture_target,
    fixed_furniture_tokens,
    icon_target_id,
    mapping_hash,
    mapping_payload,
    name_to_id,
    structure_target_id,
)


IMAGE_FILE = "F1_scaled.png"
ORIGINAL_IMAGE_FILE = "F1_original.png"
SVG_FILE = "model.svg"


@dataclass(frozen=True)
class NativeSample:
    split: str
    sample_id: str
    folder: Path
    image_path: Path
    annotation_path: Path
    split_entry: str


@dataclass(frozen=True)
class NativeResolution:
    dataset_root: Path
    split_files: dict[str, Path]
    samples: dict[str, list[NativeSample]]


def stable_id(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def detect_layout(data_root: str | Path) -> dict[str, Any]:
    root = Path(data_root)
    split_files = list(root.rglob("train.txt")) + list(root.rglob("val.txt")) + list(root.rglob("test.txt"))
    coco_files = [p for p in root.rglob("*.json") if "annotation" in p.name.lower() or "coco" in p.name.lower()]
    lmdb_files = list(root.rglob("*.lmdb")) + list(root.rglob("*.mdb"))
    svg_count = sum(1 for _ in root.rglob(SVG_FILE))
    image_count = sum(1 for _ in root.rglob(IMAGE_FILE))
    original_count = sum(1 for _ in root.rglob(ORIGINAL_IMAGE_FILE))
    mask_like = [p for p in root.rglob("*") if p.is_file() and "mask" in p.name.lower()]
    return {
        "data_root": str(root),
        "native_cubicasa": svg_count > 0 and image_count > 0,
        "model_svg_count": svg_count,
        "scaled_image_count": image_count,
        "original_image_count": original_count,
        "split_files": [str(p) for p in sorted(split_files)],
        "has_train_val_test_txt": _find_split_root(root) is not None,
        "coco_annotation_files": [str(p) for p in sorted(coco_files)],
        "has_coco_annotations": len(coco_files) > 0,
        "lmdb_files": [str(p) for p in sorted(lmdb_files)],
        "has_lmdb": len(lmdb_files) > 0,
        "mask_like_files": [str(p) for p in sorted(mask_like)[:50]],
        "has_pre_generated_binary_masks": len(mask_like) > 0,
    }


def _find_split_root(root: Path) -> Path | None:
    candidates = []
    for train in root.rglob("train.txt"):
        parent = train.parent
        if (parent / "val.txt").exists() and (parent / "test.txt").exists():
            candidates.append(parent)
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: (len(str(p)), str(p)))[0]


def read_split_entries(path: Path) -> list[str]:
    entries = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            item = line.strip()
            if item:
                entries.append(item)
    return entries


def normalize_split_entry(entry: str) -> str:
    return entry.strip().replace("\\", "/").strip("/")


def resolve_native_dataset(data_root: str | Path, image_file: str = IMAGE_FILE) -> NativeResolution:
    root = Path(data_root)
    dataset_root = _find_split_root(root)
    if dataset_root is None:
        raise FileNotFoundError(f"Could not find train.txt, val.txt, and test.txt beneath {root}")
    split_files = {
        "train": dataset_root / "train.txt",
        "val": dataset_root / "val.txt",
        "test": dataset_root / "test.txt",
    }
    samples: dict[str, list[NativeSample]] = {}
    for split, split_path in split_files.items():
        split_samples = []
        for entry in read_split_entries(split_path):
            rel = normalize_split_entry(entry)
            folder = dataset_root / rel
            sample_id = rel
            split_samples.append(
                NativeSample(
                    split=split,
                    sample_id=sample_id,
                    folder=folder,
                    image_path=folder / image_file,
                    annotation_path=folder / SVG_FILE,
                    split_entry=entry,
                )
            )
        samples[split] = split_samples
    validate_split_leakage(samples)
    return NativeResolution(dataset_root=dataset_root, split_files=split_files, samples=samples)


def validate_split_leakage(samples: dict[str, list[NativeSample]]) -> None:
    seen: dict[str, str] = {}
    duplicates = []
    for split, split_samples in samples.items():
        for sample in split_samples:
            key = sample.sample_id
            if key in seen:
                duplicates.append((key, seen[key], split))
            seen[key] = split
    if duplicates:
        detail = "; ".join(f"{sid}: {a}/{b}" for sid, a, b in duplicates[:20])
        raise ValueError(f"Sample leakage detected across splits: {detail}")


def discover_floortrans_root(data_root: str | Path, explicit_root: str | Path | None = None) -> Path | None:
    if explicit_root is not None:
        candidate = Path(explicit_root)
        if (candidate / "floortrans" / "loaders" / "house.py").exists():
            return candidate
        raise FileNotFoundError(f"Provided floortrans root does not contain floortrans/loaders/house.py: {candidate}")
    root = Path(data_root).resolve()
    candidates = [
        root.parent / "cubicasa5k",
        root.parent.parent / "cubicasa5k",
        Path.cwd().parent / "cubicasa5k",
        Path("/home/pmharris/dev/cubicasa5k"),
    ]
    for candidate in candidates:
        if (candidate / "floortrans" / "loaders" / "house.py").exists():
            return candidate
    return None


def load_official_symbols(data_root: str | Path, floortrans_root: str | Path | None = None) -> dict[str, Any]:
    root = discover_floortrans_root(data_root, floortrans_root)
    if root is None:
        raise ImportError("Could not locate local CubiCasa5K floortrans code for official SVG parsing")
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    from floortrans.loaders.house import rooms_selected  # type: ignore
    from floortrans.loaders.svg_utils import PolygonWall, get_icon, get_points, get_polygon  # type: ignore
    from skimage.draw import polygon  # type: ignore

    return {
        "floortrans_root": root,
        "rooms_selected": rooms_selected,
        "PolygonWall": PolygonWall,
        "get_icon": get_icon,
        "get_points": get_points,
        "get_polygon": get_polygon,
        "polygon": polygon,
        "wall_label_value": rooms_selected["Wall"],
    }


def _clip_pixels(rr: Any, cc: Any, height: int, width: int) -> tuple[np.ndarray, np.ndarray]:
    rr_arr = np.asarray(rr, dtype=np.int64)
    cc_arr = np.asarray(cc, dtype=np.int64)
    if rr_arr.size == 0 or cc_arr.size == 0:
        return rr_arr, cc_arr
    rr_arr = np.clip(rr_arr, 0, height - 1)
    cc_arr = np.clip(cc_arr, 0, width - 1)
    return rr_arr, cc_arr


def _raw_space_label(element: Any) -> str | None:
    parts = element.getAttribute("class").split()
    if len(parts) >= 2 and parts[0] == "Space":
        return parts[1]
    return None


def _raw_icon_label(element: Any) -> tuple[str | None, str]:
    element_id = element.getAttribute("id")
    class_attr = element.getAttribute("class")
    if element_id in {"Window", "Door"}:
        return element_id, element_id
    tokens = fixed_furniture_tokens(class_attr)
    if tokens:
        raw_name = tokens[-1] if tokens[0] == "ElectricalAppliance" and len(tokens) > 1 else tokens[0]
        return raw_name, class_attr
    return None, class_attr


def _record(
    *,
    head: str,
    raw_name: str,
    target_name: str | None,
    target_id: int | None,
    pixel_count: int = 0,
    malformed: bool = False,
    unmapped: bool = False,
) -> dict[str, Any]:
    return {
        "head": head,
        "raw_svg_class_name": raw_name,
        "target_grouped_class": target_name,
        "target_id": target_id,
        "pixel_count": int(pixel_count),
        "malformed": bool(malformed),
        "unmapped": bool(unmapped),
    }


def _parse_points(points_attr: str) -> tuple[np.ndarray, np.ndarray]:
    values = [float(item) for item in re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", points_attr)]
    xs = values[0::2]
    ys = values[1::2]
    return np.asarray(xs, dtype=np.float64), np.asarray(ys, dtype=np.float64)


def _parse_matrix(transform: str) -> np.ndarray:
    if not transform or not transform.startswith("matrix(") or not transform.endswith(")"):
        return np.eye(3, dtype=np.float64)
    values = [float(v) for v in transform[7:-1].replace(" ", "").split(",") if v != ""]
    if len(values) != 6:
        return np.eye(3, dtype=np.float64)
    a, b, c, d, e, f = values
    return np.asarray([[a, c, e], [b, d, f], [0.0, 0.0, 1.0]], dtype=np.float64)


def _geometry_points(node: Any) -> tuple[np.ndarray, np.ndarray]:
    xs: list[float] = []
    ys: list[float] = []
    for child in node.childNodes:
        if child.nodeName == "polygon":
            x, y = _parse_points(child.getAttribute("points"))
            xs.extend(x.tolist())
            ys.extend(y.tolist())
        elif child.nodeName == "rect":
            x = float(child.getAttribute("x") or 0.0)
            y = float(child.getAttribute("y") or 0.0)
            w = float(child.getAttribute("width") or 0.0)
            h = float(child.getAttribute("height") or 0.0)
            xs.extend([x, x + w, x + w, x])
            ys.extend([y, y, y + h, y + h])
        elif child.nodeName == "path":
            d = child.getAttribute("d")
            if not d:
                continue
            try:
                minx, maxx, miny, maxy = parse_path(d).bbox()
            except Exception:
                continue
            if minx != maxx and miny != maxy:
                xs.extend([minx, maxx, maxx, minx])
                ys.extend([miny, miny, maxy, maxy])
        elif child.nodeName == "g":
            x, y = _geometry_points(child)
            xs.extend(x.tolist())
            ys.extend(y.tolist())
    return np.asarray(xs, dtype=np.float64), np.asarray(ys, dtype=np.float64)


def _find_boundary_node(element: Any) -> Any:
    for child in element.childNodes:
        if child.nodeName == "g" and child.getAttribute("class") == "BoundaryPolygon":
            return child
    return element


def _rasterize_fixed_furniture_fallback(element: Any, polygon: Any, height: int, width: int) -> tuple[np.ndarray, np.ndarray]:
    boundary = _find_boundary_node(element)
    xs, ys = _geometry_points(boundary)
    if xs.size < 3 or ys.size < 3:
        raise ValueError("missing fixed-furniture boundary geometry")
    points = np.vstack([xs, ys, np.ones_like(xs)])
    matrix = _parse_matrix(element.getAttribute("transform"))
    parent = element.parentNode
    if parent is not None and getattr(parent, "getAttribute", None) and parent.getAttribute("class") == "FixedFurnitureSet":
        matrix = _parse_matrix(parent.getAttribute("transform")) @ matrix
    transformed = matrix @ points
    rr, cc = polygon(np.round(transformed[1]), np.round(transformed[0]))
    return _clip_pixels(rr, cc, height, width)


def _target_name_from_id(classes: list[str], target_id: int | None) -> str | None:
    if target_id is None or target_id < 0 or target_id >= len(classes):
        return None
    return classes[target_id]


def rasterize_wall_mask(
    svg_path: str | Path,
    height: int,
    width: int,
    data_root: str | Path,
    floortrans_root: str | Path | None = None,
    subtract_openings: bool = False,
) -> tuple[np.ndarray, dict[str, Any]]:
    symbols = load_official_symbols(data_root, floortrans_root)
    polygon_wall = symbols["PolygonWall"]
    get_points = symbols["get_points"]
    polygon = symbols["polygon"]
    wall_label_value = int(symbols["wall_label_value"])

    mask = np.zeros((height, width), dtype=np.uint8)
    svg = minidom.parse(str(svg_path))
    wall_id = 1
    skipped_small = 0
    wall_polygons = 0
    opening_polygons = 0
    for element in svg.getElementsByTagName("g"):
        element_id = element.getAttribute("id")
        if element_id == "Wall":
            try:
                wall = polygon_wall(element, wall_id, (height, width))
            except ValueError as exc:
                if str(exc) == "small wall":
                    skipped_small += 1
                    continue
                raise
            rr = np.clip(wall.rr, 0, height - 1)
            cc = np.clip(wall.cc, 0, width - 1)
            mask[rr, cc] = 1
            wall_id += 1
            wall_polygons += 1
        elif subtract_openings and element_id in {"Door", "Window"}:
            x_vals, y_vals = get_points(element)
            rr, cc = polygon(x_vals, y_vals)
            rr = np.clip(rr, 0, height - 1)
            cc = np.clip(cc, 0, width - 1)
            mask[rr, cc] = 0
            opening_polygons += 1
    metadata = {
        "parser": "floortrans.loaders.svg_utils.PolygonWall",
        "floortrans_root": str(symbols["floortrans_root"]),
        "wall_label_source": "floortrans.loaders.house.rooms_selected['Wall']",
        "wall_label_value": wall_label_value,
        "doors_windows_policy": "subtracted" if subtract_openings else "not_subtracted",
        "wall_polygons": wall_polygons,
        "opening_polygons_subtracted": opening_polygons,
        "skipped_small_walls": skipped_small,
    }
    unique = np.unique(mask)
    if not set(unique.tolist()).issubset({0, 1}):
        raise ValueError(f"Non-binary mask generated for {svg_path}: values={unique.tolist()}")
    return mask, metadata


def rasterize_multiclass_masks(
    svg_path: str | Path,
    height: int,
    width: int,
    data_root: str | Path,
    floortrans_root: str | Path | None = None,
    include_optional_structure: bool = False,
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    symbols = load_official_symbols(data_root, floortrans_root)
    polygon_wall = symbols["PolygonWall"]
    get_icon = symbols["get_icon"]
    get_polygon = symbols["get_polygon"]
    polygon = symbols["polygon"]

    structure_classes = enabled_structure_classes(include_optional_structure)
    structure_names = [item.name for item in structure_classes]
    icon_names = [item.name for item in ICON_CLASSES]
    structure_name_to_id = name_to_id(structure_classes)

    structure_mask = np.zeros((height, width), dtype=np.uint8)
    icon_mask = np.zeros((height, width), dtype=np.uint8)
    svg = minidom.parse(str(svg_path))
    wall_id = 1
    skipped_small_walls = 0
    malformed_polygons = 0
    unmapped_classes = 0
    records: list[dict[str, Any]] = []

    for element in svg.getElementsByTagName("g"):
        element_id = element.getAttribute("id")
        raw_space = _raw_space_label(element)
        if element_id == "Wall":
            target_id = structure_name_to_id["wall"]
            try:
                wall = polygon_wall(element, wall_id, (height, width))
            except ValueError as exc:
                if str(exc) == "small wall":
                    skipped_small_walls += 1
                    records.append(
                        _record(
                            head="structure",
                            raw_name="Wall",
                            target_name="wall",
                            target_id=target_id,
                            malformed=True,
                        )
                    )
                    continue
                raise
            rr, cc = _clip_pixels(wall.rr, wall.cc, height, width)
            structure_mask[rr, cc] = target_id
            records.append(
                _record(
                    head="structure",
                    raw_name="Wall",
                    target_name="wall",
                    target_id=target_id,
                    pixel_count=len(rr),
                )
            )
            wall_id += 1
            continue

        if raw_space in STRUCTURE_SOURCE_TO_TARGET and raw_space != "Wall":
            target_id = structure_target_id(raw_space, include_optional=include_optional_structure)
            target_name = _target_name_from_id(structure_names, target_id)
            if target_id is None:
                continue
            try:
                rr, cc = get_polygon(element)
            except Exception:
                malformed_polygons += 1
                records.append(
                    _record(
                        head="structure",
                        raw_name=raw_space,
                        target_name=target_name,
                        target_id=target_id,
                        malformed=True,
                    )
                )
                continue
            rr, cc = _clip_pixels(rr, cc, height, width)
            structure_mask[rr, cc] = target_id
            records.append(
                _record(
                    head="structure",
                    raw_name=raw_space,
                    target_name=target_name,
                    target_id=target_id,
                    pixel_count=len(rr),
                )
            )
            continue

        raw_icon, class_attr = _raw_icon_label(element)
        if raw_icon is None:
            continue
        target_id = icon_target_id(raw_icon, class_attr)
        if target_id is None:
            unmapped_classes += 1
            records.append(
                _record(
                    head="icons",
                    raw_name=class_attr or raw_icon,
                    target_name=None,
                    target_id=None,
                    unmapped=True,
                )
            )
            continue
        target_name = _target_name_from_id(icon_names, target_id)
        try:
            if raw_icon in {"Window", "Door"}:
                rr, cc = get_polygon(element)
            else:
                try:
                    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                        rr, cc, _, _ = get_icon(element)
                    if rr is None or cc is None:
                        raise ValueError("missing fixed-furniture boundary polygon")
                    rr, cc = _clip_pixels(rr, cc, height, width)
                except Exception:
                    rr, cc = _rasterize_fixed_furniture_fallback(element, polygon, height, width)
        except Exception:
            malformed_polygons += 1
            records.append(
                _record(
                    head="icons",
                    raw_name=class_attr or raw_icon,
                    target_name=target_name,
                    target_id=target_id,
                    malformed=True,
                )
            )
            continue
        rr, cc = _clip_pixels(rr, cc, height, width)
        if rr.size == 0 or cc.size == 0:
            malformed_polygons += 1
            records.append(
                _record(
                    head="icons",
                    raw_name=class_attr or raw_icon,
                    target_name=target_name,
                    target_id=target_id,
                    malformed=True,
                )
            )
            continue
        icon_mask[rr, cc] = target_id
        records.append(
            _record(
                head="icons",
                raw_name=class_attr or raw_icon,
                target_name=target_name,
                target_id=target_id,
                pixel_count=len(rr),
            )
        )

    metadata = {
        "parser": "floortrans.loaders.svg_utils.PolygonWall/get_polygon/get_icon",
        "floortrans_root": str(symbols["floortrans_root"]),
        "mask_schema_version": MASK_SCHEMA_VERSION,
        "mapping_hash": mapping_hash(include_optional_structure=include_optional_structure),
        "mapping": mapping_payload(include_optional_structure=include_optional_structure),
        "structure_classes": structure_names,
        "icon_classes": icon_names,
        "skipped_small_walls": skipped_small_walls,
        "malformed_polygon_count": malformed_polygons + skipped_small_walls,
        "unmapped_class_count": unmapped_classes,
        "records": records,
        "fixed_furniture_policy": (
            "Known FixedFurniture labels are grouped explicitly; ElectricalAppliance subtypes map to appliance; "
            "other valid FixedFurniture polygons map to other_fixture."
        ),
    }
    return structure_mask, icon_mask, metadata
