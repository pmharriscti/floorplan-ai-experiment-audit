# Hybrid Tiling / 1024 Global-Patch Sweep

This experiment evaluated higher-resolution wall segmentation with global and patch-tiled predictions. The locked validation selection chose crop size `1024`, overlap `0.5`, Gaussian blending, `global_weight=1.0`, and `patch_weight=0.0`.

## Source Evidence

Local report root: `/home/pmharris/dev/mitunet/reports/binary_wall_hybrid_global_patch/20260723T021006Z`

External experiment manifest root: `/mnt/e/AI_Team/mitunet/experiments/binary_wall_hybrid_global_patch/20260723T021043Z`

Primary evidence files:

- `locked_validation_selection.json`
- `validation_sweep.json`
- `test_crop1024_overlap0.5_gaussian_gw1_summary.json`
- `setup_report.json`
- `experiment_manifest.json`

## Verified Configuration

The setup report identifies a compatible binary MitUNet checkpoint trained at input size `1024`, with threshold in checkpoint `0.1`, validation IoU `0.8259883607445844`, validation Dice `0.904702766459881`, and checkpoint SHA-256 `42cad015bf894e6afe11011424b7ed88c49a1512f81593f14df5b228d65a3910`.

The selected sweep used validation split selection and explicitly records `test_used_for_selection=false`.

## Verified Metrics

Locked validation hybrid IoU: `0.8261317505223036`

Locked validation hybrid Dice: `0.9047887703458596`

Locked validation boundary IoU: `0.5809357985569126`

Test hybrid IoU for the locked crop/blending/fusion: `0.8310196912892222`

Test hybrid Dice for the locked crop/blending/fusion: `0.9077124568814448`

## Visual QA

Curated validation visual evidence is in [qa/README.md](qa/README.md). It includes three shared samples with `source.png`, ground-truth wall mask, regenerated prediction mask, error overlay, copied historical 1024 px validation overlay, and per-sample metadata.

The prediction masks were regenerated from the verified 1024 px global checkpoint at threshold `0.5`. This represents the locked hybrid selection because the selected fusion records `global_weight=1.0` and `patch_weight=0.0`.

## Interpretation

This is a positive high-resolution result, but not positive evidence for patch-fusion improvement. The selected fusion gave the patch stream zero weight, so final selected performance is effectively the high-resolution global model.

## Missing Evidence

The source git commit and DVC hash were not located in the inspected hybrid artifacts.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).
