# Experiment 14 Visual Evidence Plan

The proposal links existing parent images. Their original metadata and provenance remain in the parent entries; they are not predictions from a combined experiment-14 checkpoint.

| Parent | Image | What it shows |
| --- | --- | --- |
| 06 | [1024 wall overlay](../../06_binary_mitunet_1024/qa/high_quality_architectural__333/overlay_wall_errors.png) | Existing whole-plan wall predictions on `high_quality_architectural/333` |
| 09 | [Phase 5 contact sheet](../../09_phase5_hierarchical_multihead_512/qa/contact_sheet.png) | Existing multi-head predictions on the shared validation sample identities |
| 13 / Phase 3A.2 | [10543 / door_0003 geometry sheet](../../13_phase3a_human_review_tool/qa/geometry_updates/high_quality_architectural__10543__door_0003__door_opening.png) | Source SVG, host wall, jambs and v3/v3.1/v3.2 targets |
| 13 / Phase 3A.2 | [8690 / door_0005 geometry sheet](../../13_phase3a_human_review_tool/qa/geometry_updates/high_quality_architectural__8690__door_0005__door_opening.png) | Validation repair case and difficult source-wall context |

## Evidence To Capture From The New Run

Use the shared validation IDs `high_quality_architectural/333`, `3015`, and `5559`, plus `8690/door_0005` and the resize-survival regression `5981/door_0007`. Include train-only inspection sheets for the explicitly scoped repair instances, marked with their split. Expand the selection with a border-clipped opening, diagonal wall, sparse opening, rare fixture, empty valid target and declared unknown-source case.

For each selected plan, retain source image, raw and training masks, per-head predictions, TP/FP/FN overlays, native/model transform, head thresholds, target/reference identity, checkpoint hash and sample split. Show nine fixture classes individually rather than only their union.

For geometry cases, also retain native source threshold/host polygons, jambs, tangent/normal metadata, per-instance mask survival and before/after version differences. Mark raw predictions separately from postprocessed output. State coordinate space and metric tolerance beside every measured image.

Curate a small number of actual run images into this directory after execution. Keep full prediction dumps and probabilities in the external run archive.
