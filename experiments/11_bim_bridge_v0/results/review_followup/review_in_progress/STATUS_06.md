# Review in progress: status 06

Written 2026-10-01T17:19:30Z. Earlier status files are kept as written.
No review has been applied. In the candidate geometry every object is still `CANDIDATE_UNREVIEWED`. Scale is `ASSUMED_FOR_PREVIEW`, not confirmed. No new IFC exists.

Reviewer role in the draft: `Prototype image-space geometry reviewer`.

| Object | Decision in the draft (limited image-space preview) | Record |
| --- | --- | --- |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002` | `ACCEPT_WITH_EDITS`. Start x 266.0 to 233.0. | `decision_004_wall_002_whole_object_20260929_155308_UTC.json` |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003` | `ACCEPT`. No edits. | `decision_005_wall_003_whole_object_20261001_171930_UTC.json` |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004` | pending | |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012` | `ACCEPT_WITH_EDITS`. Axis x 304.5 to 305.5. | `decision_003_wall_012_whole_object_20260929_132739_UTC.json` |
| `opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02` | pending | |

## wall_003

- Accepted unchanged: axis [304.5, 220.5] to [474.5, 220.5], thickness 6.0 px.
- Thickness is a preview approximation, origin vectorizer.
- Left endpoint is inside the wall_012 footprint as approved. No endpoint snapping authorized.
- Accepting the wall does not accept `door_opening-c02` and does not verify its IFC cut.

## What the validator still refuses

- reviewer is empty: a named human reviewer is required
- reviewed_utc must be YYYY-MM-DDTHH:MM:SSZ
- wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004: decision must be one of ['ACCEPT', 'ACCEPT_WITH_EDITS', 'REJECT']
- opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02: decision must be one of ['ACCEPT', 'ACCEPT_WITH_EDITS', 'REJECT']

## Needed from the reviewer

1. Decisions for `wall_004` and `door_opening-c02`.
2. The reviewer name for the record.

Current draft: `review_record_DRAFT_06.json`.
