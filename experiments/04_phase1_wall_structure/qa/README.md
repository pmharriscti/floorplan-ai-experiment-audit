# Visual QA - Phase 1 wall structure

This directory contains three curated validation samples for visual audit. Structural predictions come from verified historical checkpoints or saved probability maps; no training was run.

Contact sheet: [contact_sheet.png](contact_sheet.png)

Overlay palette: green = true positive, red = false positive, blue = false negative.

| Sample | Role | Source Metrics | Metadata | Primary Overlay |
| --- | --- | --- | --- | --- |
| high_quality_architectural/333 | typical_clean_validation_case | centerline clDice 0.543596; junction F1@5 0.918919 | [metadata](high_quality_architectural__333/metadata.json) | [overlay](high_quality_architectural__333/overlay_wall_region_errors.png) |
| high_quality_architectural/3015 | strong_high_resolution_case | centerline clDice 0.757128; junction F1@5 0.780488 | [metadata](high_quality_architectural__3015/metadata.json) | [overlay](high_quality_architectural__3015/overlay_wall_region_errors.png) |
| high_quality_architectural/5559 | difficult_failure_case | centerline clDice 0.523894; junction F1@5 0.461538 | [metadata](high_quality_architectural__5559/metadata.json) | [overlay](high_quality_architectural__5559/overlay_wall_region_errors.png) |

Each sample folder includes a source image, target masks, prediction masks, overlays, historical target QA where available, and `metadata.json`.
