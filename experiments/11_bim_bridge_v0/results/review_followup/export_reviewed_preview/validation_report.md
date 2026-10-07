# Validation report: cubicasa-high-quality-architectural-333-val-region-01 (REVIEWED_PREDICTION_BRIDGE)

> The meaningful result today is not ‘we generated a 3D picture.’ It is ‘we can turn reviewed prediction-derived geometry into identifiable IFC building elements, preserve uncertainty, and inspect the result.’ That is a concrete step toward the PM’s BIM goal—and it creates a stable destination for the ML improvements that follow.

**REAL PREDICTION-DERIVED GEOMETRY. Geometry status HUMAN_REVIEWED. Scale status ASSUMED_FOR_PREVIEW. Permitted use: reviewed_geometry_preview_dimensions_unverified.**

HUMAN-REVIEWED, PREVIEW ONLY: 4 straight walls and 1 aperture(s) derived from saved Phase 5 predictions of high_quality_architectural/333 (val split).

- Technical checks: **PASS** (144 checks: 143 PASS, 1 WARN)
- A technical PASS means the file matches its input and passes schema and geometry checks. It is not a reviewed prediction bridge and not downstream acceptance.
- Run: `bim_bridge_v0_20260928_183649_UTC`; model timestamp 2026-09-28T18:37:01Z
- Tooling: bim_bridge_v0 0.2.0, IfcOpenShell 0.8.5, Python 3.12.3
- IFC schema: IFC4 (Prototype choice. No receiving BIM application or accepted IFC schema is documented in the inspected repositories.) Target application: null; compatibility UNVERIFIED.
- Length unit: metre. Scale: `ASSUMED_FOR_PREVIEW`, metres per source pixel 0.0107. Dimensional claims permitted: False.
- Scale note: NO documented scale evidence exists for this drawing: it has no dimension string and no scale bar. The value is an estimate from the apartment area label, used only so the preview has a plausible size. Metric export of real geometry is BLOCKED until a human supplies or confirms a scale.

## Files

- candidate_geometry: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/candidates/candidate_geometry.json`
- source_building_model: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/reviewed/building_model.json`
- review_record: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/reviewed/review_record.json`
- guid_map_started_from: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_preview/guid_map.json`
- building_model: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_reviewed_preview/building_model.json`
- ifc: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_reviewed_preview/cubicasa-high-quality-architectural-333-val-region-01__REVIEWED_PREVIEW_SCALE_ASSUMED_FOR_PREVIEW.ifc`
- guid_map: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_reviewed_preview/guid_map.json`
- report_json: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_reviewed_preview/validation_report.json`
- report_markdown: `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_reviewed_preview/validation_report.md`

## Counts

| Measure | Count |
| --- | --- |
| Walls exported / requested | 4 of 4 |
| Apertures exported / requested | 1 of 1 |
| Apertures with a valid host | 1 of 1 |
| Walls tracing to prediction evidence | 4 of 4 |
| Attributes assumed for preview | 11 of 21 |
| Objects reviewed by a human | 5 of 5 |
| Objects with a model semantic score | 0 of 5 |
| Edits by human / agent / automated rule | 3 / 0 / 1 |
| Unresolved geometry diagnostics | 0 |
| Measured correction time | not captured |

## Attribute origins

Origin says where a value came from. It says nothing about whether anyone verified it; review is recorded separately.

| Origin | Attributes |
| --- | ---: |
| predicted by the model | 0 |
| derived from prediction geometry | 8 |
| manually entered | 2 |
| assumed for preview (no evidence) | 11 |
| unknown (null) | 0 |
| synthetic fixture | 0 |
| **total** | **21** |

## Objects

### wall `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002`

Candidate wall wall_002 (horizontal). Centreline length 6.6004 m.

- Review: `HUMAN_ACCEPTED_WITH_EDITS`; reviewer `Paul Harris`; date `2026-10-01T20:33:50Z`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). The only persisted prediction is a thresholded mask. The upstream run saved no probability maps (save_probability_maps: false), and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (0.1381, 2.6501) -> (6.7385, 2.6501) m | manually_entered | Centreline set by a human reviewer. Converted at 0.027617 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.2486 m | derived_from_geometry | Vectorizer thickness 9.0 px, consistent with 9.0 px measured on the predicted structural_wall mask. Converted at 0.027617 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'preview_vertical_defaults_v0'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'preview_vertical_defaults_v0'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 207 of 207 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 9.0 px; predicted-mask median 9.0 px; vectorizer proposed 9.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.0 px.

