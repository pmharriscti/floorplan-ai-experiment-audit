# Phase 3A.2 Door-Opening Target Ablation: candidate_v3.1 vs candidate_v3.2 (512)

**EXPLORATORY — NOT HUMAN-GOLD VALIDATED.**

This is a label experiment, not a model experiment. Both arms are the same MitUNet, from one byte-identical initialization, trained on the same plans in the same order. The only intended free variable is the door-opening target generator version: arm A trains on `candidate_v3.1` masks, arm B on `candidate_v3.2`. The question is whether the v3.2 target repair produces a better model than v3.1 on a shared validation set.

Two things frame everything below. First, the two label versions differ on **8 of 4,600 masks** (1 of them in validation), so the experiment has very little to measure. Second, the 30-epoch training completed for both arms but **its evaluation stage was never run**, so no threshold-selected final evaluation, per-plan metrics or confidence intervals exist for the full phase.

This experiment does **not** predict walls. Its target is door openings at `0.4848%` foreground, against the `01` baseline's wall target at `8.43%`. Its IoU is not comparable with any wall IoU in this repository, and the source design says so explicitly: the historical wall checkpoint is audit evidence only and was never used to initialize this experiment.

## Source Evidence

Training run: `/mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC`

Preparation and target-materialization run: `/mnt/e/AI_Team/mitunet/phase3a2_door_opening_512_ablation/phase3a2_v31_vs_v32_door_opening_512_20260903_152401_UTC`

Primary evidence files:

- `full/{A,B}/training_history.csv` and `training_status.json` (copied under [results/](results/)) — the only full-run metrics that exist
- `full_run.log` — records the arm A `--resume` finalize and the arm B run
- `PHASE3A2_SHARED_INIT_PROBE_REPORT.md` (copied to [results/source_PHASE3A2_SHARED_INIT_PROBE_REPORT.md](results/source_PHASE3A2_SHARED_INIT_PROBE_REPORT.md)) — the completed 5-epoch probe
- `evaluation/arm_comparison.csv`, `evaluation/threshold_sweep.csv` (copied under [results/](results/))
- `audits/config_difference.json`, `audits/common_validation_subset_audit.json`, `audits/common_validation_exclusions.csv`
- `shared_initialization/shared_initialization_verification.json`
- `diagnostics/probe/changed_instance_metrics.json`, `diagnostics/probe/vanished_instance_metrics.json`
- Target-repair lineage reports from the three Phase 3A runs, copied under [results/label_repair_lineage/](results/label_repair_lineage/)

## The Target Repair Being Tested

`candidate_v3.2` differs from `candidate_v3.1` by one generator flag, `repair_door_opening_tangent_normal_semantics`, plus a 15-degree axis tolerance and an explicit instance list. The lineage:

| Phase | Version | What changed | Result |
| --- | --- | --- | --- |
| 3A | `candidate_v3` | Separated door/window **symbol** from **opening**; derived openings only after wall association and clipped them to structural-wall support. Inventoried 318 raw source classes over 5,000 samples, 153 needing review. | `blocked` at human review |
| 3A.1 | `candidate_v3.1` | Clustered 84 warnings across 32 plans into three families — A: door leaf/swing symbol geometry used as the opening seed; B: false, malformed or border-collapsed source instances; C: genuine openings rejected because association demanded direct wall overlap and failed in wall gaps. 42 resolved, 2 excluded, 16 unchanged, 24 insufficient evidence. | `blocked` at human review |
| 3A.2 | `candidate_v3.2` | Re-repaired Family A. v3.1 had inferred wall orientation by PCA over nearby wall pixels, synthesized a rectangle and snapped it to the nearest wall — which near corners, stacked doors and borders can select a nearby or perpendicular wall. v3.2 instead takes the source Door threshold polygon and its parent Wall polygon as the tangent/normal evidence. 10 instances, 10 tangent-aligned, 0 normal-aligned, 0 placed on the wrong wall. | `blocked` at human review |

The audit explicitly ruled out a global 90-degree tangent/normal inversion and any row/column parser bug in the generator. The defect was host-wall inference and provenance. A separate flat-vs-nested bbox parsing bug existed in the review UI and had been hiding bbox values from the reviewer.

