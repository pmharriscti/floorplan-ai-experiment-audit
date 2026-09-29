#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np
import torch
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitunet_cubicasa.model import load_model_from_checkpoint
from mitunet_cubicasa.ontology import (
    ICON_CLASSES,
    TASK_CUBICASA_MULTICLASS,
    deterministic_palette,
    enabled_structure_classes,
    mapping_payload,
)
from mitunet_cubicasa.transforms import build_transform
from mitunet_cubicasa.utils import detect_device


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict a binary wall mask with a MitUNet checkpoint.")
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--images", nargs="*", default=None)
    parser.add_argument("--output-mask", required=True)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--output-overlay", default=None)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--save-probabilities", action="store_true")
    parser.add_argument("--unified-export", action="store_true")
    return parser.parse_args()


def _safe_stem(path: Path) -> str:
    return path.stem.strip().replace("/", "__")


def _colorize(mask: np.ndarray, palette: dict[str, list[int]], class_names: list[str]) -> Image.Image:
    rgb = np.zeros((*mask.shape, 3), dtype=np.uint8)
    for idx, name in enumerate(class_names):
        rgb[mask == idx] = np.asarray(palette[name], dtype=np.uint8)
    return Image.fromarray(rgb, mode="RGB")


def _overlay(base: Image.Image, mask: np.ndarray, palette: dict[str, list[int]], class_names: list[str]) -> Image.Image:
    image = np.array(base.convert("RGB"), dtype=np.float32)
    color = np.array(_colorize(mask, palette, class_names), dtype=np.float32)
    fg = mask > 0
    image[fg] = 0.58 * image[fg] + 0.42 * color[fg]
    return Image.fromarray(np.clip(image, 0, 255).astype(np.uint8), mode="RGB")


