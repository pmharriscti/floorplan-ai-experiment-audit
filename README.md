# Floor Plan AI Experiment Audit

This repository is the initial evidence-backed audit index for the floor-plan segmentation and structure experiments. It records small, inspectable metadata and a curated set of review images. Checkpoints, datasets, caches, prediction dumps, and bulk raw outputs remain in their original artifact locations and are not committed here.

Audit date: 2026-08-31. Updated 2026-09-17 with the RunPod 1024 high-resolution crop treatment.

## Scope

The current audit covers eight experiments:

| ID | Experiment | Status | Read next |
| --- | --- | --- | --- |
| 01 | Binary MitUNet baseline | completed | [experiments/01_binary_mitunet/README.md](experiments/01_binary_mitunet/README.md) |
| 02 | Hybrid tiling / 1024 global-patch sweep | completed | [experiments/02_hybrid_tiling/README.md](experiments/02_hybrid_tiling/README.md) |
| 03 | DeepLabV3-ResNet50 comparator | completed | [experiments/03_deeplabv3/README.md](experiments/03_deeplabv3/README.md) |
| 04 | Phase 1 wall structure | completed | [experiments/04_phase1_wall_structure/README.md](experiments/04_phase1_wall_structure/README.md) |
| 05 | Phase 2 boundary and door/openings | completed | [experiments/05_phase2_boundary_openings/README.md](experiments/05_phase2_boundary_openings/README.md) |
| 06 | Binary MitUNet 1024 px global | completed | [experiments/06_binary_mitunet_1024/README.md](experiments/06_binary_mitunet_1024/README.md) |
| 07 | MitUNet 512 AdamW optimizer comparator | completed | [experiments/07_mitunet_512_adamw/README.md](experiments/07_mitunet_512_adamw/README.md) |
| 08 | MitUNet 1024 high-resolution crop treatment on RunPod | completed | [experiments/08_mitunet_1024_highres_runpod/README.md](experiments/08_mitunet_1024_highres_runpod/README.md) |

The top-level scorecard is [EXPERIMENT_SCOREBOARD.csv](EXPERIMENT_SCOREBOARD.csv), and the source/evidence index is [EXPERIMENT_INDEX.md](EXPERIMENT_INDEX.md).

## Visual Evidence

Curated visual QA evidence is included under each experiment's `qa/` directory. Experiments 01-06 use the same three validation sample identities: `high_quality_architectural/333`, `high_quality_architectural/3015`, and `high_quality_architectural/5559`. Experiment 07 uses its own six representative Adam-vs-AdamW test samples selected by the source evaluation artifacts. Experiment 08 includes four historical composites from its best RunPod checkpoint.

For experiments organized into sample folders, each folder includes a review source image, ground-truth mask(s), prediction mask(s), error overlay(s), and `metadata.json` with source paths and provenance. Experiments 01-04 and 06 use regenerated inference from verified checkpoints; Phase 2 prediction masks are derived from saved historical validation probability maps. Experiment 08 preserves the source run's four-panel composites directly.

Start at [docs/visual_comparisons/shared_validation_samples.md](docs/visual_comparisons/shared_validation_samples.md) for the shared-sample index, [docs/visual_comparisons/adamw_optimizer_samples.md](docs/visual_comparisons/adamw_optimizer_samples.md) for the AdamW comparator, and [docs/visual_comparisons/runpod_1024_highres_samples.md](docs/visual_comparisons/runpod_1024_highres_samples.md) for the RunPod crop treatment. Overlay colors are green for true positive, red for false positive, and blue for false negative.

## Evidence Policy

No metric is included unless it was located in a source artifact. Missing or ambiguous values are recorded as `UNKNOWN` in CSV/Markdown and as `null` in JSON. Historical values that were mentioned in planning notes but were not found in the inspected artifacts are not promoted to verified metrics.

## Verified Takeaways

Binary MitUNet is the 512 px wall-mask baseline. Verified best validation IoU is `0.8179796353020612`, best validation Dice is `0.8998776657541074`, and test micro IoU/Dice at threshold `0.10` are `0.8244338473612428` and `0.9037695157362454`.

The hybrid tiling experiment verified the strongest wall-region score in this audit on validation, with IoU `0.8261317505223036` and Dice `0.9047887703458596`. The locked best fusion used `global_weight=1.0` and `patch_weight=0.0`, so it should be interpreted as a positive 1024 px high-resolution global result, not evidence that patch fusion improved the model.

DeepLabV3-ResNet50 completed as an architecture comparator and underperformed the MitUNet baseline. Verified best validation IoU/Dice were `0.7702792714789161` and `0.8702347520969547`.

The standalone 1024 px Binary MitUNet run improved over the 512 px baseline, with best validation IoU/Dice `0.8259883607445844` and `0.904702766459881`; test micro IoU/Dice at threshold `0.10` were `0.8317579184170079` and `0.9081526658673402`.

The 512 px AdamW optimizer comparator regressed versus the Adam control: test micro IoU/Dice were `0.8206001227094942` and `0.9014611308366193`, with deltas of `-0.0038337246517485823` IoU and `-0.002308384899626148` Dice. Because configured `weight_decay=0.0`, this does not test nonzero decoupled weight decay.

The RunPod 1024 crop treatment completed 10 epochs on an A100 80GB, with best validation IoU/Dice of `0.43214381550960096` and `0.6034922063407869` at epoch 3. It underperformed the supplied 512 whole-plan control, but the comparison changed both resolution and spatial context. Pod-local data staging and epoch-level checkpointing reduced the measured training portion to about `8.4` minutes per epoch.

Phase 1 added wall-region, centerline, and junction heads. Verified validation wall-region IoU/Dice were `0.8208656034763073` and `0.9016212969360846`, centerline clDice was `0.6464444601388634`, junction F1@5 px was `0.769385212829412`, and structural score was `0.7608172018780399`.

Phase 2 added wall-boundary and door-opening heads from the Phase 1 checkpoint. It verified strong final boundary F1@2 px `0.9347893344704645` and door object F1 `0.7796991077953163`, but degraded Phase 1-compatible structural score by `-0.14096779852795083` and wall IoU by `-0.05004927229517453`.

## Open Evidence Gaps

The exact baseline source git commit and DVC hash were not located in the inspected baseline artifacts. The standalone 1024 px run records a source git commit, but its captured git state was dirty. The AdamW harness directory is not a Git repository, though the protected core implementation is clean and commit-pinned. The exact cloud-only Fast1024 runner package was not found locally, although its hashes and matching scientific source modules are documented. Several Phase 1 historical values mentioned in task context were not found in the Phase 1 run reports and are therefore not recorded as verified. Phase 1 and Phase 2 checkpoint SHA-256 hashes are deferred in their manifests, so this repository records checkpoint paths and sizes but not hashes.

## Method Notes

See [docs/methodology.md](docs/methodology.md), [docs/metrics_definitions.md](docs/metrics_definitions.md), and [docs/reproducibility.md](docs/reproducibility.md) for audit rules, metric definitions, and the current reproducibility handoff.
