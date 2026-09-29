# Visual QA - bim_bridge_v0 downstream IFC bridge

This directory holds one review aid copied without regeneration from the bridge run, and three review images
added on 2026-09-29 as reduced derived copies. No training and no inference was performed.

| File | Content | Metadata |
| --- | --- | --- |
| [review_overlay_candidates_on_source.png](review_overlay_candidates_on_source.png) | Region of interest of `high_quality_architectural/333` (val split), letterbox space, 5x zoom | [metadata.json](metadata.json) |

The image has two panels.

1. Top: the source image, letterboxed and cropped to the region of interest.
2. Bottom: the same crop with the predicted `structural_wall` mask in grey and the predicted `door_opening`
   mask in orange. Candidate walls are drawn with a blue outline and a green centreline. The candidate
   aperture has a magenta outline.

**This overlay contains no ground truth.** It does not use the audit's green, red and blue error palette,
because this experiment compares nothing with a reference and makes no accuracy claim. It shows what the
model predicted and what geometry the bridge proposes from it, so that a person can review the candidates.

**No IFC viewer screenshot exists.** No viewer was run. The steps for a person to inspect the file are in
[../results/real_VIEWER_INSPECTION_STEPS.md](../results/real_VIEWER_INSPECTION_STEPS.md).

The sample is a CubiCasa5K validation image that this repository already publishes for experiments 01-06 and 09.

## Review follow-up images (2026-09-29)

These three images are reduced derived copies: resized and saved as JPEG files to keep the
repository small. The full-size sources stay in the run directory. Source paths and hashes are in
[metadata.json](metadata.json).

| File | Content |
| --- | --- |
| [review_followup/review_batch_02_combined_overlay_approved_edits_NOT_APPLIED.jpg](review_followup/review_batch_02_combined_overlay_approved_edits_NOT_APPLIED.jpg) | Original drawing, and below it the candidate geometry with only the two approved edits drawn in. `wall_003`, `wall_004` and `door_opening-c02` are marked as pending. |
| [review_followup/proposal_wall_012_axis_shift_original_current_proposed.jpg](review_followup/proposal_wall_012_axis_shift_original_current_proposed.jpg) | `wall_012`: original drawing, current footprint at axis x 304.5, proposed footprint at axis x 305.5, and both. |
| [review_followup/proposal_wall_002_start_extension_original_current_proposed.jpg](review_followup/proposal_wall_002_start_extension_original_current_proposed.jpg) | `wall_002`: original drawing, current start at x 266, proposed start at x 233. Upstream `wall_001` is labelled NOT SELECTED / NOT EXPORTED. |

**The approved edits are drawn for review only. They were not applied to the candidate geometry and were not
exported.** The IFC of this experiment still holds the unreviewed candidate.

These images contain no ground truth and make no accuracy claim. They are not viewer screenshots.
