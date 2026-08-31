# Metrics Definitions

These definitions summarize how metrics are interpreted in this audit. Exact implementation details should be checked in the original experiment code and reports before making new claims.

## Wall IoU

Intersection over Union for the wall-region binary mask:

`TP / (TP + FP + FN)`

Higher is better.

## Wall Dice

Dice coefficient for the wall-region binary mask:

`2TP / (2TP + FP + FN)`

Higher is better.

## Boundary F1@2 px

F1 score for predicted wall-boundary pixels using a 2 pixel matching tolerance. In Phase 2 this comes from the dedicated wall-boundary head. For experiments without a dedicated boundary objective, this field is left `UNKNOWN` in the scoreboard unless a comparable final metric is explicitly audited.

## Centerline clDice

Centerline topology overlap score for predicted wall centerlines. Phase 1 reports `cldice_mean`; Phase 2 reports `centerline_skeleton_cldice_mean`.

Higher is better.

## Junction F1@5 px

F1 score for detected junction points using a 5 pixel matching tolerance. Higher is better.

## Door Object F1

Object-level F1 score for door/opening components. Phase 2 final evaluation uses IoU threshold 0.25 for the scoreboard value because the source report records `door_object_f1_iou_0_25_mean` and `door_opening_object_f1_mean` with the same value.

## Micro vs Macro

Micro metrics aggregate counts across the split before computing the score. Macro metrics compute per-sample scores and then average them. The scoreboard prefers the primary metric used by the source report for the experiment. Detailed metrics retain micro/macro distinctions where they were present.

## Thresholds

Thresholds are copied from selected-threshold artifacts. A configured threshold and a selected threshold can differ; the scoreboard uses selected thresholds when available.

