from __future__ import annotations

import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2


IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)
MODEL_DOWNSAMPLING_STRIDE = 32
SUPPORTED_EXPERIMENT_IMAGE_SIZES = {512, 1024, 1536}


def validate_experiment_image_size(size: int, stride: int = MODEL_DOWNSAMPLING_STRIDE) -> int:
    size = int(size)
    if size not in SUPPORTED_EXPERIMENT_IMAGE_SIZES:
        allowed = ", ".join(str(value) for value in sorted(SUPPORTED_EXPERIMENT_IMAGE_SIZES))
        raise ValueError(f"Unsupported image_size={size}; expected one of: {allowed}")
    if size % stride != 0:
        raise ValueError(f"image_size={size} is not compatible with model stride {stride}")
    return size


def resize_ops(size: int, mode: str) -> list[A.BasicTransform]:
    if mode == "direct":
        return [A.Resize(size, size, interpolation=cv2.INTER_LINEAR, mask_interpolation=cv2.INTER_NEAREST)]
    if mode == "letterbox":
        return [
            A.LongestMaxSize(max_size=size, interpolation=cv2.INTER_LINEAR, mask_interpolation=cv2.INTER_NEAREST),
            A.PadIfNeeded(
                min_height=size,
                min_width=size,
                border_mode=cv2.BORDER_CONSTANT,
                fill=(255, 255, 255),
                fill_mask=0,
            ),
        ]
    raise ValueError(f"Unsupported resize mode: {mode}")


def build_transform(
    split: str,
    size: int = 512,
    resize_mode: str = "letterbox",
    augment: bool = True,
    additional_mask_names: list[str] | None = None,
) -> A.Compose:
    ops: list[A.BasicTransform] = []
    if split == "train" and augment:
        ops.extend(
            [
                A.HorizontalFlip(p=0.5),
                A.VerticalFlip(p=0.5),
                A.RandomRotate90(p=0.5),
                A.RandomBrightnessContrast(brightness_limit=0.15, contrast_limit=0.15, p=0.35),
            ]
        )
    ops.extend(resize_ops(size, resize_mode))
    ops.extend(
        [
            A.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
            ToTensorV2(transpose_mask=True),
        ]
    )
    additional_targets = {name: "mask" for name in (additional_mask_names or [])}
    return A.Compose(ops, additional_targets=additional_targets)
