# Experiment Index

This index points to the source artifacts used for the initial audit. Paths are recorded as evidence references only; the original experiment directories were not modified.

| ID | Local audit folder | Source run/artifact roots | Primary evidence files |
| --- | --- | --- | --- |
| 01 | [experiments/01_binary_mitunet](experiments/01_binary_mitunet/README.md) | `/home/pmharris/dev/mitunet/experiments/cubicasa5k_mitunet/full_gpu` | `metrics.json`, `config.yaml`, `parameters.json`, `threshold_search.csv`, `test_metrics.json`, `validation_metrics.json` |
| 02 | [experiments/02_hybrid_tiling](experiments/02_hybrid_tiling/README.md) | `/home/pmharris/dev/mitunet/reports/binary_wall_hybrid_global_patch/20260723T021006Z`; `/mnt/e/AI_Team/mitunet/experiments/binary_wall_hybrid_global_patch/20260723T021043Z` | `locked_validation_selection.json`, `validation_sweep.json`, `test_crop1024_overlap0.5_gaussian_gw1_summary.json`, `setup_report.json`, `experiment_manifest.json` |
| 03 | [experiments/03_deeplabv3](experiments/03_deeplabv3/README.md) | `/mnt/e/AI_Team/mitunet/experiments/cubicasa5k_deeplabv3_resnet50/deeplabv3_resnet50_wall_512_imagenet_aux_seed42_20260805T154529Z` | `summary.json`, `metrics.json`, `config.yaml`, `comparison_to_mitunet_baseline.json`, `best_model.pth.metadata.json`, `git_state.json` |
| 04 | [experiments/04_phase1_wall_structure](experiments/04_phase1_wall_structure/README.md) | `/mnt/e/AI_Team/mitunet/phase1_wall_structure/experiments/mitunet_phase1_wall_region_centerline_junctions_20260807_163622_UTC` | `reports/FINAL_REPORT.md`, `metrics/evaluation_summary.json`, `reports/summary.json`, `proof/full_training.json`, `checkpoint_manifest.json`, MLflow artifact config |
| 05 | [experiments/05_phase2_boundary_openings](experiments/05_phase2_boundary_openings/README.md) | `/mnt/e/AI_Team/mitunet/phase2_wall_boundary_door_openings/experiments/mitunet_phase2_wall_boundary_door_openings_20260810_200219_UTC` | `reports/FINAL_REPORT.md`, `reports/evaluate_summary.json`, `metrics/final_metrics.csv`, `metrics/phase1_comparison.csv`, `metrics/training_history.csv`, `checkpoint_manifest.json`, MLflow artifact config |

## Evidence Confidence

All five rows in the scoreboard are marked `VERIFIED` because the reported primary metrics and configurations were located in source artifacts. Some fields inside each row remain `UNKNOWN` because the source artifacts did not contain them or explicitly deferred them.

## Notable Missing Items

- Baseline git commit and DVC hash were not located in the inspected baseline artifacts.
- Hybrid git commit and DVC hash were not located in the inspected hybrid artifacts.
- Phase 1 and Phase 2 checkpoint SHA-256 hashes were deferred by their checkpoint manifests.
- Historical Phase 1 boundary and door metrics were not found in the inspected Phase 1 artifacts; Phase 1 did not include boundary or door heads.
- Phase 2 final report verifies door object F1 `0.7796991077953163`; the higher `0.8194901582399987` value was found in `training_history.csv` as a validation-history peak, not as the final selected-checkpoint evaluation.

