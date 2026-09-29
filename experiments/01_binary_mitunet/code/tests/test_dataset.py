from __future__ import annotations

import csv
from pathlib import Path

import albumentations as A
import cv2
import numpy as np
from PIL import Image

from mitunet_cubicasa.cubicasa_parser import NativeSample, validate_split_leakage
from mitunet_cubicasa.dataset import CubiCasaWallDataset, MANIFEST_FIELDS


def _write_manifest(tmp_path: Path) -> Path:
    image = np.zeros((32, 32, 3), dtype=np.uint8)
    image[8:24, 10:20] = 255
    mask = np.zeros((32, 32), dtype=np.uint8)
    mask[8:24, 10:20] = 1
    image_path = tmp_path / "image.png"
    mask_path = tmp_path / "mask.png"
    Image.fromarray(image).save(image_path)
    Image.fromarray(mask).save(mask_path)
    manifest = tmp_path / "manifest.csv"
    with manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerow(
            {
                "split": "train",
                "sample_id": "sample",
                "image_path": image_path,
                "annotation_path": tmp_path / "model.svg",
                "mask_path": mask_path,
                "original_width": 32,
                "original_height": 32,
                "wall_pixels": int(mask.sum()),
                "wall_fraction": float(mask.mean()),
            }
        )
    return manifest


def test_dataset_mask_binary_and_tensor_shapes(tmp_path: Path):
    manifest = _write_manifest(tmp_path)
    dataset = CubiCasaWallDataset(manifest, "train", image_size=32, resize_mode="direct", augment=False)
    sample = dataset[0]
    assert sample["image"].shape == (3, 32, 32)
    assert sample["mask"].shape == (1, 32, 32)
    assert set(sample["mask"].unique().tolist()).issubset({0.0, 1.0})


def test_joint_flip_keeps_image_and_mask_aligned():
    image = np.zeros((16, 16, 3), dtype=np.uint8)
    mask = np.zeros((16, 16), dtype=np.uint8)
    image[:, :4, 0] = 255
    mask[:, :4] = 1
    transform = A.Compose([A.HorizontalFlip(p=1.0), A.Resize(16, 16, interpolation=cv2.INTER_LINEAR, mask_interpolation=cv2.INTER_NEAREST)])
    out = transform(image=image, mask=mask)
    red = out["image"][:, :, 0] > 0
    assert np.array_equal(red.astype(np.uint8), out["mask"].astype(np.uint8))


def test_split_manifest_duplicate_detection():
    sample = NativeSample(
        split="train",
        sample_id="same",
        folder=Path("same"),
        image_path=Path("same/F1_scaled.png"),
        annotation_path=Path("same/model.svg"),
        split_entry="/same/",
    )
    samples = {"train": [sample], "val": [sample], "test": []}
    try:
        validate_split_leakage(samples)
    except ValueError as exc:
        assert "leakage" in str(exc).lower()
    else:
        raise AssertionError("Expected duplicate split leakage to fail")
