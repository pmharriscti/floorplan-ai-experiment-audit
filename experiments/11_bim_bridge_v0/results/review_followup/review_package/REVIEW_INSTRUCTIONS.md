# Human review package: bim_bridge_v0

Run `bim_bridge_v0_20260928_183649_UTC`. Package written 20260928_195105 UTC. Model `cubicasa-high-quality-architectural-333-val-region-01`.

**Nothing in this package is a review.** Every object is `CANDIDATE_UNREVIEWED`. The plan scale is
`ASSUMED_FOR_PREVIEW` and is not confirmed. Gates G2 and G6 stay BLOCKED and G7 stays NOT_RUN until a
person records the evidence. This file is for a human reviewer. Do not fill in the record on someone's behalf.

## 1. What to look at

| File | Shows |
| --- | --- |
| `01_overview_full_plan.png` | whole plan overlay |
| `02_overview_region.png` | region overlay with a source-only panel |
| `03_closeup_wall_002.png` | close-up of wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002 |
| `04_closeup_wall_003.png` | close-up of wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003 |
| `05_closeup_wall_004.png` | close-up of wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004 |
| `06_closeup_wall_012.png` | close-up of wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012 |
| `07_closeup_door_opening-c02.png` | close-up of opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02 |
| `08_excluded_aperture_component_01.png` | excluded predicted aperture component |

Each close-up has a source-only panel and an overlay panel. Coordinates in labels are `letterbox_512` pixels,
the space the review record uses.

## 2. Object IDs

Images use the last segment of the object ID as a display label. The exact IDs are:

| Display label | Exact object ID | IFC class | IFC GlobalId |
| --- | --- | --- | --- |
| `wall_002` | `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002` | IfcWall | `1XkaxwpSjJ8Qnf5B_jRxg1` |
| `wall_003` | `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003` | IfcWall | `3d2OAZpCHGUAZ91g4AXd7s` |
| `wall_004` | `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004` | IfcWall | `1b$tabjrHGbPd9xW5BjLOQ` |
| `wall_012` | `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012` | IfcWall | `11mnaExH9O2vr$qGRs3ceQ` |
| `door_opening-c02` | `opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02` | IfcOpeningElement | `1Y$u78JbXJIggJrkmIA5ew` |

## 3. Two automated decisions to check

Neither decision was made or checked by a person.

**wall_012 thickness, 40 px to 4 px.** See `06_closeup_wall_012.png`.

- Object: `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012`
- Made by: `bim_bridge candidates.thickness_from_predicted_mask rule 0.2` (actor type `automated_rule`) at 2026-09-28T18:37:01Z.
- Before: vectorizer thickness 40.0 px. After: 4.0 px.
- Recorded reason: Vectorizer thickness 40.0 px disagrees with the predicted mask by more than 2.0 px; the median perpendicular run on the predicted structural_wall mask is 4.0 px.
- Recorded evidence: candidate_geometry.json diagnostics for wall_012: 70 perpendicular samples, p10-p90 [4.0, 4.0] px
- Measured for this package at row 201: the predicted wall covers x pixels 304..307
  (span 303.5..307.5). The footprint in use spans 302.5..306.5.
  The axis position is therefore also yours to judge, not only the thickness.
- To keep 4 px: `ACCEPT`. To set another value: `ACCEPT_WITH_EDITS` with field `thickness_px`.

**Excluded aperture component 1.** See `08_excluded_aperture_component_01.png`.

- Predicted `door_opening` component 1, 159 px, bbox_px [413, 193, 419, 216].
- Recorded reason: "no selected wall hosts this component".
- Unselected upstream wall axis under it: wall_013. The wall selection was made by an AI assistant.
- It is not an object. It has no ID, no IFC element, and no slot in the review record. If you think it
  belongs in the model, say so in an object's `notes`. Adding it needs a new candidate preparation in a new run.

## 3a. Known limits of the candidates

- Wall height, base elevation, storey elevation, aperture height and sill are preview assumptions.
  They are not reviewable here and an accept decision does not confirm them.
