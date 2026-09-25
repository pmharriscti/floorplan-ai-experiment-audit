# Phase 3A.2 Door-Opening Target Ablation: candidate_v3.1 vs candidate_v3.2 (512)

**EXPLORATORY — NOT HUMAN-GOLD VALIDATED.**

This is a **label experiment**. The primary question is not which arm trains a better model, it is whether the `candidate_v3.2` target repair produced **more correct door-opening labels** than `candidate_v3.1`. Both arms are the same MitUNet, from one byte-identical initialization, trained on the same plans in the same order; the only intended free variable is the target generator version.

The label question is answered first, below, because it is the one the evidence can actually speak to. The two label versions differ on just **8 of 4,600 masks** (1 of them in validation), which makes the model-level comparison structurally underpowered — it appears later as secondary, corroborating evidence, not as the result.

**Verdict in one line: v3.2 demonstrably repaired the labels it targeted — 10 instances, 5 of 7 human-adjudicated so far, with a clean geometry audit — but that is a statement about 10 instances out of 45,857, not about the corpus.**

## Label Correctness: Did v3.2 Repair the Labels?

### Yes, for what it targeted

**1. Human adjudication — the only evidence that is directly about labels.** Five of the seven reviewed instances were judged `Correct` / preferred `Candidate`. Two of those five, `10543/door_0003` and `10620/door_0005`, are exactly the instances where a reviewer had marked `candidate_v3.1` a `Critical issue`, with specific reasons ("added foreground at the wrong location/orientation rather than at the true source doorway"; "source SVG shows an exterior door in the bottom horizontal wall; candidate_v3.1 adds a vertical segment"). **v3.1's two worst confirmed failures were re-reviewed and passed under v3.2.** See [the review record](#v32-review-result-5-of-7-reviewed-instances-judged-correct) for the per-instance verdicts, and the [data-integrity incident](#data-integrity-incident-and-restoration) for the defect that briefly destroyed four of them.

**2. Geometry audit, all 10 Family A instances.** Tangent-aligned `10`, normal-aligned `0`, ambiguous wall orientation `0`, missing jamb evidence `0`, **placed on wrong wall `0`**, placed outside an architectural opening `0`. The architectural invariant holds on every one: the opening's long axis is parallel to the host-wall tangent and its short axis to the wall normal. Measured on `10620/door_0005`: wall tangent `0.15103162146491964` degrees, wall normal `90.15103162146492`, opening long axis `0.0`, angle to tangent `0.151`, angle to normal `89.849`.

**3. The derivation is now based on source geometry, not inferred raster geometry.** Exactly `10` instances in the v3.2 records carry `derivation_method: source_threshold_polygon_tangent_normal_repair` — the opening axis read from the source Door threshold polygon and its parent Wall polygon. This replaces v3.1's PCA over nearby wall pixels, synthesized rectangle, and snap-to-nearest-wall-pixel. That is the difference between reading the annotation and guessing from the raster, and it is what removed the wrong-wall failure mode.

**4. One instance went from no opening at all to a correct opening.** Like-for-like on the same 42 plans, `13110/door_0006` was `review_required_no_opening_generated` under v3.1 and is generated under v3.2. This is the case v3.1's own Family A report recorded as `Unchanged: no wall component intersects or lies near the opening seed`. A reviewer confirmed the repair: "candidate_v3.2 correctly repairs door_0006. The opening is horizontal and now matches the jamb-to-jamb doorway span shown in the source SVG and opening-centered crop. candidate_v3.1 was also horizontal but overshot the true opening extent."

**5. No door-opening warnings remain in v3.2's scope.** Within its 42 plans, `8` `review_required` rows remain and **all 8 are `window_opening`**. Zero door rows.

**6. Integrity clean.** `0` mechanical invariant violations, `0` pixel-preservation violations, `0` unexpected changes outside the declared repair scope.

**7. Weak corroboration from the models.** On the one differing validation plan, the v3.2-trained arm predicts 16 pixels that are all true positives against `candidate_v3.2` and all false positives against `candidate_v3.1`, while the v3.1-trained arm predicts nothing. This shows the v3.2 label is coherent and learnable. It is circular as evidence of correctness — each arm is scored against the labels it trained on — so it corroborates, it does not adjudicate.

