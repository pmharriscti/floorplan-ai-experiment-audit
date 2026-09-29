# Review in progress: status 03

Written 2026-09-29T13:27:39Z. Earlier status files are kept as written.
No review has been applied. In the candidate geometry every object is still `CANDIDATE_UNREVIEWED`. Scale is `ASSUMED_FOR_PREVIEW`, not confirmed. No new IFC exists.

## Decisions in the draft record

| Object | Decision | Record |
| --- | --- | --- |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_012` | `ACCEPT_WITH_EDITS`, limited image-space preview | `decision_003_wall_012_whole_object_20260929_132739_UTC.json` |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002` | pending | |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003` | pending | |
| `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004` | pending | |
| `opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02` | pending | |

## wall_012

- Axis x 305.5 at both ends. y unchanged.
- Thickness 4.0 px: preview approximation. Not a verified thickness or a real-world measurement. Origin stays prediction-mask-derived.
- Lower junction with wall_004: 2D connection accepted for the limited preview.
- Disclosed limitation: outside of the L-shaped corner underfilled. Corner shape not confirmed.
- No corner-filling or neighbouring-wall edits authorized.
- The file was written by an AI assistant from the reviewer's instruction. The reviewer did not sign it.

## What the validator still refuses

- reviewer is empty: a named human reviewer is required
- reviewer_role is empty
- reviewed_utc must be YYYY-MM-DDTHH:MM:SSZ
- wall:cubicasa-high-quality-architectural-333-val-region-01:wall_002: decision must be one of ['ACCEPT', 'ACCEPT_WITH_EDITS', 'REJECT']
- wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003: decision must be one of ['ACCEPT', 'ACCEPT_WITH_EDITS', 'REJECT']
- wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004: decision must be one of ['ACCEPT', 'ACCEPT_WITH_EDITS', 'REJECT']
- opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02: decision must be one of ['ACCEPT', 'ACCEPT_WITH_EDITS', 'REJECT']

## Next

1. The reviewer decides the four pending objects.
2. The reviewer states `reviewer_role`.
3. Then `apply-review` runs on the completed record, and a new IFC revision is exported beside the earlier one.

Current draft: `review_record_DRAFT_03.json`.
