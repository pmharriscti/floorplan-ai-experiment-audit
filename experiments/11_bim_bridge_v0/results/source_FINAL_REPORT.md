# bim_bridge_v0 final report

Run `bim_bridge_v0_20260928_183649_UTC`. Written 2026-09-28T18:37:46Z. Bridge version 0.2.0.

## Non-negotiable objective

> The meaningful result today is not ‘we generated a 3D picture.’ It is ‘we can turn reviewed prediction-derived geometry into identifiable IFC building elements, preserve uncertainty, and inspect the result.’ That is a concrete step toward the PM’s BIM goal—and it creates a stable destination for the ML improvements that follow.

This is the acceptance principle. A render, an anonymous mesh, a syntactically valid IFC, or a synthetic-only example does not establish the prediction-to-BIM bridge.

Experiment question: Can a small, explicitly reviewed subset of current floor-plan predictions become individually identifiable IFC walls and a hosted opening, with inspectable dimensions, provenance, uncertainty, and reproducible validation?

## Outcome

| Milestone | Status | Meaning |
| --- | --- | --- |
| technical exporter | **PASS** | The exporter turns a valid building_model.json into a checked IFC4 file. Shown on synthetic geometry. |
| reviewed prediction bridge | **PARTIAL** | Reviewed prediction-derived geometry becomes identifiable IFC elements with evidenced dimensions. |
| downstream application acceptance | **NOT_RUN** | A person opened the file in the target application or a viewer and recorded the result. |

**The reviewed-prediction IFC milestone remains partial and was NOT demonstrated.** Gates not passed on the real track: G2, G6.

These three milestones are different. A pass on one is not a pass on another.

## What was built

- A versioned input contract, `building_model.json` 0.2, with a JSON Schema and semantic checks.
- A coordinate transform module: letterbox inversion, region translation, rotation, y flip, scale.
- Candidate preparation from saved prediction bitmasks, reusing the existing floorplan-synth vectorizer unmodified.
- An editable human review record and a command that applies it. It refuses incomplete records.
- An IFC4 exporter using IfcOpenShell: project, site, building, storey, individual `IfcWall` objects, hosted `IfcOpeningElement`, property sets `AutoAutoCAD_Provenance` and `AutoAutoCAD_ModelProvenance`.
- A persistent object-ID to IFC GlobalId map.
- Checks that reopen the file, validate the schema, and rebuild the geometry with the IfcOpenShell geometry kernel.
- A run directory with stage results, gates, checksums and this report.

## Track A: SYNTHETIC_EXPORT_SMOKE

**Synthetic. This track shows exporter behaviour only. It shows nothing about prediction accuracy, human review, or BIM readiness on company drawings.**