### No, not as a statement about the label set

- **Scope is 10 instances out of 45,857 source opening instances.** v3.2 is a targeted patch applied to a configured Family A list, not a re-derivation. It says nothing about the other ~45,847.
- **Only 7 of 44 re-review rows are adjudicated (15.9%); 37 are pending.** That includes all **34 control rows**, which exist precisely to catch regressions the repair might have introduced elsewhere. No regression check has been completed.
- **One of v3.1's three confirmed critical failures is still unresolved.** `11709/door_0013` was marked `Critical issue` under v3.1 ("adds foreground that does not correspond to any actual architectural opening"). Under v3.2 it was reviewed and left `Skipped`, never marked `Correct`. Same for `11709/door_0014`. So of v3.1's three confirmed failures, two are confirmed fixed and one is open.
- **The validation gold queue is 0 of 49 resolved**, so the label set used to score the ablation is not frozen or adjudicated.
- **Phase 3A upstream is 0 of 105,000 rows reviewed**, with 153 review-required source classes pending. The taxonomy underneath all of this is unadjudicated.
- **Families B and C were untouched by v3.2.** From Phase 3A.1, 16 warnings remain unchanged and 24 unresolved for insufficient evidence (empty or unrenderable seeds). Eight window-opening instances still generate no opening at all.
- **A target-pipeline defect neither version fixes:** 46 unique instances vanish entirely during the 512 conversion (45 train, 1 validation). At 30 epochs **both** arms confidently predict the vanished `5981` opening — 39 and 35 pixels at maximum probability `1.0`, against a 20-pixel reference. The models recover an opening the 512 conversion destroyed. That is a defect sitting underneath both label versions and is not addressed by either.

### What would settle it

Adjudicate `11709/door_0013` and `door_0014` first — that closes the last known v3.1 critical failure. Then work the 34 control rows to confirm v3.2 regressed nothing it was not meant to touch. Neither needs compute.

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
| 3A.2 (`candidate_v3.2`) | 7 of 44 queue rows, **15.9% progress**, 37 pending | see below |

**v3.1's automated verdicts were overturned.** [results/label_repair_lineage/superseding_human_findings_v3_1.csv](results/label_repair_lineage/superseding_human_findings_v3_1.csv) records three instances v3.1 reported as "Resolved: valid opening generated correctly" that a reviewer marked `Critical issue`:

- `10543/door_0003` — "candidate_v3.1 added foreground at the wrong location/orientation rather than at the true source doorway"
- `10620/door_0005` — "source SVG shows an exterior door in the bottom horizontal wall; candidate_v3.1 adds a vertical segment"
- `11709/door_0013` — "adds foreground that does not correspond to an architectural opening in the source floorplan"

### v3.2 review result: 5 of 7 reviewed instances judged Correct

Of the 7 instances adjudicated so far, **5 were judged `Correct` / preferred `Candidate`**:

| Instance | Verdict | Note recorded |
| --- | --- | --- |
| `10543/door_0003` | **`Correct`** | — (v3.1 here was `Critical issue`) |
| `10620/door_0005` | **`Correct`** | — (v3.1 here was `Critical issue`) |
| `11709/door_0012` | **`Correct`** | "v3.2 correctly repairs door_0012. The opening is now generated vertically between the two identified doorway jambs. candidate_v3.1 used incorrect horizontal geometry, while v3.2 matches the architectural doorway shown in the source instance." |
| `11709/door_0013` | `Skipped` | — (v3.1 here was `Critical issue`; **still unresolved**) |
| `11709/door_0014` | `Skipped` | — |
| `13110/door_0006` | **`Correct`** | "v3.2 correctly repairs door_0006. The opening is horizontal and now matches the jamb-to-jamb doorway span shown in the source SVG and opening-centered crop. candidate_v3.1 was also horizontal but overshot the true opening extent." |
| `13827/door_0004` | **`Correct`** | "v3.2 correctly repairs door_0004. The doorway opening is horizontal in the opening-centered crop and source SVG evidence. v3.2 matches the jamb-to-jamb opening axis, while earlier versions were aligned incorrectly to the wall-edge interpretation." |

Two of the five, `10543/door_0003` and `10620/door_0005`, are exactly the instances where human review had marked `candidate_v3.1` a `Critical issue`. A third, `13110/door_0006`, is the instance the v3.1 Family A repair had left `Unchanged: no wall component intersects or lies near the opening seed`.

