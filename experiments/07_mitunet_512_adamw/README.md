# MitUNet 512 AdamW Optimizer Comparator

This experiment tests whether replacing the canonical Adam optimizer with AdamW changes binary wall segmentation quality when every other audited setting is held constant.

The supplied artifact path and resolved config verify `image_size: 512`, not `1024`. This audit entry therefore documents the provided 512 px AdamW run.

## Source Evidence

Source run directory: `/mnt/e/test/_folder/floorplan_ai/experiments/mitunet_cubicasa5k_512_adamw/20260901_134158`

Primary evidence files:

- `EXPERIMENT_SUMMARY.md`
- `configs/resolved_config.yaml`
- `logs/run.log`
- `logs/training_history.csv`
- `logs/training_curves.png`
- `evaluation/adam_vs_adamw_comparison.json`
- `evaluation/metrics.json`
- `evaluation/validation_metrics.json`
- `evaluation/test_metrics.json`
- `evaluation/threshold_search.csv`
- `evaluation/representative_samples.csv`
- `evaluation/visual_comparison_index.json`
- `splits/reproducibility_gate.json`
- `label_validation/label_validation_summary.json`

## Verified Configuration

The run used CubiCasa5K v4 with the exact historical train/validation/test membership, counts of `4200`/`400`/`400`, RGB input size `512`, letterbox resize, AdamW optimizer, learning rate `0.0001`, weight decay `0.0`, batch size `4`, AMP enabled, seed `42`, 30 epochs, and threshold search enabled.

The model used MiT-UNet with MiT-B4, ImageNet encoder weights, SCSE decoder attention, one output channel, and binary wall masks from native CubiCasa5K SVG wall polygons.

## Verified Metrics

Best validation IoU: `0.8142022203773948`

Best validation Dice: `0.8975870619406721`

Best epoch: `30`

Selected validation threshold: `0.1`

AdamW test micro IoU at threshold `0.10`: `0.8206001227094942`

AdamW test micro Dice at threshold `0.10`: `0.9014611308366193`

AdamW minus Adam control test micro IoU: `-0.0038337246517485823`

AdamW minus Adam control test micro Dice: `-0.002308384899626148`

AdamW precision improved slightly by `+0.0005428471008782632`, but recall dropped by `-0.005041449125746333`.

## Visual QA

Curated visual evidence is in [qa/README.md](qa/README.md). It includes six representative test samples from the run's historical Adam-vs-AdamW comparison artifacts: strongest clean case, difficult worst case, false-positive-heavy case, false-negative-heavy case, sparse target, and dense target.

Each sample folder includes source image, ground-truth wall mask, Adam control prediction mask, AdamW prediction mask, AdamW overlay, target overlay, Adam-vs-AdamW comparison composite, and per-sample metadata.

Training curves are included in [plots/training_curves.png](plots/training_curves.png).

## Interpretation

This is a negative optimizer comparator. AdamW with configured `weight_decay=0.0` did not improve the canonical 512 px Adam baseline. The test regression is small, but directionally consistent in the aggregate metrics: AdamW reduced recall enough to lower IoU and Dice despite a slight precision gain.

This experiment does not test decoupled nonzero weight decay. A separate AdamW run with nonzero `weight_decay` would be needed for that question.

## Missing Evidence

The experiment harness at `/home/pmharris/dev/mitunet_adam_w` is not a Git repository, so no harness commit hash is available. The protected core implementation is a clean Git repository at commit `0775f80a4cad366866990419aed18ea7434676f8`. A DVC dataset hash was not located in the inspected artifacts.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).
