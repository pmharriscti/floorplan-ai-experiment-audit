# Phase 2 Boundary And Door/Openings

Phase 2 continued from the completed Phase 1 wall-structure checkpoint and added independent wall-boundary and door-opening sigmoid heads.

## Source Evidence

Source run directory: `/mnt/e/AI_Team/mitunet/phase2_wall_boundary_door_openings/experiments/mitunet_phase2_wall_boundary_door_openings_20260810_200219_UTC`

Primary evidence files:

- `reports/FINAL_REPORT.md`
- `reports/evaluate_summary.json`
- `reports/summary.json`
- `proof/summary.json`
- `metrics/final_metrics.csv`
- `metrics/phase1_comparison.csv`
- `metrics/training_history.csv`
- `checkpoint_manifest.json`
- `dvc_status.json`
- `mlflow_status.json`
- MLflow artifact config `mitunet_phase2_wall_boundary_door_openings.yaml`

## Verified Configuration

The parent checkpoint was Phase 1 `best_structural_score.pth`. Phase 2 preserved the inherited wall-region, centerline, and junction heads, then added `wall_boundary_logits` and `door_opening_logits`.

Boundary targets were one-pixel inner contours from Phase 1 wall-region masks. Door-opening targets came from top-level Door polygons, excluding Panel, swing, and door-leaf symbols.

Training was configured for 30 total epochs with 2 warmup epochs for new heads and fine-tuning afterward. The run completed 12 total epochs. The best Phase 2 epoch was `4`, with best Phase 2 score `0.6767861011937464`.

## Verified Metrics

Selected thresholds: wall-region `0.05`, centerline `0.95`, junction `0.9`, junction NMS radius `2`, wall-boundary `0.95`, door-opening `0.85`, door minimum component area `1`.

Final wall-region IoU: `0.7708163311811328`

Final wall-region Dice: `0.8705773914644204`

Final centerline skeleton clDice: `0.38908625787638323`

Final junction F1@5 px: `0.5278302922503402`

Final boundary F1@2 px: `0.9347893344704645`

Final door object F1: `0.7796991077953163`

Final Phase 2 structural score: `0.6757521275016246`

Final Phase 1-compatible structural score: `0.6198494033500891`

## Visual QA

Curated validation visual evidence is in [qa/README.md](qa/README.md). It includes three shared samples with source images, wall-region, centerline, junction, wall-boundary, and door-opening masks, plus error overlays and per-sample metadata.

The prediction masks were derived from saved historical `probability_maps/val/*.npz` files using the verified Phase 2 thresholds. Historical target QA composites were copied where exact sample files existed; unavailable exact composites are marked `NOT_YET_AVAILABLE` in the sample folders and metadata.

## Interpretation

This result is mixed. Boundary and door/opening heads produced strong final metrics, but inherited Phase 1 structural quality regressed. The comparison CSV records wall IoU delta `-0.05004927229517453`, junction F1@5 px delta `-0.2415549205790718`, and Phase 1-compatible structural score delta `-0.14096779852795083` versus the saved Phase 1 evaluation.

The higher door value `0.8194901582399987` was found in `training_history.csv` as a validation-history value, not as the final selected-checkpoint evaluation used in the scoreboard.

## Missing Evidence

The Phase 2 checkpoint manifest defers SHA-256 hashing for large checkpoints. Gradio was recorded as not tested in the proof summary.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).
