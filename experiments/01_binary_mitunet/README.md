# Binary MitUNet Baseline

This is the 512 px binary wall-mask baseline using MitUNet with a MiT-B4 encoder and SCSE decoder attention.

## Source Evidence

Source run directory: `/home/pmharris/dev/mitunet/experiments/cubicasa5k_mitunet/full_gpu`

Primary evidence files:

- `metrics.json`
- `config.yaml`
- `parameters.json`
- `threshold_search.csv`
- `test_metrics.json`
- `validation_metrics.json`
- DeepLab comparator file `comparison_to_mitunet_baseline.json` for the copied baseline checkpoint SHA-256

## Verified Configuration

The run used CubiCasa5K v4 with train/validation/test counts of `4200`/`400`/`400`, RGB input size `512`, letterbox resize, Adam optimizer, learning rate `0.0001`, batch size `4`, AMP enabled, seed `42`, 30 configured epochs, and threshold search enabled.

The model used `segmentation_models_pytorch`, encoder `mit_b4`, ImageNet encoder weights, one output class, and raw logits. Verified model parameter count from `parameters.json` is `64250658`.

## Verified Metrics

Best validation IoU: `0.8179796353020612`

Best validation Dice: `0.8998776657541074`

Selected validation threshold: `0.1`

Test micro IoU at threshold `0.10`: `0.8244338473612428`

Test micro Dice at threshold `0.10`: `0.9037695157362454`

## Interpretation

This run is a successful baseline for binary wall segmentation. It remains the reference point for DeepLabV3 and the starting point for later structure work.

## Missing Evidence

The source git commit and DVC hash for this baseline were not located in the inspected baseline artifacts.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).

