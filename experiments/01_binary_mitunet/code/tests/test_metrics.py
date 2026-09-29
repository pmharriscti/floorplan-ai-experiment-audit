from __future__ import annotations

import numpy as np

from mitunet_cubicasa.metrics import counts_from_binary, metrics_from_counts, per_image_metrics


def test_perfect_prediction_dice_iou_one():
    target = np.array([[1, 0], [0, 1]], dtype=np.uint8)
    pred = target.copy()
    metrics = metrics_from_counts(counts_from_binary(pred, target))
    assert metrics["dice"] == 1.0
    assert metrics["iou"] == 1.0


def test_no_overlap_dice_iou_zero():
    target = np.array([[1, 1], [0, 0]], dtype=np.uint8)
    pred = np.array([[0, 0], [1, 1]], dtype=np.uint8)
    metrics = metrics_from_counts(counts_from_binary(pred, target))
    assert metrics["dice"] == 0.0
    assert metrics["iou"] == 0.0


def test_partial_overlap_expected_values():
    target = np.array([[1, 1], [0, 0]], dtype=np.uint8)
    pred = np.array([[1, 0], [1, 0]], dtype=np.uint8)
    metrics = metrics_from_counts(counts_from_binary(pred, target))
    assert abs(metrics["dice"] - 0.5) < 1e-6
    assert abs(metrics["iou"] - (1 / 3)) < 1e-6


def test_empty_prediction_and_target_policy():
    target = np.zeros((4, 4), dtype=np.uint8)
    pred = np.zeros((4, 4), dtype=np.uint8)
    row = per_image_metrics(pred, target, "empty")
    assert row["dice"] == 1.0
    assert row["iou"] == 1.0
    assert row["both_empty"] is True
