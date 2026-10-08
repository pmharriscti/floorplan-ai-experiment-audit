# Validation report: cc-high-quality--4712-p01 (REVIEWED_PREDICTION_BRIDGE)

> The meaningful result today is not ‘we generated a 3D picture.’ It is ‘we can turn reviewed prediction-derived geometry into identifiable IFC building elements, preserve uncertainty, and inspect the result.’ That is a concrete step toward the PM’s BIM goal—and it creates a stable destination for the ML improvements that follow.

**REAL PREDICTION-DERIVED GEOMETRY. Geometry status CANDIDATE_UNREVIEWED. Scale status ASSUMED_FOR_PREVIEW. Permitted use: preview_only_not_for_engineering_or_inspection.**

CANDIDATE_UNREVIEWED, PREVIEW ONLY, SCALE ASSUMED_FOR_PREVIEW: 14 straight walls and 13 aperture(s) from the saved Phase 5 prediction of source plan high_quality/4712 (whole-plan attempt after candidate repair). Arbitrary visualization scale; no dimensional, construction or inspection claim.

- Technical checks: **FAIL** (267 checks: 1 FAIL, 238 PASS, 28 WARN)
- A technical PASS means the file matches its input and passes schema and geometry checks. It is not a reviewed prediction bridge and not downstream acceptance.
- Run: `bim_bridge_pm_comparison_v0_20261006_130747_UTC`; model timestamp 2026-10-08T13:18:26Z
- Tooling: bim_bridge_v0 0.2.0, IfcOpenShell 0.8.5, Python 3.12.3
- IFC schema: IFC4 (Prototype choice. No receiving BIM application or accepted IFC schema is documented in the inspected repositories.) Target application: null; compatibility UNVERIFIED.
- Length unit: metre. Scale: `ASSUMED_FOR_PREVIEW`, metres per source pixel 0.0100. Dimensional claims permitted: False.
- Scale note: ARBITRARY VISUALIZATION SCALE. No verified plan scale exists for this source. 1 original raster pixel is drawn as 0.01 preview metres so the model has a viewable size. This is not a measurement and not a claim about the dataset or the building. Metric export stays BLOCKED.

## Files

- source_building_model: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_pm_comparison_v0/bim_bridge_pm_comparison_v0_20261006_130747_UTC/samples/cc-01/building_model_r05.json`
- guid_map_started_from: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_pm_comparison_v0/bim_bridge_pm_comparison_v0_20261006_130747_UTC/samples/cc-01/export_candidate_preview_whole_plan_r04/guid_map.json`
- building_model: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_pm_comparison_v0/bim_bridge_pm_comparison_v0_20261006_130747_UTC/samples/cc-01/export_candidate_preview_whole_plan_r05/building_model.json`
- ifc: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_pm_comparison_v0/bim_bridge_pm_comparison_v0_20261006_130747_UTC/samples/cc-01/export_candidate_preview_whole_plan_r05/cc-high-quality--4712-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r05.ifc`
- guid_map: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_pm_comparison_v0/bim_bridge_pm_comparison_v0_20261006_130747_UTC/samples/cc-01/export_candidate_preview_whole_plan_r05/guid_map.json`
- report_json: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_pm_comparison_v0/bim_bridge_pm_comparison_v0_20261006_130747_UTC/samples/cc-01/export_candidate_preview_whole_plan_r05/validation_report.json`
- report_markdown: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_pm_comparison_v0/bim_bridge_pm_comparison_v0_20261006_130747_UTC/samples/cc-01/export_candidate_preview_whole_plan_r05/validation_report.md`

## Counts

| Measure | Count |
| --- | --- |
| Walls exported / requested | 0 of 14 |
| Apertures exported / requested | 0 of 13 |
| Apertures with a valid host | 13 of 13 |
| Walls tracing to prediction evidence | 14 of 14 |
| Attributes assumed for preview | 55 of 109 |
| Objects reviewed by a human | 0 of 27 |
| Objects with a model semantic score | 0 of 27 |
| Edits by human / agent / automated rule | 0 / 0 / 62 |
| Unresolved geometry diagnostics | 11 |
| Measured correction time | not captured |

## Attribute origins

Origin says where a value came from. It says nothing about whether anyone verified it; review is recorded separately.

| Origin | Attributes |
| --- | ---: |
| predicted by the model | 0 |
| derived from prediction geometry | 54 |
| manually entered | 0 |
| assumed for preview (no evidence) | 55 |
| unknown (null) | 0 |
| synthetic fixture | 0 |
| **total** | **109** |

## Objects

### wall `wall:cc-high-quality--4712-p01:wall_001`

Candidate wall wall_001 (merged: wall_001, wall_002, wall_003). Centreline length 11.4782 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (1.1346, 12.6568) -> (12.6129, 12.6568) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_001). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1055 m | derived_from_geometry | Vectorizer thickness 4.0 px, consistent with 4.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 436 of 436 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 4.0 px; predicted-mask median 4.0 px; vectorizer proposed 4.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.5 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 4.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `PASS` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [4.0, 5.0] px (spread 1.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_012'].
- `PASS` endpoint_supported[end]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_022'].
- `WARN` corner_fill_at_junctions: 2 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 5 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [242.0, 22.8125], "start": [45.0, 22.8125]}, "orientation": "horizontal", "source": "vectorizer output, unedited", "thickness_px": 4.0}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [45.0, 22.8125], "end": [242.0, 22.8125]}, "thickness_px": 4.0}` -> `{"axis_px": {"start": [45.0, 22.8125], "end": [257.0, 22.8125]}, "thickness_px": 4.0}`. R2 end extension: the predicted structural_wall mask continues 15 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [45.0, 22.8125], "end": [257.0, 22.8125]}, "thickness_px": 4.0}` -> `{"axis_px": {"start": [45.0, 22.3125], "end": [257.0, 22.3125]}, "thickness_px": 4.0}`. R3 recentre after R2 extension of end: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset -0.5 px).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [45.0, 22.3125], "end": [257.0, 22.3125]}, "thickness_px": 4.0}` -> `{"axis_px": {"start": [43.0, 22.3125], "end": [257.0, 22.3125]}, "thickness_px": 4.0}`. R2 end extension: the predicted structural_wall mask continues 2 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [43.0, 22.3125], "end": [257.0, 22.3125]}, "thickness_px": 4.0}` -> `{"axis_px": {"start": [43.0, 22.8125], "end": [257.0, 22.8125]}, "thickness_px": 4.0}`. R3 recentre after R2 extension of start: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).
- Edit of `repair:R1_merge` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"kept": {"id": "wall_001", "axis_px": {"start": [43.0, 22.8125], "end": [257.0, 22.8125]}, "thickness_px": 4.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 4.0 px, consistent with 4.0 px measured on the predicted structural_wall mask."}, "merged": {"id": "wall_002", "axis_px": {"start": [236.0, 22.0], "end": [377.0, 22.0]}, "thickness_px": 5.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 5.0 px, consistent with 5.0 px measured on the predicted structural_wall mask."}}` -> `{"axis_px": {"start": [43.0, 22.489788732394366], "end": [377.0, 22.489788732394366]}, "thickness_px": 4.0}`. R1 collinear merge with wall_002: parallel axes 0.81 px apart, gap -21.0 px along the axis, 100% of the gap on predicted structural_wall pixels. One wall now spans both segments.
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [43.0, 22.489788732394366], "end": [377.0, 22.489788732394366]}, "thickness_px": 4.0}` -> `{"axis_px": {"start": [43.0, 22.989788732394366], "end": [377.0, 22.989788732394366]}, "thickness_px": 4.0}`. R3 recentre after R1 merge with wall_002: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).
- Edit of `repair:R1_merge` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"kept": {"id": "wall_001", "axis_px": {"start": [43.0, 22.989788732394366], "end": [377.0, 22.989788732394366]}, "thickness_px": 4.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 4.0 px, consistent with 4.0 px measured on the predicted structural_wall mask."}, "merged": {"id": "wall_003", "axis_px": {"start": [325.0, 22.5], "end": [478.0, 22.5]}, "thickness_px": 4.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 4.0 px, consistent with 4.0 px measured on the predicted structural_wall mask."}}` -> `{"axis_px": {"start": [43.0, 22.835912600861846], "end": [478.0, 22.835912600861846]}, "thickness_px": 4.0}`. R1 collinear merge with wall_003: parallel axes 0.49 px apart, gap -52.0 px along the axis, 100% of the gap on predicted structural_wall pixels. One wall now spans both segments.
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [43.0, 22.835912600861846], "end": [478.0, 22.835912600861846]}, "thickness_px": 4.0}` -> `{"axis_px": {"start": [43.0, 22.335912600861846], "end": [478.0, 22.335912600861846]}, "thickness_px": 4.0}`. R3 recentre after R1 merge with wall_003: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset -0.5 px).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_004`

