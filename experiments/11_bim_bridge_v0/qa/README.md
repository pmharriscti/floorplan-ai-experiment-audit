# Visual QA - bim_bridge_v0 downstream IFC bridge

This directory holds one review aid, copied without regeneration from the bridge run. No training and no
inference was performed.

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
