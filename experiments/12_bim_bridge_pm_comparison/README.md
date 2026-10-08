# bim_bridge PM comparison: CubiCasa test plans vs AI-generated plans

**A downstream illustration, not a benchmark.** Fifteen plans were taken through the frozen Phase 5 multi-head model
(experiment 09) and the bim_bridge_v0 IFC chain (experiment 11). No model was trained and no threshold was chosen.
The results are not comparable with the segmentation rankings above; the scoreboard's pixel-metric columns are `UNKNOWN`.

## Question

How does the chain behave from masks to IFC files on a few CubiCasa5K test plans and on AI-generated plans, and how
much of the loss between the masks and the IFC walls can automated bridge repairs recover?

## Inputs

| Group | Plans | How chosen | Predictions | Labels |
| --- | --- | --- | --- | --- |
| CubiCasa5K test | 3 | `random.Random(42)` over the 400 test plans | saved upstream predictions | dataset labels |
| AI-generated, residential/mixed | 6 | every image in the folder, file-name order | from run `bim_bridge_synth_images_v0_20261002_200115_UTC` | **draft, unreviewed** |
| AI-generated, commercial | 6 | every image in the folder, file-name order | fresh frozen inference | **draft, unreviewed** |

The AI-generated images were made with an image generator and depict no real building. Their labels were drawn by an
AI assistant by tracing dark pixels inside hand-placed guide bands; **none of the 12 was reviewed by a person**. Scores
against them are agreement with draft labels, not verified accuracy. The model also follows dark ink, so agreement may
overstate true accuracy.

## Results, pooled by group

| Group | Labels | Mask wall IoU | IFC wall IoU before repair (r01) | IFC wall IoU after repair (r04) | Doors in IFC, r01 | Doors in IFC, r04 |
| --- | --- | --- | --- | --- | --- | --- |
| CubiCasa test (3) | dataset | 79.8% | 64.8% | 71.1% | 18/23 | 19/23 |
| AI residential/mixed (6) | draft, unreviewed | 79.3% | 76.4% | 82.7% | 24/33 | 30/33 |
| AI commercial (6) | draft, unreviewed | 73.5% | 71.0% | 76.5% | 68/93 | 74/93 |

For context, the model's mean wall IoU over all 400 CubiCasa test plans is 81.1% (boundary F1 at 2 px 95.4%).

