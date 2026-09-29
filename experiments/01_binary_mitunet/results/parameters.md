# Parameters: full_gpu

- Run directory: `/home/pmharris/dev/mitunet/experiments/cubicasa5k_mitunet/full_gpu`
- Source checkpoint: `/home/pmharris/dev/mitunet/experiments/cubicasa5k_mitunet/full_gpu/best_model.pth`
- Model: `MitUNet` with `mit_b4` encoder
- Model parameters: `64,250,658`
- Checkpoint epoch: `29`
- Checkpoint threshold: `0.1`

## Training

- Epochs: `30` configured, `30` logged
- Optimizer: `adam`
- Learning rate: `0.0001`
- Weight decay: `0.0`
- Batch size: `4` physical, `4` effective
- AMP active: `True`
- Seed: `42`
- Early stopping: `val_iou`, patience `8`, min delta `0.0`
- Scheduler patience: `3`

## Data And Preprocessing

- Data root: `/home/pmharris/dev/cubicasa5k_data`
- Cache dir: `artifacts/cubicasa5k_wall_cache`
- Image/input size: `512`
- Resize mode: `letterbox`
- Augmentation: `True`
- Subtract openings: `False`

## Loss And Selection

- Loss: `AsymmetricTverskyLoss`
- Tversky alpha/beta: `0.6` / `0.4`
- Configured threshold: `0.5`
- Threshold search enabled: `True`

## Best Logged Metrics

- Best validation IoU: epoch `29`, IoU `0.817980`, Dice `0.899878`, val loss `0.101225`
- Final epoch: epoch `30`, IoU `0.816274`, Dice `0.898844`, val loss `0.101535`

## Environment

- Device: `cuda`
- GPU: `NVIDIA RTX PRO 3000 Blackwell Generation Laptop GPU`
- Torch: `2.12.0+cu130`
- CUDA: `13.0`
- Python executable: `/home/pmharris/dev/mitunet/.venv/bin/python`