Candidate wall wall_004 (merged: wall_004, wall_005, wall_006). Centreline length 11.3859 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (1.2006, 7.7864) -> (12.5865, 7.7864) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_004). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.2639 m | derived_from_geometry | Vectorizer thickness 10.0 px, consistent with 10.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 432 of 432 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 10.0 px; predicted-mask median 9.0 px; vectorizer proposed 10.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: -0.5 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 10.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `PASS` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [9.0, 10.0] px (spread 1.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_012', 'wall_014'].
- `PASS` endpoint_supported[end]: free end: the predicted wall also stops here. Touching candidates: none.
- `PASS` corner_fill_at_junctions: 2 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [473.0, 205.0], "start": [359.0, 205.0]}, "orientation": "horizontal", "source": "vectorizer output, unedited", "thickness_px": 10.0}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [359.0, 205.0], "end": [473.0, 205.0]}, "thickness_px": 10.0}` -> `{"axis_px": {"start": [359.0, 205.0], "end": [477.0, 205.0]}, "thickness_px": 10.0}`. R2 end extension: the predicted structural_wall mask continues 4 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [359.0, 205.0], "end": [477.0, 205.0]}, "thickness_px": 10.0}` -> `{"axis_px": {"start": [359.0, 205.5], "end": [477.0, 205.5]}, "thickness_px": 10.0}`. R3 recentre after R2 extension of end: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [359.0, 205.5], "end": [477.0, 205.5]}, "thickness_px": 10.0}` -> `{"axis_px": {"start": [319.0, 205.5], "end": [477.0, 205.5]}, "thickness_px": 10.0}`. R2 end extension: the predicted structural_wall mask continues 40 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [319.0, 205.5], "end": [477.0, 205.5]}, "thickness_px": 10.0}` -> `{"axis_px": {"start": [319.0, 206.0], "end": [477.0, 206.0]}, "thickness_px": 10.0}`. R3 recentre after R2 extension of start: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).
- Edit of `repair:R1_merge` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"kept": {"id": "wall_004", "axis_px": {"start": [319.0, 206.0], "end": [477.0, 206.0]}, "thickness_px": 10.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 10.0 px, consistent with 10.0 px measured on the predicted structural_wall mask."}, "merged": {"id": "wall_005", "axis_px": {"start": [159.0, 206.0], "end": [375.0, 206.0]}, "thickness_px": 9.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 9.0 px, consistent with 9.0 px measured on the predicted structural_wall mask."}}` -> `{"axis_px": {"start": [159.0, 206.0], "end": [477.0, 206.0]}, "thickness_px": 10.0}`. R1 collinear merge with wall_005: parallel axes 0.00 px apart, gap -56.0 px along the axis, 100% of the gap on predicted structural_wall pixels. One wall now spans both segments.
- Edit of `repair:R1_merge` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"kept": {"id": "wall_004", "axis_px": {"start": [159.0, 206.0], "end": [477.0, 206.0]}, "thickness_px": 10.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 10.0 px, consistent with 10.0 px measured on the predicted structural_wall mask."}, "merged": {"id": "wall_006", "axis_px": {"start": [45.5, 207.8173741921094], "end": [138.99952217485878, 207.8173741921094]}, "thickness_px": 9.5, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 9.5 px, consistent with 9.0 px measured on the predicted structural_wall mask."}}` -> `{"axis_px": {"start": [45.5, 206.4129375841728], "end": [477.0, 206.4129375841728]}, "thickness_px": 10.0}`. R1 collinear merge with wall_006: parallel axes 1.82 px apart, gap 20.0 px along the axis, 100% of the gap on predicted structural_wall pixels. One wall now spans both segments and the gap.
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [45.5, 206.4129375841728], "end": [477.0, 206.4129375841728]}, "thickness_px": 10.0}` -> `{"axis_px": {"start": [45.5, 206.9129375841728], "end": [477.0, 206.9129375841728]}, "thickness_px": 10.0}`. R3 recentre after R1 merge with wall_006: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_007`

Candidate wall wall_007 (horizontal). Centreline length 2.1637 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (5.4357, 5.5412) -> (7.5994, 5.5412) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_007). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1319 m | derived_from_geometry | Median perpendicular run 5.0 px on the predicted structural_wall mask; the vectorizer value 24.0 px was replaced by an automated rule. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 83 of 83 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 5.0 px; predicted-mask median 5.0 px; vectorizer proposed 24.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.0 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 24.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `PASS` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [5.0, 5.0] px (spread 0.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_016'].
- `PASS` endpoint_supported[end]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_008'].
- `PASS` corner_fill_at_junctions: 2 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [279.0, 292.0], "start": [208.0, 292.0]}, "orientation": "horizontal", "source": "vectorizer output, unedited", "thickness_px": 24.0}`

- Edit of `thickness` by **automated_rule** (bim_bridge candidates.thickness_from_predicted_mask rule 0.2) at 2026-10-08T13:18:26Z: `{"thickness_px": 24.0}` -> `{"thickness_px": 5.0}`. Vectorizer thickness 24.0 px disagrees with the predicted mask by more than 2.0 px; the median perpendicular run on the predicted structural_wall mask of THIS plan is 5.0 px.
- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [208.0, 292.0], "end": [279.0, 292.0]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [208.0, 292.0], "end": [288.0, 292.0]}, "thickness_px": 5.0}`. R2 end extension: the predicted structural_wall mask continues 9 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [208.0, 292.0], "end": [288.0, 292.0]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [206.0, 292.0], "end": [288.0, 292.0]}, "thickness_px": 5.0}`. R2 end extension: the predicted structural_wall mask continues 2 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_008`

