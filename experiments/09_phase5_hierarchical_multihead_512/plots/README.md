# Plots - Phase 5 hierarchical multi-head MitUNet 512

[joint_phase_wall_iou_and_score.png](joint_phase_wall_iou_and_score.png): per-epoch validation structural-wall IoU at the baseline threshold (top) and validation hierarchical score (bottom) for the audited no-augmentation run and the two earlier augmentation-on runs of the same design (GradNorm weighting; fixed weighting). The grey band marks the four heads-only warm-up epochs, the dashed line the reproduced baseline (`0.8188`), and the dotted line the wall-gate floor (`0.8138`).

The plot was drawn by the audit from the copied training histories in [../results/training_history.csv](../results/training_history.csv) and [../results/related_runs/](../results/related_runs/). It contains no values that are not in those CSV files.
