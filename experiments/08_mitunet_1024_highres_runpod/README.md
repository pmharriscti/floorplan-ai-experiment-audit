# MitUNet 1024 High-Resolution Crop Treatment on RunPod

This experiment tested native-resolution `1024 x 1024` crop training for binary wall segmentation on a RunPod A100 80GB. It completed the planned 10-epoch exploratory treatment and also documented a major infrastructure improvement: moving active data and the Python environment off the RunPod Network Volume and onto pod-local storage.

## Source Evidence

Local artifact archive: `/mnt/e/AI_Team/mitunet/fast1024_final_results`

Local source repository: `/home/pmharris/dev/mitunet_uniform_1024_crop`

Primary evidence files:

- `summary.json`
- `history.json`
- `history.csv`
- `PROVENANCE.json`
- `launch.log`
- `local_environment.txt`
- `CHECKPOINT_SHA256SUMS`
- `overlays/epoch_003_01.png` through `overlays/epoch_003_04.png`
- `checkpoints/epoch_003.pth`
- `checkpoints/epoch_010.pth`
- `control/epoch_008.pth`
- `control/resume.pth`

Small original result and provenance files are preserved under [results](results) and [source_provenance](source_provenance). Checkpoints remain in the external archive.

## Verified Configuration

The treatment used native `1024 x 1024` training crops, 4,200 samples per epoch, physical batch size `4`, no gradient accumulation, AMP, seed `42`, Adam at learning rate `0.0001`, and Asymmetric Tversky loss. The MitUNet model used a MiT-B4 ImageNet encoder and one output channel.

Validation used all 400 validation plans as whole-plan `512 x 512` letterboxes at threshold `0.1`. This means the experiment changed both resolution and spatial context: it was not a controlled comparison of the same image presentation at 512 and 1024.

The run used PyTorch `2.8.0+cu128` on an NVIDIA A100 80GB PCIe. Peak reserved PyTorch memory was `44,589,645,824` bytes, approximately `41.53 GiB`.

## RunPod Execution Study

The supplied preflight report records successful diagnostic steps for both configurations. The 512 control used approximately `5.42 GiB` allocated and `5.62 GiB` reserved; the 1024 treatment used approximately `38.35 GiB` allocated and `41.49 GiB` reserved. Both produced finite, nonzero gradients and parameter updates without an out-of-memory failure. This established that the A100 80GB could sustain physical batch size `4` at 1024 without a memory-driven gradient-accumulation workaround.

The initial cloud layout placed the dataset, environment, source, checkpoints, and audit artifacts on a persistent RunPod Network Volume. GPU utilization was reportedly often only `0-5%` because the A100 waited on thousands of small reads and frequent writes. The original runner also rewrote a roughly 737 MB recovery checkpoint after every batch, or 1,050 times per epoch.

The Fast1024 runner changed the hot path:

```text
RunPod Network Volume
    -> one-time staging
    -> pod-local data and Python environment
    -> A100 training
    -> one checkpoint per completed epoch
    -> persistent Network Volume backup
```

The launch log verifies that 9,202 files totaling `2.05 GiB` were staged locally before training and that each completed epoch checkpoint was copied back to `/workspace`. This preserved durable recovery while removing the Network Volume from batch-level reads and writes.

## Verified Metrics

Best validation epoch: `3`

Best validation IoU: `0.43214381550960096`

Best validation Dice: `0.6034922063407869`

Best validation precision: `0.5905856781496122`

Best validation recall: `0.6169754507591669`

Final epoch validation IoU: `0.3817684301247201`

Final epoch validation Dice: `0.552579465273007`

Training time across 10 epochs: `5,050.85` seconds (`84.18` minutes)

Validation time across 10 epochs: `177.36` seconds (`2.96` minutes)

No test inference was run, so this entry does not report test metrics.

## Validation History

| Epoch | IoU | Dice | Precision | Recall | Train loss |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.424587 | 0.596085 | 0.584675 | 0.607949 | 0.339093 |
| 2 | 0.351710 | 0.520392 | 0.424363 | 0.672593 | 0.141881 |
| **3** | **0.432144** | **0.603492** | **0.590586** | **0.616975** | **0.131574** |
| 4 | 0.401949 | 0.573415 | 0.506415 | 0.660847 | 0.126739 |
| 5 | 0.423382 | 0.594895 | 0.596532 | 0.593268 | 0.122413 |
| 6 | 0.415306 | 0.586878 | 0.610993 | 0.564595 | 0.121789 |
| 7 | 0.430324 | 0.601716 | 0.592345 | 0.611388 | 0.118015 |
| 8 | 0.395199 | 0.566513 | 0.486451 | 0.678120 | 0.111900 |
| 9 | 0.415963 | 0.587534 | 0.557239 | 0.621312 | 0.110168 |
| 10 | 0.381768 | 0.552579 | 0.482425 | 0.646611 | 0.106704 |

Training loss continued to fall after epoch 3 while validation quality remained below the best checkpoint.

## Visual QA

The [visual QA page](qa/README.md) includes four historical best-epoch composites for validation samples `high_quality_architectural/333`, `1654`, `5559`, and `3015`. Each PNG contains the input, target, prediction, and a TP/FP/FN overlay. These are copied artifacts; the audit performed no new inference.

Green is true positive, red is false positive, and blue is false negative. The dense examples visibly support the reported failure modes: over-thick exterior-wall predictions and missed interior partitions.

## Interpretation

This is a negative high-resolution crop treatment. The user-supplied experiment summary reports a best nine-epoch 512 whole-plan control IoU/Dice of `0.801067`/`0.889547`, versus `0.432144`/`0.603492` for this treatment. Because the treatment trained on local crops while validation remained whole-plan letterboxing, the result does not establish that high resolution itself is harmful.

The infrastructure result is positive. Staging 9,202 files (`2.05 GiB`) to pod-local storage and reducing checkpoint writes to once per epoch produced approximately `8.4` minutes of training and `18` seconds of validation per epoch. The earlier Network Volume-heavy 512 execution reportedly required roughly 40-45 minutes per epoch, but this is not a controlled speed benchmark because both workload and I/O architecture changed.

This run should not be conflated with [experiment 06](../06_binary_mitunet_1024/README.md), which trained and evaluated whole-plan 1024 letterboxes and achieved much stronger validation results.

## Reproducibility Limits

The exact cloud runner package `/workspace/fast1024.zip` was not present in the supplied local paths. Its runtime `prepare.py`, `train.py`, and `io_utils.py` hashes are retained in the original provenance, and [src/README.md](src/README.md) records the source availability audit. All 15 provenance-listed scientific modules under `mitunet_cubicasa/` and `study/core.py` match the local repository byte-for-byte.

The local source repository is at origin commit `6e55b50ab1cf8be9a40eb82efbb8a22b28c8f3c7`; the supplied summary reports later cloud runtime-repair commit `10907a7f6dafcad62a024f12c69b4383586f009d`, which is not present locally. The launch log also records CUDA deterministic-operation warnings because `CUBLAS_WORKSPACE_CONFIG` was not set, so bitwise hardware-migration equivalence is not claimed.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).
