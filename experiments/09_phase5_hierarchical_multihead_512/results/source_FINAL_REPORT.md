# mitunet_hierarchical_multihead_512 — final report

Run: `mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED`  |  generated 2026-09-24T16:18:41.242909+00:00  |  git {'commit': '459778bd07b1a0b8a60413a2e681bbd4ff7bd829', 'branch': 'master', 'dirty_entries': 162}

## Experiment identity

CONTROL BASELINE: MitUNet + MiT-B4, CubiCasa5K, 512×512 RGB, same train/val/test split, Adam, LR 1e-4, weight decay 0, batch 4, AMP, 30 epochs, Tversky α=0.6 β=0.4, seed 42, baseline preprocessing, baseline target semantics, baseline evaluation protocol.

EXPERIMENTAL VARIABLES: (1) output structure — shared encoder + task-group decoders + independent sigmoid heads; (2) added targets — boundary, centerline, junction, endpoint, door_opening, window_opening, fixtures; (3) staged schedule from the baseline checkpoint (heads warm-up → joint fine-tune, encoder LR 1e-5); (4) GradNorm task weighting; (5) wall-floor-gated checkpoint selection.

HELD CONSTANT: dataset, split manifests, preprocessing, optimizer family, weight decay, batch sizes, AMP, seed, 30 total epochs, Tversky wall loss, patience values, validation-only threshold selection, untouched test set.

## Baseline comparison (baseline §19)

| Configuration | Val IoU | Val Dice | Test IoU | Test Dice | Threshold | Main change |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| baseline_historical | 0.8188 | 0.9004 | 0.8244 | 0.9038 | 0.1 | none |
| baseline_reproduced_same_code | 0.8188 | 0.9004 | 0.8244 | 0.9038 | 0.1 | none (same checkpoint, this evaluator) |
| hierarchical_at_baseline_threshold | 0.8162 | 0.8988 | 0.8200 | 0.9011 | 0.1 | hierarchical multi-head (structural_wall head) |
| hierarchical_at_selected_threshold | 0.8164 | 0.8989 | 0.8202 | 0.9012 | 0.05 | hierarchical multi-head (structural_wall head, validation-selected threshold) |

Replacement requirement (val structural_wall IoU ≥ reproduced baseline 0.8188 − 0.005 = 0.8138): **MET**  (Δ val IoU vs reproduced baseline: -0.0027; Δ test IoU: -0.0044).

