# Metrics Definitions

These definitions summarize how metrics are interpreted in this audit. Exact implementation details should be checked in the original experiment code and reports before making new claims.

## Wall IoU

Intersection over Union for the wall-region binary mask:

`TP / (TP + FP + FN)`

Higher is better.

## Wall Dice

Dice coefficient for the wall-region binary mask:

`2TP / (2TP + FP + FN)`

Higher is better.

## Boundary F1@2 px

F1 score for predicted wall-boundary pixels using a 2 pixel matching tolerance. In Phase 2 this comes from the dedicated wall-boundary head. For experiments without a dedicated boundary objective, this field is left `UNKNOWN` in the scoreboard unless a comparable final metric is explicitly audited.

## Centerline clDice

Centerline topology overlap score for predicted wall centerlines. Phase 1 reports `cldice_mean` (hard clDice of the thresholded centerline mask); Phase 2 and Phase 5 report `centerline_skeleton_cldice_mean` (clDice after skeletonisation). The scoreboard column carries whichever the source report used, so Phase 1 and Phase 2/5 centerline values are not a like-for-like comparison.

Higher is better.

## Junction F1@5 px

F1 score for detected junction points using a 5 pixel matching tolerance. Higher is better.

## Door Object F1

Object-level F1 score for door/opening components. Phase 2 final evaluation uses IoU threshold 0.25 for the scoreboard value because the source report records `door_object_f1_iou_0_25_mean` and `door_opening_object_f1_mean` with the same value.

## Window Object F1

Object-level F1 for window-opening components, computed with the same component-matching implementation as door object F1 (IoU threshold 0.25). Introduced in Phase 5. Higher is better.

## Endpoint F1@5 px

F1 score for detected wall-centerline endpoints using a 5 pixel point-matching tolerance, the same family as junction F1@5 px. Introduced in Phase 5. Higher is better.

## Fixtures Macro IoU

Mean over the nine fixture classes of the per-class micro IoU on the split (classes: cabinetry_storage, appliance, toilet_urinal, sink_tap, sauna_bench, fireplace, bathtub_shower_jacuzzi, chimney, other_fixture). Classes with little support (chimney, other_fixture) pull the macro value down; per-class values are kept in the experiment `metrics.json`. Higher is better.

## Hierarchical Score

Phase 5's checkpoint-selection composite: `0.40 x structural_wall IoU + 0.10 x boundary F1@2 px + 0.10 x centerline skeleton clDice + 0.05 x junction F1@5 px + 0.05 x endpoint F1@5 px + 0.10 x door object F1 + 0.10 x window object F1 + 0.10 x fixtures macro IoU`, evaluated only for epochs that pass the wall gate. It is a selection device, not a scoreboard metric.

## Visible Wall (derived)

`structural_wall AND NOT raw door opening AND NOT raw window opening`, derived from three predicted masks; it is not a trained head and is reported for context only.

## Integration Gates (experiment 11)

`bim_bridge_v0` reports evidence gates, not segmentation metrics. Each gate is `PASS`, `FAIL`, `BLOCKED` or `NOT_RUN`, and the synthetic and real tracks have separate gates.

| Gate | Meaning |
| --- | --- |
| G1 | Input identity and provenance established |
| G2 | Coordinate mapping, units, and scale established |
| G3 | Schema and geometry checks pass |
| G4 | IFC identities, relationships, and properties survive reopening |
| G5 | Uncertainty and assumptions are preserved |
| G6 | Real prediction lineage and recorded human review are established |
| G7 | Actual target application/viewer inspection is recorded |

A gate pass rate is not an accuracy. Gate results and object counts are never placed in the IoU, Dice or F1 columns of the scoreboard, which stay `UNKNOWN` for this experiment. A technical exporter pass, a reviewed prediction bridge, and downstream application acceptance are three different milestones.

## Attribute Origin and Review State (experiment 11)

Origin says where a value came from: `predicted_by_model`, `derived_from_geometry`, `manually_entered`, `assumed_for_preview`, `unknown`, or `synthetic_fixture`. Review state says whether a person verified the object: `CANDIDATE_UNREVIEWED`, `HUMAN_ACCEPTED`, `HUMAN_ACCEPTED_WITH_EDITS` or `HUMAN_REJECTED`. They are recorded separately. An edit by an agent or by an automated rule is not a review.

## Semantic Score (experiment 11)

A raw model score for an object, with its source and aggregation method. It is `null` when the only persisted prediction is a thresholded mask. It is never derived from binary pixels, IoU, F1, appearance or a successful export, and no overall confidence is computed.

## Micro vs Macro

Micro metrics aggregate counts across the split before computing the score. Macro metrics compute per-sample scores and then average them. The scoreboard prefers the primary metric used by the source report for the experiment. Detailed metrics retain micro/macro distinctions where they were present.

## Thresholds

Thresholds are copied from selected-threshold artifacts. A configured threshold and a selected threshold can differ; the scoreboard uses selected thresholds when available.

