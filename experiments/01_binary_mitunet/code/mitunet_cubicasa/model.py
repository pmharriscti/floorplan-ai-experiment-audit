from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import segmentation_models_pytorch as smp
import torch
from torch import nn

from .ontology import (
    ICON_CLASSES,
    MASK_SCHEMA_VERSION,
    TASK_BINARY_WALL,
    TASK_CUBICASA_MULTICLASS,
    class_names,
    enabled_structure_classes,
    mapping_hash,
)


@dataclass(frozen=True)
class ModelBuildResult:
    model: torch.nn.Module
    architecture: dict[str, Any]
    pretrained_loaded: bool
    pretrained_error: str | None


class MultiHeadMitUNet(nn.Module):
    def __init__(self, base_model: torch.nn.Module, structure_classes: int, icon_classes: int):
        super().__init__()
        self.encoder = base_model.encoder
        self.decoder = base_model.decoder
        self.classification_head = getattr(base_model, "classification_head", None)
        head_conv = base_model.segmentation_head[0]
        in_channels = int(head_conv.in_channels)
        self.structure_head = nn.Conv2d(in_channels, structure_classes, kernel_size=1)
        self.icon_head = nn.Conv2d(in_channels, icon_classes, kernel_size=1)
        self._check_input_shape = base_model.check_input_shape

    def check_input_shape(self, x: torch.Tensor) -> None:
        self._check_input_shape(x)

    def forward(self, x: torch.Tensor) -> dict[str, torch.Tensor]:
        if not (torch.jit.is_scripting() or torch.jit.is_tracing()):
            self.check_input_shape(x)
        features = self.encoder(x)
        decoder_output = self.decoder(features)
        return {
            "structure": self.structure_head(decoder_output),
            "icons": self.icon_head(decoder_output),
        }


def normalize_encoder_weights(value: str | None) -> str | None:
    if value is None:
        return None
    value = str(value)
    if value.lower() in {"none", "null", "false", "random", ""}:
        return None
    return value


def build_mitunet(
    encoder_name: str = "mit_b4",
    encoder_weights: str | None = "imagenet",
    in_channels: int = 3,
    classes: int = 1,
    decoder_attention_type: str = "scse",
    strict_pretrained: bool = False,
    task_mode: str = TASK_BINARY_WALL,
    include_optional_structure: bool = False,
) -> ModelBuildResult:
    requested_weights = normalize_encoder_weights(encoder_weights)
    pretrained_loaded = False
    pretrained_error = None

    if task_mode not in {TASK_BINARY_WALL, TASK_CUBICASA_MULTICLASS}:
        raise ValueError(f"Unsupported task_mode={task_mode!r}")

    def make(weights: str | None) -> torch.nn.Module:
        aux_segformer = smp.Segformer(encoder_name=encoder_name, encoder_weights=weights)
        model = smp.Unet(
            encoder_name=encoder_name,
            encoder_weights=None,
            in_channels=in_channels,
            classes=classes,
            activation=None,
            decoder_attention_type=decoder_attention_type,
        )
        model.encoder = aux_segformer.encoder
        if task_mode == TASK_CUBICASA_MULTICLASS:
            return MultiHeadMitUNet(
                model,
                structure_classes=len(enabled_structure_classes(include_optional_structure)),
                icon_classes=len(ICON_CLASSES),
            )
        return model

    try:
        model = make(requested_weights)
        pretrained_loaded = requested_weights is not None
    except Exception as exc:
        pretrained_error = str(exc)
        if strict_pretrained or requested_weights is None:
            raise
        model = make(None)

    architecture = {
        "name": "MitUNet",
        "library": "segmentation_models_pytorch",
        "encoder_name": encoder_name,
        "encoder_weights_requested": requested_weights,
        "encoder_weights_loaded": requested_weights if pretrained_loaded else None,
        "in_channels": in_channels,
        "classes": classes if task_mode == TASK_BINARY_WALL else None,
        "decoder_attention_type": decoder_attention_type,
        "output": "raw_logits",
        "task_mode": task_mode,
        "include_optional_structure": include_optional_structure if task_mode == TASK_CUBICASA_MULTICLASS else None,
        "structure_classes": class_names(enabled_structure_classes(include_optional_structure)) if task_mode == TASK_CUBICASA_MULTICLASS else None,
        "icon_classes": class_names(ICON_CLASSES) if task_mode == TASK_CUBICASA_MULTICLASS else None,
        "mask_schema_version": MASK_SCHEMA_VERSION if task_mode == TASK_CUBICASA_MULTICLASS else None,
        "mapping_hash": mapping_hash(include_optional_structure) if task_mode == TASK_CUBICASA_MULTICLASS else None,
        "multihead_output": task_mode == TASK_CUBICASA_MULTICLASS,
        "uses_segformer_encoder_transplant": True,
    }
    return ModelBuildResult(
        model=model,
        architecture=architecture,
        pretrained_loaded=pretrained_loaded,
        pretrained_error=pretrained_error,
    )


def load_model_from_checkpoint(checkpoint: dict[str, Any], map_location: str | torch.device = "cpu") -> ModelBuildResult:
    arch = checkpoint.get("architecture", {})
    task_mode = arch.get("task_mode") or checkpoint.get("task_mode") or TASK_BINARY_WALL
    binary_classes = arch.get("classes", 1)
    if binary_classes is None:
        binary_classes = 1
    result = build_mitunet(
        encoder_name=arch.get("encoder_name", "mit_b4"),
        encoder_weights=None,
        in_channels=int(arch.get("in_channels", 3)),
        classes=int(binary_classes),
        decoder_attention_type=arch.get("decoder_attention_type", "scse"),
        task_mode=task_mode,
        include_optional_structure=bool(arch.get("include_optional_structure", False)),
    )
    state = checkpoint.get("model_state") or checkpoint.get("model")
    if state is None:
        raise KeyError("Checkpoint does not contain 'model_state' or 'model'")
    result.model.load_state_dict(state)
    result.model.to(map_location)
    return result


def load_matching_weights(model: torch.nn.Module, state: dict[str, torch.Tensor]) -> dict[str, list[str]]:
    current = model.state_dict()
    compatible = {}
    skipped_shape_mismatch = []
    for key, value in state.items():
        if key in current and tuple(current[key].shape) == tuple(value.shape):
            compatible[key] = value
        elif key in current:
            skipped_shape_mismatch.append(key)
    missing, unexpected = model.load_state_dict(compatible, strict=False)
    unexpected = list(unexpected) + [key for key in state if key not in current]
    return {
        "loaded_keys": sorted(compatible),
        "missing_keys": sorted(missing),
        "unexpected_keys": sorted(unexpected),
        "skipped_shape_mismatch_keys": sorted(skipped_shape_mismatch),
    }