Original candidate: `{"axis_px": {"end": [472.0, 160.04166666666666], "start": [266.0, 160.04166666666666]}, "orientation": "horizontal", "source": "vectorizer output, unedited", "thickness_px": 9.0}`

- Edit of `axis_px.start` by **human** (Paul Harris) at 2026-10-01T20:33:50Z: `{"axis_px.start": [266.0, 160.04166666666666]}` -> `{"axis_px.start": [233.0, 160.04166666666666]}`. I accept extending this selected segment across the previously omitted interval for the preview. The original extraction cause remains unresolved.

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'preview_vertical_defaults_v0'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003`

Candidate wall wall_003 (horizontal). Centreline length 4.6949 m.

- Review: `HUMAN_ACCEPTED`; reviewer `Paul Harris`; date `2026-10-01T20:33:50Z`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). The only persisted prediction is a thresholded mask. The upstream run saved no probability maps (save_probability_maps: false), and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (2.1127, 0.9804) -> (6.8075, 0.9804) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_003). Converted at 0.027617 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1657 m | derived_from_geometry | Vectorizer thickness 6.0 px, consistent with 6.0 px measured on the predicted structural_wall mask. Converted at 0.027617 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'preview_vertical_defaults_v0'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'preview_vertical_defaults_v0'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 171 of 171 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 6.0 px; predicted-mask median 6.0 px; vectorizer proposed 6.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: -0.5 px.

Original candidate: `{"axis_px": {"end": [474.5, 220.5], "start": [304.5, 220.5]}, "orientation": "horizontal", "source": "vectorizer output, unedited", "thickness_px": 6.0}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'preview_vertical_defaults_v0'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004`

Candidate wall wall_004 (horizontal). Centreline length 1.7261 m.

- Review: `HUMAN_ACCEPTED`; reviewer `Paul Harris`; date `2026-10-01T20:33:50Z`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). The only persisted prediction is a thresholded mask. The upstream run saved no probability maps (save_probability_maps: false), and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (0.3866, 0.3866) -> (2.1127, 0.4004) m | derived_from_geometry | Centreline proposed by the vectorizer from the predicted wall mask (upstream object wall_004). Converted at 0.027617 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1105 m | derived_from_geometry | Vectorizer thickness 4.0 px, consistent with 4.0 px measured on the predicted structural_wall mask. Converted at 0.027617 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'preview_vertical_defaults_v0'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'preview_vertical_defaults_v0'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 63 of 63 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 4.0 px; predicted-mask median 4.0 px; vectorizer proposed 4.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.5 px.

Original candidate: `{"axis_px": {"end": [304.5, 241.5], "start": [242.0, 242.0]}, "orientation": "horizontal", "source": "vectorizer output, unedited", "thickness_px": 4.0}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'preview_vertical_defaults_v0'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### wall `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012`

Candidate wall wall_012 (vertical). Centreline length 2.2496 m.