Candidate wall wall_008 (horizontal). Centreline length 1.4513 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (7.3091, 5.2773) -> (8.7604, 5.2773) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_008). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.6861 m | derived_from_geometry | Vectorizer thickness 26.0 px, consistent with 26.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 56 of 56 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 26.0 px; predicted-mask median 26.0 px; vectorizer proposed 26.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.5 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 26.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `PASS` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [26.0, 26.0] px (spread 0.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_017'].
- `PASS` endpoint_supported[end]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_018'].
- `PASS` corner_fill_at_junctions: 3 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [320.0, 302.0], "start": [289.0, 302.0]}, "orientation": "horizontal", "source": "vectorizer output, unedited", "thickness_px": 26.0}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [289.0, 302.0], "end": [320.0, 302.0]}, "thickness_px": 26.0}` -> `{"axis_px": {"start": [289.0, 302.0], "end": [332.0, 302.0]}, "thickness_px": 26.0}`. R2 end extension: the predicted structural_wall mask continues 12 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [289.0, 302.0], "end": [332.0, 302.0]}, "thickness_px": 26.0}` -> `{"axis_px": {"start": [289.0, 302.5], "end": [332.0, 302.5]}, "thickness_px": 26.0}`. R3 recentre after R2 extension of end: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [289.0, 302.5], "end": [332.0, 302.5]}, "thickness_px": 26.0}` -> `{"axis_px": {"start": [277.0, 302.5], "end": [332.0, 302.5]}, "thickness_px": 26.0}`. R2 end extension: the predicted structural_wall mask continues 12 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [277.0, 302.5], "end": [332.0, 302.5]}, "thickness_px": 26.0}` -> `{"axis_px": {"start": [277.0, 302.0], "end": [332.0, 302.0]}, "thickness_px": 26.0}`. R3 recentre after R2 extension of start: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset -0.5 px).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_009`

Candidate wall wall_009 (merged: wall_009, wall_010). Centreline length 3.3247 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (5.4357, 3.2192) -> (8.7604, 3.2192) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_009). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1319 m | derived_from_geometry | Vectorizer thickness 5.0 px, consistent with 5.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 127 of 127 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 5.0 px; predicted-mask median 5.0 px; vectorizer proposed 5.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.0 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 5.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `PASS` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [4.0, 5.0] px (spread 1.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: free end: the predicted wall also stops here. Touching candidates: none.
- `PASS` endpoint_supported[end]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_018'].
- `PASS` corner_fill_at_junctions: 1 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [257.0, 380.0], "start": [209.0, 380.0]}, "orientation": "horizontal", "source": "vectorizer output, unedited", "thickness_px": 5.0}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [209.0, 380.0], "end": [257.0, 380.0]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [209.0, 380.0], "end": [259.0, 380.0]}, "thickness_px": 5.0}`. R2 end extension: the predicted structural_wall mask continues 2 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [209.0, 380.0], "end": [259.0, 380.0]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [206.0, 380.0], "end": [259.0, 380.0]}, "thickness_px": 5.0}`. R2 end extension: the predicted structural_wall mask continues 3 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R1_merge` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"kept": {"id": "wall_009", "axis_px": {"start": [206.0, 380.0], "end": [259.0, 380.0]}, "thickness_px": 5.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 5.0 px, consistent with 5.0 px measured on the predicted structural_wall mask."}, "merged": {"id": "wall_010", "axis_px": {"start": [272.0, 380.0], "end": [332.0, 380.0]}, "thickness_px": 5.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 5.0 px, consistent with 5.0 px measured on the predicted structural_wall mask."}}` -> `{"axis_px": {"start": [206.0, 380.0], "end": [332.0, 380.0]}, "thickness_px": 5.0}`. R1 collinear merge with wall_010: parallel axes 0.00 px apart, gap 13.0 px along the axis, 100% of the gap on predicted structural_wall pixels. One wall now spans both segments and the gap.

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_011`

Candidate wall wall_011 (horizontal). Centreline length 11.3628 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (1.2138, 1.1775) -> (12.5766, 1.1775) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_011). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.2111 m | derived_from_geometry | Vectorizer thickness 8.0 px, consistent with 8.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 431 of 431 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 8.0 px; predicted-mask median 8.0 px; vectorizer proposed 8.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.0 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 8.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `PASS` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [8.0, 9.0] px (spread 1.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_014'].
- `PASS` endpoint_supported[end]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_021'].
- `PASS` corner_fill_at_junctions: 2 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [472.625, 456.375], "start": [51.0, 456.375]}, "orientation": "horizontal", "source": "vectorizer output, unedited", "thickness_px": 8.0}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [51.0, 456.375], "end": [472.625, 456.375]}, "thickness_px": 8.0}` -> `{"axis_px": {"start": [51.0, 456.375], "end": [476.625, 456.375]}, "thickness_px": 8.0}`. R2 end extension: the predicted structural_wall mask continues 4 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [51.0, 456.375], "end": [476.625, 456.375]}, "thickness_px": 8.0}` -> `{"axis_px": {"start": [51.0, 457.375], "end": [476.625, 457.375]}, "thickness_px": 8.0}`. R3 recentre after R2 extension of end: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 1.0 px).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [51.0, 457.375], "end": [476.625, 457.375]}, "thickness_px": 8.0}` -> `{"axis_px": {"start": [46.0, 457.375], "end": [476.625, 457.375]}, "thickness_px": 8.0}`. R2 end extension: the predicted structural_wall mask continues 5 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_012`

Candidate wall wall_012 (merged: wall_012, wall_013). Centreline length 4.9129 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (1.2039, 7.7841) -> (1.2039, 12.6970) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_012). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1319 m | derived_from_geometry | Vectorizer thickness 5.0 px, consistent with 5.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 187 of 187 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 5.0 px; predicted-mask median 5.0 px; vectorizer proposed 5.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: -0.5 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 5.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `PASS` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [4.0, 6.0] px (spread 2.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_004', 'wall_014'].
- `PASS` endpoint_supported[end]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_001'].
- `PASS` corner_fill_at_junctions: 5 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [45.0, 22.8125], "start": [45.0, 139.0]}, "orientation": "vertical", "source": "vectorizer output, unedited", "thickness_px": 5.0}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [45.0, 139.0], "end": [45.0, 22.8125]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [45.0, 139.0], "end": [45.0, 20.8125]}, "thickness_px": 5.0}`. R2 end extension: the predicted structural_wall mask continues 2 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [45.0, 139.0], "end": [45.0, 20.8125]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [45.0, 150.0], "end": [45.0, 20.8125]}, "thickness_px": 5.0}`. R2 end extension: the predicted structural_wall mask continues 11 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [45.0, 150.0], "end": [45.0, 20.8125]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [45.5, 150.0], "end": [45.5, 20.8125]}, "thickness_px": 5.0}`. R3 recentre after R2 extension of start: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).
- Edit of `repair:R1_merge` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"kept": {"id": "wall_012", "axis_px": {"start": [45.5, 150.0], "end": [45.5, 20.8125]}, "thickness_px": 5.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 5.0 px, consistent with 5.0 px measured on the predicted structural_wall mask."}, "merged": {"id": "wall_013", "axis_px": {"start": [47.5, 148.0], "end": [47.5, 207.0]}, "thickness_px": 6.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 6.0 px, consistent with 6.0 px measured on the predicted structural_wall mask."}}` -> `{"axis_px": {"start": [46.12703420790435, 207.0], "end": [46.12703420790435, 20.8125]}, "thickness_px": 5.0}`. R1 collinear merge with wall_013: parallel axes 2.00 px apart, gap -2.0 px along the axis, 100% of the gap on predicted structural_wall pixels. One wall now spans both segments.
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [46.12703420790435, 207.0], "end": [46.12703420790435, 20.8125]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [45.62703420790435, 207.0], "end": [45.62703420790435, 20.8125]}, "thickness_px": 5.0}`. R3 recentre after R1 merge with wall_013: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset -0.5 px).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_014`

Candidate wall wall_014 (vertical). Centreline length 6.6890 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (1.3126, 1.1874) -> (1.3126, 7.8764) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_014). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.2375 m | derived_from_geometry | Vectorizer thickness 9.0 px, consistent with 9.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 254 of 254 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 9.0 px; predicted-mask median 9.0 px; vectorizer proposed 9.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.0 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 9.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `PASS` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [9.0, 9.0] px (spread 0.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_011'].
- `WARN` endpoint_supported[end]: predicted wall continues past this endpoint (5 of 6 probe pixels are wall and are covered by no candidate): the wall may be truncated. Touching candidates: ['wall_004', 'wall_012'].
- `WARN` corner_fill_at_junctions: 6 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 8 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [49.5, 207.5], "start": [50.0, 417.0]}, "orientation": "vertical", "source": "vectorizer output, unedited", "thickness_px": 9.0}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [50.0, 417.0], "end": [49.5, 207.5]}, "thickness_px": 9.0}` -> `{"axis_px": {"start": [50.0, 417.0], "end": [49.49045348780908, 203.5000113920031]}, "thickness_px": 9.0}`. R2 end extension: the predicted structural_wall mask continues 4 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [50.0, 417.0], "end": [49.49045348780908, 203.5000113920031]}, "thickness_px": 9.0}` -> `{"axis_px": {"start": [49.74522674390454, 417.0], "end": [49.74522674390454, 203.5000113920031]}, "thickness_px": 9.0}`. R3 recentre after R2 extension of end: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.0 px).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [49.74522674390454, 417.0], "end": [49.74522674390454, 203.5000113920031]}, "thickness_px": 9.0}` -> `{"axis_px": {"start": [49.74522674390454, 457.0], "end": [49.74522674390454, 203.5000113920031]}, "thickness_px": 9.0}`. R2 end extension: the predicted structural_wall mask continues 40 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_015`

