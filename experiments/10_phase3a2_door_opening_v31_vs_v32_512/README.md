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

## Label Repairs by Version

The experimental variable is a chain of three target-generation repairs. Each one fixed a specific, named defect in how a door *opening* is derived from the CubiCasa5K SVG. The governing semantic throughout is that **a door opening is not a door symbol**: the leaf, swing arc and panel paths are evidence for locating the opening, never the target itself.

### Baseline problem: `candidate_v2`

Openings were rasterized more or less directly from source polygons. Two consequences: the door/window *symbol* footprint and the *opening* target were conflated, and an opening could be painted anywhere the polygon fell, including off any wall.

### Phase 3A → `candidate_v3` — source-class and symbol/opening separation

**Defect.** Symbol and opening were the same thing, and openings were not constrained to lie on a wall.

**Repair.**
1. **Symbol/opening split.** Door and window *symbol* masks are drawn from visual outlines and strokes. Opening masks are derived separately. Neither is a copy of the other.
2. **Wall association first.** An opening is derived only *after* it is associated with a host structural wall, then **clipped to structural-wall support**, so opening pixels cannot exist off-wall.
3. **Source taxonomy inventory.** All 5,000 samples and 1,957,806 source element rows were inventoried: **318 distinct raw source classes**, of which **153 were marked review-required**, plus 2,542 geometry failures.

**Outcome.** 0 pilot mechanical violations, 0 semantic violations, 0 pixel-preservation violations, 0 unexplained symbol/opening equality cases. `candidate_v2` left untouched. Verdict `blocked` at human review.

### Phase 3A.1 → `candidate_v3.1` — opening-rule repairs (three families)

**Defect.** `candidate_v3` still produced 84 warnings over 32 plans (43 door, 41 window). Clustering them gave three root causes.

| Family | Defect | Repair | Flag |
| --- | --- | --- | --- |
| **A — seed semantics** | The door **leaf/swing symbol** geometry was used as the opening seed, so the opening inherited the symbol's axis and ran perpendicular to its host wall | Re-derive the seed so the opening follows the wall rather than the symbol | `repair_door_opening_seed_semantics` |
| **B — source instances** | False, malformed or **border-collapsed** instances entered the pipeline; a bbox touching the image edge collapsed to a single raster row or column | Classify and re-localize source instances; exclude confirmed false ones | `repair_source_instance_classification_and_localization` |
| **C — wall association** | Association demanded direct overlap with wall foreground, so a genuine opening sitting in a **wall gap** — exactly where a doorway is — was rejected | Gap-aware association with a search radius and a relaxed overlap ratio | `repair_opening_host_wall_association` |

Supporting parameters: `association_max_distance_px: 3`, `min_wall_overlap_ratio: 0.05`, `door_seed_repair_min_wall_overlap_ratio: 0.02`, `door_seed_repair_local_radius_px: 48`, `gap_association_search_radius_px: 36`.

Warning counts behind the families: 24 empty seeds, 44 border-collapsed bboxes, 58 seed/wall orientation mismatches, 5 plausible seeds rejected by association.

**Outcome.** 42 warnings resolved, 2 excluded as false source instances, 16 unchanged, 24 unresolved for insufficient evidence (empty or unrenderable seeds). 0 mechanical and 0 pixel-preservation violations. Border-collapsed bboxes fell from 44 to 35. Verdict `blocked` at human review.

### Phase 3A.2 → `candidate_v3.2` — opening-axis repair

**Defect — in v3.1's own Family A repair.** v3.1 never confirmed that the opening was supported by actual doorway jambs. Instead it:

1. inferred a local wall orientation by **PCA over nearby wall pixels**,
2. synthesized a **rectangle** from the old seed span, and
3. **snapped that rectangle's centre to the nearest wall pixel**.

Near corners, stacked doors and image borders, step 3 can select a *nearby or perpendicular* wall. The result looks like a clean opening but sits on the wrong wall. Human review confirmed this on real cases.

Two hypotheses were explicitly **ruled out**: it was not a global 90-degree tangent/normal inversion, and there was no row/column or width/height parser bug in the generator. A flat-vs-nested bbox parsing bug did exist, but in the **review UI**, where it had been hiding bbox values from the reviewer.

