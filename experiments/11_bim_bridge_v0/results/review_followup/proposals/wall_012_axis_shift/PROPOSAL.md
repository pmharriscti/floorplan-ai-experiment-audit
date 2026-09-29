# Proposal: move the wall_012 axis +1 px in x

Run `bim_bridge_v0_20260928_183649_UTC`. Written 2026-09-28T22:38:46Z.

**Status: PROPOSED_AWAITING_HUMAN_REVIEW. Nothing was applied.** The candidate geometry, the preview IFC, the
review template and every gate are unchanged. No acceptance is recorded. Scale stays `ASSUMED_FOR_PREVIEW`, not confirmed.

Object: `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012` (review state `CANDIDATE_UNREVIEWED`)

| | axis_px.start | axis_px.end | thickness_px |
| --- | --- | --- | --- |
| Current | `[304.5, 241.5]` | `[304.5, 160.04166666666666]` | 4.0 |
| Proposed | `[305.5, 241.5]` | `[305.5, 160.04166666666666]` | 4.0 |

Reason given by the requester: At the reported row 201, the predicted mask spans 303.5-307.5, while the current footprint spans 302.5-306.5. The original-image close-up also suggests that the current footprint is left of the intended wall strip.

## Alignment against the predicted mask

57 rows were checked, every row of the wall at least 3 px from a junction band.

| Section | Rows | Mask x pixels seen | Current axis minus mask centre (median, px) | Proposed (median, px) | Mask covered, current | Mask covered, proposed |
| --- | --- | --- | --- | --- | --- | --- |
| rows 168 to 214 | 47 | 304..307 | -1 | +0 | 75% | 100% |
| rows 227 to 236 | 10 | 303..307, 304..307 | -1 | +0 | 76% | 94% |

- Rows where the proposed axis is closer to the mask centre: 54 of 57. Rows where the current axis is closer: 0.
- This compares geometry with the model's own prediction. It says nothing about the building.

## Alignment against the drawn ink (heuristic)

- Wall centre from the ink, median over 57 rows: x 305.19 to 305.49 letterbox px, depending on the pixel mapping.
- Range over rows: 304.99 to 306.27.
- Current axis x 304.5. Proposed axis x 305.5.
- Drawn width, median: 5.0 letterbox px (range 4.7 to 6.6). Thickness stays 4.0 for this comparison, as requested.
- A heuristic on the drawing, not a measurement of the building. Nearby ink (door frames, hatching, text) can fall in the window. Two pixel mappings are reported because the letterbox registration is known only to about 0.3 letterbox px.

## Junctions

- `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002`: wall_012 ends on the axis of this wall (T junction). After the proposal: wall_012 still ends on this axis, at x 305.5; the other wall runs x 266..472.
- `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003`: this wall starts on the axis of wall_012 (T junction). After the proposal: its endpoint is 1 px from the proposed axis and inside the proposed footprint (x 303.5..307.5).
- `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004`: axis endpoints coincide with wall_012 start today. After the proposal: axis endpoints 1 px apart in x; the other wall's endpoint is inside the proposed footprint (x 303.5..307.5).
- Aperture `opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02`: host `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003`, not moved. Gap from the wall_012 face to the aperture: 2 px now, 1 px proposed.

The proposal moves only `wall_012`. The endpoints of the other walls stay where they are.

## Contract dry run (in memory)

- Current geometry: {'PASS': 60, 'FAIL': 0, 'WARN': 6, 'INFO': 0}
- Proposed geometry: {'PASS': 60, 'FAIL': 0, 'WARN': 6, 'INFO': 0}
- In-memory only. No model, IFC or review state was written. The trial geometry is still CANDIDATE_UNREVIEWED with an ASSUMED_FOR_PREVIEW scale.

## Pictures

- `01_full_wall_original_current_proposed.png`: full wall with its three junctions: original, current, proposed, both; no mask tint
- `02_full_wall_with_prediction_mask.png`: same views with the predicted wall mask tinted
- `03_detail_junction_wall_002.png`: detail at junction_wall_002
- `04_detail_junction_wall_003.png`: detail at junction_wall_003
- `05_detail_junction_wall_004.png`: detail at junction_wall_004
- `06_detail_mid_span.png`: detail at mid_span

## If you agree

Put this entry in your own review record for this object, with your own reason, and apply the record as
`REVIEW_INSTRUCTIONS.md` describes. Until then nothing changes.

```json
{
  "object_id": "wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012",
  "kind": "wall",
  "decision": "ACCEPT_WITH_EDITS",
  "edits": [
    {
      "field": "axis_px.start",
      "after": [
        305.5,
        241.5
      ],
      "reason": "<reviewer's own reason>"
    },
    {
      "field": "axis_px.end",
      "after": [
        305.5,
        160.04166666666666
      ],
      "reason": "<reviewer's own reason>"
    }
  ],
  "notes": null
}
```

If you do not agree, record `ACCEPT` (keeps x 304.5), `REJECT`, or `ACCEPT_WITH_EDITS` with other values.
