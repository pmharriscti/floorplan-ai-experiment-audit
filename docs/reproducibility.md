# Reproducibility Notes

This repository is an audit index, not a runnable copy of the experiment workspace. It intentionally excludes raw data, checkpoints, caches, prediction images, and full outputs.

## Artifact Roots

- Local source repository: `/home/pmharris/dev/mitunet`
- Windows-backed archive root: `/mnt/e/AI_Team`
- CubiCasa5K v4 paths appear in source configs and manifests under `/home/pmharris/dev/cubicasa5k_data/...`

## Reproduction Handoff

1. Use the original `mitunet` source tree at the recorded git commit when available.
2. Restore or mount the artifact roots listed in each experiment's `provenance.json`.
3. Confirm the CubiCasa5K v4 dataset split counts: train `4200`, validation `400`, test `400`.
4. Use the audited `config.yaml` files as compact configuration summaries, then compare against the original source YAML before rerunning.
5. Keep generated checkpoints and outputs outside this audit repo.
6. Recompute metrics with the selected thresholds recorded in each experiment folder.

## DVC And MLflow Status

Phase 1 recorded DVC targets but did not have DVC installed in the run environment. Phase 2 recorded DVC as available and configured, with full `dvc status` intentionally deferred because it walks large external output trees. DeepLabV3 and the Phase experiments recorded MLflow run IDs; baseline and hybrid MLflow status is `UNKNOWN` in this audit.

## Large Artifact Policy

The `.gitignore` blocks common checkpoint, dataset, cache, media, and generated-output patterns. This repo should stay small enough to inspect in a normal code review.

## Recommended Next Build

The next build should add a small validation script that reads `EXPERIMENT_SCOREBOARD.csv` and every experiment `metrics.json`/`provenance.json`, verifies schema consistency, checks links, and confirms no forbidden artifact extensions are staged.