Candidate wall wall_015 (vertical). Centreline length 2.3220 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (5.4752, 7.2036) -> (5.4752, 9.5256) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_015). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1055 m | derived_from_geometry | Vectorizer thickness 4.0 px, consistent with 4.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 89 of 89 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 4.0 px; predicted-mask median 4.0 px; vectorizer proposed 4.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: -0.5 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 4.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `WARN` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [4.0, 83.60000000000028] px (spread 79.60000000000028). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: free end: the predicted wall also stops here. Touching candidates: none.
- `PASS` endpoint_supported[end]: free end: the predicted wall also stops here. Touching candidates: none.
- `PASS` corner_fill_at_junctions: 0 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [207.0, 141.0], "start": [207.0, 227.0]}, "orientation": "vertical", "source": "vectorizer output, unedited", "thickness_px": 4.0}`

- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [207.0, 227.0], "end": [207.0, 141.0]}, "thickness_px": 4.0}` -> `{"axis_px": {"start": [207.0, 229.0], "end": [207.0, 141.0]}, "thickness_px": 4.0}`. R2 end extension: the predicted structural_wall mask continues 2 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [207.0, 229.0], "end": [207.0, 141.0]}, "thickness_px": 4.0}` -> `{"axis_px": {"start": [207.5, 229.0], "end": [207.5, 141.0]}, "thickness_px": 4.0}`. R3 recentre after R2 extension of start: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_016`

Candidate wall wall_016 (vertical). Centreline length 2.2165 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (5.4884, 4.0108) -> (5.4884, 6.2273) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_016). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1319 m | derived_from_geometry | Vectorizer thickness 5.0 px, consistent with 5.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 85 of 85 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 5.0 px; predicted-mask median 5.0 px; vectorizer proposed 5.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.0 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 5.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `PASS` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [5.0, 5.0] px (spread 0.0). A large spread means one constant thickness is a poor fit.
- `WARN` endpoint_supported[start]: predicted wall continues past this endpoint (6 of 6 probe pixels are wall and are covered by no candidate): the wall may be truncated. Touching candidates: none.
- `WARN` endpoint_supported[end]: predicted wall continues past this endpoint (3 of 6 probe pixels are wall and are covered by no candidate): the wall may be truncated. Touching candidates: none.
- `PASS` corner_fill_at_junctions: 1 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [208.0, 268.0], "start": [208.0, 348.0]}, "orientation": "vertical", "source": "vectorizer output, unedited", "thickness_px": 5.0}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [208.0, 348.0], "end": [208.0, 268.0]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [208.0, 348.0], "end": [208.0, 266.0]}, "thickness_px": 5.0}`. R2 end extension: the predicted structural_wall mask continues 2 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [208.0, 348.0], "end": [208.0, 266.0]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [208.0, 350.0], "end": [208.0, 266.0]}, "thickness_px": 5.0}`. R2 end extension: the predicted structural_wall mask continues 2 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_017`

Candidate wall wall_017 (vertical). Centreline length 2.4276 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (7.3619, 5.5940) -> (7.3619, 3.1664) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_017). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1319 m | derived_from_geometry | Median perpendicular run 5.0 px on the predicted structural_wall mask; the vectorizer value 19.0 px was replaced by an automated rule. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 93 of 93 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 5.0 px; predicted-mask median 5.0 px; vectorizer proposed 19.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.0 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 19.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `WARN` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [4.0, 56.0] px (spread 52.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_007', 'wall_008'].
- `PASS` endpoint_supported[end]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_009'].
- `PASS` corner_fill_at_junctions: 4 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [279.0, 380.0], "start": [279.0, 316.0]}, "orientation": "vertical", "source": "vectorizer output, unedited", "thickness_px": 19.0}`

- Edit of `thickness` by **automated_rule** (bim_bridge candidates.thickness_from_predicted_mask rule 0.2) at 2026-10-08T13:18:26Z: `{"thickness_px": 19.0}` -> `{"thickness_px": 5.0}`. Vectorizer thickness 19.0 px disagrees with the predicted mask by more than 2.0 px; the median perpendicular run on the predicted structural_wall mask of THIS plan is 5.0 px.
- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [279.0, 316.0], "end": [279.0, 380.0]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [279.0, 316.0], "end": [279.0, 382.0]}, "thickness_px": 5.0}`. R2 end extension: the predicted structural_wall mask continues 2 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [279.0, 316.0], "end": [279.0, 382.0]}, "thickness_px": 5.0}` -> `{"axis_px": {"start": [279.0, 290.0], "end": [279.0, 382.0]}, "thickness_px": 5.0}`. R2 end extension: the predicted structural_wall mask continues 26 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_018`

Candidate wall wall_018 (merged: wall_018, wall_019, wall_020). Centreline length 6.5274 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (8.7126, 1.0720) -> (8.7126, 7.5994) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_018). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1187 m | derived_from_geometry | Vectorizer thickness 4.5 px, consistent with 4.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 248 of 248 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 4.5 px; predicted-mask median 5.0 px; vectorizer proposed 4.5 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.5 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 4.5 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `WARN` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [4.0, 56.0] px (spread 52.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_011'].
- `PASS` endpoint_supported[end]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: none.
- `PASS` corner_fill_at_junctions: 3 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [330.0, 254.0], "start": [330.0, 291.0]}, "orientation": "vertical", "source": "vectorizer output, unedited", "thickness_px": 4.5}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [330.0, 291.0], "end": [330.0, 254.0]}, "thickness_px": 4.5}` -> `{"axis_px": {"start": [330.0, 291.0], "end": [330.0, 214.0]}, "thickness_px": 4.5}`. R2 end extension: the predicted structural_wall mask continues 40 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [330.0, 291.0], "end": [330.0, 214.0]}, "thickness_px": 4.5}` -> `{"axis_px": {"start": [330.5, 291.0], "end": [330.5, 214.0]}, "thickness_px": 4.5}`. R3 recentre after R2 extension of end: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [330.5, 291.0], "end": [330.5, 214.0]}, "thickness_px": 4.5}` -> `{"axis_px": {"start": [330.5, 331.0], "end": [330.5, 214.0]}, "thickness_px": 4.5}`. R2 end extension: the predicted structural_wall mask continues 40 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [330.5, 331.0], "end": [330.5, 214.0]}, "thickness_px": 4.5}` -> `{"axis_px": {"start": [331.0, 331.0], "end": [331.0, 214.0]}, "thickness_px": 4.5}`. R3 recentre after R2 extension of start: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).
- Edit of `repair:R1_merge` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"kept": {"id": "wall_018", "axis_px": {"start": [331.0, 331.0], "end": [331.0, 214.0]}, "thickness_px": 4.5, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 4.5 px, consistent with 4.0 px measured on the predicted structural_wall mask."}, "merged": {"id": "wall_019", "axis_px": {"start": [331.0, 273.0], "end": [331.0, 401.0]}, "thickness_px": 4.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 4.0 px, consistent with 4.0 px measured on the predicted structural_wall mask."}}` -> `{"axis_px": {"start": [331.0, 401.0], "end": [331.0, 214.0]}, "thickness_px": 4.5}`. R1 collinear merge with wall_019: parallel axes 0.00 px apart, gap -58.0 px along the axis, 100% of the gap on predicted structural_wall pixels. One wall now spans both segments.
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [331.0, 401.0], "end": [331.0, 214.0]}, "thickness_px": 4.5}` -> `{"axis_px": {"start": [330.5, 401.0], "end": [330.5, 214.0]}, "thickness_px": 4.5}`. R3 recentre after R1 merge with wall_019: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset -0.5 px).
- Edit of `repair:R1_merge` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"kept": {"id": "wall_018", "axis_px": {"start": [330.5, 401.0], "end": [330.5, 214.0]}, "thickness_px": 4.5, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 4.5 px, consistent with 4.0 px measured on the predicted structural_wall mask."}, "merged": {"id": "wall_020", "axis_px": {"start": [331.0, 461.375], "end": [331.0, 349.0]}, "thickness_px": 5.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 5.0 px, consistent with 5.0 px measured on the predicted structural_wall mask."}}` -> `{"axis_px": {"start": [330.68768267223385, 461.375], "end": [330.68768267223385, 214.0]}, "thickness_px": 4.5}`. R1 collinear merge with wall_020: parallel axes 0.50 px apart, gap -52.0 px along the axis, 100% of the gap on predicted structural_wall pixels. One wall now spans both segments.
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [330.68768267223385, 461.375], "end": [330.68768267223385, 214.0]}, "thickness_px": 4.5}` -> `{"axis_px": {"start": [330.18768267223385, 461.375], "end": [330.18768267223385, 214.0]}, "thickness_px": 4.5}`. R3 recentre after R1 merge with wall_020: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset -0.5 px).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_021`

