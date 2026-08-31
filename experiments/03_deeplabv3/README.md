# DeepLabV3-ResNet50 Comparator

This experiment evaluated DeepLabV3-ResNet50 as an alternate binary wall segmentation architecture.

## Source Evidence

Source run directory: `/mnt/e/AI_Team/mitunet/experiments/cubicasa5k_deeplabv3_resnet50/deeplabv3_resnet50_wall_512_imagenet_aux_seed42_20260805T154529Z`

Primary evidence files:

- `summary.json`
- `metrics.json`
- `config.yaml`
- `comparison_to_mitunet_baseline.json`
- `best_model.pth.metadata.json`
- `git_state.json`

## Verified Configuration

The run used DeepLabV3-ResNet50 from torchvision with ImageNet1K V2 backbone weights, auxiliary loss enabled, RGB input, binary wall target, image size `512`, Adam optimizer, learning rate `0.0001`, batch size `4`, AMP enabled, seed `42`, and threshold search enabled.

Verified parameter count is `41993794`. The run completed `15` epochs and selected epoch `11`.

## Verified Metrics

Best validation IoU: `0.7702792714789161`

Best validation Dice: `0.8702347520969547`

Selected threshold: `0.5`

Test micro IoU at selected threshold: `0.7723460788233382`

Test micro Dice at selected threshold: `0.8715522188940653`

The comparison artifact reports negative deltas versus the MitUNet baseline: validation IoU `-0.04770036382314513`, validation Dice `-0.02964291365715277`, test micro IoU `-0.052087768537904644`, and test micro Dice `-0.03221729684218011`.

## Interpretation

This was a completed negative comparator: useful evidence that the tested DeepLabV3-ResNet50 setup did not outperform the MitUNet baseline.

## Missing Evidence

DVC hash/status was not located in the inspected DeepLabV3 artifacts.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).