Selected checkpoint: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/checkpoints/best_gated_hierarchical_score.pth` (epoch 30, phase joint_finetune, gate-met checkpoint: yes).

## Per-head results (selected thresholds)

| Head | Stage metric | Val | Test | Val pixel IoU | Val precision | Val recall | Test pixel IoU |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| structural_wall | micro_iou | 0.8164 | 0.8202 | 0.8164 | 0.9031 | 0.8948 | 0.8202 |
| wall_boundary | boundary_f1_2px | 0.9546 | 0.9539 | 0.3023 | 0.3139 | 0.8914 | 0.3039 |
| wall_centerline | skeleton_cldice | 0.4992 | 0.5035 | 0.6478 | 0.7775 | 0.7952 | 0.6530 |
| junction | f1_5px | 0.7871 | 0.7667 | 0.3655 | 0.6644 | 0.4483 | 0.3628 |
| endpoint | f1_5px | 0.3367 | 0.3174 | 0.0730 | 0.2970 | 0.0882 | 0.0680 |
| door_opening | object_f1 | 0.8803 | 0.8752 | 0.5903 | 0.6393 | 0.8851 | 0.5909 |
| window_opening | object_f1 | 0.8806 | 0.8557 | 0.7032 | 0.7442 | 0.9274 | 0.6987 |
| fixtures | macro_iou | 0.4582 | 0.4562 | 0.6037 | 0.7414 | 0.7648 | 0.5870 |
| visible_wall (derived) | micro IoU | 0.7890 | 0.7935 | 0.7890 | 0.8907 | 0.8736 | 0.7935 |

Fixture classes (val IoU / test IoU / val sample support):

- appliance: 0.5987 / 0.5964 / 393
- bathtub_shower_jacuzzi: 0.2515 / 0.2832 / 332
- cabinetry_storage: 0.6990 / 0.6903 / 395
- chimney: 0.1328 / 0.0891 / 45
- fireplace: 0.4047 / 0.4358 / 131
- other_fixture: 0.1463 / 0.1234 / 82
- sauna_bench: 0.7468 / 0.7277 / 240
- sink_tap: 0.5137 / 0.5265 / 390
- toilet_urinal: 0.6300 / 0.6332 / 379

Hierarchical score — val 0.7500, test 0.7467 (weights {'door_opening_object_f1': 0.1, 'endpoint_f1_5px': 0.05, 'fixtures_macro_iou': 0.1, 'junction_f1_5px': 0.05, 'structural_wall_iou': 0.4, 'wall_boundary_f1_2px': 0.1, 'wall_centerline_skeleton_cldice': 0.1, 'window_opening_object_f1': 0.1}).

Selected thresholds: `{"door_opening": 0.95, "endpoint": 0.8, "endpoint_nms_radius": 3, "fixtures": {"appliance": 0.45, "bathtub_shower_jacuzzi": 0.1, "cabinetry_storage": 0.8, "chimney": 0.95, "fireplace": 0.1, "other_fixture": 0.95, "sauna_bench": 0.75, "sink_tap": 0.65, "toilet_urinal": 0.3}, "junction": 0.85, "junction_nms_radius": 3, "opening_min_component_area": 1, "structural_wall": 0.05, "wall_boundary": 0.95, "wall_centerline": 0.95, "window_opening": 0.9}`

## Training

- epochs configured 30 (warm-up 4, joint 26); completed 30; stopped early: no
- weighting method: fixed; final task weights: {'door_opening': 0.12, 'endpoint': 0.03, 'fixtures': 0.08, 'junction': 0.05, 'structural_wall': 0.4, 'wall_boundary': 0.08, 'wall_centerline': 0.12, 'window_opening': 0.12}
- bests: {"gated": {"epoch": 30, "score": 0.7445317228890463, "wall_iou_at_baseline_threshold": 0.8161948635674233}, "score": {"epoch": 30, "gate_passed": true, "score": 0.7445317228890463, "wall_iou_at_baseline_threshold": 0.8161948635674233}, "wall": {"epoch": 11, "score": 0.8230897318865986}}
- mean epoch time 767.6 s; total 12223 s; steps/epoch 1050
- parameters: 74468332 (added 10219668 over the baseline)
- GPU peak (smoke): {'max_memory_allocated_gb': 10.07205376, 'max_memory_reserved_gb': 10.315890688}
- MLflow: {'active': True, 'failure': None, 'run_id': '88a860218a924f6f88bf614ca2dc00fe', 'tracking_uri': 'sqlite:////mnt/e/AI_Team/mitunet/mlflow/mlflow.db'}

| Epoch | Phase | Train loss | Val wall IoU@ref | Gate | Score | Door F1 | Window F1 | Fixtures mIoU | Boundary F1 | clDice |
| ---: | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | heads_warmup | 0.1916 | 0.8188 | True | 0.6716 | 0.8131 | 0.7947 | 0.2208 | 0.9241 | 0.4949 |
| 2 | heads_warmup | 0.1296 | 0.8188 | True | 0.6854 | 0.8324 | 0.8186 | 0.2929 | 0.9342 | 0.4935 |
| 3 | heads_warmup | 0.1223 | 0.8188 | True | 0.7062 | 0.8362 | 0.8421 | 0.3310 | 0.9365 | 0.5056 |
| 4 | heads_warmup | 0.1177 | 0.8188 | True | 0.7172 | 0.8329 | 0.8574 | 0.3698 | 0.9327 | 0.5112 |
| 5 | joint_finetune | 0.1151 | 0.8210 | True | 0.7128 | 0.8312 | 0.8130 | 0.3775 | 0.9350 | 0.5191 |
| 6 | joint_finetune | 0.1114 | 0.8211 | True | 0.7225 | 0.8555 | 0.8459 | 0.3856 | 0.9395 | 0.5244 |
| 7 | joint_finetune | 0.1074 | 0.8218 | True | 0.7246 | 0.8500 | 0.8532 | 0.3916 | 0.9402 | 0.5117 |
| 8 | joint_finetune | 0.1037 | 0.8224 | True | 0.7293 | 0.8491 | 0.8602 | 0.4079 | 0.9400 | 0.5234 |
| 9 | joint_finetune | 0.1004 | 0.8228 | True | 0.7296 | 0.8677 | 0.8507 | 0.4072 | 0.9406 | 0.5184 |
| 10 | joint_finetune | 0.0976 | 0.8229 | True | 0.7290 | 0.8695 | 0.8431 | 0.4195 | 0.9419 | 0.5087 |
| 11 | joint_finetune | 0.0947 | 0.8231 | True | 0.7297 | 0.8511 | 0.8578 | 0.4182 | 0.9366 | 0.5140 |
| 12 | joint_finetune | 0.0920 | 0.8224 | True | 0.7321 | 0.8595 | 0.8633 | 0.4183 | 0.9401 | 0.5161 |
| 13 | joint_finetune | 0.0897 | 0.8220 | True | 0.7304 | 0.8609 | 0.8451 | 0.4317 | 0.9358 | 0.5088 |
| 14 | joint_finetune | 0.0873 | 0.8217 | True | 0.7318 | 0.8576 | 0.8495 | 0.4219 | 0.9414 | 0.5098 |
| 15 | joint_finetune | 0.0849 | 0.8219 | True | 0.7326 | 0.8534 | 0.8601 | 0.4267 | 0.9379 | 0.5075 |
| 16 | joint_finetune | 0.0829 | 0.8210 | True | 0.7337 | 0.8675 | 0.8605 | 0.4227 | 0.9394 | 0.5032 |
| 17 | joint_finetune | 0.0811 | 0.8204 | True | 0.7340 | 0.8679 | 0.8639 | 0.4299 | 0.9410 | 0.5044 |
| 18 | joint_finetune | 0.0790 | 0.8189 | True | 0.7329 | 0.8638 | 0.8549 | 0.4362 | 0.9414 | 0.4968 |
| 19 | joint_finetune | 0.0771 | 0.8197 | True | 0.7356 | 0.8705 | 0.8504 | 0.4303 | 0.9425 | 0.5099 |
| 20 | joint_finetune | 0.0752 | 0.8193 | True | 0.7336 | 0.8613 | 0.8571 | 0.4327 | 0.9403 | 0.5037 |
| 21 | joint_finetune | 0.0735 | 0.8189 | True | 0.7368 | 0.8683 | 0.8599 | 0.4369 | 0.9437 | 0.4968 |
| 22 | joint_finetune | 0.0719 | 0.8178 | True | 0.7388 | 0.8706 | 0.8730 | 0.4378 | 0.9454 | 0.5060 |
| 23 | joint_finetune | 0.0702 | 0.8187 | True | 0.7387 | 0.8607 | 0.8779 | 0.4357 | 0.9427 | 0.5022 |
| 24 | joint_finetune | 0.0685 | 0.8175 | True | 0.7402 | 0.8698 | 0.8634 | 0.4373 | 0.9440 | 0.5024 |
| 25 | joint_finetune | 0.0671 | 0.8176 | True | 0.7342 | 0.8690 | 0.8510 | 0.4391 | 0.9448 | 0.4917 |
| 26 | joint_finetune | 0.0657 | 0.8178 | True | 0.7363 | 0.8772 | 0.8462 | 0.4373 | 0.9446 | 0.5041 |
| 27 | joint_finetune | 0.0645 | 0.8166 | True | 0.7377 | 0.8690 | 0.8664 | 0.4401 | 0.9462 | 0.5023 |
| 28 | joint_finetune | 0.0630 | 0.8163 | True | 0.7402 | 0.8684 | 0.8681 | 0.4441 | 0.9442 | 0.5028 |
| 29 | joint_finetune | 0.0601 | 0.8166 | True | 0.7441 | 0.8729 | 0.8722 | 0.4444 | 0.9474 | 0.5032 |
| 30 | joint_finetune | 0.0588 | 0.8162 | True | 0.7445 | 0.8685 | 0.8743 | 0.4491 | 0.9460 | 0.4992 |

## Label Validation

- status: **PASS**; critical failures: []; warnings: 2
- inspected samples: 5000; integrity per split: {"test": {"analysed_samples": 400, "failed_samples": 0, "invalid_value_masks": 0, "missing_files": 0, "semantic_failures": 0, "semantic_warnings": 321, "shape_mismatches": 0, "successfully_loaded": 400, "total_samples": 400, "warning_histogram": {"door_opening_raw_component_without_wall_support": 2, "empty_door_opening": 1, "empty_fixtures": 2, "empty_window_opening": 2, "window_opening_identical_to_window_symbol": 313, "window_opening_raw_component_without_wall_support": 1}}, "train": {"analysed_samples": 4200, "failed_samples": 0, "invalid_value_masks": 0, "missing_files": 0, "semantic_failures": 0, "semantic_warnings": 3379, "shape_mismatches": 0, "successfully_loaded": 4200, "total_samples": 4200, "warning_histogram": {"door_opening_raw_component_without_wall_support": 8, "empty_door_opening": 1, "empty_fixtures": 17, "empty_window_opening": 21, "window_opening_identical_to_window_symbol": 3329, "window_opening_raw_component_without_wall_support": 3}}, "val": {"analysed_samples": 400, "failed_samples": 0, "invalid_value_masks": 0, "missing_files": 0, "semantic_failures": 0, "semantic_warnings": 328, "shape_mismatches": 0, "successfully_loaded": 400, "total_samples": 400, "warning_histogram": {"door_opening_raw_component_without_wall_support": 1, "empty_fixtures": 1, "empty_window_opening": 1, "window_opening_identical_to_window_symbol": 325}}}
- structural_wall identical to baseline target: yes (100 samples, min IoU 1.0000)
- splits identical to baseline manifests: yes
- semantic checks: {"boundary_within_1px_of_wall_ratio_mean": 1.0, "centerline_inside_wall_ratio_mean": 1.0, "door_opening_identical_to_symbol_fraction": 0.9389755902360944, "door_opening_raw_components": 49425, "door_opening_raw_components_without_wall_support": 12, "door_opening_raw_wall_overlap_ratio_mean": 0.998948474456871, "door_opening_raw_without_wall_support_fraction": 0.00024279210925644916, "door_opening_vs_door_symbol_iou_mean": 0.9981829281427376, "endpoint_components_on_centerline_ratio_mean": 1.0, "junction_components_on_centerline_ratio_mean": 1.0, "note": "symbol == opening equality is RECORDED, never assumed; a high identical fraction means the candidate_v2 opening definition coincides with the symbol footprint for this parser and must be interpreted as such", "visible_subset_violations": 0, "visible_wall_removed_fraction_mean": 0.2370680519862004, "window_opening_identical_to_symbol_fraction": 0.7972266881028939, "window_opening_raw_components": 39573, "window_opening_raw_components_without_wall_support": 5, "window_opening_raw_wall_overlap_ratio_mean": 0.9991656247852495, "window_opening_raw_without_wall_support_fraction": 0.0001263487731534127, "window_opening_vs_window_symbol_iou_mean": 0.9973508522025082}
- target generation: version cubicasa-hierarchical-multihead-v1 hash 0e8b66cffa20f7ae3539193cf5673f66386dc1f01a66749876118d52e7e6f391
- overlays: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/label_validation`; review manifest: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/label_validation/review_manifest.csv` (100 rows)

Were the validation/test targets identical to the baseline experiment? **structural_wall: YES** (Phase 1 wall_region == letterboxed baseline wall mask). All other heads: **NO — they are new targets the baseline never had**, so their metrics have no baseline counterpart.

## Proofs

- wall logit equivalence with baseline at initialisation: yes (max |Δ| = 0.0)
- baseline reproduction with this evaluator: within tolerance yes; deltas {"test@0.10": {"abs_delta_iou": 7.768426143472951e-07, "historical_dice": 0.9037695157362454, "historical_iou": 0.8244338473612428, "reproduced_dice": 0.9037690489618984, "reproduced_iou": 0.8244330705186285}, "test@0.50": {"abs_delta_iou": 1.37927470111876e-07, "historical_dice": 0.9032839283924962, "historical_iou": 0.8236260521545145, "reproduced_dice": 0.9032838454438651, "reproduced_iou": 0.8236259142270443}, "val@0.10": {"abs_delta_iou": 8.310851061787972e-07, "historical_dice": 0.9004022456862498, "historical_iou": 0.8188469303015113, "reproduced_dice": 0.9004017432471942, "reproduced_iou": 0.8188460992164052}}
- smoke: yes; head gradients present: {'door_opening': True, 'endpoint': True, 'fixtures': True, 'junction': True, 'structural_wall': True, 'wall_boundary': True, 'wall_centerline': True, 'window_opening': True}

## What this run does NOT establish

- It does not prove the flat multiclass head was the sole cause of the earlier regression; it tests whether the hierarchical design preserves the wall baseline while adding heads.
- GradNorm vs fixed weighting is only established if the paired `--weighting fixed` control run is executed.
- window_opening uses the candidate_v2 top-level-polygon definition; the recorded symbol-equality fraction must be read before treating it as a corridor target.

## Artifacts

- run_dir: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED`
- checkpoints: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/checkpoints`
- logs: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/logs`
- metrics: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/metrics`
- predictions: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/predictions`
- masks: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/masks`
- overlays: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/overlays`
- label_validation: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/label_validation`
- proof: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/audit`
- reports: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/artifacts`
- manifest_dir: `/mnt/e/AI_Team/mitunet/derived_data/mitunet_hierarchical_multihead_512/manifests/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED`
- cache_root: `/mnt/e/AI_Team/mitunet/targets/mitunet_hierarchical_multihead_512`
- mlflow: `/mnt/e/AI_Team/mitunet/mlflow`
