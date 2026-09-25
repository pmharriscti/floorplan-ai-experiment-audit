# Phase 3A.2 Door-Opening Target Ablation: candidate_v3.1 vs candidate_v3.2 (512)

**EXPLORATORY — NOT HUMAN-GOLD VALIDATED.**

This is a label experiment, not a model experiment. Both arms are the same MitUNet, from one byte-identical initialization, trained on the same plans in the same order. The only intended free variable is the door-opening target generator version: arm A trains on `candidate_v3.1` masks, arm B on `candidate_v3.2`. The question is whether the v3.2 target repair produces a better model than v3.1 on a shared validation set.

Both arms completed 30 epochs, and the full-phase evaluation was executed on 2026-09-25 against the existing checkpoints — no retraining. The answer is that **candidate_v3.2 did not improve on candidate_v3.1**. On pixel metrics the two are statistically indistinguishable; on opening-instance F1 the control is ahead by a margin whose confidence interval excludes zero. The framing caveat is that the two label versions differ on only **8 of 4,600 masks** (1 of them in validation), so the experiment has very little label signal to measure.

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

### 30-epoch evaluation — the headline result

Executed 2026-09-25 with `evaluate_exploratory.py --phase full` against the existing checkpoints (A epoch 30, B epoch 28). Status `PASS`, test split never touched. Both arms select threshold **`0.1`** — the same operating point the `01` wall baseline selected, and not the `0.5` used during training. The sweep declines monotonically from `0.1` to `0.9` for both arms.

Common 398-plan subset, each arm at its selected threshold:

| Metric | A (`candidate_v3.1`) | B (`candidate_v3.2`) | B − A |
| --- | ---: | ---: | ---: |
| micro Dice | `0.811210840` | `0.807523663` | `-0.003687177` |
| micro IoU | `0.682384116` | `0.677182128` | `-0.005201988` |
| macro Dice | `0.803946173` | `0.801972066` | `-0.001974107` |
| macro IoU | `0.688315583` | `0.685842789` | `-0.002472794` |
| precision | `0.840109879` | `0.847648341` | `+0.007538462` |
| recall | `0.784233885` | `0.771026015` | `-0.013207870` |
| opening-instance precision | `0.906537007` | `0.891992551` | `-0.014544456` |
| opening-instance recall | `0.885721826` | `0.884930061` | `-0.000791766` |
| **opening-instance F1** | **`0.896008544`** | **`0.888447271`** | **`-0.007561273`** |
| boundary F1 | `0.849638093` | `0.847837266` | `-0.001800827` |
| fragmentation rate | `0.004222750` | `0.005542359` | `+0.001319609` |
| merge rate | `0.000810373` | `0.002128226` | `+0.001317853` |
| validation loss | `0.191241787` | `0.191180605` | `-0.000061182` |
| empty-prediction rate | `0.000000000` | `0.000000000` | `0.000000000` |

The control leads on every aggregate quality metric except precision and validation loss. The treatment is more precise but less complete, and it fragments and merges more.

### Significance

Paired plan bootstrap, 2,000 resamples, seed 42. The run's built-in bootstrap covers macro Dice and macro IoU; the audit added micro Dice, micro IoU and opening-instance F1 in [results/full_supplementary_bootstrap.json](results/full_supplementary_bootstrap.json), using an aggregation that reproduces the evaluator's own reported values exactly.

| Metric (common subset) | B − A | 95% CI | Excludes zero |
| --- | ---: | --- | --- |
| macro Dice | `-0.001974107` | `[-0.005968093, +0.001871868]` | no |
| macro IoU | `-0.002472794` | `[-0.007683295, +0.002519650]` | no |
| micro Dice | `-0.003687177` | `[-0.007528662, +0.000244651]` | no |
| micro IoU | `-0.005201988` | `[-0.010508753, +0.000346231]` | no |
| **opening-instance F1** | `-0.007561273` | `[-0.013241644, -0.001232924]` | **yes** |

**On pixel metrics the two arms are statistically indistinguishable.** All four Dice/IoU intervals straddle zero, on all three references. The opening-instance F1 interval excludes zero on all three references (common subset, REFERENCE_V31 `[-0.013967, -0.001831]`, REFERENCE_V32 `[-0.013549, -0.001621]`), favouring the control.

That significance must be read carefully. The common subset contains only plans whose two targets are byte-identical, and the arms' training labels differ on 7 of 4,200 training masks. A significant difference measured there separates the two trained **models**, not the two **label versions**. The diverged learning-rate schedules are a second confounder.

This also reverses the probe. At 5 epochs the treatment held a marginal macro-metric advantage (macro Dice `+0.004988`, macro IoU `+0.005386`, intervals barely excluding zero) and a better instance F1 (`0.837424` vs `0.831942`). At 30 epochs both signs flip and the instance-F1 advantage belongs to the control. A 5-epoch probe did not predict the 30-epoch outcome here.

### 5-epoch probe

