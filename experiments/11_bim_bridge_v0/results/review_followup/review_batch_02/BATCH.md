# Review batch 02: wall_003, wall_004, door_opening-c02

Run `bim_bridge_v0_20260928_183649_UTC`. Written 2026-09-29T16:25:11Z.

**APPROVED EDITS SHOWN FOR REVIEW — NOT APPLIED OR EXPORTED**

Visualization only. No review record was applied. These three objects are not accepted; each waits for an explicit decision.
Scale is `ASSUMED_FOR_PREVIEW`, not confirmed. Viewer inspection: NOT_RUN.

## Combined overlay

`/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/review_batch_02_20260929_162511_UTC/01_combined_overlay_approved_edits_NOT_APPLIED.png`

It shows the original drawing, and below it the state with only the approved edits: wall_012 axis x = 305.5 at both ends, wall_002 start x = 233.0.

## Existing close-ups, reused

| Object | Close-up |
| --- | --- |
| `wall_003` | `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/review_package_20260928_195105_UTC/04_closeup_wall_003.png` |
| `wall_004` | `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/review_package_20260928_195105_UTC/05_closeup_wall_004.png` |
| `door_opening-c02` | `/mnt/e/AI_Team/mitunet/experiments/bim_bridge_v0/bim_bridge_v0_20260928_183649_UTC/real/review_package_20260928_195105_UTC/07_closeup_door_opening-c02.png` |

These were drawn before the approved edits. They show wall_012 at x 304.5 and the wall_002 start at x 266.

## wall_003

`wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003`

- Axis [304.5, 220.5] to [474.5, 220.5], thickness 6.0 px (source: vectorizer). Edits recorded: 0.
- At mid-length: predicted wall covers y 217.5..223.5; footprint spans 217.5..223.5.
- start [304.5, 220.5]: inside the wall_012 footprint as approved (x 303.5..307.5); 1 px from the approved wall_012 axis x 305.5; before the approved edit the axes met exactly at x 304.5.
- end [474.5, 220.5]: upstream intersection with wall_014, which is NOT SELECTED / NOT EXPORTED.
- Along its length: upstream wall_013 meets it at [416.0, 220.5]; NOT SELECTED / NOT EXPORTED.
- It hosts door_opening-c02.

## wall_004

`wall:cubicasa-high-quality-architectural-333-val-region-01:wall_004`

- Axis [242.0, 242.0] to [304.5, 241.5], thickness 4.0 px (source: vectorizer). Edits recorded: 0.
- The axis is not exactly horizontal: y differs by 0.5 px between its ends.
- At mid-length: predicted wall covers y 240.5..244.5; footprint spans 239.75..243.75.
- start [242.0, 242.0]: no selected wall and no upstream intersection recorded at this end.
- end [304.5, 241.5]: inside the wall_012 footprint as approved (x 303.5..307.5); 1 px from the approved wall_012 axis x 305.5; before the approved edit the axes met exactly at x 304.5.
- Decision 002 on wall_012 accepted the 2D connection at this junction for the limited preview and disclosed the underfilled outside corner. It authorized no edit to wall_004 and is not a decision on wall_004.

## door_opening-c02

`opening:cubicasa-high-quality-architectural-333-val-region-01:door_opening-c02`

- Host, from the candidate record (`host_wall_id`): `wall:cubicasa-high-quality-architectural-333-val-region-01:wall_003`. Host decision in the draft: pending.
- offset_px 4.0, width_px 28.0, measured from the host axis start x 304.5: x 308.5 to 336.5.
- From predicted door_opening component 2 (168 px, bbox [309, 218, 336, 223]). Component centroid is 0.00 px from the host axis. 84% of the predicted door_opening pixels are also predicted structural_wall pixels.
- Gap from the wall_012 face to the aperture: 2 px in the candidate, 1 px with the approved wall_012 edit. The aperture itself is not moved.
- An aperture is exported only if its host wall is exported. A decision on the aperture does not decide its host.
- Aperture height and sill are preview assumptions, not predictions.

## How to decide

For each object: `ACCEPT`, `ACCEPT_WITH_EDITS` (wall fields `axis_px.start`, `axis_px.end`, `thickness_px`; aperture fields `offset_px`, `width_px`) or `REJECT`.
