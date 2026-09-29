# CubiCasa5K MitUNet Training

This workflow trains MitUNet for one binary target:

- `1`: wall
- `0`: non-wall

It uses the local CubiCasa5K dataset at `/home/pmharris/dev/cubicasa5k_data` and does not download data or use Roboflow credentials.

## Detected Dataset Format

The local dataset is native CubiCasa5K, not COCO:

- split files: `train.txt`, `val.txt`, `test.txt`
- sample folders containing `F1_scaled.png`, `F1_original.png`, and `model.svg`
- no detected COCO annotation file in the native tree
- no detected LMDB files
- no pre-generated binary wall masks

The pipeline uses the official local CubiCasa5K `floortrans` code when available. The wall mapping is taken from `floortrans.loaders.house.rooms_selected["Wall"] == 2`. Masks are rasterized from native SVG `Wall` polygons at the `F1_scaled.png` coordinate system and then resized for the model.

Doors and windows are not subtracted from the native SVG wall target by default. This matches the native parser's separation of wall semantics and opening icons. The optional `--subtract-openings` flag changes that target preprocessing and records it in the experiment config.

## Commands

Validate data and build the mask cache:

```bash
.venv/bin/python scripts/validate_cubicasa.py \
  --data-root /home/pmharris/dev/cubicasa5k_data \
  --output-dir artifacts/cubicasa_validation
```

Train and evaluate:

```bash
.venv/bin/python scripts/train_mitunet_cubicasa.py \
  --data-root /home/pmharris/dev/cubicasa5k_data \
  --config configs/cubicasa5k_mitunet.yaml
```

Generate observability reports for an existing run:

```bash
.venv/bin/python scripts/generate_training_observability.py \
  experiments/cubicasa5k_mitunet/<run>
```

Evaluate an existing checkpoint:

```bash
.venv/bin/python scripts/evaluate_mitunet_cubicasa.py \
  --data-root /home/pmharris/dev/cubicasa5k_data \
  --checkpoint experiments/cubicasa5k_mitunet/<run>/best_model.pth \
  --split test \
  --also-threshold-05
```

## Outputs

Each training run writes a new timestamped directory under `experiments/cubicasa5k_mitunet/` with:

- `config.yaml`
- `environment.json`
- `dataset_summary.json`
- `train_manifest.csv`, `val_manifest.csv`, `test_manifest.csv`
- `invalid_samples.csv`
- `training_history.csv`
- `metrics.json`
- `metrics_summary.csv`
- `per_image_test_metrics.csv`
- `threshold_search.csv`
- `best_model.pth`
- `last_model.pth`
- `training_curves.png`
- `confusion_counts.json`
- validation and test prediction overlays
- `run.log`

Training also writes ML observability artifacts under `reports/training_runs/<run_id>/`:

- `training_log.csv` with one row per epoch, including train/validation loss, validation Dice/IoU, learning rate, checkpoint path, and best-checkpoint flag
- `plots/train_loss_vs_val_loss.png`
- `plots/val_dice_vs_val_iou.png`
- `plots/learning_rate.png`
- `summary.md`

Generated masks are cached under `artifacts/cubicasa5k_wall_cache/` with metadata that invalidates stale masks when source files or preprocessing settings change.

## Early Stopping

By default, early stopping and LR plateau scheduling monitor validation IoU. Set `early_stopping_metric: val_loss` in the config, or pass `--early-stopping-metric val_loss`, to stop on validation loss instead. `early_stopping_min_delta` controls the minimum required improvement.

## Metric Policy

Metrics are computed after sigmoid probabilities are thresholded into binary masks. Dataset-level micro metrics aggregate TP, FP, TN, and FN across all pixels. Per-image macro summaries report mean, median, standard deviation, minimum, maximum, and sample count.

When prediction and target are both empty, per-image Dice and IoU are defined as `1.0`; macro summaries are reported both including and excluding such samples. Micro metrics always use aggregate counts.

The default threshold is `0.5`. If threshold search is enabled, thresholds from `0.10` to `0.90` in steps of `0.05` are evaluated on validation only. The selected threshold maximizes validation micro Dice, with micro IoU as a tie-breaker, and is frozen before test evaluation.
