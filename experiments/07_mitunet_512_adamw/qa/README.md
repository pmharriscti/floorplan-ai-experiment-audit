# Visual QA - MitUNet 512 AdamW optimizer comparator

This directory contains six representative test samples copied from the historical Adam-vs-AdamW comparison artifacts. No training or inference was run for this audit copy.

Contact sheet: [contact_sheet.png](contact_sheet.png)

| Role | Sample | Adam IoU | AdamW IoU | AdamW minus Adam IoU | Metadata | Comparison |
| --- | --- | ---: | ---: | ---: | --- | --- |
| clean_strongest | high_quality_architectural/7696 | 0.954881 | 0.961971 | +0.007090 | [metadata](high_quality_architectural__7696/metadata.json) | [comparison](high_quality_architectural__7696/comparison_adam_vs_adamw.png) |
| difficult_worst | high_quality_architectural/9543 | 0.571387 | 0.520311 | -0.051076 | [metadata](high_quality_architectural__9543/metadata.json) | [comparison](high_quality_architectural__9543/comparison_adam_vs_adamw.png) |
| false_positive_heavy | high_quality_architectural/9422 | 0.756660 | 0.734919 | -0.021741 | [metadata](high_quality_architectural__9422/metadata.json) | [comparison](high_quality_architectural__9422/comparison_adam_vs_adamw.png) |
| false_negative_heavy | high_quality_architectural/7715 | 0.646253 | 0.624026 | -0.022227 | [metadata](high_quality_architectural__7715/metadata.json) | [comparison](high_quality_architectural__7715/comparison_adam_vs_adamw.png) |
| sparse_target | high_quality_architectural/3527 | 0.572162 | 0.599554 | +0.027392 | [metadata](high_quality_architectural__3527/metadata.json) | [comparison](high_quality_architectural__3527/comparison_adam_vs_adamw.png) |
| dense_target | high_quality_architectural/5617 | 0.898926 | 0.838575 | -0.060351 | [metadata](high_quality_architectural__5617/metadata.json) | [comparison](high_quality_architectural__5617/comparison_adam_vs_adamw.png) |

Each sample folder includes `source.png`, `ground_truth_wall_mask.png`, `adam_prediction_wall_mask.png`, `adamw_prediction_wall_mask.png`, `adamw_prediction_overlay.png`, `ground_truth_wall_overlay.png`, `comparison_adam_vs_adamw.png`, and `metadata.json`.
