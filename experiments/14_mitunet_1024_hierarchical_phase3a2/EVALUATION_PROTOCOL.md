# Evaluation Protocol

This is the proposed measurement plan for experiment 14. Freeze its resolved choices and artifact identities before the matched full runs. Parent observations are context; measured results belong in [metrics.json](metrics.json) only after execution.

## Questions And Comparators

| Question | Comparator |
| --- | --- |
| Does the integrated model protect walls? | Experiment-06 checkpoint reproduced at 1024 with the new evaluator and identical wall labels |
| Does it add useful heads? | Per-head metrics, QA and task support on the frozen common reference |
| What did Phase 3A labeling change? | Matched 1024 multi-head arms with explicit target-policy differences |
| What did resolution change? | Optional matched 512/1024 pair using one common initialization and compatible target definitions |
| Does better labeling survive preprocessing? | Per-instance native-to-model audit, independent of model accuracy |
| Does it support downstream geometry? | Versioned exports, coordinate fidelity, opening-host/width checks and the separately recorded bridge acceptance evidence |

## Paired Arms

All new 1024 arms use the experiment-06 parent, same architecture, fixture mappings, official membership, sample order, random state, batch policy, training bands, loss weights and training budget.

| Arm | Door labels | Window labels | Role |
| --- | --- | --- | --- |
| A: `1024_phase5_label_control` | Phase 2 semantic definition, regenerated at 1024 | Phase 5 candidate-v2 definition, regenerated at 1024 | Measures the integrated topology with historical Phase 5 label definitions |
| B: `1024_phase3a1_label_control` | Source-associated v3.1 definition | Phase 3A wall-associated window definition with frozen inherited repairs | Common parent for the scoped axis-repair comparison |
| C: `1024_phase3a2_integrated` | Same as B plus the explicit v3.2 door-instance scope | Byte-identical to B | Primary experiment-14 treatment |

C versus B isolates the scoped door repair. B versus A changes the broader door and window contracts together; report it as a combined label-policy comparison. Never attribute the entire A-to-C difference to the ten v3.2 door repairs.

Historical experiment 09 starts from experiment 01 at 512, while the new primary arm starts from experiment 06 at 1024. Their comparison includes initialization history, resolution, targets and batch behavior. For a resolution-only study, initialize both new 512/1024 arms from the same state, hold targets/recipe fixed apart from declared scale adaptations, and evaluate on the same canonical reference. Historical parent numbers are not that controlled study.

Use seed `42` for the first integration. Replicate paired comparisons with seeds `43` and `44` before claiming robust improvements across training runs. Paired plan bootstrap intervals alone do not capture training-seed variation.

## Fair Optimization In Label Comparisons

The primary integration recipe inherits Phase 5's ReduceLROnPlateau schedule. Different label arms may trigger it differently. For a causal C-versus-B label study, freeze a common LR timetable before those runs, with all inherited/new group rates and warm-up steps identical. Publish that resolved timetable as a separate comparison override and make no label-only attribution if trajectories diverge. Experiment 10 demonstrated why adaptive-schedule divergence matters.

Fixed task weights, positive-weight estimation procedure, initialization, sampler seeds and augmentation draws must also be declared. If train-only positive weights differ with the new labels, record that as an additional optimization difference or freeze common weights for the causal comparison.

## Reference Labels And Split Policy

- Use exactly one frozen reference bundle for evaluating every compared model.
- Preserve source/class/instance provenance and recorded human decisions with that bundle.
- Report metrics on all eligible validation plans, the explicitly changed-instance subset, and a common unchanged-target subset, with exact denominators.
- Do not call a score against each arm's own target version evidence that one label version is more correct.
- Keep true negatives, unsupported sources, generation failures and vanished positives distinct.
- Structural-wall labels must remain identical to the experiment-06 definition on the common 1024 reference.
- Use train/validation for development. Keep the existing test membership for one final frozen evaluation after settings are locked. Historical parent test numbers are context, not a tuning signal for new thresholds or targets.

The existing Phase 5 reproduction stage reads both validation and test. Adapt it so the experiment-14 wall floor is computed from validation only; defer the new test evaluation to the final stage.

## Wall Protection

```text
reference = reproduce experiment-06 validation micro wall IoU at threshold 0.1
floor = reference - 0.005
eligible = integrated validation micro wall IoU at threshold 0.1 >= floor
```

The historical reference is `0.8267843774749646`, giving an illustrative floor of `0.8217843774749646` if reproduction is exact. Recompute and persist the actual reference. Do not substitute experiment 06's training-history best IoU (`0.8259883607445844`) or experiment 09's old 512 floor (`0.8138460992164052`).

Freeze the reproduction method, acceptable implementation discrepancy and gate before training. Investigate source/transform/metric differences when reproduction fails its declared tolerance. A wall-floor pass demonstrates bounded regression; wall improvement requires its own measured delta and uncertainty.

Select the best hierarchical score among eligible checkpoints and separately retain best wall, best ungated and last. If no checkpoint is eligible, report that outcome rather than relaxing the floor after viewing the results.

