# Review in progress: status 07

Written 2026-10-01T20:20:30Z. Earlier status files are kept as written.
No review has been applied. In the candidate geometry every object is still `CANDIDATE_UNREVIEWED`. Scale is `ASSUMED_FOR_PREVIEW`, not confirmed. No new IFC exists.

Reviewer role in the draft: `Prototype image-space geometry reviewer`.

| Object | Decision in the draft (limited image-space preview) |
| --- | --- |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002` | `ACCEPT_WITH_EDITS`, axis_px.start |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003` | `ACCEPT`, no edits |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004` | `ACCEPT`, no edits |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012` | `ACCEPT_WITH_EDITS`, axis_px.start; axis_px.end |
| `opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02` | pending |

## wall_004

- Accepted unchanged: axis [242.0, 242.0] to [304.5, 241.5], thickness 4.0 px, origin vectorizer.
- Limitation: at column 273 the footprint is 0.75 px higher than the prediction-mask centre.
- Limitation: the outside corner at wall_012 remains underfilled.
- Limitation: physical thickness, real-world dimensions and tolerance compliance are not verified.
- Not authorized: flattening the axis, snapping endpoints, filling the corner.
- To verify after export: geometric contact with wall_012 in the new IFC.

## What the validator still refuses

- reviewer is empty: a named human reviewer is required
- reviewed_utc must be YYYY-MM-DDTHH:MM:SSZ
- opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02: decision must be one of ['ACCEPT', 'ACCEPT_WITH_EDITS', 'REJECT']

## Needed from the reviewer

1. A decision for `door_opening-c02`.
2. The reviewer name for the record.

Current draft: `review_record_DRAFT_07.json`.
