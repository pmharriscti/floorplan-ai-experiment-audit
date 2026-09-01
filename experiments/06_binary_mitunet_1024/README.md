# Binary MitUNet 1024 px Global

This is the standalone 1024 px binary wall-mask MitUNet run. It uses the same wall-vs-background target family as the 512 px baseline, but increases the letterboxed training/evaluation image size to `1024`.

## Source Evidence

Source run directory: `/home/pmharris/dev/mitunet/experiments/cubicasa5k_mitunet/full_gpu_1024`

Primary evidence files:

- `run_config_resolved.yaml`
- `command.txt`
- `run.log`
- `history.csv`
- `summary.json`
- `metrics.json`
- `validation_metrics.json`
- `test_metrics.json`
- `threshold_search.csv`
- `source_resolution_audit.csv`
- `source_resolution_audit.json`
- `train_manifest.csv`
- `val_manifest.csv`
- `test_manifest.csv`
- `manifest_checksums.json`
- `environment.txt`
- `environment.json`
- Hybrid setup report `setup_report.json` for the checkpoint SHA-256

## Verified Configuration

The run used CubiCasa5K v4 with train/validation/test counts of `4200`/`400`/`400`, RGB input size `1024`, letterbox resize, Adam optimizer, learning rate `0.0001`, physical batch size `1`, gradient accumulation `4`, effective batch size `4`, AMP enabled, seed `42`, 30 epochs, and threshold search enabled.

The model used `segmentation_models_pytorch`, encoder `mit_b4`, ImageNet encoder weights, one output class, raw logits, and SCSE decoder attention.

## Verified Metrics

Best validation IoU: `0.8259883607445844`

Best validation Dice: `0.904702766459881`

Best epoch: `28`

Selected validation threshold: `0.1`

Validation threshold-search micro IoU at threshold `0.10`: `0.8267843774749646`

Validation threshold-search micro Dice at threshold `0.10`: `0.9051800394940649`

Test micro IoU at threshold `0.10`: `0.8317579184170079`

Test micro Dice at threshold `0.10`: `0.9081526658673402`

## Visual QA

Curated validation visual evidence is in [qa/README.md](qa/README.md). It includes three shared samples with `source.png`, ground-truth wall mask, regenerated prediction mask at threshold `0.1`, error overlay, copied historical validation overlay, and per-sample metadata.

Training plot images are included under [plots](plots/README.md):

- [learning_rate.png](plots/learning_rate.png)
- [train_loss_vs_val_loss.png](plots/train_loss_vs_val_loss.png)
- [val_dice_vs_val_iou.png](plots/val_dice_vs_val_iou.png)

## Interpretation

This is a positive high-resolution binary wall-segmentation run. Compared with the 512 px baseline, the logged best validation IoU increased from `0.8179796353020612` to `0.8259883607445844`, and test micro IoU at the selected threshold increased from `0.8244338473612428` to `0.8317579184170079`.

This run is also the global 1024 checkpoint reused by the hybrid tiling audit. The hybrid sweep later selected `global_weight=1.0` and `patch_weight=0.0`, so this standalone run is the cleaner place to review the underlying high-resolution model.

## Missing Evidence

The source run records git commit `ade0aa6ba01c72f02a32a33a605c36b54b264a7a`, but the recorded git state also includes uncommitted and untracked files. A DVC dataset hash was not located in the inspected artifacts.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).