`FIVE_EPOCH_PROBE_COMPLETE`, selected thresholds A `0.5`, B `0.3`. Retained in [metrics.json](metrics.json) as the infrastructure and learnability gate it was designed to be. Its numbers should not be quoted as the experiment's result.

### The two plans that carry the label difference

`high_quality_architectural/8690` is the **only** validation plan whose v3.1 and v3.2 targets differ. At 30 epochs, at threshold `0.1`:

| Arm | vs candidate_v3.1 | vs candidate_v3.2 |
| --- | --- | --- |
| A (`candidate_v3.1`) | 0 TP, 0 FP, 70 FN — Dice `0.0` | 0 TP, 0 FP, 70 FN — Dice `0.0` |
| B (`candidate_v3.2`) | 0 TP, **16 FP**, 70 FN — Dice `0.0` | **16 TP**, 0 FP, 54 FN — Dice `0.372093`, IoU `0.228571` |

The treatment arm places 16 pixels on this instance, and **every one of them is a true positive against its own label version and a false positive against the other**, while the control arm still predicts nothing there. The label difference is learnable and the model followed its training labels exactly where the two versions disagree. It does **not** establish which version is correct — each arm is scored against the labels it was trained on. The source diagnostic still records `PROVISIONAL_DIAGNOSTIC_NO_WINNER` with `target_correctness_decision: null`. Only the human gold review can settle it.

`high_quality_architectural/5981` is the 512 survivability failure, where the opening vanishes from the target in **both** versions (20 reference pixels in the ROI). At 5 epochs arm A predicted nothing there. At 30 epochs **both arms predict it confidently** — 39 and 35 pixels, maximum probability `1.0` each. The models recover an opening the 512 target pipeline lost. That is evidence about the target pipeline, not about either label version. The plan stays excluded from primary positive-instance metrics and was neither dilated nor restored.

## Visual QA

[qa/README.md](qa/README.md) holds three sets of historical images, all copied — this audit performed no training and no inference:

- **Label repair** — five three-way panels from the Phase 3A.2 run showing source evidence, `candidate_v3.1` and `candidate_v3.2` side by side, including the one differing validation plan and two instances a reviewer later marked as v3.1 failures.
- **Model diagnostics** — the changed and vanished validation instances with both arms' 5-epoch predictions.
- **Shared samples** — both arms on `high_quality_architectural/333`, `3015` and `5559`, the same identities used by experiments 01-06 and 09.

## Interpretation

`candidate_v3.2` did not beat `candidate_v3.1`. With the evaluation now complete, the defensible statement is: indistinguishable on pixel quality, and measurably behind on opening-instance F1 by about `0.0076` with an interval that excludes zero. Nothing here supports promoting v3.2 on model performance.

What the experiment cannot do is attribute that to the target version. The significant instance-F1 gap is measured over 398 plans whose targets are byte-identical in both arms; the arms' training data differs on 7 masks out of 4,200. Two training runs that differ that little can still differ by this much, and the arms' `ReduceLROnPlateau` schedules did diverge — arm A took a second reduction at epoch 29 that arm B never got, and arm A's best epoch is 30. The clean reading is that these are two samples from the same distribution of training outcomes, and the label version is not visibly moving that distribution.

The one place the label variable is directly visible is `8690`, and it behaves exactly as designed: the treatment model learned its own version's geometry, pixel for pixel. That is a working experiment with a real but unadjudicated signal, waiting on human review rather than on more compute.

The Phase 3A lineage remains the more substantive contribution. The repairs are specific and the v3.2 Family A geometry audit is clean on all 10 instances, while the human superseding findings show automated "resolved" verdicts in this pipeline were wrong 3 times out of 9. The bottleneck is adjudication: the Phase 3A gate stands at 0 of 105,000 rows reviewed, and this ablation's 49-row gold queue at 0 resolved.

## Missing Evidence and Non-Claims

- The full-run evaluation was executed by the audit on 2026-09-25, after the entry was first published. The source run's own master report still records `Full 30-epoch run executed: false`, and its top-level `evaluation/` directory is still the probe's; the full-phase artifacts live under `full/` and `diagnostics/full/`.
- The significant opening-instance F1 difference separates the two trained models, not the two label versions: it is measured on plans with byte-identical targets, from arms whose training labels differ on 7 of 4,200 masks, with diverged learning-rate schedules.
- Validation labels are provisional. The 49-row gold review is 0 resolved, so nothing here can promote either version, authorize production, or establish which version is correct on `8690` — where each arm is scored against the labels it was trained on.
- No test metrics. The test split was never loaded, scored, visualized or predicted, by design.
- The probe project is a git repository with **zero commits**; the run report records `Git HEAD: None`. No code commit identifies the full run.
- Arm A was relaunched with `--resume` after its 30 epochs had already finished, to repair its best checkpoint and write the final status. Its recorded `completed_at_utc` is the finalize time, not the end of training.
- No MLflow run and no DVC status are recorded by this project, unlike Phase 1 and Phase 2.
- The curated QA images support visual diagnosis only.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).
