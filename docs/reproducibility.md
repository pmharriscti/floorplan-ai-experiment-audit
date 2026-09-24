# Reproducibility Notes

This repository is an audit index, not a runnable copy of the experiment workspace. It intentionally excludes raw data, checkpoints, caches, prediction images, and full outputs.

## Artifact Roots

- Local source repository: `/home/pmharris/dev/mitunet`
- RunPod crop-treatment source repository: `/home/pmharris/dev/mitunet_uniform_1024_crop`
- Windows-backed archive root: `/mnt/e/AI_Team`
- CubiCasa5K v4 paths appear in source configs and manifests under `/home/pmharris/dev/cubicasa5k_data/...`
- Phase 5 layout under `/mnt/e/AI_Team/mitunet`: runs in `experiments/mitunet_hierarchical_multihead_512/<run_id>/{checkpoints,logs,metrics,predictions,masks,overlays,label_validation,audit,artifacts}`, generated targets in `targets/mitunet_hierarchical_multihead_512`, split manifests in `derived_data/mitunet_hierarchical_multihead_512/manifests/<run_id>`, MLflow in `mlflow/mlflow.db`; Phase 1 and Phase 2 caches are reused by reference.

## Reproduction Handoff

1. Use the original `mitunet` source tree at the recorded git commit when available.
2. Restore or mount the artifact roots listed in each experiment's `provenance.json`.
3. Confirm the CubiCasa5K v4 dataset split counts: train `4200`, validation `400`, test `400`.
4. Use the audited `config.yaml` files as compact configuration summaries, then compare against the original source YAML before rerunning.
5. Keep generated checkpoints and outputs outside this audit repo.
6. Recompute metrics with the selected thresholds recorded in each experiment folder.
7. For experiment 08, restore the exact `fast1024.zip` runner from RunPod and verify its files against the preserved provenance hashes before claiming an exact rerun.
8. For experiment 09, verify the untracked Phase 5 source files against the SHA-256 values in its `provenance.json`, run with `data.augmentation: false` and `--weighting fixed`, and expect one host-independent difference: the audited run was resumed once from `last.pth` after epoch 15.
9. Any fine-tune that starts from the experiment 01 checkpoint must not enable the repository's current geometric augmentations (flips, 90-degree rotations); the baseline was not trained with them and regresses 3-5 IoU points within one epoch when it is fine-tuned under them (experiment 09 root-cause diagnostics).

## DVC And MLflow Status

Phase 1 recorded DVC targets but did not have DVC installed in the run environment. Phase 2 recorded DVC as available and configured, with full `dvc status` intentionally deferred because it walks large external output trees. DeepLabV3 and the Phase experiments recorded MLflow run IDs; baseline and hybrid MLflow status is `UNKNOWN` in this audit. Phase 5 records an MLflow run ID in the shared `mlflow/mlflow.db` and writes no DVC status.

## Large Artifact Policy

The `.gitignore` blocks common checkpoint, dataset, cache, media, and generated-output patterns. This repo should stay small enough to inspect in a normal code review.

## Recommended Next Build

The next build should add a small validation script that reads `EXPERIMENT_SCOREBOARD.csv` and every experiment `metrics.json`/`provenance.json`, verifies schema consistency, checks links, and confirms no forbidden artifact extensions are staged.
