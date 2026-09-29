# Review in progress: status 04

Written 2026-09-29T15:53:08Z. Earlier status files are kept as written.
No review has been applied. In the candidate geometry every object is still `CANDIDATE_UNREVIEWED`. Scale is `ASSUMED_FOR_PREVIEW`, not confirmed. No new IFC exists.

| Object | Decision in the draft | Record |
| --- | --- | --- |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002` | `ACCEPT_WITH_EDITS`, limited image-space preview. Start x 266.0 to 233.0. | `decision_004_wall_002_whole_object_20260929_155308_UTC.json` |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012` | `ACCEPT_WITH_EDITS`, limited image-space preview. Axis x 304.5 to 305.5. | `decision_003_wall_012_whole_object_20260929_132739_UTC.json` |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003` | pending | |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004` | pending | |
| `opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02` | pending | |

## What the validator still refuses

- reviewer is empty: a named human reviewer is required
- reviewer_role is empty
- reviewed_utc must be YYYY-MM-DDTHH:MM:SSZ
- wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003: decision must be one of ['ACCEPT', 'ACCEPT_WITH_EDITS', 'REJECT']
- wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004: decision must be one of ['ACCEPT', 'ACCEPT_WITH_EDITS', 'REJECT']
- opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02: decision must be one of ['ACCEPT', 'ACCEPT_WITH_EDITS', 'REJECT']

## Needed from the reviewer

1. Decisions for the three pending objects.
2. `reviewer_role`.

Then: apply the record, export a new IFC revision beside the earlier one, reopen it and verify geometry, ReviewDecisionNotes, Edits, CandidateOriginal and GlobalIds.

Current draft: `review_record_DRAFT_04.json`.
