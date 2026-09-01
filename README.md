# Floor Plan AI Experiment Audit

This repository is the initial evidence-backed audit index for the floor-plan segmentation and structure experiments. It records only small, inspectable metadata: Markdown summaries, CSV, YAML, and JSON. Checkpoints, datasets, caches, prediction dumps, and raw outputs remain in their original artifact locations and are not committed here.

Audit date: 2026-08-31.

## Scope

The current audit covers five experiments:

| ID | Experiment | Status | Read next |
| --- | --- | --- | --- |
| 01 | Binary MitUNet baseline | completed | [experiments/01_binary_mitunet/README.md](experiments/01_binary_mitunet/README.md) |
| 02 | Hybrid tiling / 1024 global-patch sweep | completed | [experiments/02_hybrid_tiling/README.md](experiments/02_hybrid_tiling/README.md) |
| 03 | DeepLabV3-ResNet50 comparator | completed | [experiments/03_deeplabv3/README.md](experiments/03_deeplabv3/README.md) |
| 04 | Phase 1 wall structure | completed | [experiments/04_phase1_wall_structure/README.md](experiments/04_phase1_wall_structure/README.md) |
| 05 | Phase 2 boundary and door/openings | completed | [experiments/05_phase2_boundary_openings/README.md](experiments/05_phase2_boundary_openings/README.md) |

The top-level scorecard is [EXPERIMENT_SCOREBOARD.csv](EXPERIMENT_SCOREBOARD.csv), and the source/evidence index is [EXPERIMENT_INDEX.md](EXPERIMENT_INDEX.md).

## Visual Evidence

Curated visual QA evidence is included for all five experiments under each experiment's `qa/` directory. Every QA set uses the same three validation sample identities: `high_quality_architectural/333`, `high_quality_architectural/3015`, and `high_quality_architectural/5559`.

Each sample folder includes a review source image, ground-truth mask(s), prediction mask(s), error overlay(s), and `metadata.json` with source paths and provenance. Experiments 01-04 use regenerated inference from verified checkpoints; Phase 2 prediction masks are derived from saved historical validation probability maps.

Start at [docs/visual_comparisons/shared_validation_samples.md](docs/visual_comparisons/shared_validation_samples.md) for the shared-sample index and [docs/visual_qa_generation_summary.json](docs/visual_qa_generation_summary.json) for the generation summary. Overlay colors are green for true positive, red for false positive, and blue for false negative.

## Evidence Policy

No metric is included unless it was located in a source artifact. Missing or ambiguous values are recorded as `UNKNOWN` in CSV/Markdown and as `null` in JSON. Historical values that were mentioned in planning notes but were not found in the inspected artifacts are not promoted to verified metrics.

## Verified Takeaways

Binary MitUNet is the 512 px wall-mask baseline. Verified best validation IoU is `0.8179796353020612`, best validation Dice is `0.8998776657541074`, and test micro IoU/Dice at threshold `0.10` are `0.8244338473612428` and `0.9037695157362454`.

The hybrid tiling experiment verified the strongest wall-region score in this audit on validation, with IoU `0.8261317505223036` and Dice `0.9047887703458596`. The locked best fusion used `global_weight=1.0` and `patch_weight=0.0`, so it should be interpreted as a positive 1024 px high-resolution global result, not evidence that patch fusion improved the model.

DeepLabV3-ResNet50 completed as an architecture comparator and underperformed the MitUNet baseline. Verified best validation IoU/Dice were `0.7702792714789161` and `0.8702347520969547`.

Phase 1 added wall-region, centerline, and junction heads. Verified validation wall-region IoU/Dice were `0.8208656034763073` and `0.9016212969360846`, centerline clDice was `0.6464444601388634`, junction F1@5 px was `0.769385212829412`, and structural score was `0.7608172018780399`.

Phase 2 added wall-boundary and door-opening heads from the Phase 1 checkpoint. It verified strong final boundary F1@2 px `0.9347893344704645` and door object F1 `0.7796991077953163`, but degraded Phase 1-compatible structural score by `-0.14096779852795083` and wall IoU by `-0.05004927229517453`.

## Open Evidence Gaps

The exact baseline source git commit and DVC hash were not located in the inspected baseline artifacts. Several Phase 1 historical values mentioned in task context were not found in the Phase 1 run reports and are therefore not recorded as verified. Phase 1 and Phase 2 checkpoint SHA-256 hashes are deferred in their manifests, so this repository records checkpoint paths and sizes but not hashes.

## Method Notes

See [docs/methodology.md](docs/methodology.md), [docs/metrics_definitions.md](docs/metrics_definitions.md), and [docs/reproducibility.md](docs/reproducibility.md) for audit rules, metric definitions, and the current reproducibility handoff.