- On the residential AI plans the masks agree with the draft labels about as well as on CubiCasa; commercial plans are lower.
- Most of the loss happened between the masks and the IFC walls. On CubiCasa the repair rules narrowed that gap from 15.0 to 8.7 points; on the AI plans the repaired IFC walls now score at or above the masks.
- Doors: the model finds most doors in the masks, but some are lost when masks become walls.
- Windows: not exported until revision r05 (2026-10-08), which exports them as apertures with an assumed vertical profile; see [Window apertures](#window-apertures-revision-r05-windows_v1-2026-10-08).

## Results per plan

| Plan | Labels | Mask wall IoU | IFC r01 | IFC r04 | Doors in IFC r01 | Doors in IFC r04 | Walls r01 → r04 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `cc-01` CubiCasa high_quality/4712 | dataset | 70.5% | 57.7% | 66.4% | 5/6 | 5/6 | 23 → 14 |
| `cc-02` CubiCasa high_quality_architectural/4847 | dataset | 87.7% | 56.2% | 59.6% | 3/7 | 4/7 | 12 → 8 |
| `cc-03` CubiCasa high_quality_architectural/2539 | dataset | 83.9% | 76.4% | 82.9% | 10/10 | 10/10 | 18 → 16 |
| `img-01` house, ground floor | draft, unreviewed | 81.3% | 72.9% | 79.3% | 2/6 | 5/6 | 25 → 17 |
| `img-02` house, upper floor | draft, unreviewed | 79.2% | 79.5% | 84.1% | 7/9 | 7/9 | 21 → 19 |
| `img-03` apartment | draft, unreviewed | 79.0% | 71.3% | 82.6% | 6/6 | 6/6 | 22 → 16 |
| `img-04` office | draft, unreviewed | 75.9% | 74.3% | 79.5% | 6/6 | 6/6 | 17 → 10 |
| `img-05` retail | draft, unreviewed | 81.0% | 80.0% | 88.1% | 1/3 | 3/3 | 11 → 7 |
| `img-06` restaurant | draft, unreviewed | 80.5% | 82.4% | 83.6% | 2/3 | 3/3 | 15 → 8 |
| `com-01` warehouse | draft, unreviewed | 61.7% | 60.3% | 59.2% | 10/11 | 10/11 | 22 → 13 |
| `com-02` hotel | draft, unreviewed | 76.3% | 67.2% | 74.3% | 11/25 | 14/25 | 45 → 35 |
| `com-03` clinic | draft, unreviewed | 77.3% | 76.7% | 81.2% | 15/17 | 16/17 | 29 → 23 |
| `com-04` school | draft, unreviewed | 76.6% | 72.0% | 85.0% | 13/14 | 14/14 | 22 → 16 |
| `com-05` grocery | draft, unreviewed | 68.3% | 75.6% | 76.7% | 11/12 | 11/12 | 21 → 19 |
| `com-06` manufacturing | draft, unreviewed | 73.0% | 70.6% | 74.9% | 8/14 | 9/14 | 20 → 17 |

IFC wall IoU is measured on the walls read back from each IFC file, mapped to the model's 512 grid. Doors count as
found when a predicted region shares at least one pixel with a labelled door (a loose detection count).

## Bridge repair rules (revision r04, `repair_v1.2`)

Applied after the vectorizer and before door hosting, evidenced on each plan's predicted mask only:

1. **R1 collinear merge.** Two walls on the same line become one when at least 90% of the gap lies on the predicted mask; overlapping duplicates merge too.
2. **R2 end extension.** A wall end moves along its axis while the mask continues under the wall body, up to 40 px per end in total, stopping at parallel neighbours. Through a perpendicular neighbour this closes the corner.
3. **R3 recentre.** A merged or extended axis is snapped orthogonal and moved onto the mask centreline (at most 3.0 px).

Across the 15 plans the rules made 1030 automated edits (R2_extend 577, R3_recentre 368, R1_merge 85). Each is recorded on its object with before and
after values, so a reviewer can see and undo it. IFC wall IoU improved on 14 of 15 plans; com-01 got slightly worse.

Two earlier versions are kept on disk as evidence: r02 (`repair_v1.0`) left overlapping duplicate walls on three plans,
which the input contract refused; r03 (`repair_v1.1`) let a short segment's slope tilt a long merged wall off the mask and
let extensions compound across rounds, and two plans regressed. **The rules were developed and checked on these same
15 plans, so their gains are not held-out evidence.**

## Window apertures (revision r05, `windows_v1`, 2026-10-08)

Through r04 the window head's components were recorded in every candidate file and left unexported, because the
preview profile gave `window_opening` no vertical profile and the bridge invents no heights. That was the largest
gap between what the model predicts and what reaches the IFC: 175 window components across the 15 plans, none exported.

Revision r05 adds a window entry to the preview profile (sill 0.9 m, height 1.2 m; **assumptions chosen by the AI
assistant in the working session, confirmed by nobody**, and labelled as assumptions on every exported object like the
door values) and hosts window components with the same host rule as doors. A window is still a rectangular void
through the wall; no `IfcWindow` is created. The vectorizer, the repair rules, the core bridge code and the door and
wall geometry are unchanged: every plan's walls, IFC wall IoU and doors are identical to r04, and every r04 GlobalId is reused.

One new rule was needed. Components of the two heads often abut on the same wall (a window beside a door), and the
half-pixel padding makes them overlap. Two components of the **same** head that overlap are both left unexported as
ambiguous, as before. Where a **window overlaps a door**, the door keeps its void and the window is trimmed to stop
0.5 px short of it, recorded as an automated edit on the object; if the door covers the window or would split it, the
window is left unexported with that reason. The gap exists because two voids that merely touch fail the input
contract's 1e-9 m overlap test once offset and width are rounded separately; the first cc-01 export failed that way
and its report is kept ([results/r05_exports/cc-01/attempt01_FAILED_validation_report.md](results/r05_exports/cc-01/attempt01_FAILED_validation_report.md)).

| Group | Labels | Doors in IFC, r04 | Doors in IFC, r05 | Windows found by masks | Windows found in IFC, r05 |
| --- | --- | --- | --- | --- | --- |
| CubiCasa test (3) | dataset | 19/23 | 19/23 | 19/19 | 19/19 |
| AI residential/mixed (6) | draft, unreviewed | 30/33 | 30/33 | 43/43 | 43/43 |
| AI commercial (6) | draft, unreviewed | 74/93 | 74/93 | 90/92 | 90/92 |

| Plan | Doors in IFC r04 → r05 | Window components predicted → exported | Windows found: mask | Windows found: IFC r05 | Trimmed |
| --- | --- | --- | --- | --- | --- |
| `cc-01` CubiCasa high_quality/4712 | 7 → 7 | 6 → 6 | 4/4 | 4/4 | 3 |
| `cc-02` CubiCasa high_quality_architectural/4847 | 4 → 4 | 6 → 6 | 6/6 | 6/6 |  |
| `cc-03` CubiCasa high_quality_architectural/2539 | 10 → 10 | 9 → 9 | 9/9 | 9/9 |  |
| `img-01` house, ground floor | 7 → 7 | 11 → 11 | 9/9 | 9/9 |  |
| `img-02` house, upper floor | 8 → 8 | 8 → 8 | 8/8 | 8/8 |  |
| `img-03` apartment | 10 → 10 | 10 → 8 | 6/6 | 6/6 |  |
| `img-04` office | 6 → 6 | 6 → 6 | 6/6 | 6/6 |  |
| `img-05` retail | 3 → 3 | 3 → 3 | 3/3 | 3/3 |  |
| `img-06` restaurant | 3 → 3 | 11 → 11 | 11/11 | 11/11 |  |
| `com-01` warehouse | 11 → 11 | 19 → 18 | 12/14 | 12/14 |  |
| `com-02` hotel | 18 → 18 | 16 → 16 | 16/16 | 16/16 |  |
| `com-03` clinic | 16 → 16 | 10 → 10 | 10/10 | 10/10 |  |
| `com-04` school | 14 → 14 | 16 → 16 | 16/16 | 16/16 |  |
| `com-05` grocery | 17 → 17 | 20 → 19 | 16/16 | 16/16 | 2 |
| `com-06` manufacturing | 9 → 9 | 24 → 23 | 20/20 | 20/20 | 1 |

170 of 175 predicted window components reached the IFC (4 × no candidate wall hosts this component; 1 × component smaller than min_aperture_component_px (20)). 6 windows were trimmed to yield to a door.
Windows count as found by the same loose one-pixel rule as doors. All 15 r05 files pass the bridge checks, the 8
run-specific checks, the independent web-ifc parse and a byte-identical repeat export.

The comparison script now reads each void's `PredictedClass` and scores door and window voids separately, so the door
counts above cannot be inflated by window voids. Re-scoring the r04 exports with the changed script reproduced every
pre-existing number exactly ([results/comparison_r04_regression_check_20261008/](results/comparison_r04_regression_check_20261008/)).

## Why the warehouse (com-01) scores lowest

Its walls are about 4 px wide on the 512 grid. A 1-pixel disagreement on each wall edge would alone cap IoU at about 67%.
88% of its error lies within 2 px of a labelled wall edge, and its boundary F1 at 2 px is 94%. The rest is mostly the
entrance vestibule walls and a stub near the restrooms. IoU understates thin-walled plans; report boundary F1 with it.

## Status of the IFC files

All 45 files (r01, r04 and r05 for 15 plans) pass the bridge checks, 8 run-specific checks, the independent web-ifc parse
and a byte-identical repeat export. Every file is a **candidate, unreviewed** preview with an assumed scale (0.01 preview
metres per source pixel). Windows are not exported in r01 and r04; r05 exports them as apertures with an assumed vertical
profile. No viewer inspection is recorded. The IFC files are
not committed; their paths and hashes are in [metrics.json](metrics.json).

## Evidence

- Comparison tables and reports: [results/comparison_r05/](results/comparison_r05/), [results/comparison_r04/](results/comparison_r04/), [results/comparison_r01/](results/comparison_r01/)
- r05 export checks per plan and the cc-01 candidate file with its trims: [results/r05_exports/](results/r05_exports/); r05 configuration: [results/config/bim_bridge_pm_comparison_v0_windows_v1.yaml](results/config/bim_bridge_pm_comparison_v0_windows_v1.yaml)
- The label bundle's own evaluator, run at full resolution as a cross-check: `results/comparison_r0x/label_bundle_evaluator/`
- Inputs and inference contract: [results/subset_manifest.json](results/subset_manifest.json), [results/config/inference_contract.json](results/config/inference_contract.json)
- Repair configurations: [results/config/](results/config/)
- Draft label bundle README and manifest: [results/draft_labels/](results/draft_labels/)
- Visual QA: [qa/README.md](qa/README.md)

## Non-claims

- Not a benchmark; 15 plans illustrate behaviour and establish nothing in general.
- No claim about real company drawings; AI-generated plans share one drawing style.
- No dimensional accuracy, no human review of these plans, no viewer acceptance.

## Publication Status

Published on 2026-10-07 after the repository owner asked for this entry. Updated on 2026-10-08 with revision r05 (window apertures), after the repository owner asked for the update.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).