- Technical checks: PASS ({'PASS': 130})
- 5 walls and 1 hosted aperture on a storey raised to 3.0 m, which catches an exporter that applies elevation twice.
- The aperture removed the expected wall volume, confirmed by the geometry kernel.
- Report: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/synthetic/validation_report.md`

| Gate | Meaning | Status | Reason |
| --- | --- | --- | --- |
| G1 | Input identity and provenance established | **PASS** | The fixture is identified and labelled synthetic in the model, the IFC and the report. No real input exists in this track, so this says nothing about real provenance. |
| G2 | Coordinate mapping, units, and scale established | **PASS** | Units are metres, the wall axis is the centreline, storey and base elevation are applied once (raised storey at 3.0 m), and the transform tests pass. Scale does not apply: the geometry is authored in metres. |
| G3 | Schema and geometry checks pass | **PASS** | Input checks 46/46 and geometry-kernel checks 35/35 pass, including the volume removed by the aperture. |
| G4 | IFC identities, relationships, and properties survive reopening | **PASS** | The file was reopened from disk; 49/49 schema, structure, identity and property checks pass; a repeat export reuses every GlobalId. |
| G5 | Uncertainty and assumptions are preserved | **PASS** | 20/20 property checks pass. The semantic score is null with availability UNAVAILABLE and a reason; every object is marked synthetic. |
| G6 | Real prediction lineage and recorded human review are established | **NOT_RUN** | Does not apply to synthetic geometry: there is no prediction and nothing to review. |
| G7 | Actual target application/viewer inspection is recorded | **NOT_RUN** | No viewer or target application was used. |

## Track B: REVIEWED_PREDICTION_BRIDGE

Input: saved Phase 5 predictions of `high_quality_architectural/333` (val split). No inference was run. No threshold was selected. No annotation SVG or ground-truth mask was read.

- Geometry status: **CANDIDATE_UNREVIEWED**. Permitted use: preview_only_not_for_engineering_or_inspection.
- Scale status: **ASSUMED_FOR_PREVIEW**. Dimensional claims permitted: False.
- Metric export of real geometry: **BLOCKED**. No documented, human-confirmed plan scale (scale status ASSUMED_FOR_PREVIEW). No recorded human review (geometry status CANDIDATE_UNREVIEWED).
- A preview file was written and checked: technical checks PASS ({'PASS': 138, 'WARN': 6}).
- Report: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_preview/validation_report.md`

| Measure | Count |
| --- | --- |
| Walls exported / requested | 4 of 4 |
| Apertures exported / requested | 1 of 1 |
| Apertures with a valid host | 1 of 1 |
| Walls tracing to prediction evidence | 4 of 4 |
| Attributes assumed for preview | 11 of 21 |
| Objects reviewed by a human | 0 of 5 |
| Objects with a model semantic score | 0 of 5 |
| Edits by human / agent / automated rule | 0 / 0 / 1 |
| Unresolved geometry diagnostics | 0 |
| Measured correction time | not captured (no human correction took place) |
| Dimensional accuracy | unknown (no reference geometry was used) |

| Gate | Meaning | Status | Reason |
| --- | --- | --- | --- |
| G1 | Input identity and provenance established | **PASS** | Source image, split, sample, prediction file, thresholds, config snapshot and checkpoint are on disk with hashes. The image hash equals the upstream manifest and the checkpoint hash equals audit entry 09. |
| G2 | Coordinate mapping, units, and scale established | **BLOCKED** | BLOCKED on scale. The mapping from image pixels through the letterbox and region of interest to model metres is established and tested, and units are metres. But the drawing has no dimension string and no scale bar, so no documented scale evidence exists. The scale in use is an estimate from the apartment area label, marked ASSUMED_FOR_PREVIEW. No dimensional claim is permitted. |
| G3 | Schema and geometry checks pass | **PASS** | Input checks 66/66 and geometry-kernel checks 29/29 pass on the preview export. These check the file against its input, not against the building. |
| G4 | IFC identities, relationships, and properties survive reopening | **PASS** | The preview file was reopened from disk; 49/49 schema, structure, identity and property checks pass; a repeat export reuses every GlobalId. |
| G5 | Uncertainty and assumptions are preserved | **PASS** | 21/21 property checks pass. Every object carries a null semantic score with a reason, its attribute origins, its assumptions, its diagnostics, its edits and its review state inside the IFC. |
| G6 | Real prediction lineage and recorded human review are established | **BLOCKED** | BLOCKED on human review. Prediction lineage is established: every wall names the prediction mask region it came from. But no human has reviewed this geometry. Every object is CANDIDATE_UNREVIEWED. Adjustments made by automated rules are recorded as edits and are not a review. |
| G7 | Actual target application/viewer inspection is recorded | **NOT_RUN** | No viewer or target application is available in this environment (Blender is installed without an IFC add-on). Nobody has opened the file in a viewer. The independent parser check is not a viewer test. |

## Manual inputs, corrections and assumptions