Candidate wall wall_021 (vertical). Centreline length 6.1580 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (12.4710, 7.2563) -> (12.4710, 1.0983) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_021). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.2375 m | derived_from_geometry | Vectorizer thickness 9.0 px, consistent with 9.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 234 of 234 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 9.0 px; predicted-mask median 9.0 px; vectorizer proposed 9.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.0 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 9.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `PASS` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [8.0, 9.0] px (spread 1.0). A large spread means one constant thickness is a poor fit.
- `WARN` endpoint_supported[start]: predicted wall continues past this endpoint (6 of 6 probe pixels are wall and are covered by no candidate): the wall may be truncated. Touching candidates: none.
- `PASS` endpoint_supported[end]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_011'].
- `PASS` corner_fill_at_junctions: 2 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 0 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [472.625, 456.375], "start": [472.625, 229.0]}, "orientation": "vertical", "source": "vectorizer output, unedited", "thickness_px": 9.0}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [472.625, 229.0], "end": [472.625, 456.375]}, "thickness_px": 9.0}` -> `{"axis_px": {"start": [472.625, 229.0], "end": [472.625, 460.375]}, "thickness_px": 9.0}`. R2 end extension: the predicted structural_wall mask continues 4 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [472.625, 229.0], "end": [472.625, 460.375]}, "thickness_px": 9.0}` -> `{"axis_px": {"start": [472.625, 227.0], "end": [472.625, 460.375]}, "thickness_px": 9.0}`. R2 end extension: the predicted structural_wall mask continues 2 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cc-high-quality--4712-p01:wall_022`

Candidate wall wall_022 (merged: wall_022, wall_023). Centreline length 4.4066 m.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (12.5205, 12.6656) -> (12.5205, 8.2590) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_022). Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.2111 m | derived_from_geometry | Vectorizer thickness 8.0 px, consistent with 8.0 px measured on the predicted structural_wall mask. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 168 of 168 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 8.0 px; predicted-mask median 8.0 px; vectorizer proposed 8.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: -0.5 px.
- `PASS` vectorizer_thickness_not_at_clamp: Vectorizer thickness 8.0 px; its clamp range is 3.0..40.0 px. A value at a clamp is a limit of the tool, not a measurement.
- `WARN` thickness_uniform_along_wall: p10-p90 of the perpendicular run on the predicted mask: [2.0, 8.0] px (spread 6.0). A large spread means one constant thickness is a poor fit.
- `PASS` endpoint_supported[start]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: ['wall_001'].
- `PASS` endpoint_supported[end]: the endpoint meets another candidate wall or covered wall evidence. Touching candidates: none.
- `WARN` corner_fill_at_junctions: 2 junction zone(s) involve this wall; the largest count of predicted wall pixels covered by no candidate body is 5 px. Wall joins are not resolved by this exporter.

Original candidate: `{"axis_px": {"end": [474.0, 71.0], "start": [474.0, 25.0]}, "orientation": "vertical", "source": "vectorizer output, unedited", "thickness_px": 8.0}`

- Edit of `repair:R2_extend_end` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [474.0, 25.0], "end": [474.0, 71.0]}, "thickness_px": 8.0}` -> `{"axis_px": {"start": [474.0, 25.0], "end": [474.0, 110.0]}, "thickness_px": 8.0}`. R2 end extension: the predicted structural_wall mask continues 39 px past the end of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [474.0, 25.0], "end": [474.0, 110.0]}, "thickness_px": 8.0}` -> `{"axis_px": {"start": [474.5, 25.0], "end": [474.5, 110.0]}, "thickness_px": 8.0}`. R3 recentre after R2 extension of end: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset -0.5 px).
- Edit of `repair:R2_extend_start` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [474.5, 25.0], "end": [474.5, 110.0]}, "thickness_px": 8.0}` -> `{"axis_px": {"start": [474.5, 22.0], "end": [474.5, 110.0]}, "thickness_px": 8.0}`. R2 end extension: the predicted structural_wall mask continues 3 px past the start of this axis; the end was moved to where the mask stops (or 40 px, whichever came first).
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [474.5, 22.0], "end": [474.5, 110.0]}, "thickness_px": 8.0}` -> `{"axis_px": {"start": [475.0, 22.0], "end": [475.0, 110.0]}, "thickness_px": 8.0}`. R3 recentre after R2 extension of start: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset -0.5 px).
- Edit of `repair:R1_merge` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"kept": {"id": "wall_022", "axis_px": {"start": [475.0, 22.0], "end": [475.0, 110.0]}, "thickness_px": 8.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 8.0 px, consistent with 8.0 px measured on the predicted structural_wall mask."}, "merged": {"id": "wall_023", "axis_px": {"start": [475.0, 54.0], "end": [475.0, 189.0]}, "thickness_px": 6.0, "thickness_source": "vectorizer", "thickness_basis": "Vectorizer thickness 6.0 px, consistent with 6.0 px measured on the predicted structural_wall mask."}}` -> `{"axis_px": {"start": [475.0, 22.0], "end": [475.0, 189.0]}, "thickness_px": 8.0}`. R1 collinear merge with wall_023: parallel axes 0.00 px apart, gap -56.0 px along the axis, 100% of the gap on predicted structural_wall pixels. One wall now spans both segments.
- Edit of `repair:R3_recentre` by **automated_rule** (bim_bridge_pm_comparison_v0 candidate_repair repair_v1.2) at 2026-10-08T13:18:26Z: `{"axis_px": {"start": [475.0, 22.0], "end": [475.0, 189.0]}, "thickness_px": 8.0}` -> `{"axis_px": {"start": [474.5, 22.0], "end": [474.5, 189.0]}, "thickness_px": 8.0}`. R3 recentre after R1 merge with wall_023: axis snapped exactly orthogonal and moved onto the median centreline of the predicted structural_wall mask (offset 0.5 px).

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### aperture `opening:cc-high-quality--4712-p01:door_opening-c01`