**Human review overturned v3.1's own verdicts.** [results/label_repair_lineage/superseding_human_findings_v3_1.csv](results/label_repair_lineage/superseding_human_findings_v3_1.csv) records three instances v3.1 reported as "Resolved: valid opening generated correctly" that a reviewer marked `Critical issue`: `10543/door_0003` ("added foreground at the wrong location/orientation rather than at the true source doorway"), `10620/door_0005` ("source SVG shows an exterior door in the bottom horizontal wall; candidate_v3.1 adds a vertical segment") and `11709/door_0013` ("adds foreground that does not correspond to an architectural opening"). That is the justification for v3.2, and it is why "resolved by the repair path" is not treated as evidence of correctness in this pipeline.

The 10 repaired Family A instances span exactly 8 plans, and those are exactly the 8 masks that differ between the two arms.

## Verified Controls

All passed, and they are stronger than the baseline protocol requires:

| Control | Result |
| --- | --- |
| Config difference | `PASS` — only `experiment_name`, `output_directory`, `target_manifest`, `target_version` differ |
| Shared initialization | `SHARED_INITIALIZATION_PASS` — both arms load model tensor hash `5fc4586a...`; optimizer, scheduler, GradScaler, RNG state and starting LR all identical |
| Data order and augmentation | `PASS` — per-epoch order and augmentation SHA-256 match across arms |
| Preflight | `PREFLIGHT_PASS` |
| Target integrity | `PASS` — 18,400 mask files, 9,200 manifest rows, binary values, 512x512; 0 unexpected changes outside the declared repair scope |
| Splits | `EXACT_BASELINE_SPLITS_RECOVERED` — 4200/400/400, ordered hashes match the baseline |
| Test isolation | test manifest and content never accessed |

Checkpoint integrity was re-verified by this audit: all four full-run checkpoints hash to the values recorded in `training_status.json`, and their stored epoch numbers are 30 (A best), 30 (A last), 28 (B best) and 30 (B last).

## Verified Metrics

### 30-epoch run — training history only

No evaluation stage was run, so these are best-epoch values read from `training_history.csv` at the **fixed** threshold `0.5` (not validation-selected) on the 398-plan provisional common subset.

| | A (`candidate_v3.1`) | B (`candidate_v3.2`) | B − A |
| --- | ---: | ---: | ---: |
| Best epoch | 30 | 28 | |
| Dice @ 0.5 | `0.810702838491235` | `0.8066504533142688` | `-0.0040523851769662` |
| IoU @ 0.5 | `0.6816654951591425` | `0.6759548830890035` | `-0.005710612070139` |
| Validation loss | `0.1912420242276024` | `0.1911806437238377` | `-0.0000613805037647` |
| Wall-clock | 3.76 h | 3.56 h | |

Arm A finishes ahead on Dice and IoU; the arms are tied on loss to five decimal places. Neither arm early-stopped and arm A was still improving at the 30-epoch cap.

The per-epoch record does not support reading that gap as an effect. **B led on 17 of 30 epochs, A on 13.** Mean `B − A` IoU over the last ten epochs is `+0.001089`, i.e. B is marginally ahead late in training while A happens to be ahead at its single best epoch. The standard deviation of the per-epoch `B − A` IoU is `0.081015`, roughly 14 times the final `0.0057` gap.

Arm B's first epoch collapsed to IoU `0.0354` and recovered fully by epoch 2, from a byte-identical initialization and identical data order — the same behaviour seen in the probe, attributable to AMP/kernel nondeterminism.

### 5-epoch probe — the only completed evaluation

`FIVE_EPOCH_PROBE_COMPLETE`. Selected thresholds A `0.5`, B `0.3`. The arms split the metric set almost evenly: B is ahead on macro Dice (`+0.004988`), macro IoU (`+0.005386`), opening-instance F1 (`+0.005482`), precision and validation loss; A is ahead on micro Dice (`+0.001021`), micro IoU (`+0.001335`), recall, fragmentation and merge rate. Neither arm produced empty predictions.

Paired plan bootstrap, 2,000 resamples, seed 42, on the 398-plan common subset:

| Metric | B − A delta | 95% CI |
| --- | ---: | --- |
| macro Dice | `0.004987979778471606` | `[0.00010094944756597308, 0.00950762899987806]` |
| macro IoU | `0.005385877710282746` | `[0.000006518135761461555, 0.01125299372704522]` |

Both intervals exclude zero, but their lower bounds sit essentially **on** zero (`1.0e-04` and `6.5e-06`). The bootstrap covers macro Dice and macro IoU only — micro metrics and instance F1 have no intervals in any phase. This marginal 5-epoch advantage for v3.2 did not persist: at 30 epochs the fixed-threshold pixel metrics favour v3.1.