- Human inputs: none. No human reviewed or edited the geometry.
- Agent inputs: the area label `1 H+K+S 39.5 M2` was read from the source image by an AI assistant, and the wall selection was chosen by the same assistant. Both are recorded in the configuration.
- Edits by automated rule: 1.
  - `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012` `thickness`: `{"thickness_px": 40.0}` -> `{"thickness_px": 4.0}`. Vectorizer thickness 40.0 px disagrees with the predicted mask by more than 2.0 px; the median perpendicular run on the predicted structural_wall mask is 4.0 px.
- Assumed for preview: every wall height, wall base elevation, storey elevation, aperture height and aperture bottom elevation, from the configuration profile `preview_vertical_defaults_v0`.
- Plan scale: an estimate from the apartment area label, marked ASSUMED_FOR_PREVIEW and not human-confirmed.
- Semantic confidence: null for every object. The input is a thresholded mask; no score was derived from pixels, IoU, F1 or a successful export.
- No overall confidence is computed.

Predicted aperture components inside the region that were not exported:

- component 1 (159 px): no selected wall hosts this component

## Automated tests

- Total 130, passed 130, failed 0, errors 0, skipped 0.
- Expected negative tests (the bridge must refuse or flag bad input): 76. They are counted among the passed tests.
- Results: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/tests/pytest_junit.xml`

## Independent parser cross-check

A second IFC engine, web-ifc, parsed and tessellated the files. **This is not a viewer test.**

- synthetic: PASS (23 passed, 0 failed)
- real: PASS (19 passed, 0 failed)

## Viewer and target application

- Status: **NOT_RUN**. No viewer or target application is available in this environment (Blender is installed without an IFC add-on). Nobody has opened the file in a viewer. The independent parser check is not a viewer test.
- No screenshot exists. None was fabricated.
- Inspection steps for a person: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/VIEWER_INSPECTION_STEPS.md`

## What this experiment does not claim

- No new wall IoU, no segmentation improvement, no training comparison and no broad reliability claim.
- No dimensional accuracy. Without reference geometry, accuracy is unknown.
- No fitness for engineering, inspection or construction use.
- No conformance to a model view definition.

## Next smallest actions

1. G6: a human reviewer fills in `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/candidates/review_record_TEMPLATE.json` (one decision per object) and runs `bim-bridge apply-review`. This is one person and about 5 objects.
2. G2: a human supplies or confirms a plan scale with its evidence in the same review record (`scale_confirmation`), for example from a dimensioned version of the drawing or a known room dimension.
3. G7: a person opens the IFC in the target application or a viewer and records the result, following `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/VIEWER_INSPECTION_STEPS.md`. Name the target BIM application first.

## Reproduce

```bash
cd /home/pmharris/dev/bim_bridge_v0
.venv/bin/python -m bim_bridge new-run --config /home/pmharris/dev/bim_bridge_v0/configs/bim_bridge_v0.yaml            # prints the new run directory
RUN=/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC
.venv/bin/python -m bim_bridge inspect --run-dir $RUN
.venv/bin/python -m bim_bridge synthetic --run-dir $RUN
.venv/bin/python -m bim_bridge prepare-candidates --run-dir $RUN
.venv/bin/python -m bim_bridge export --run-dir $RUN --preview
.venv/bin/python -m bim_bridge independent-parser --run-dir $RUN
.venv/bin/python -m bim_bridge test --run-dir $RUN
.venv/bin/python -m bim_bridge finalize --run-dir $RUN
# after a human fills in the review record:
# .venv/bin/python -m bim_bridge apply-review --run-dir $RUN --review <review_record.json>
```

## Paths

- Run directory: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC`
- Input inventory: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/inputs/INPUT_INVENTORY.md`
- Gates: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/gates.json`
- Stage results: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/stages`
- Checksums: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/checksums.sha256`
- Source code: `/home/pmharris/dev/bim_bridge_v0`
- Upstream artifacts (read-only, not copied): `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED`
