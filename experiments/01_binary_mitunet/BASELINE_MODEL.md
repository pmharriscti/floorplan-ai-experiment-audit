# Baseline model: binary MitUNet, 512 px

Reference description of the baseline neural network of this audit. Figures come from the run's own records,
copied under [results/](results/). Code is under [code/](code/), with the limits stated in [code/README.md](code/README.md).

## Task

Binary segmentation of walls in floor-plan images. One output channel. Each pixel is wall or not wall.
Door and window openings are not subtracted from the wall target.

## Network

| Item | Value |
| --- | --- |
| Architecture | U-Net style encoder-decoder ("MitUNet") |
| Library | `segmentation_models_pytorch` 0.5.0 |
| Encoder | MiT-B4 (Mix Transformer, SegFormer family), ImageNet weights |
| Decoder | U-Net decoder with SCSE attention |
| Input | RGB, 512 x 512 |
| Output | 1 channel, raw logits; sigmoid and threshold are applied afterwards |
| Trainable parameters | 64,248,664 |
| Parameters plus buffers | 64,250,658 (the figure recorded in `parameters.json`) |

## Data

| Item | Value |
| --- | --- |
| Dataset | CubiCasa5K, version 4 |
| Split | train 4,200, validation 400, test 400 |
| Image | `F1_scaled.png` of each sample |
| Target | wall polygons from the dataset's SVG annotations |
| Resize | letterbox to 512 (longest side scaled, then padded) |
| Normalisation | ImageNet mean and standard deviation |
| Augmentation | recorded as on; the operations applied are **not recorded** |

## Training

| Item | Value |
| --- | --- |
| Loss | asymmetric Tversky, alpha 0.6, beta 0.4 |
| Optimiser | Adam, learning rate 0.0001, weight decay 0 |
| Schedule | learning rate reduced on plateau, patience 3; it ended at 2.5e-05 |
| Batch size | 4 |
| Epochs | 30 configured, 30 run |
| Early stopping | on validation IoU, patience 8; not triggered |
| Mixed precision | on |
| Seed | 42 |
| Hardware | NVIDIA RTX PRO 3000 Blackwell Generation Laptop GPU, 12 GB |
| Software | Python 3.12.3, torch 2.12.0, albumentations 2.0.8 |
| Duration | 3.0 hours |
| Date | 2026-06-25 |

Per-epoch values are in [results/training_history.csv](results/training_history.csv).

## Results

| Measure | Value |
| --- | --- |
| Best validation IoU | 0.8180, at epoch 29 |
| Best validation Dice | 0.8999 |
| Selected threshold | 0.10, chosen on the validation split |
| Test IoU at 0.10 (micro) | 0.8244 |
| Test Dice at 0.10 (micro) | 0.9038 |

The threshold was selected on validation data and then applied to the test split once.
Full values are in [metrics.json](metrics.json) and the copied run files.

## Checkpoint

Not in this repository. Path `/home/pmharris/dev/mitunet/experiments/cubicasa5k_mitunet/full_gpu/best_model.pth`, SHA-256 `fb9665056aa06057a571f247882ba5d32abde297215f2ae94d210759f540b72f`.
The hash was recomputed from the file on 2026-09-29 and equals the value already recorded in this audit.

## Role in later experiments

- Experiment 03 (DeepLabV3) is compared with it.
- Experiment 04 names it as its baseline parent.
- Experiment 09 is initialised from its checkpoint and uses its reproduced validation IoU, 0.8188, as the
  wall-protection gate.

## Known limits

- **The training code is not identified.** No commit was recorded for the run. See [code/README.md](code/README.md).
- **The augmentation is not recorded.** Any fine-tune from this checkpoint should follow the note in
  [docs/reproducibility.md](../../docs/reproducibility.md).
- **One dataset.** All figures are on CubiCasa5K. Nothing is claimed for other drawings.
- **Pixel metrics only.** No boundary, centreline or junction metric exists for this run.
- **The run was not repeated.** One seed, no variance estimate.
