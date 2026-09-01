# Visual QA - Phase 2 boundary and door/openings

This directory contains three curated validation samples for visual audit. Structural predictions come from verified historical checkpoints or saved probability maps; no training was run.

Contact sheet: [contact_sheet.png](contact_sheet.png)

Overlay palette: green = true positive, red = false positive, blue = false negative.

| Sample | Role | Source Metrics | Metadata | Primary Overlay |
| --- | --- | --- | --- | --- |
| high_quality_architectural/333 | typical_clean_validation_case | wall IoU 0.718133; boundary F1@2 0.890143; door F1 1.000000 | [metadata](high_quality_architectural__333/metadata.json) | [overlay](high_quality_architectural__333/overlay_wall_boundary_errors.png) |
| high_quality_architectural/3015 | strong_high_resolution_case | wall IoU 0.755953; boundary F1@2 0.975916; door F1 0.384615 | [metadata](high_quality_architectural__3015/metadata.json) | [overlay](high_quality_architectural__3015/overlay_wall_boundary_errors.png) |
| high_quality_architectural/5559 | difficult_failure_case | wall IoU 0.597686; boundary F1@2 0.859041; door F1 0.375000 | [metadata](high_quality_architectural__5559/metadata.json) | [overlay](high_quality_architectural__5559/overlay_wall_boundary_errors.png) |

Each sample folder includes a source image, target masks, prediction masks, overlays, historical target QA where available, and `metadata.json`.
