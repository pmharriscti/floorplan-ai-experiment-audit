# Floor Plan AI Experiment Audit

This repository is the initial evidence-backed audit index for the floor-plan segmentation and structure experiments. It records small, inspectable metadata and a curated set of review images. Checkpoints, datasets, caches, prediction dumps, and bulk raw outputs remain in their original artifact locations and are not committed here.

GitHub repository: [pmharriscti/floorplan-ai-experiment-audit](https://github.com/pmharriscti/floorplan-ai-experiment-audit)

Audit date: 2026-08-31. Updated 2026-09-17 with the RunPod 1024 high-resolution crop treatment, 2026-09-24 with the Phase 5 hierarchical multi-head expansion and the Phase 3A.2 door-opening target ablation, and 2026-09-25 with that ablation's completed 30-epoch evaluation.

## Scope

The current audit covers ten experiments:

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
| 09 | Phase 5 hierarchical multi-head MitUNet 512 | completed | [experiments/09_phase5_hierarchical_multihead_512/README.md](experiments/09_phase5_hierarchical_multihead_512/README.md) |
| 10 | Phase 3A.2 door-opening target ablation, candidate_v3.1 vs candidate_v3.2 (512) | completed | [experiments/10_phase3a2_door_opening_v31_vs_v32_512/README.md](experiments/10_phase3a2_door_opening_v31_vs_v32_512/README.md) |

The top-level scorecard is [EXPERIMENT_SCOREBOARD.csv](EXPERIMENT_SCOREBOARD.csv), and the source/evidence index is [EXPERIMENT_INDEX.md](EXPERIMENT_INDEX.md).

## Visual Evidence

Curated visual QA evidence is included under each experiment's `qa/` directory. Experiments 01-06 and 09 use the same three validation sample identities: `high_quality_architectural/333`, `high_quality_architectural/3015`, and `high_quality_architectural/5559`. Experiment 07 uses its own six representative Adam-vs-AdamW test samples selected by the source evaluation artifacts. Experiment 08 includes four historical composites from its best RunPod checkpoint.

For experiments organized into sample folders, each folder includes a review source image, ground-truth mask(s), prediction mask(s), error overlay(s), and `metadata.json` with source paths and provenance. Experiments 01-04 and 06 use regenerated inference from verified checkpoints; Phase 2 prediction masks are derived from saved historical validation probability maps. Experiment 08 preserves the source run's four-panel composites directly. Experiment 09 decodes its eight heads from the source run's saved thresholded prediction bitmasks. Experiment 10 copies historical images only: Phase 3A.2 three-way label-repair panels, the two special validation-plan diagnostics at both 5 and 30 epochs, and both arms on the three shared sample identities at 30 epochs.

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

Phase 5 extended the 512 px binary baseline into an eight-head hierarchical model (shared MiT-B4 encoder, four task-group decoders, independent sigmoid heads) under a wall-protection gate of baseline minus `0.005` validation IoU. The audited run met the gate on all 26 joint epochs: validation structural-wall IoU `0.8163773956524429` and test `0.8201544454854268` at the selected threshold (`-0.0027` validation and `-0.0044` test versus the reproduced baseline at threshold `0.1`), with boundary F1@2 px `0.9545912416245511`, junction F1@5 px `0.7870734231563665`, door object F1 `0.8802919575908823`, window object F1 `0.8806236251106608`, endpoint F1@5 px `0.33671869601605553`, and fixtures macro IoU `0.45816277648462456`. Three earlier runs of the same design with data augmentation enabled failed the gate on every joint epoch; a wall-only ablation and one-epoch diagnostics traced that regression to fine-tuning the June 2026 baseline under geometric augmentations it was never trained with, not to the new heads, GradNorm, or BatchNorm.

Experiment 10 is the repository's first target-version (label) ablation. Two MitUNet arms were trained from one byte-identical initialization on identical plans in identical order, differing only in the door-opening target version: `candidate_v3.1` (control) against `candidate_v3.2` (treatment). Its target is door openings at `0.4848%` foreground, not walls, so its numbers are not comparable with the wall experiments above. Both arms completed 30 epochs and the full-phase evaluation ran on 2026-09-25 against those checkpoints; both select threshold `0.1`. **The treatment did not improve on the control.** On the 398-plan provisional common subset the control scores micro Dice/IoU `0.811210840` / `0.682384116` and opening-instance F1 `0.896008544`, against the treatment's `0.807523663` / `0.677182128` and `0.888447271`. A paired bootstrap (2,000 resamples, seed 42) puts every macro and micro Dice/IoU interval across zero, so the arms are statistically indistinguishable on pixel metrics; the opening-instance F1 interval excludes zero (`-0.007561273`, CI `[-0.013241644, -0.001232924]`) in the control's favour. That significance separates the two trained models rather than the two label versions: it is measured on plans whose targets are byte-identical, the arms' training labels differ on just 7 of 4,200 masks, and the learning-rate schedules diverged. The 5-epoch probe pointed the other way on both counts, so it did not predict the 30-epoch outcome. On the single differing validation plan the treatment predicts 16 pixels that are all true positives against its own version and all false positives against the other, while the control predicts nothing — a clean demonstration that the label difference is learnable, and no evidence at all about which version is right. Labels remain provisional: the 49-row gold review is 0 resolved. The entry also explains the Phase 3A label-repair lineage it tests, version by version: `candidate_v3` split the door/window symbol from the opening and clipped openings to structural-wall support; `candidate_v3.1` fixed three warning families (symbol geometry used as the opening seed, false or border-collapsed source instances, and openings rejected by wall association in wall gaps); and `candidate_v3.2` re-repaired Family A after v3.1's own fix was found to synthesize a rectangle and snap it to the nearest wall, sometimes the wrong one. Human review overturned three of v3.1's automated "resolved" verdicts, and has so far noted three instances where v3.2 corrected what earlier versions could not — though only one of those is filed as a formal `Correct`, and the v3.2 queue stands at 7 of 44 rows reviewed.

## Open Evidence Gaps

The exact baseline source git commit and DVC hash were not located in the inspected baseline artifacts. The standalone 1024 px run records a source git commit, but its captured git state was dirty. The AdamW harness directory is not a Git repository, though the protected core implementation is clean and commit-pinned. The exact cloud-only Fast1024 runner package was not found locally, although its hashes and matching scientific source modules are documented. Several Phase 1 historical values mentioned in task context were not found in the Phase 1 run reports and are therefore not recorded as verified. Phase 1 and Phase 2 checkpoint SHA-256 hashes are deferred in their manifests, so this repository records checkpoint paths and sizes but not hashes. The Phase 5 code (modules, experiment script, configs) is untracked in the source repository, so its entry records file hashes instead of a clean commit, and its pipeline records no DVC status. Experiment 10's full-run evaluation was executed by the audit rather than by the original run, so that run's own master report still records `Full 30-epoch run executed: false`; its probe project has zero Git commits; its validation labels are unadjudicated, which is what prevents its one significant result from being attributed to the label version; and it records no MLflow run or DVC status.

## Method Notes

See [docs/audit_creation_workflow.md](docs/audit_creation_workflow.md) for the complete audit-creation runbook. Supporting references include [docs/methodology.md](docs/methodology.md), [docs/metrics_definitions.md](docs/metrics_definitions.md), and [docs/reproducibility.md](docs/reproducibility.md).