- Semantic score is null for every object. The input is a thresholded mask.
- The images do not show accuracy. No reference geometry or annotation was used.

## 4. How to record decisions

1. Copy the template to a new file. Do not edit the template.

   ```bash
   cp /mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/review_package_20260928_195105_UTC/review_record_TEMPLATE.json /mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/review_package_20260928_195105_UTC/review_record.json
   ```

   The template is a byte-identical copy of `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/candidates/review_record_TEMPLATE.json` (sha256 `72d35f658e0bb8ad86df0f7a22533064eb0b9d38dac88c4be522e181d1cd8718`).
2. Set `reviewer` (your name), `reviewer_role`, and `reviewed_utc` as `YYYY-MM-DDTHH:MM:SSZ`.
3. For each of the 5 objects set `decision` to one of: `ACCEPT`, `ACCEPT_WITH_EDITS`, `REJECT`.
   These become the review states `HUMAN_ACCEPTED`, `HUMAN_ACCEPTED_WITH_EDITS`, `HUMAN_REJECTED`.
4. Use `ACCEPT_WITH_EDITS` to correct an object. List one entry in `edits` per change, each with `field`,
   `after` and `reason` (3 characters or more). Edits are allowed only with `ACCEPT_WITH_EDITS`, and
   `ACCEPT_WITH_EDITS` needs at least one edit.
   - Wall fields: `axis_px.start`, `axis_px.end`, `thickness_px`. `axis_px.start` and `axis_px.end` take `[x, y]`.
   - Aperture fields: `offset_px`, `width_px`, measured along the host wall axis from its start.
   - All values are `letterbox_512` pixels.
5. Do not change `run_id`, `model_id`, `candidate_geometry_sha256`, the `object_id` values, or the list of objects.
   The record is refused if any of them differs, or if any decision is missing.
6. Scale (gate G2). Leave `scale_confirmation.confirmed` as `null` unless you have evidence. To confirm a scale
   set `confirmed` to `true` and give `metres_per_source_px`, `evidence_kind` and `evidence_description`.
   The current estimate, 0.010720 m per source pixel, comes from the area label
   and was derived by an AI assistant. It is not evidence. Do not copy it without your own evidence.

Example of one corrected object (values are placeholders, not a recommendation):

```json
{
  "object_id": "wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012",
  "kind": "wall",
  "decision": "ACCEPT_WITH_EDITS",
  "edits": [{"field": "thickness_px", "after": 5.0, "reason": "<why, from what you saw on the drawing>"}],
  "notes": "<optional>"
}
```

7. Apply the record:

   ```bash
   cd /home/pmharris/dev/bim_bridge_v0
   .venv/bin/python -m bim_bridge apply-review --run-dir /mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC --review /mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/review_package_20260928_195105_UTC/review_record.json
   .venv/bin/python -m bim_bridge export --run-dir /mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC
   .venv/bin/python -m bim_bridge finalize --run-dir /mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC
   ```

   `apply-review` writes a new folder `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/reviewed`. It runs once per run and overwrites nothing.
   `export` without `--preview` writes a metric IFC only if every object is human-reviewed and the scale is evidenced.
   `finalize` writes new numbered gate and report files. Earlier reports stay as they are.

## 5. IFC file and viewer inspection (gate G7)

- IFC: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_preview/cubicasa-high-quality-architectural-333-val-region-01__PREVIEW_CANDIDATE_UNREVIEWED.ifc`
- sha256: `e4def87979953d853790d3c3f63ddde4d4b39f3a7c7a8df7eecb492713dcd09e`
- It is a preview of unreviewed candidates with an assumed scale. It was exported before any review.
- Steps: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/VIEWER_INSPECTION_STEPS.md` (copy in this folder).
- Record template: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/viewer_inspection_record_TEMPLATE.json`. Save the filled record as
  `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/viewer_inspection_record.json`, as the steps say.
- GlobalId map: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_preview/guid_map.json`
