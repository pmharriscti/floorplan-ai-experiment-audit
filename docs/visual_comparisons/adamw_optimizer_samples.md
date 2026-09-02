# AdamW Optimizer Visual Samples

These representative test samples come from the historical Adam-vs-AdamW comparison artifacts for experiment `07_mitunet_512_adamw`.

| Role | Sample | Adam Dice | AdamW Dice | AdamW minus Adam Dice | Adam IoU | AdamW IoU | AdamW minus Adam IoU | Comparison |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| clean_strongest | high_quality_architectural/7696 | 0.976920 | 0.980617 | +0.003697 | 0.954881 | 0.961971 | +0.007090 | [comparison](../../experiments/07_mitunet_512_adamw/qa/high_quality_architectural__7696/comparison_adam_vs_adamw.png) |
| difficult_worst | high_quality_architectural/9543 | 0.727239 | 0.684480 | -0.042759 | 0.571387 | 0.520311 | -0.051076 | [comparison](../../experiments/07_mitunet_512_adamw/qa/high_quality_architectural__9543/comparison_adam_vs_adamw.png) |
| false_positive_heavy | high_quality_architectural/9422 | 0.861475 | 0.847208 | -0.014267 | 0.756660 | 0.734919 | -0.021741 | [comparison](../../experiments/07_mitunet_512_adamw/qa/high_quality_architectural__9422/comparison_adam_vs_adamw.png) |
| false_negative_heavy | high_quality_architectural/7715 | 0.785120 | 0.768493 | -0.016627 | 0.646253 | 0.624026 | -0.022227 | [comparison](../../experiments/07_mitunet_512_adamw/qa/high_quality_architectural__7715/comparison_adam_vs_adamw.png) |
| sparse_target | high_quality_architectural/3527 | 0.727867 | 0.749651 | +0.021785 | 0.572162 | 0.599554 | +0.027392 | [comparison](../../experiments/07_mitunet_512_adamw/qa/high_quality_architectural__3527/comparison_adam_vs_adamw.png) |
| dense_target | high_quality_architectural/5617 | 0.946773 | 0.912201 | -0.034572 | 0.898926 | 0.838575 | -0.060351 | [comparison](../../experiments/07_mitunet_512_adamw/qa/high_quality_architectural__5617/comparison_adam_vs_adamw.png) |

The experiment-level outcome should be read from the official metrics JSON: AdamW improved precision slightly but reduced recall enough to lower held-out test IoU and Dice versus the Adam control.
