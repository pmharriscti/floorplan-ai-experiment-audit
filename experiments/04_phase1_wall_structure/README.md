# Phase 1 Wall Structure

Phase 1 extended the wall segmentation work with three independent sigmoid heads: wall-region, centerline, and junction.

## Source Evidence

Source run directory: `/mnt/e/AI_Team/mitunet/phase1_wall_structure/experiments/mitunet_phase1_wall_region_centerline_junctions_20260807_163622_UTC`

Primary evidence files:

- `reports/FINAL_REPORT.md`
- `metrics/evaluation_summary.json`
- `reports/summary.json`
- `proof/full_training.json`
- `checkpoint_manifest.json`
- `dvc_status.json`
- `mlflow_status.json`
- MLflow artifact config `mitunet_phase1_wall_region_centerline_junctions.yaml`

## Verified Configuration

The run used task mode `multitask_wall_structure`, seed `42`, input size `512`, letterbox resize, MitUNet with MiT-B4 encoder and SCSE attention, and outputs for `wall_region`, `centerline`, and `junction`.

The baseline parent was `/home/pmharris/dev/mitunet/experiments/cubicasa5k_mitunet/full_gpu`, checkpoint epoch `29`, threshold `0.1`, validation IoU `0.817980`, and validation Dice `0.899878`.

Training was configured for 30 epochs with Adam, learning rate `0.0001`, batch size `4`, AMP enabled, early stopping on `val_structural_score`, and task weights wall `0.60`, centerline `0.30`, junction `0.10`.

## Verified Metrics

Selected thresholds: wall-region `0.05`, centerline `0.95`, junction `0.85`, junction NMS radius `3`.

Validation wall-region IoU: `0.8208656034763073`

Validation wall-region Dice: `0.9016212969360846`

Validation centerline clDice: `0.6464444601388634`

Validation junction F1@5 px: `0.769385212829412`

Validation graph edge coverage: `0.9554306800116725`

Validation structural score: `0.7608172018780399`

## Visual QA

Curated validation visual evidence is in [qa/README.md](qa/README.md). It includes three shared samples with source images, wall-region masks, centerline masks, junction-point masks, error overlays, copied historical target QA composites, and per-sample metadata.

The prediction masks were regenerated from `best_structural_score.pth` using the verified Phase 1 thresholds. This QA evidence covers only Phase 1 heads: wall-region, centerline, and junction.

## Interpretation

This is a positive structural expansion. It preserved strong wall-region performance while adding measurable centerline, junction, and graph-connectivity metrics. It should not be treated as evidence for boundary or door/opening quality because those heads were not part of Phase 1.

## Missing Evidence

The Phase 1 checkpoint manifest defers SHA-256 hashing for large checkpoints. Boundary F1 and door object F1 values mentioned in historical notes were not found in the inspected Phase 1 artifacts.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).