- Review: `HUMAN_ACCEPTED_WITH_EDITS`; reviewer `Paul Harris`; date `2026-10-01T20:33:50Z`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). The only persisted prediction is a thresholded mask. The upstream run saved no probability maps (save_probability_maps: false), and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| axis | (2.1403, 0.4004) -> (2.1403, 2.6501) m | manually_entered | Centreline set by a human reviewer. Converted at 0.027617 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| thickness | 0.1105 m | derived_from_geometry | Median perpendicular run 4.0 px on the predicted structural_wall mask; the vectorizer value 40.0 px was replaced by an automated rule. Converted at 0.027617 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| height | 2.7000 m | assumed_for_preview | Wall height from configuration profile 'preview_vertical_defaults_v0'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| base_elevation | 0.0000 m | assumed_for_preview | Wall base elevation from configuration profile 'preview_vertical_defaults_v0'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` axis_lies_on_predicted_wall: 82 of 82 centreline samples lie on predicted structural_wall pixels.
- `PASS` thickness_matches_predicted_mask: Thickness in use 4.0 px; predicted-mask median 4.0 px; vectorizer proposed 40.0 px.
- `PASS` centreline_offset_from_predicted_wall: Median offset between the axis and the middle of the predicted wall: 0.5 px.

Original candidate: `{"axis_px": {"end": [304.5, 160.04166666666666], "start": [304.5, 241.5]}, "orientation": "vertical", "source": "vectorizer output, unedited", "thickness_px": 40.0}`

- Edit of `thickness` by **automated_rule** (bim_bridge candidates.thickness_from_predicted_mask rule 0.2) at 2026-09-28T18:37:01Z: `{"thickness_px": 40.0}` -> `{"thickness_px": 4.0}`. Vectorizer thickness 40.0 px disagrees with the predicted mask by more than 2.0 px; the median perpendicular run on the predicted structural_wall mask is 4.0 px.
- Edit of `axis_px.start` by **human** (Paul Harris) at 2026-10-01T20:33:50Z: `{"axis_px.start": [304.5, 241.5]}` -> `{"axis_px.start": [305.5, 241.5]}`. The proposed teal footprint follows the original drawing’s vertical wall more centrally than the current blue footprint.
- Edit of `axis_px.end` by **human** (Paul Harris) at 2026-10-01T20:33:50Z: `{"axis_px.end": [304.5, 160.04166666666666]}` -> `{"axis_px.end": [305.5, 160.04166666666666]}`. The proposed teal footprint follows the original drawing’s vertical wall more centrally than the current blue footprint.

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; length, position and thickness in metres are preview values, not dimensions of the building.
- Height 2.7 m and base elevation 0.0 m are preview assumptions from profile 'preview_vertical_defaults_v0'.
- Modelled as a straight constant-thickness prism centred on its centreline; joins with neighbouring walls are not resolved.

### aperture `opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02`

Candidate aperture (door_opening component 2) in wall_003. Host `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003`. Predicted class `door_opening`; modelled as an aperture only.

- Review: `HUMAN_ACCEPTED`; reviewer `Paul Harris`; date `2026-10-01T20:33:50Z`
- Semantic score: `null` (UNAVAILABLE; calibration NOT_CALIBRATED). The only persisted prediction is a thresholded mask. The upstream run saved no probability maps (save_probability_maps: false), and no score can be derived from binary pixels.

| Attribute | Value | Origin | Basis |
| --- | --- | --- | --- |
| offset_along_host | 0.1105 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.027617 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| width | 0.7733 m | derived_from_geometry | Extent of the predicted door_opening component projected on the host centreline. Converted at 0.027617 m per letterbox_512 px (scale status ASSUMED_FOR_PREVIEW). |
| bottom_elevation | 0.0000 m | assumed_for_preview | Aperture bottom elevation from configuration profile 'preview_vertical_defaults_v0'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |
| height | 2.1000 m | assumed_for_preview | Aperture height from configuration profile 'preview_vertical_defaults_v0'. A plan drawing carries no vertical information; this is an assumption, not a measurement. |

Geometry diagnostics against the prediction (not a confidence):
- `PASS` aperture_lies_in_host_band: Component centroid is 0.00 px from the host axis.
- `PASS` aperture_overlaps_predicted_wall: 84% of the predicted door_opening pixels are also predicted structural_wall pixels.

Original candidate: `{"along_host_px": [4.0, 32.0], "component": {"bbox_px": [309, 218, 336, 223], "centroid_px": [322.5, 220.5], "component_id": 2, "pixel_count": 168}, "source": "connected component of the predicted door_opening mask, projected on the host axis"}`

Assumptions:
- Plan scale is ASSUMED_FOR_PREVIEW; offset and width in metres are preview values, not dimensions of the building.
- Bottom elevation 0.0 m and height 2.1 m are preview assumptions from profile 'preview_vertical_defaults_v0'.
- Modelled as an aperture (void) only. The model head that proposed it is 'door_opening'; no door or window element is created or asserted.

## Checks

| Group | PASS | FAIL | WARN | INFO |
| --- | ---: | ---: | ---: | ---: |
| input | 65 | 0 | 1 | 0 |
| ifc_reopen | 2 | 0 | 0 | 0 |
| ifc_schema | 2 | 0 | 0 | 0 |
| ifc_structure | 15 | 0 | 0 | 0 |
| ifc_identity | 9 | 0 | 0 | 0 |
| ifc_provenance | 21 | 0 | 0 | 0 |
| geometry | 29 | 0 | 0 | 0 |

### Warnings

- `input/scale_evidence`: Plan scale is ASSUMED_FOR_PREVIEW: every plan dimension is preview-only and no dimensional claim is permitted.

### All checks

| Status | Group | Check | Detail |
| --- | --- | --- | --- |
| PASS | input | `no_unevidenced_fields` | No material, fire-rating, load-bearing, equipment, inspection or overall-confidence fields. |
| PASS | input | `all_numbers_finite` | No NaN or infinite numbers. |
| PASS | input | `json_schema` | Conforms to building_model schema 0.2. |
| PASS | input | `unique_object_ids` | 9 object IDs, all unique. |
| PASS | input | `required_dimensions_present` | Every dimension needed for export has a value. |
| PASS | input | `unknown_origin_means_null` | origin=unknown is used exactly where the value is null. |
| PASS | input | `origins_match_track` | Attribute origins are consistent with track REVIEWED_PREDICTION_BRIDGE. |
| PASS | input | `real_lineage_fields_present` | Sample, split, source image, prediction artifacts, upstream model, extraction record and transforms are all recorded. |
| PASS | input | `scale_status_valid` | Scale status ASSUMED_FOR_PREVIEW. |
| PASS | input | `evidenced_scale_is_documented` | Scale is not claimed as evidenced. |
| PASS | input | `dimensional_claims_follow_scale` | dimensional_claims_permitted=False with scale status ASSUMED_FOR_PREVIEW. |
| PASS | input | `geometry_status_follows_review` | geometry_status=HUMAN_REVIEWED; object review states ['HUMAN_ACCEPTED', 'HUMAN_ACCEPTED_WITH_EDITS'] require HUMAN_REVIEWED. |
| PASS | input | `permitted_use_follows_status` | permitted_use=reviewed_geometry_preview_dimensions_unverified; review and scale status require reviewed_geometry_preview_dimensions_unverified. |
| WARN | input | `scale_evidence` | Plan scale is ASSUMED_FOR_PREVIEW: every plan dimension is preview-only and no dimensional claim is permitted. |
| PASS | input | `no_confidence_from_thresholded_masks` | No semantic score is claimed from thresholded masks. |
| PASS | input | `walls_trace_to_prediction_evidence` | Every wall references a region of a prediction mask with pixel support. |
| PASS | input | `candidate_original_preserved` | The originally proposed geometry is preserved for every object. |
| PASS | input | `scale_matches_transform` | scale.metres_per_source_px 0.010720103 equals metres_per_candidate_px x letterbox scale 0.010720103. |
| PASS | input | `metric_values_match_transform` | Every plan dimension equals its candidate-space source converted exactly once. |
| PASS | input | `wall_length[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Centreline length 6.6004 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Thickness 0.2486 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Assigned to storey 'storey:cubicasa-high-quality-architectural-333-val-region-01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Every manually entered value has a recorded edit. |
| PASS | input | `human_review_is_recorded[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Reviewer, date and review record are all present. |
| PASS | input | `review_state_not_rejected[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Review state HUMAN_ACCEPTED_WITH_EDITS. |
| PASS | input | `review_state_matches_edits[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | State HUMAN_ACCEPTED_WITH_EDITS; human edits recorded: True. |
| PASS | input | `wall_length[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Centreline length 4.6949 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Thickness 0.1657 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Assigned to storey 'storey:cubicasa-high-quality-architectural-333-val-region-01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Every manually entered value has a recorded edit. |
| PASS | input | `human_review_is_recorded[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Reviewer, date and review record are all present. |
| PASS | input | `review_state_not_rejected[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Review state HUMAN_ACCEPTED. |
| PASS | input | `review_state_matches_edits[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | State HUMAN_ACCEPTED; human edits recorded: False. |
| PASS | input | `wall_length[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Centreline length 1.7261 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Thickness 0.1105 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Assigned to storey 'storey:cubicasa-high-quality-architectural-333-val-region-01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Every manually entered value has a recorded edit. |
| PASS | input | `human_review_is_recorded[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Reviewer, date and review record are all present. |
| PASS | input | `review_state_not_rejected[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Review state HUMAN_ACCEPTED. |
| PASS | input | `review_state_matches_edits[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | State HUMAN_ACCEPTED; human edits recorded: False. |
| PASS | input | `wall_length[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Centreline length 2.2496 m (allowed 0.05..500.0). |
| PASS | input | `wall_thickness[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Thickness 0.1105 m (allowed 0..2.0). |
| PASS | input | `wall_height[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Height 2.7000 m (allowed 0..30.0). |
| PASS | input | `wall_storey[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Assigned to storey 'storey:cubicasa-high-quality-architectural-333-val-region-01:level-0'. |
| PASS | input | `candidate_geometry_checks[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Every manually entered value has a recorded edit. |
| PASS | input | `human_review_is_recorded[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Reviewer, date and review record are all present. |
| PASS | input | `review_state_not_rejected[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Review state HUMAN_ACCEPTED_WITH_EDITS. |
| PASS | input | `review_state_matches_edits[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | State HUMAN_ACCEPTED_WITH_EDITS; human edits recorded: True. |
| PASS | input | `no_duplicate_wall_geometry` | No two walls share a centreline. |
| PASS | input | `aperture_host_resolves[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | Host wall 'wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003' found. |
| PASS | input | `aperture_size[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | Width 0.7733 m, height 2.1000 m. |
| PASS | input | `aperture_within_host_length[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | Spans 0.1105..0.8837 m along a 4.6949 m host. |
| PASS | input | `aperture_within_host_height[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | Spans 0.0000..2.1000 m above the wall base in a 2.7000 m high host. |
| PASS | input | `candidate_geometry_checks[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | No failed geometry diagnostics are recorded on this object. |
| PASS | input | `manual_values_have_edit_records[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | Every manually entered value has a recorded edit. |
| PASS | input | `human_review_is_recorded[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | Reviewer, date and review record are all present. |
| PASS | input | `review_state_not_rejected[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | Review state HUMAN_ACCEPTED. |
| PASS | input | `review_state_matches_edits[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | State HUMAN_ACCEPTED; human edits recorded: False. |
| PASS | input | `apertures_do_not_overlap[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Apertures in this wall do not overlap. |
| PASS | ifc_reopen | `file_exists` | /mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/export_reviewed_preview/cubicasa-high-quality-architectural-333-val-region-01__REVIEWED_PREVIEW_SCALE_ASSUMED_FOR_PREVIEW.ifc (64870 bytes) |
| PASS | ifc_reopen | `reopens` | Reopened with IfcOpenShell 0.8.5; 470 entities. |
| PASS | ifc_schema | `schema_identifier` | File schema is 'IFC4' (expected 'IFC4'). |
| PASS | ifc_schema | `schema_and_express_rules` | ifcopenshell.validate reports no attribute-type, cardinality, inverse or EXPRESS WHERE-rule violations. |
| PASS | ifc_structure | `exactly_one_IfcProject` | 1 IfcProject instance(s). |
| PASS | ifc_structure | `exactly_one_IfcSite` | 1 IfcSite instance(s). |
| PASS | ifc_structure | `exactly_one_IfcBuilding` | 1 IfcBuilding instance(s). |
| PASS | ifc_structure | `exactly_one_IfcBuildingStorey` | 1 IfcBuildingStorey instance(s). |
| PASS | ifc_structure | `spatial_chain` | Project > Site > Building > Storey are linked by IfcRelAggregates. |
| PASS | ifc_structure | `length_unit_is_metre` | Length unit METRE, prefix None, scale to metres 1. |
| PASS | ifc_structure | `storey_elevation` | Storey elevation 0.0 m. |
| PASS | ifc_structure | `wall_count` | 4 IfcWall (input has 4). |
| PASS | ifc_structure | `opening_count` | 1 IfcOpeningElement (input has 1). |
| PASS | ifc_structure | `objects_identified_by_tag` | Every input object is present, identified by Tag = object_id. |
| PASS | ifc_structure | `walls_contained_in_storey` | Every wall is contained in the storey. |
| PASS | ifc_structure | `aperture_hosted[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | IfcRelVoidsElement links it to host 'wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003' (expected 'wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003'). |
| PASS | ifc_structure | `no_unevidenced_entities` | No material or classification entities were written. |
| PASS | ifc_structure | `no_standard_psets_claimed` | No buildingSMART Pset_/Qto_ sets were written; only application-specific sets. |
| PASS | ifc_structure | `no_unevidenced_properties` | No material / fire / load-bearing / inspection properties were written. |
| PASS | ifc_identity | `global_ids_unique` | 28 rooted entities, 28 distinct GlobalIds. |
| PASS | ifc_identity | `global_ids_well_formed` | Every GlobalId is a valid 22-character IFC GUID. |
| PASS | ifc_identity | `guid_map_matches_file` | All 28 active GUID-map entries resolve to an entity of the recorded class, and every GlobalId in the file is in the map. |
| PASS | ifc_identity | `object_guid[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | GlobalId 1XkaxwpSjJ8Qnf5B_jRxg1 matches the GUID map. |
| PASS | ifc_identity | `object_guid[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | GlobalId 3d2OAZpCHGUAZ91g4AXd7s matches the GUID map. |
| PASS | ifc_identity | `object_guid[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | GlobalId 1b$tabjrHGbPd9xW5BjLOQ matches the GUID map. |
| PASS | ifc_identity | `object_guid[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | GlobalId 11mnaExH9O2vr$qGRs3ceQ matches the GUID map. |
| PASS | ifc_identity | `object_guid[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | GlobalId 1Y$u78JbXJIggJrkmIA5ew matches the GUID map. |
| PASS | ifc_provenance | `model_pset_present` | AutoAutoCAD_ModelProvenance is attached to the building. |
| PASS | ifc_provenance | `model_pset_values` | Model provenance values match the input. |
| PASS | ifc_provenance | `pset_present[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | AutoAutoCAD_Provenance is attached. |
| PASS | ifc_provenance | `pset_complete[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | All 38 required properties exist. |
| PASS | ifc_provenance | `pset_values[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Provenance, uncertainty and review values match the input (a null score stays null). |
| PASS | ifc_provenance | `prediction_evidence_in_ifc[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | The wall's property set names the prediction mask region and the hash of the prediction artifact it came from. |
| PASS | ifc_provenance | `pset_present[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | AutoAutoCAD_Provenance is attached. |
| PASS | ifc_provenance | `pset_complete[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | All 38 required properties exist. |
| PASS | ifc_provenance | `pset_values[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Provenance, uncertainty and review values match the input (a null score stays null). |
| PASS | ifc_provenance | `prediction_evidence_in_ifc[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | The wall's property set names the prediction mask region and the hash of the prediction artifact it came from. |
| PASS | ifc_provenance | `pset_present[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | AutoAutoCAD_Provenance is attached. |
| PASS | ifc_provenance | `pset_complete[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | All 38 required properties exist. |
| PASS | ifc_provenance | `pset_values[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Provenance, uncertainty and review values match the input (a null score stays null). |
| PASS | ifc_provenance | `prediction_evidence_in_ifc[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | The wall's property set names the prediction mask region and the hash of the prediction artifact it came from. |
| PASS | ifc_provenance | `pset_present[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | AutoAutoCAD_Provenance is attached. |
| PASS | ifc_provenance | `pset_complete[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | All 38 required properties exist. |
| PASS | ifc_provenance | `pset_values[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Provenance, uncertainty and review values match the input (a null score stays null). |
| PASS | ifc_provenance | `prediction_evidence_in_ifc[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | The wall's property set names the prediction mask region and the hash of the prediction artifact it came from. |
| PASS | ifc_provenance | `pset_present[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | AutoAutoCAD_Provenance is attached. |
| PASS | ifc_provenance | `pset_complete[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | All 37 required properties exist. |
| PASS | ifc_provenance | `pset_values[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | Provenance, uncertainty and review values match the input (a null score stays null). |
| PASS | geometry | `wall_placement[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | World placement origin [0.138084, 2.650065, 0.0] and axis [1.0, 0.0, 0.0] match the input start point, base elevation (applied once) and direction. |
| PASS | geometry | `wall_geometry_builds[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Geometry kernel produced 8 vertices, 12 triangles. |
| PASS | geometry | `wall_length[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Extent along axis 0.00000..6.60042 m (expected 0..6.60042). |
| PASS | geometry | `wall_thickness[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Extent across axis -0.12428..0.12428 m (expected ±0.12428; centred on the centreline). |
| PASS | geometry | `wall_vertical_extent[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | z 0.00000..2.70000 m (expected 0.00000..2.70000). |
| PASS | geometry | `wall_gross_volume[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002]` | Gross volume 4.429462 m3 (expected length x thickness x height = 4.429462). |
| PASS | geometry | `wall_placement[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | World placement origin [2.112687, 0.980397, 0.0] and axis [1.0, 0.0, 0.0] match the input start point, base elevation (applied once) and direction. |
| PASS | geometry | `wall_geometry_builds[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Geometry kernel produced 8 vertices, 12 triangles. |
| PASS | geometry | `wall_length[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Extent along axis 0.00000..4.69486 m (expected 0..4.69486). |
| PASS | geometry | `wall_thickness[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Extent across axis -0.08285..0.08285 m (expected ±0.08285; centred on the centreline). |
| PASS | geometry | `wall_vertical_extent[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | z 0.00000..2.70000 m (expected 0.00000..2.70000). |
| PASS | geometry | `wall_gross_volume[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Gross volume 2.100447 m3 (expected length x thickness x height = 2.100447). |
| PASS | geometry | `wall_net_volume_after_voids[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | Net volume with 1 aperture(s) subtracted 1.831370 m3 (expected 1.831370). |
| PASS | geometry | `void_removes_intended_volume[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003]` | The void removed 0.269077 m3 of wall (expected width x wall thickness x height = 0.269077). |
| PASS | geometry | `wall_placement[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | World placement origin [0.386636, 0.386636, 0.0] and axis [0.999968, 0.008, 0.0] match the input start point, base elevation (applied once) and direction. |
| PASS | geometry | `wall_geometry_builds[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Geometry kernel produced 8 vertices, 12 triangles. |
| PASS | geometry | `wall_length[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Extent along axis -0.00000..1.72611 m (expected 0..1.72611). |
| PASS | geometry | `wall_thickness[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Extent across axis -0.05523..0.05523 m (expected ±0.05523; centred on the centreline). |
| PASS | geometry | `wall_vertical_extent[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | z 0.00000..2.70000 m (expected 0.00000..2.70000). |
| PASS | geometry | `wall_gross_volume[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004]` | Gross volume 0.514830 m3 (expected length x thickness x height = 0.514830). |
| PASS | geometry | `wall_placement[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | World placement origin [2.140304, 0.400444, 0.0] and axis [0.0, 1.0, 0.0] match the input start point, base elevation (applied once) and direction. |
| PASS | geometry | `wall_geometry_builds[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Geometry kernel produced 8 vertices, 12 triangles. |
| PASS | geometry | `wall_length[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Extent along axis 0.00000..2.24962 m (expected 0..2.24962). |
| PASS | geometry | `wall_thickness[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Extent across axis -0.05523..0.05523 m (expected ±0.05523; centred on the centreline). |
| PASS | geometry | `wall_vertical_extent[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | z 0.00000..2.70000 m (expected 0.00000..2.70000). |
| PASS | geometry | `wall_gross_volume[wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012]` | Gross volume 0.670974 m3 (expected length x thickness x height = 0.670974). |
| PASS | geometry | `aperture_position_and_width[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | Along host 0.11047..0.88374 m (expected 0.11047..0.88374). |
| PASS | geometry | `aperture_passes_through_wall[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | Across host -0.09285..0.09285 m; covers the full 0.16570 m thickness plus the 0.01 m exporter overcut per face. |
| PASS | geometry | `aperture_vertical_extent[opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02]` | z 0.00000..2.10000 m (expected 0.00000..2.10000). |
| PASS | ifc_identity | `repeat_export_reuses_guids` | Repeat export created 0 new GlobalIds, reused 28, byte-identical: True. |

## GUID map

- GlobalIds created by this export: 0
- GlobalIds reused from the existing map: 28
- Entries retired (kept, never reassigned): 0

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