Candidate aperture (door_opening component 1) in wall_004. Host `wall:cc-high-quality--4712-p01:wall_004`. Predicted class `door_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 0.4222 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 1.0027 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.0000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 2.1000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 1.92 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 88% of the predicted door_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 38.0 px of a 431.5 px host.

Original candidate: `{"along_host_px": [16.0, 54.0], "component": {"bbox_px": [62, 203, 99, 213], "centroid_px": [81.67752442996742, 208.83387622149837], "component_id": 1, "pixel_count": 307}, "source": "connected component of the predicted door_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.0 m and height 2.1 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'door_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:door_opening-c02`

Candidate aperture (door_opening component 2) in wall_004. Host `wall:cc-high-quality--4712-p01:wall_004`. Predicted class `door_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 2.5595 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 1.0819 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.0000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 2.1000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.26 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 84% of the predicted door_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 41.0 px of a 431.5 px host.

Original candidate: `{"along_host_px": [97.0, 138.0], "component": {"bbox_px": [143, 202, 183, 212], "centroid_px": [163.0070257611241, 207.1686182669789], "component_id": 2, "pixel_count": 427}, "source": "connected component of the predicted door_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.0 m and height 2.1 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'door_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:door_opening-c03`

Candidate aperture (door_opening component 3) in wall_004. Host `wall:cc-high-quality--4712-p01:wall_004`. Predicted class `door_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 5.4093 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 0.9499 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.0000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 2.1000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.01 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 90% of the predicted door_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 36.0 px of a 431.5 px host.

Original candidate: `{"along_host_px": [205.0, 241.0], "component": {"bbox_px": [251, 202, 286, 211], "centroid_px": [269.1246105919003, 206.9221183800623], "component_id": 3, "pixel_count": 321}, "source": "connected component of the predicted door_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.0 m and height 2.1 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'door_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:door_opening-c05`

Candidate aperture (door_opening component 5) in wall_009. Host `wall:cc-high-quality--4712-p01:wall_009`. Predicted class `door_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 0.2507 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 0.8180 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.0000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 2.1000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.00 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 71% of the predicted door_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 31.0 px of a 126.0 px host.

Original candidate: `{"along_host_px": [9.5, 40.5], "component": {"bbox_px": [216, 377, 246, 383], "centroid_px": [231.0, 380.0], "component_id": 5, "pixel_count": 217}, "source": "connected component of the predicted door_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.0 m and height 2.1 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'door_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:door_opening-c06`

Candidate aperture (door_opening component 6) in wall_009. Host `wall:cc-high-quality--4712-p01:wall_009`. Predicted class `door_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 1.9922 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 0.7652 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.0000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 2.1000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.01 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 72% of the predicted door_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 29.0 px of a 126.0 px host.

Original candidate: `{"along_host_px": [75.5, 104.5], "component": {"bbox_px": [282, 377, 310, 383], "centroid_px": [296.07, 379.985], "component_id": 6, "pixel_count": 200}, "source": "connected component of the predicted door_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.0 m and height 2.1 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'door_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:door_opening-c07`

Candidate aperture (door_opening component 7) in wall_018. Host `wall:cc-high-quality--4712-p01:wall_018`. Predicted class `door_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 1.1049 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 0.8971 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.0000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 2.1000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.08 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 77% of the predicted door_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 34.0 px of a 247.4 px host.

Original candidate: `{"along_host_px": [41.875, 75.875], "component": {"bbox_px": [327, 386, 333, 419], "centroid_px": [330.2723004694836, 401.78403755868544], "component_id": 7, "pixel_count": 213}, "source": "connected component of the predicted door_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.0 m and height 2.1 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'door_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:door_opening-c08`

Candidate aperture (door_opening component 8) in wall_011. Host `wall:cc-high-quality--4712-p01:wall_011`. Predicted class `door_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 6.2405 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 1.1346 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.0000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 2.1000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.02 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 89% of the predicted door_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 43.0 px of a 430.6 px host.

Original candidate: `{"along_host_px": [236.5, 279.5], "component": {"bbox_px": [283, 452, 325, 462], "centroid_px": [303.5990783410138, 457.3963133640553], "component_id": 8, "pixel_count": 434}, "source": "connected component of the predicted door_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.0 m and height 2.1 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'door_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:window_opening-c01`

Candidate aperture (window_opening component 1) in wall_004. Host `wall:cc-high-quality--4712-p01:wall_004`. Predicted class `window_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 8.2854 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 1.8998 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.9000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 1.2000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.50 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 85% of the predicted window_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 72.0 px of a 431.5 px host.

Original candidate: `{"along_host_px": [314.0, 386.0], "component": {"bbox_px": [360, 201, 431, 212], "centroid_px": [395.1588235294118, 206.40941176470588], "component_id": 1, "pixel_count": 850}, "source": "connected component of the predicted window_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.9 m and height 1.2 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'window_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:window_opening-c02`

Candidate aperture (window_opening component 2) in wall_004. Host `wall:cc-high-quality--4712-p01:wall_004`. Predicted class `window_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 0.2375 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 0.1847 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.9000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 1.2000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.36 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 100% of the predicted window_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 7.0 px of a 431.5 px host.

Original candidate: `{"along_host_px": [9.0, 19.0], "component": {"bbox_px": [55, 203, 64, 212], "centroid_px": [58.976470588235294, 207.27058823529413], "component_id": 2, "pixel_count": 85}, "source": "connected component of the predicted window_opening mask, projected on the host axis"}`

- Edit of `offset_along_host` by **automated_rule** (bim_bridge_pm_comparison candidates.yield_to_earlier_head rule windows_v1) at 2026-10-08T13:18:26Z: `{"along_host_px": [9.0, 19.0]}` -> `{"along_host_px": [9.0, 16.0]}`. The component's span overlapped door_opening-c01 on the same host, predicted by an earlier head in heads.aperture_heads; this aperture was trimmed to abut the kept void. Two voids cannot share one stretch of wall; the overlap is usually the half-pixel padding of two abutting components.

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.9 m and height 1.2 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'window_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:window_opening-c03`

Candidate aperture (window_opening component 3) in wall_004. Host `wall:cc-high-quality--4712-p01:wall_004`. Predicted class `window_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 1.4513 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 1.0555 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.9000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 1.2000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.98 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 87% of the predicted window_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 40.0 px of a 431.5 px host.

Original candidate: `{"along_host_px": [55.0, 95.0], "component": {"bbox_px": [101, 203, 140, 213], "centroid_px": [120.66913580246914, 207.88888888888889], "component_id": 3, "pixel_count": 405}, "source": "connected component of the predicted window_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.9 m and height 1.2 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'window_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:window_opening-c04`

Candidate aperture (window_opening component 4) in wall_004. Host `wall:cc-high-quality--4712-p01:wall_004`. Predicted class `window_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 3.6414 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 0.4750 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.9000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 1.2000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.35 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 99% of the predicted window_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 18.0 px of a 431.5 px host.

Original candidate: `{"along_host_px": [138.0, 156.0], "component": {"bbox_px": [184, 202, 201, 211], "centroid_px": [192.08860759493672, 206.5632911392405], "component_id": 4, "pixel_count": 158}, "source": "connected component of the predicted window_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.9 m and height 1.2 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'window_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:window_opening-c05`

Candidate aperture (window_opening component 5) in wall_004. Host `wall:cc-high-quality--4712-p01:wall_004`. Predicted class `window_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 4.4330 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 0.9763 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.9000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 1.2000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.34 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 91% of the predicted window_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 37.0 px of a 431.5 px host.

Original candidate: `{"along_host_px": [168.0, 206.0], "component": {"bbox_px": [214, 202, 251, 211], "centroid_px": [231.9266304347826, 206.57065217391303], "component_id": 5, "pixel_count": 368}, "source": "connected component of the predicted window_opening mask, projected on the host axis"}`

- Edit of `offset_along_host` by **automated_rule** (bim_bridge_pm_comparison candidates.yield_to_earlier_head rule windows_v1) at 2026-10-08T13:18:26Z: `{"along_host_px": [168.0, 206.0]}` -> `{"along_host_px": [168.0, 205.0]}`. The component's span overlapped door_opening-c03 on the same host, predicted by an earlier head in heads.aperture_heads; this aperture was trimmed to abut the kept void. Two voids cannot share one stretch of wall; the overlap is usually the half-pixel padding of two abutting components.

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.9 m and height 1.2 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'window_opening'; no door or window element is created or asserted.

### aperture `opening:cc-high-quality--4712-p01:window_opening-c06`

Candidate aperture (window_opening component 6) in wall_004. Host `wall:cc-high-quality--4712-p01:wall_004`. Predicted class `window_opening`; modelled as an aperture only.

- Review: `CANDIDATE_UNREVIEWED`; reviewer `null`; date `null`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). Geometry is derived from the saved thresholded mask. The upstream run saved no probability maps, and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 6.3592 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 0.3166 m | derived_from_geometry | Extent of the predicted window_opening component projected on the host centreline. Converted at 0.026387 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.9000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 1.2000 m | assumed_for_preview | Aperture height from configuration profile 'pilot_preview_profile_v1'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.53 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 93% of the predicted window_opening pixels are also predicted structural_wall pixels.
- `PASS` aperture_host_unambiguous: Other candidate walls whose host band also contains the component centroid: none. The nearest axis was chosen.
- `PASS` aperture_narrower_than_host: Aperture spans 12.0 px of a 431.5 px host.

Original candidate: `{"along_host_px": [240.0, 253.0], "component": {"bbox_px": [286, 202, 298, 211], "centroid_px": [292.26363636363635, 206.38181818181818], "component_id": 6, "pixel_count": 110}, "source": "connected component of the predicted window_opening mask, projected on the host axis"}`

- Edit of `offset_along_host` by **automated_rule** (bim_bridge_pm_comparison candidates.yield_to_earlier_head rule windows_v1) at 2026-10-08T13:18:26Z: `{"along_host_px": [240.0, 253.0]}` -> `{"along_host_px": [241.0, 253.0]}`. The component's span overlapped door_opening-c03 on the same host, predicted by an earlier head in heads.aperture_heads; this aperture was trimmed to abut the kept void. Two voids cannot share one stretch of wall; the overlap is usually the half-pixel padding of two abutting components.

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.9 m and height 1.2 m are preview assumptions from profile 'pilot_preview_profile_v1'.
- Modelled as an aperture (void) only. The model head that proposed it is 'window_opening'; no door or window element is created or asserted.

## Checks

| Group | PASS | FAIL | WARN | INFO |
| --- | ---: | ---: | ---: | ---: |
| input | 238 | 1 | 28 | 0 |

**No IFC file was written because the input checks failed.**

### Failed checks

- `input/apertures_do_not_overlap[wall:cc-high-quality--4712-p01:wall_004]`: Overlapping apertures: [('opening:cc-high-quality--4712-p01:window_opening-c05', 'opening:cc-high-quality--4712-p01:door_opening-c03')]

### Warnings

- `input/scale_evidence`: Plan scale is ASSUMED_FOR_PREVIEW: every plan dimension is preview-only and no dimensional claim is permitted.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_001]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_004]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_007]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_008]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_009]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_011]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_012]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_014]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_015]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_016]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_017]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_018]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_021]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[wall:cc-high-quality--4712-p01:wall_022]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:door_opening-c01]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:door_opening-c02]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:door_opening-c03]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:door_opening-c05]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:door_opening-c06]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:door_opening-c07]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:door_opening-c08]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:window_opening-c01]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:window_opening-c02]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:window_opening-c03]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:window_opening-c04]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:window_opening-c05]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.
- `input/human_review[opening:cc-high-quality--4712-p01:window_opening-c06]`: CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review.

### All checks

| Status | Group | Check | Detail |
| --- | --- | --- | --- |
| PASS | input | `no_unevidenced_fields` | No material, fire-rating, load-bearing, equipment, inspection or overall-confidence fields. |
| PASS | input | `all_numbers_finite` | No NaN or infinite numbers. |
| PASS | input | `json_schema` | Conforms to building_model schema 0.2. |
| PASS | input | `unique_object_ids` | 31 object IDs, all unique. |
| PASS | input | `required_dimensions_present` | Every dimension needed for export has a value. |
| PASS | input | `unknown_origin_means_null` | origin=unknown is used exactly where the value is null. |
| PASS | input | `origins_match_track` | Attribute origins are consistent with track REVIEWED_PREDICTION_BRIDGE. |
| PASS | input | `real_lineage_fields_present` | Sample, split, source image, prediction artifacts, upstream model, extraction record and transforms are all recorded. |
| PASS | input | `scale_status_valid` | Scale status ASSUMED_FOR_PREVIEW. |
| PASS | input | `evidenced_scale_is_documented` | Scale is not claimed as evidenced. |
| PASS | input | `dimensional_claims_follow_scale` | dimensional_claims_permitted=False with scale status ASSUMED_FOR_PREVIEW. |
| PASS | input | `geometry_status_follows_review` | geometry_status=CANDIDATE_UNREVIEWED; object review states ['CANDIDATE_UNREVIEWED'] require CANDIDATE_UNREVIEWED. |
| PASS | input | `permitted_use_follows_status` | permitted_use=preview_only_not_for_engineering_or_inspection; review and scale status require preview_only_not_for_engineering_or_inspection. |
| WARN | input | `scale_evidence` | Plan scale is ASSUMED_FOR_PREVIEW: every plan dimension is preview-only and no dimensional claim is permitted. |
| PASS | input | `no_confidence_from_thresholded_masks` | No semantic score is claimed from thresholded masks. |
| PASS | input | `walls_trace_to_prediction_evidence` | Every wall references a region of a prediction mask with pixel support. |
| PASS | input | `candidate_original_preserved` | The originally proposed geometry is preserved for every object. |
| PASS | input | `scale_matches_transform` | scale.metres_per_source_px 0.010000000 equals metres_per_candidate_px x letterbox scale 0.010000000. |
| PASS | input | `metric_values_match_transform` | Every plan dimension equals its candidate-space source converted exactly once. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_001]` | Centreline length 11.4782 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_001]` | Thickness 0.1055 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_001]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_001]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_001]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_001]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_001]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_001]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_001]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_004]` | Centreline length 11.3859 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_004]` | Thickness 0.2639 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_004]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_004]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_004]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_004]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_004]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_004]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_004]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_007]` | Centreline length 2.1637 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_007]` | Thickness 0.1319 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_007]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_007]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_007]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_007]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_007]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_007]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_007]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_008]` | Centreline length 1.4513 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_008]` | Thickness 0.6861 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_008]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_008]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_008]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_008]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_008]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_008]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_008]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_009]` | Centreline length 3.3247 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_009]` | Thickness 0.1319 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_009]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_009]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_009]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_009]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_009]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_009]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_009]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_011]` | Centreline length 11.3628 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_011]` | Thickness 0.2111 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_011]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_011]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_011]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_011]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_011]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_011]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_011]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_012]` | Centreline length 4.9129 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_012]` | Thickness 0.1319 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_012]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_012]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_012]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_012]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_012]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_012]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_012]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_014]` | Centreline length 6.6890 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_014]` | Thickness 0.2375 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_014]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_014]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_014]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_014]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_014]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_014]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_014]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_015]` | Centreline length 2.3220 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_015]` | Thickness 0.1055 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_015]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_015]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_015]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_015]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_015]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_015]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_015]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_016]` | Centreline length 2.2165 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_016]` | Thickness 0.1319 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_016]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_016]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_016]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_016]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_016]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_016]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_016]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_017]` | Centreline length 2.4276 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_017]` | Thickness 0.1319 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_017]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_017]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_017]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_017]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_017]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_017]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_017]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_018]` | Centreline length 6.5274 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_018]` | Thickness 0.1187 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_018]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_018]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_018]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_018]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_018]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_018]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_018]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_021]` | Centreline length 6.1580 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_021]` | Thickness 0.2375 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_021]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_021]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_021]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_021]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_021]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_021]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_021]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `wall_length[wall:cc-high-quality--4712-p01:wall_022]` | Centreline length 4.4066 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cc-high-quality--4712-p01:wall_022]` | Thickness 0.2111 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cc-high-quality--4712-p01:wall_022]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cc-high-quality--4712-p01:wall_022]` | Assigned to storey 'storey:cc-high-quality--4712-p01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cc-high-quality--4712-p01:wall_022]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cc-high-quality--4712-p01:wall_022]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[wall:cc-high-quality--4712-p01:wall_022]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[wall:cc-high-quality--4712-p01:wall_022]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[wall:cc-high-quality--4712-p01:wall_022]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `no_duplicate_wall_geometry` | No two walls share a centreline. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:door_opening-c01]` | Host wall 'wall:cc-high-quality--4712-p01:wall_004' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:door_opening-c01]` | Width 1.0027 m, height 2.1000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:door_opening-c01]` | Spans 0.4222..1.4249 m along a 11.3859 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:door_opening-c01]` | Spans 0.0000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:door_opening-c01]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:door_opening-c01]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:door_opening-c01]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:door_opening-c01]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:door_opening-c01]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:door_opening-c02]` | Host wall 'wall:cc-high-quality--4712-p01:wall_004' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:door_opening-c02]` | Width 1.0819 m, height 2.1000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:door_opening-c02]` | Spans 2.5595..3.6414 m along a 11.3859 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:door_opening-c02]` | Spans 0.0000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:door_opening-c02]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:door_opening-c02]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:door_opening-c02]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:door_opening-c02]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:door_opening-c02]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:door_opening-c03]` | Host wall 'wall:cc-high-quality--4712-p01:wall_004' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:door_opening-c03]` | Width 0.9499 m, height 2.1000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:door_opening-c03]` | Spans 5.4093..6.3592 m along a 11.3859 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:door_opening-c03]` | Spans 0.0000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:door_opening-c03]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:door_opening-c03]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:door_opening-c03]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:door_opening-c03]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:door_opening-c03]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:door_opening-c05]` | Host wall 'wall:cc-high-quality--4712-p01:wall_009' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:door_opening-c05]` | Width 0.8180 m, height 2.1000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:door_opening-c05]` | Spans 0.2507..1.0687 m along a 3.3247 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:door_opening-c05]` | Spans 0.0000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:door_opening-c05]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:door_opening-c05]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:door_opening-c05]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:door_opening-c05]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:door_opening-c05]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:door_opening-c06]` | Host wall 'wall:cc-high-quality--4712-p01:wall_009' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:door_opening-c06]` | Width 0.7652 m, height 2.1000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:door_opening-c06]` | Spans 1.9922..2.7574 m along a 3.3247 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:door_opening-c06]` | Spans 0.0000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:door_opening-c06]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:door_opening-c06]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:door_opening-c06]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:door_opening-c06]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:door_opening-c06]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:door_opening-c07]` | Host wall 'wall:cc-high-quality--4712-p01:wall_018' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:door_opening-c07]` | Width 0.8971 m, height 2.1000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:door_opening-c07]` | Spans 1.1049..2.0021 m along a 6.5274 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:door_opening-c07]` | Spans 0.0000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:door_opening-c07]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:door_opening-c07]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:door_opening-c07]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:door_opening-c07]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:door_opening-c07]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:door_opening-c08]` | Host wall 'wall:cc-high-quality--4712-p01:wall_011' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:door_opening-c08]` | Width 1.1346 m, height 2.1000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:door_opening-c08]` | Spans 6.2405..7.3751 m along a 11.3628 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:door_opening-c08]` | Spans 0.0000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:door_opening-c08]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:door_opening-c08]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:door_opening-c08]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:door_opening-c08]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:door_opening-c08]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:window_opening-c01]` | Host wall 'wall:cc-high-quality--4712-p01:wall_004' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:window_opening-c01]` | Width 1.8998 m, height 1.2000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:window_opening-c01]` | Spans 8.2854..10.1853 m along a 11.3859 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:window_opening-c01]` | Spans 0.9000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:window_opening-c01]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:window_opening-c01]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:window_opening-c01]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:window_opening-c01]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:window_opening-c01]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:window_opening-c02]` | Host wall 'wall:cc-high-quality--4712-p01:wall_004' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:window_opening-c02]` | Width 0.1847 m, height 1.2000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:window_opening-c02]` | Spans 0.2375..0.4222 m along a 11.3859 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:window_opening-c02]` | Spans 0.9000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:window_opening-c02]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:window_opening-c02]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:window_opening-c02]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:window_opening-c02]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:window_opening-c02]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:window_opening-c03]` | Host wall 'wall:cc-high-quality--4712-p01:wall_004' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:window_opening-c03]` | Width 1.0555 m, height 1.2000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:window_opening-c03]` | Spans 1.4513..2.5067 m along a 11.3859 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:window_opening-c03]` | Spans 0.9000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:window_opening-c03]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:window_opening-c03]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:window_opening-c03]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:window_opening-c03]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:window_opening-c03]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:window_opening-c04]` | Host wall 'wall:cc-high-quality--4712-p01:wall_004' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:window_opening-c04]` | Width 0.4750 m, height 1.2000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:window_opening-c04]` | Spans 3.6414..4.1163 m along a 11.3859 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:window_opening-c04]` | Spans 0.9000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:window_opening-c04]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:window_opening-c04]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:window_opening-c04]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:window_opening-c04]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:window_opening-c04]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:window_opening-c05]` | Host wall 'wall:cc-high-quality--4712-p01:wall_004' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:window_opening-c05]` | Width 0.9763 m, height 1.2000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:window_opening-c05]` | Spans 4.4330..5.4093 m along a 11.3859 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:window_opening-c05]` | Spans 0.9000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:window_opening-c05]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:window_opening-c05]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:window_opening-c05]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:window_opening-c05]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:window_opening-c05]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| PASS | input | `aperture_host_resolves[opening:cc-high-quality--4712-p01:window_opening-c06]` | Host wall 'wall:cc-high-quality--4712-p01:wall_004' found. |
| PASS | input | `aperture_size[opening:cc-high-quality--4712-p01:window_opening-c06]` | Width 0.3166 m, height 1.2000 m. |
| PASS | input | `aperture_within_host_length[opening:cc-high-quality--4712-p01:window_opening-c06]` | Spans 6.3592..6.6758 m along a 11.3859 m host. |
| PASS | input | `aperture_within_host_height[opening:cc-high-quality--4712-p01:window_opening-c06]` | Spans 0.9000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cc-high-quality--4712-p01:window_opening-c06]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cc-high-quality--4712-p01:window_opening-c06]` | Every manually entered value has a recorded edit. |
| PASS | input | `unreviewed_has_no_reviewer[opening:cc-high-quality--4712-p01:window_opening-c06]` | Unreviewed candidate names no reviewer and no review date. |
| PASS | input | `no_human_edits_without_review[opening:cc-high-quality--4712-p01:window_opening-c06]` | No human edit is recorded on an unreviewed object. |
| WARN | input | `human_review[opening:cc-high-quality--4712-p01:window_opening-c06]` | CANDIDATE_UNREVIEWED: no human has reviewed this object. Agent and automated adjustments are not a review. |
| FAIL | input | `apertures_do_not_overlap[wall:cc-high-quality--4712-p01:wall_004]` | Overlapping apertures: [('opening:cc-high-quality--4712-p01:window_opening-c05', 'opening:cc-high-quality--4712-p01:door_opening-c03')] |
| PASS | input | `apertures_do_not_overlap[wall:cc-high-quality--4712-p01:wall_009]` | Apertures in this wall do not overlap. |
| PASS | input | `apertures_do_not_overlap[wall:cc-high-quality--4712-p01:wall_018]` | Apertures in this wall do not overlap. |
| PASS | input | `apertures_do_not_overlap[wall:cc-high-quality--4712-p01:wall_011]` | Apertures in this wall do not overlap. |

## Not modelled

- materials and material layers
- fire ratings
- load-bearing or external status
- equipment data
- inspection or construction status
- wall joins and corner clean-up
- doors and windows as IfcDoor / IfcWindow (only the aperture void is modelled)
- spaces and rooms
- georeferencing
- curved, tapered or sloped walls
- classification references

## Not established by this report

- segmentation accuracy, wall IoU or any training comparison
- dimensional accuracy of the geometry (no reference geometry was used, so accuracy is unknown, not zero error)
- acceptance by any BIM viewer or authoring tool
- conformance to a model view definition or an IDS
- fitness for engineering, inspection or construction use
