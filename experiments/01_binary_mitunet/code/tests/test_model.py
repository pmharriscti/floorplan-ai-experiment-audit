from __future__ import annotations

import torch

from mitunet_cubicasa.model import build_mitunet, load_model_from_checkpoint
from mitunet_cubicasa.ontology import TASK_CUBICASA_MULTICLASS
from mitunet_cubicasa.transforms import validate_experiment_image_size


def test_model_output_shape_512():
    torch.set_num_threads(2)
    build = build_mitunet(encoder_weights=None)
    model = build.model.eval()
    x = torch.randn(1, 3, 512, 512)
    with torch.no_grad():
        y = model(x)
    assert y.shape == (1, 1, 512, 512)


def test_multiclass_model_output_heads_512():
    torch.set_num_threads(2)
    build = build_mitunet(encoder_weights=None, task_mode=TASK_CUBICASA_MULTICLASS)
    model = build.model.eval()
    x = torch.randn(1, 3, 512, 512)
    with torch.no_grad():
        y = model(x)
    assert set(y) == {"structure", "icons"}
    assert y["structure"].shape == (1, 2, 512, 512)
    assert y["icons"].shape == (1, 12, 512, 512)
    assert build.architecture["task_mode"] == TASK_CUBICASA_MULTICLASS


def test_checkpoint_loads_same_architecture():
    build = build_mitunet(encoder_weights=None)
    checkpoint = {
        "model_state": build.model.state_dict(),
        "architecture": build.architecture,
    }
    loaded = load_model_from_checkpoint(checkpoint)
    assert loaded.architecture["encoder_name"] == build.architecture["encoder_name"]
    assert loaded.architecture["decoder_attention_type"] == build.architecture["decoder_attention_type"]


def test_experiment_image_size_validation():
    assert validate_experiment_image_size(1024) == 1024
    try:
        validate_experiment_image_size(1000)
    except ValueError as exc:
        assert "image_size" in str(exc)
    else:
        raise AssertionError("Expected unsupported image size to fail")