def _save_indexed(mask: np.ndarray, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(mask.astype(np.uint8), mode="L").save(path)


def _resize_mask(mask: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    return np.array(Image.fromarray(mask.astype(np.uint8), mode="L").resize(size, Image.Resampling.NEAREST), dtype=np.uint8)


def _predict_multiclass(args: argparse.Namespace, checkpoint: dict, model: torch.nn.Module, device: torch.device) -> None:
    preprocessing = checkpoint.get("preprocessing", {})
    size = int(preprocessing.get("image_size", preprocessing.get("input_size", 512)))
    resize_mode = preprocessing.get("resize_mode", "letterbox")
    include_optional_structure = bool(checkpoint.get("architecture", {}).get("include_optional_structure", False))
    structure_classes = enabled_structure_classes(include_optional_structure)
    icon_classes = ICON_CLASSES
    structure_names = [item.name for item in structure_classes]
    icon_names = [item.name for item in icon_classes]
    structure_palette = deterministic_palette(structure_classes)
    icon_palette = deterministic_palette(icon_classes)
    image_paths = [Path(p) for p in (args.images or [args.image])]
    output_dir = Path(args.output_dir or Path(args.output_mask).parent)
    output_dir.mkdir(parents=True, exist_ok=True)
    transform = build_transform("test", size=size, resize_mode=resize_mode, augment=False)
    batch_size = max(1, int(args.batch_size))
    for start in range(0, len(image_paths), batch_size):
        chunk = image_paths[start : start + batch_size]
        tensors = []
        originals: list[Image.Image] = []
        for path in chunk:
            image = Image.open(path).convert("RGB")
            originals.append(image)
            arr = np.array(image, dtype=np.uint8)
            dummy_mask = np.zeros(arr.shape[:2], dtype=np.uint8)
            augmented = transform(image=arr, mask=dummy_mask)
            tensors.append(augmented["image"].float())
        tensor = torch.stack(tensors, dim=0).to(device)
        with torch.no_grad():
            with torch.amp.autocast(device_type="cuda", enabled=device.type == "cuda"):
                outputs = model(tensor)
                structure_probs = torch.softmax(outputs["structure"], dim=1).detach().cpu()
                icon_probs = torch.softmax(outputs["icons"], dim=1).detach().cpu()
        structure_pred = torch.argmax(structure_probs, dim=1).numpy().astype(np.uint8)
        icon_pred = torch.argmax(icon_probs, dim=1).numpy().astype(np.uint8)
        for bidx, image_path in enumerate(chunk):
            stem = _safe_stem(image_path)
            sample_dir = output_dir / stem
            sample_dir.mkdir(parents=True, exist_ok=True)
            original = originals[bidx]
            original_size = original.size
            structure_mask = _resize_mask(structure_pred[bidx], original_size)
            icon_mask = _resize_mask(icon_pred[bidx], original_size)
            _save_indexed(structure_mask, sample_dir / "structure_indexed.png")
            _save_indexed(icon_mask, sample_dir / "icon_indexed.png")
            _colorize(structure_mask, structure_palette, structure_names).save(sample_dir / "structure_colorized.png")
            _colorize(icon_mask, icon_palette, icon_names).save(sample_dir / "icon_colorized.png")
            _overlay(original, structure_mask, structure_palette, structure_names).save(sample_dir / "structure_overlay.png")
            _overlay(original, icon_mask, icon_palette, icon_names).save(sample_dir / "icon_overlay.png")
            if args.unified_export:
                unified = structure_mask.copy()
                unified[icon_mask > 0] = icon_mask[icon_mask > 0] + 64
                _save_indexed(unified, sample_dir / "unified_lossy_indexed.png")
            if args.save_probabilities:
                np.savez_compressed(
                    sample_dir / "class_probabilities.npz",
                    structure=structure_probs[bidx].numpy(),
                    icons=icon_probs[bidx].numpy(),
                )
            metadata = {
                "image": str(image_path),
                "original_size": {"width": original_size[0], "height": original_size[1]},
                "structure_classes": [{"id": item.id, "name": item.name} for item in structure_classes],
                "icon_classes": [{"id": item.id, "name": item.name} for item in icon_classes],
                "palette": {"structure": structure_palette, "icons": icon_palette},
                "class_mapping": mapping_payload(include_optional_structure),
                "unified_export": {
                    "written": bool(args.unified_export),
                    "lossy": True,
                    "priority": "icons/openings > structural classes > background",
                },
            }
            (sample_dir / "prediction_metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    device, _ = detect_device()
    checkpoint = torch.load(args.checkpoint, map_location=device, weights_only=False)
    loaded = load_model_from_checkpoint(checkpoint, map_location=device)
    model = loaded.model.eval()
    if (checkpoint.get("task_mode") or checkpoint.get("architecture", {}).get("task_mode")) == TASK_CUBICASA_MULTICLASS:
        _predict_multiclass(args, checkpoint, model, device)
        return
    preprocessing = checkpoint.get("preprocessing", {})
    size = int(preprocessing.get("image_size", preprocessing.get("input_size", 512)))
    resize_mode = preprocessing.get("resize_mode", "letterbox")
    threshold = float(args.threshold if args.threshold is not None else checkpoint.get("threshold", 0.5))
    transform = build_transform("test", size=size, resize_mode=resize_mode, augment=False)
    image = np.array(Image.open(args.image).convert("RGB"), dtype=np.uint8)
    dummy_mask = np.zeros(image.shape[:2], dtype=np.uint8)
    augmented = transform(image=image, mask=dummy_mask)
    tensor = augmented["image"].unsqueeze(0).to(device)
    with torch.no_grad():
        with torch.amp.autocast(device_type="cuda", enabled=device.type == "cuda"):
            probs = torch.sigmoid(model(tensor))[0, 0].detach().cpu().numpy()
    mask = (probs >= threshold).astype(np.uint8)
    out_mask = Path(args.output_mask)
    out_mask.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(mask * 255, mode="L").save(out_mask)
    if args.output_overlay:
        base = Image.fromarray(augmented["image"].permute(1, 2, 0).detach().cpu().numpy()).convert("RGB")
        overlay = Image.new("RGBA", base.size, (235, 50, 50, 0))
        overlay.putalpha(Image.fromarray(mask * 110, mode="L"))
        out_overlay = Path(args.output_overlay)
        out_overlay.parent.mkdir(parents=True, exist_ok=True)
        Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB").save(out_overlay)


if __name__ == "__main__":
    main()