### The two plans that actually distinguish the label versions

`high_quality_architectural/8690` is the **only** validation plan whose v3.1 and v3.2 targets differ (628 changed pixels, inter-version mask IoU `0.911`). At 5 epochs **both arms predicted zero positive pixels on it**, against both references — 70 false negatives, 0 true positives, Dice `0.0` for every combination. The source diagnostic labels it `PROVISIONAL_DIAGNOSTIC_NO_WINNER` with `target_correctness_decision: null`. The single instance that carries the experimental variable into validation contributed no discriminating signal at all.

`high_quality_architectural/5981` is a 512 target-survivability failure: the opening vanishes during the verified 512 conversion in **both** versions (20 reference positive pixels in the ROI each). Arm A predicts nothing there (max probability `0.00027`); arm B predicts 46 pixels (max probability `1.0`). It is excluded from primary positive-instance metrics and was neither dilated nor restored.

## Visual QA

[qa/README.md](qa/README.md) holds three sets of historical images, all copied — this audit performed no training and no inference:

- **Label repair** — five three-way panels from the Phase 3A.2 run showing source evidence, `candidate_v3.1` and `candidate_v3.2` side by side, including the one differing validation plan and two instances a reviewer later marked as v3.1 failures.
- **Model diagnostics** — the changed and vanished validation instances with both arms' 5-epoch predictions.
- **Shared samples** — both arms on `high_quality_architectural/333`, `3015` and `5559`, the same identities used by experiments 01-06 and 09.

## Interpretation

This is an inconclusive label-version ablation. It is recorded as evidence of process, not as a result that ranks the two target versions.

The design is unusually well controlled — shared initialization down to the RNG state, per-epoch data-order hashes, a frozen threshold rule, and a sealed test split. The problem is not the protocol, it is the effect size. With 8 of 4,600 masks differing, 1 of them in validation, and that one instance predicted as empty by both arms, the experiment cannot separate the target version from ordinary training variation. The 5-epoch probe gives v3.2 a marginal macro-metric edge whose confidence intervals touch zero; the 30-epoch run reverses the sign on the fixed-threshold pixel metrics. Neither observation survives the per-epoch variance.

A confounder compounds this: the two `ReduceLROnPlateau` schedules diverged. Both dropped `1e-4` → `5e-5` at epoch 24, but arm A received a second reduction to `2.5e-5` at epoch 29 that arm B never got, and A's best epoch is 30 — two epochs later, including its largest late-run jump. That is legitimate scheduler behaviour responding to each arm's own validation curve, not a protocol break, but the final A-vs-B gap cannot be attributed to the target version alone.

The Phase 3A lineage is the more useful finding here. The repairs are real and specific, the v3.2 Family A geometry audit is clean on all 10 instances, and the human superseding findings demonstrate that automated "resolved" verdicts in this pipeline were wrong 3 times out of 9. What the lineage has not yet produced is adjudicated labels: the Phase 3A gate stands at 0 of 105,000 rows reviewed, and this ablation's own 49-row gold queue at 0 resolved.

## Missing Evidence and Non-Claims

- **The full-run evaluation does not exist.** No threshold sweep, per-plan metrics, macro/instance/boundary metrics or paired bootstrap for the 30-epoch checkpoints. The source run's master report still records `Full 30-epoch run executed: false`, and its `evaluation/` directory dates from the probe.
- The full-run figures above are training-history values at a fixed threshold, not a threshold-selected final evaluation. They are not interchangeable with the selected-checkpoint evaluations reported for experiments 01-09.
- Validation labels are provisional. The 49-row gold review is 0 resolved, so nothing here can promote `candidate_v3.2`, authorize production, or establish which of the two versions is correct on `8690`.
- No test metrics. The test split was never loaded, scored, visualized or predicted, by design.
- The probe project is a git repository with **zero commits**; the run report records `Git HEAD: None`. No code commit identifies the full run.
- Arm A was relaunched with `--resume` after its 30 epochs had already finished, to repair its best checkpoint and write the final status. Its recorded `completed_at_utc` is the finalize time, not the end of training.
- No MLflow run and no DVC status are recorded by this project, unlike Phase 1 and Phase 2.
- The curated QA images support visual diagnosis only.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).
