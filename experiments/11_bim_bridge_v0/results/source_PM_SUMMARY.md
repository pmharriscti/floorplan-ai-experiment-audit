# PM summary: bim_bridge_v0

> The meaningful result today is not ‘we generated a 3D picture.’ It is ‘we can turn reviewed prediction-derived geometry into identifiable IFC building elements, preserve uncertainty, and inspect the result.’ That is a concrete step toward the PM’s BIM goal—and it creates a stable destination for the ML improvements that follow.

## What the persisted evidence proves

- The bridge turns a described set of walls into **individually identifiable IFC walls**, each with its own GlobalId, placement, dimensions and storey, and a **hosted opening that really removes wall volume**.
- It does this from **saved model predictions**, with every wall traced to the prediction file and region it came from.
- Identities are stable: exporting again reuses every GlobalId.
- Uncertainty travels with the object inside the IFC: where each value came from, what is assumed, that no confidence score exists, and that nobody has reviewed it.
- The file reopens, passes IFC4 schema validation, and its geometry matches its input.

## What it does not prove

- **Nobody has reviewed the real geometry.** It is a candidate. The reviewed part of the milestone is not met.
- **The real dimensions are not real.** The drawing has no scale, so the plan scale is an estimate and all heights are assumptions.
- **No viewer or BIM application has opened the file.**
- It says nothing about how accurate the segmentation model is, and it is not fit for engineering or inspection use.
- The synthetic example proves the exporter works. It proves nothing about real drawings.

## Status

| Milestone | Status |
| --- | --- |
| technical exporter | PASS |
| reviewed prediction bridge | PARTIAL |
| downstream application acceptance | NOT_RUN |

## What is needed next

1. G6: a human reviewer fills in `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/candidates/review_record_TEMPLATE.json` (one decision per object) and runs `bim-bridge apply-review`. This is one person and about 5 objects.
2. G2: a human supplies or confirms a plan scale with its evidence in the same review record (`scale_confirmation`), for example from a dimensioned version of the drawing or a known room dimension.
3. G7: a person opens the IFC in the target application or a viewer and records the result, following `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/VIEWER_INSPECTION_STEPS.md`. Name the target BIM application first.

## Bottom line

> The meaningful result today is not ‘we generated a 3D picture.’ It is ‘we can turn reviewed prediction-derived geometry into identifiable IFC building elements, preserve uncertainty, and inspect the result.’ That is a concrete step toward the PM’s BIM goal—and it creates a stable destination for the ML improvements that follow.

**The reviewed-prediction IFC milestone remains partial and was NOT demonstrated.** The technical chain from saved predictions to inspectable IFC objects works end to end on unreviewed candidates. It becomes the milestone once a person reviews the five objects and a scale is confirmed.

The required progress is an inspectable, traceable IFC representation of reviewed prediction-derived geometry, not merely a 3D picture.