### Data-integrity incident and restoration

Four of those five verdicts were **destroyed and later restored**. Between 2026-09-02 and 2026-09-08 the saved decision file silently lost `10543/door_0003`, `10620/door_0005`, `11709/door_0012` and `13110/door_0006`, each reverting from `Correct` / `Candidate` to `Skipped` / `Cannot determine`. Only `13827/door_0004` survived, so the file reported 1 `Correct` where the reviewer had recorded 5.

**Cause.** `ReviewController.skip_opening` in `scripts/gradio_phase3a_target_review.py` called `save_opening(..., "Skipped", [], "Cannot determine", "None", ...)` unconditionally. The button was labelled only `Skip`, so it read as navigation; pressing it while paging back through already-reviewed records overwrote the stored verdict with the widget defaults. Reviewer notes survived because the Skip path passes the pre-filled notes textbox through, which is why affirmative notes were left sitting on `Skipped` decisions.

**Detection.** The app's own audit log records every verdict transition with a timestamp, so the original `Correct` saves and the later reversions are both on record. That log, not the decision CSV, is what made the loss visible.

**Restoration.** On 2026-09-25 the four verdicts were written back through the app's persistence layer, which created backups and appended new audit-log entries for the change. The decision file now reads 5 `Correct` / 2 `Skipped` and the re-review manifest reads `correct: 5, skipped: 2, pending: 37`. Full history in [results/v3_2_review_verdict_history.json](results/v3_2_review_verdict_history.json).

**Fix.** `skip_opening` now refuses to overwrite an existing decision: it advances without writing and reports `Skip refused: … is already saved as '<decision>'`. The button is relabelled `Skip (undecided only)`. Covered by `tests/test_phase3a_review_skip_guard.py` (4 cases; the existing review suite still passes, 16 tests).

No model metric in this entry depended on these decisions.

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

## Model Comparison (Secondary Evidence)

Recorded for completeness. With 8 of 4,600 masks differing between the arms, this comparison is structurally underpowered and it is **not** the basis for the label verdict above.

### 30-epoch evaluation

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

**On labels, the primary question.** v3.2 repaired what it set out to repair. The evidence converges from three independent directions: a human reviewer accepted 5 of the 7 instances examined, including both of v3.1's worst confirmed failures; an automated geometry audit finds the architectural invariant satisfied on all 10 repaired instances with none on the wrong wall; and the derivation itself moved from inferring geometry out of wall pixels to reading it from the source threshold and parent wall polygons, which is a categorically sounder basis. One instance that previously produced no opening at all now produces a correct one. That is a real, specific, verifiable repair.

It is also small. Ten instances out of 45,857, on a queue that is 15.9% adjudicated, with the 34 regression-control rows entirely unreviewed and one of v3.1's three confirmed failures still open. The correct summary is that the repair works where it has been checked, and most of it has not been checked.

**On models, the secondary question.** The 30-epoch comparison does not support v3.2 and mildly favours v3.1, but it cannot carry weight in either direction. The arms' training labels differ on 7 of 4,200 masks and the common evaluation subset has byte-identical targets, so the one significant result — opening-instance F1 favouring the control — separates two training runs rather than two label versions. The learning-rate schedules also diverged. A 5-epoch probe pointed the opposite way on both pixel and instance metrics, which is itself a demonstration that run-to-run variation dominates here.

**Why the two answers differ, and which to believe.** The label evidence is per-instance and directly verifiable against source annotations; the model evidence is an aggregate over 398 plans whose labels are identical in both arms. When a label change touches 0.17% of the training set, aggregate model metrics are the wrong instrument — they are measuring training noise with a label-shaped name on it. The label-correctness evidence is the one to act on.

**What remains blocked, and on what.** Not compute. The Phase 3A gate stands at 0 of 105,000 rows, this ablation's gold queue at 0 of 49, and the Family A re-review at 7 of 44. Separately, the saved Phase 3A.2 decision file is not trustworthy until the review app is fixed and the four overwritten verdicts are restored. Underneath both label versions sits an unfixed 512-conversion defect that destroys 46 openings, one of them in validation, and which both trained models can be shown to see through.

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