**Repair.** Take the geometry from the source, not from the raster. v3.2 uses the **source Door threshold polygon and its parent Wall polygon** as the tangent/normal evidence, so the opening's long axis is the host wall's tangent and its short axis the wall normal, jamb to jamb. Mechanism: PCA/SVD for polygon tangent estimation, modulo-180 axis comparison, tangent/normal decomposition, and boolean mask set operations for per-instance pixel provenance. Gated by `repair_door_opening_tangent_normal_semantics` with `door_tangent_normal_axis_tolerance_degrees: 15.0`, applied only to a configured list of Family A instances.

**Outcome.** 10 Family A instances audited: **10 tangent-aligned, 0 normal-aligned, 0 ambiguous orientation, 0 missing jamb evidence, 0 placed on the wrong wall, 0 placed outside an architectural opening.** 0 mechanical and 0 pixel-preservation violations. The legacy `wall_orientation` field was found stale on all 10 and ambiguously named on all 44 queue rows, but with **0 actual geometric disagreement** — the field was mislabelled, not wrong. Verdict `blocked` at human review.

### Net effect on the two arms

The 10 repaired Family A instances split evenly between the two warning clusters — 5 `door-symbol geometry used as opening seed` and 5 `seed/wall axis mismatch` — and span exactly **8 plans**, which are exactly the 8 masks that differ between arm A and arm B. All 10 sit in the re-review queue as `repair_family: A`; the other 34 rows are untouched controls carried along for regression review.

In the queue metadata those 10 rows are the ones marked `association_confidence: low`, `legacy_orientation_is_stale: True` and `actual_geometric_disagreement: True`, and they carry `derivation_method: review_required_no_opening_generated` — the earlier derivation flagged them rather than emitting a usable opening. The 34 control rows carry `explicit_source_opening_polygon_clipped_to_associated_structural_wall` with `association_confidence: high`.

### What human review has actually said

Counts below are parsed CSV rows, not line counts; the notes fields contain embedded newlines, so `wc -l` overstates them.

| Phase | Decisions recorded | Breakdown |
| --- | ---: | --- |
| 3A (`candidate_v3`) | 21 | 16 `Critical issue`, 3 `Ambiguous`, 2 `Needs generator repair`; preferred version `Cannot determine` on all 21 |
| 3A.1 (`candidate_v3.1`) | 4 | 3 `Critical issue` (preferred `Neither acceptable`), 1 `Correct` (preferred `Candidate`) |
| 3A.2 (`candidate_v3.2`) | 7 | 6 `Skipped`, 1 `Correct` (preferred `Candidate`) |

The v3.2 re-review queue stands at **7 of 44 rows reviewed, 37 pending** (`human_review_status`: 6 `skipped`, 1 `correct`, 37 `pending`).

**v3.1's automated verdicts were overturned.** [results/label_repair_lineage/superseding_human_findings_v3_1.csv](results/label_repair_lineage/superseding_human_findings_v3_1.csv) records three instances v3.1 reported as "Resolved: valid opening generated correctly" that a reviewer marked `Critical issue`:

- `10543/door_0003` — "candidate_v3.1 added foreground at the wrong location/orientation rather than at the true source doorway"
- `10620/door_0005` — "source SVG shows an exterior door in the bottom horizontal wall; candidate_v3.1 adds a vertical segment"
- `11709/door_0013` — "adds foreground that does not correspond to an architectural opening in the source floorplan"

**Where v3.2 was judged to have fixed what earlier versions could not.** Three of the seven reviewed v3.2 instances carry explicit reviewer notes to that effect:

- `11709/door_0012` — "candidate_v3.2 correctly repairs door_0012. The opening is now generated vertically between the two identified doorway jambs. candidate_v3.1 used incorrect horizontal geometry, while v3.2 matches the architectural doorway shown in the source instance."
- `13110/door_0006` — "candidate_v3.2 correctly repairs door_0006. The opening is horizontal and now matches the jamb-to-jamb doorway span shown in the source SVG and opening-centered crop. candidate_v3.1 was also horizontal but overshot the true opening extent." This is also the one instance the v3.1 Family A repair had left `Unchanged: no wall component intersects or lies near the opening seed`.
- `13827/door_0004` — "candidate_v3.2 correctly repairs door_0004. The doorway opening is horizontal in the opening-centered crop and source SVG evidence. v3.2 matches the jamb-to-jamb opening axis, while earlier versions were aligned incorrectly to the wall-edge interpretation." This is the single formal `Correct` / preferred `Candidate` verdict in the v3.2 queue.

Only `13827/door_0004` was filed as a formal `Correct`. The other two were filed as `Skipped` / `Cannot determine` despite the affirmative notes, so they do not count as resolutions and the queue remains blocked.

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
