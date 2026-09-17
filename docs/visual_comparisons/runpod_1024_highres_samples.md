# RunPod 1024 High-Resolution Crop Samples

These four historical validation composites come from epoch 3, the best checkpoint for experiment `08_mitunet_1024_highres_runpod`. They show input, target, prediction, and TP/FP/FN overlay in one PNG.

| Sample | Composite | Main visible error pattern |
| --- | --- | --- |
| `high_quality_architectural/333` | [view](../../experiments/08_mitunet_1024_highres_runpod/qa/epoch_003_01.png) | Exterior false positives and missed interior partitions |
| `high_quality_architectural/1654` | [view](../../experiments/08_mitunet_1024_highres_runpod/qa/epoch_003_02.png) | Local edge overprediction and interior false negatives |
| `high_quality_architectural/5559` | [view](../../experiments/08_mitunet_1024_highres_runpod/qa/epoch_003_03.png) | Thick exterior prediction and substantial missing interior structure |
| `high_quality_architectural/3015` | [view](../../experiments/08_mitunet_1024_highres_runpod/qa/epoch_003_04.png) | Exterior overprediction and widespread interior-wall misses |

Green indicates true positive, red false positive, and blue false negative. These are copied historical artifacts; no new inference was run for the audit.