## Coordinate Profiles

| Profile | Evaluation space | Boundary tolerance | Point tolerance | Use |
| --- | --- | --- | --- | --- |
| `native_1024` | 1024 whole-plan letterbox | 4 px | 10 px | Primary integrated selection and scale-aware geometry metrics |
| `common_512` | Fixed canonical 512 reference | 2 px | 5 px | Companion comparison with Phase 5 conventions |
| `native_1024_strict` | 1024 whole-plan letterbox | 2 px | 5 px | Additional strict localization diagnostic |

The first two profiles have nominally equal relative tolerances. They are not assumed numerically identical: rasterization, skeletonization, object survival and rounding can differ. Publish the profile in every field name, table and threshold artifact. A `4px` score must not populate the scoreboard's `boundary_f1_2px` column.

For the common-512 evaluation, transform probabilities from the model letterbox through the recorded source-canvas map into the canonical 512 map, then threshold; transform coordinates consistently. Use a separately frozen 512 reference generated from native labels. Do not resize binary predictions with linear interpolation, reuse a 1024 padding value at 512 or treat a resized training band as the raw evaluation target.

The primary scoreboard convention is native-1024 micro wall IoU/Dice; boundary F1@2 px and point F1@5 px columns use the companion `common_512` profile. Record that mixed-profile convention explicitly in the notes and detailed metrics. Scale-aware 4/10 px scores get separate fields. If a companion result is unavailable, leave the corresponding scoreboard field unknown.

## Checkpoint Score And Thresholds

For training checkpoint selection, use fixed documented diagnostic thresholds and native-1024 scale-aware metrics. Proposed starting thresholds are wall `0.1`, all other heads/classes `0.5`, junction/endpoint NMS radius `6`. They are proposed selection settings, not transferred validation optima.

The hierarchical score retains Phase 5's metric weights: wall IoU `0.40`, boundary F1 `0.10`, skeleton clDice `0.10`, junction F1 `0.05`, endpoint F1 `0.05`, door object F1 `0.10`, window object F1 `0.10`, fixtures macro IoU `0.10`. At 1024, the boundary and point terms use 4/10 px tolerances under the named profile.

After checkpoint selection, sweep validation-only sigmoid thresholds per head and fixture class. Use the grid in config; expand the boundary grid above `0.95` as a declared initial design choice because the parent's boundary optimum hit its grid edge. Search NMS radii under the same coordinate profile. Freeze threshold/NMS choices before test. Any common-512-specific calibration must be labeled separately and also use validation only.

## Metrics And Diagnostics

| Output | Required metrics |
| --- | --- |
| Structural wall | Micro and macro IoU/Dice, precision/recall; fixed `0.1` gate values plus selected-threshold values |
| Wall boundary | F1/precision/recall at named tolerances, raw pixel IoU, predicted/true thickness or pixel count, surface distance |
| Centerline | Skeleton clDice, components, continuity and support within structural wall |
| Junction/endpoint | Point precision/recall/F1, localization error, count error and overflow under each profile |
| Door/window | Pixel IoU/Dice; object F1 at IoU `0.25` and `0.5`; center/width errors; unsupported-host rate |
| Scoped repaired doors | Axis-to-source-host error modulo 180 degrees, jamb alignment, per-instance masks and prediction changes |
| Fixtures | Per-class IoU/Dice/precision/recall, support counts, macro IoU, rare-class and overlap diagnostics |
| Visible wall | Derived-mask IoU and structural/opening relationship checks |
| Resources | Peak allocated/reserved VRAM, data wait, examples/s, epoch time, total time and final frozen inference latency |

Keep raw and postprocessed prediction metrics separate. Source host geometry used to audit validation labels must not be fed to deployment predictions without declaring that extra input. A successful IFC export is downstream integration evidence; its technical pass does not supply a segmentation score or a building scale.

## Uncertainty And Acceptance Evidence

Use paired plan-level bootstrap with `2000` resamples and seed `42` for model deltas on common references. Bootstrap counts correctly for micro metrics; preserve original per-plan counts and matching outputs. Publish train-seed variation separately. Report changed-instance evidence even if aggregate confidence intervals span zero.

Record acceptance for each question independently: target-contract checks, wall gate, per-head utility, per-instance geometry, survivability, resources and downstream coordinate compatibility. Per-head improvement claims need measured common-reference deltas. No numerical opening/fixture improvement target is inferred from parent scores.

## Required Result Package

The external run directory should contain resolved config and environment, source manifest and checkpoint identity, frozen dataset and target manifests, scope/disposition records, final-mask validation, reproduction and initialization proof, training/probe histories, all checkpoint identities, threshold/NMS sweeps, per-plan/per-instance metrics, paired uncertainty, resource profiles, prediction contract and curated QA.

Update this audit's experiment-14 status, metrics, scoreboard and provenance only with the recorded results. Parent evidence remains identified separately and the proposed protocol remains recoverable through Git history.
