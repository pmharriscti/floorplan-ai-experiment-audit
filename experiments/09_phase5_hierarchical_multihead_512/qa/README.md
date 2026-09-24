# Visual QA - Phase 5 hierarchical multi-head MitUNet 512

This directory contains the three shared validation samples for visual audit. Prediction masks were decoded from the source run's saved thresholded bitmasks (`masks/val/<sample>__heads.png`, `masks/val/<sample>__fixtures.png`), written by its evaluate stage at the validation-selected thresholds. No model inference, training or threshold selection was performed, and the historical run directory was not modified.

Contact sheet: [contact_sheet.png](contact_sheet.png) (columns: source, then TP/FP/FN overlays for structural wall, wall boundary, centerline, junction, endpoint, door opening, window opening, fixtures union).

Overlay palette: green = true positive, red = false positive, blue = false negative.

| Sample | Role | Source Metrics (per-image CSV) | Metadata | Primary Overlay |
| --- | --- | --- | --- | --- |
| high_quality_architectural/333 | typical_clean_validation_case | wall IoU 0.807032; boundary F1@2 0.952146; junction F1@5 0.864865; door F1 1.000000; window F1 0.800000 | [metadata](high_quality_architectural__333/metadata.json) | [overlay](high_quality_architectural__333/overlay_structural_wall_errors.png) |
| high_quality_architectural/3015 | strong_high_resolution_case | wall IoU 0.810389; boundary F1@2 0.964178; junction F1@5 0.864198; door F1 0.647059; window F1 0.690909 | [metadata](high_quality_architectural__3015/metadata.json) | [overlay](high_quality_architectural__3015/overlay_structural_wall_errors.png) |
| high_quality_architectural/5559 | difficult_failure_case | wall IoU 0.636836; boundary F1@2 0.842826; junction F1@5 0.438356; door F1 0.428571; window F1 0.666667 | [metadata](high_quality_architectural__5559/metadata.json) | [overlay](high_quality_architectural__5559/overlay_structural_wall_errors.png) |

Each sample folder includes `source.png` (512 letterbox review copy), `ground_truth_<head>_mask.png` and `prediction_<head>_mask.png` for the seven binary heads plus a fixtures union mask, `overlay_<head>_errors.png` for each, and `metadata.json` with source paths, hashes, thresholds, the run's per-image metrics and the pixel metrics recomputed from the saved masks. The recomputed structural-wall IoU matches the run's per-image CSV exactly for all three samples.

Junction and endpoint ground truth are small disks and their predictions are thresholded heatmap pixels; those overlays are for visual inspection only, and the historical point-matching F1@5 px metrics remain authoritative. Fixture overlays show the union over the nine classes; per-class pixel IoU for the classes present is in each `metadata.json`.
