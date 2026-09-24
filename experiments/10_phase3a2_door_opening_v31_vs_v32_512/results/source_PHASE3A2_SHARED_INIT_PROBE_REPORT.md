# Phase 3A.2 Shared-Initialization Five-Epoch Probe

**EXPLORATORY — NOT HUMAN-GOLD VALIDATED**

Final status: `FIVE_EPOCH_PROBE_COMPLETE`

## Paths and provenance

- New project: `/home/pmharris/dev/mitunet_phase3a2_shared_init_probe`
- New run: `/mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC`
- Read-only source run: `/mnt/e/AI_Team/mitunet/phase3a2_door_opening_512_ablation/phase3a2_v31_vs_v32_door_opening_512_exploratory_20260903_205410_UTC`
- Git HEAD: `None`
- Git status: `?? .gitignore
?? README.md
?? configs/
?? mitunet_cubicasa
?? phase3a2_512
?? pyproject.toml
?? scripts/
?? src/
?? tests/`
- Full 30-epoch run executed: `false`
- Test split manifest/content accessed: `false`

## Configuration and validation controls

- Config comparison: `PASS`
- Only differing keys: `['experiment_name', 'output_directory', 'target_manifest', 'target_version']`
- Common validation subset: `398` of `400` plans
- Duplicate IDs / train overlap / unexplained exclusions: `0` / `0` / `0`

| Excluded validation plan | Verified reason | v3.1 pixels | v3.2 pixels | Vanished | Targets differ |
|---|---|---:|---:|---|---|
| `high_quality_architectural/5981` | opening vanished during verified 512 conversion | 351 | 351 | True | False |
| `high_quality_architectural/8690` | candidate_v3.1 and candidate_v3.2 masks differ | 1339 | 1339 | False | True |

## Shared initialization

- Status: `SHARED_INITIALIZATION_PASS`
- Shared initialization file SHA-256: `bb1acecbc8a3f2c9c222be3012f3d26eb4c19dc333bd736f2d3b8cd119a85194`
- Shared model tensor hash: `5fc4586ad6a2c537a2cac8da457eb4de4a9d1dfd1c9d07c582f343a47a4ee54a`
- Arm A loaded-state hash: `5fc4586ad6a2c537a2cac8da457eb4de4a9d1dfd1c9d07c582f343a47a4ee54a`
- Arm B loaded-state hash: `5fc4586ad6a2c537a2cac8da457eb4de4a9d1dfd1c9d07c582f343a47a4ee54a`
- Optimizer state/groups identical: `True`
- Scheduler state identical: `True`
- GradScaler state identical: `True`
- RNG state identical: `True`
- Starting learning rate identical: `True`

## Data order and preflight

- Data-order comparison: `PASS`; augmentation comparison: `PASS`
- Epoch 1 runtime order SHA-256: `641ab19820121466512db0f0da646af17f53d9ceb918a4e3fe0ed9e9d586822c`; augmentation SHA-256: `8554fb7d4dc19aafe7fae610597dcf00b5f720b427ee2bb649415c32ee6c37fe`
- Epoch 2 runtime order SHA-256: `834ee1764de564549856ebd2f095eaa2b19303daa507ca6da6f322e740a60b5c`; augmentation SHA-256: `7b95b158b3f2e6d9151e9561a1a83e5ffedcd07917fb3eafdb1edbed8f5cc46c`
- Epoch 3 runtime order SHA-256: `f9f16784c2bdc26f8a9ecc7477012ccbab3f040ecbfff5f82d9f8fd9cc3f6814`; augmentation SHA-256: `3983356f82821e41ce4752ff4b0bb6e3b91aab8b2e6682df256ce7514075e2a9`
- Epoch 4 runtime order SHA-256: `bb20bd0d357c400ac855400b8cae6d0e6c55e95368671b17440b8292c14908bc`; augmentation SHA-256: `6f0393badc34826c608d553c355edf2ccbe7faf041b016fcd9f8921cc2977096`
- Epoch 5 runtime order SHA-256: `33bfa6606d41458a6770f93d10fa7a9c4fc701c7ad4362ea29c9f42ef9ae1448`; augmentation SHA-256: `dde45ce1035611814a95a37f7847d368b7d059682dd656ae34f0980a541b92c1`
- Preflight status: `PREFLIGHT_PASS`
- GPU for both arms: `NVIDIA RTX PRO 3000 Blackwell Generation Laptop GPU`
- Train split ordered hash: `102304f85cdcc386a645d9881c1661e796c8e2fcb556a87ee9127815277a204d`
- Validation split ordered hash: `13ad0418944b42ede6ede44d16378e625a924ae3d3b500b4cdad10a7d14606fc`
- CUDA forward/backward, finite Tversky, Adam, AMP, scheduler, paired tensors, and checkpoint reload: `PASS`

## Five-epoch training

| Arm | Epoch | Train loss | Common val loss | Dice@0.5 | IoU@0.5 | Duration (s) |
|---|---:|---:|---:|---:|---:|---:|
| `A_candidate_v3_1` | 1 | 0.802801 | 0.367182 | 0.643203 | 0.474059 | 328.1 |
| `A_candidate_v3_1` | 2 | 0.344858 | 0.276658 | 0.736052 | 0.582344 | 474.0 |
| `A_candidate_v3_1` | 3 | 0.279957 | 0.271135 | 0.738979 | 0.586016 | 513.9 |
| `A_candidate_v3_1` | 4 | 0.261361 | 0.242750 | 0.764071 | 0.618216 | 464.4 |
| `A_candidate_v3_1` | 5 | 0.249257 | 0.239470 | 0.760162 | 0.613113 | 507.1 |
| `B_candidate_v3_2` | 1 | 0.809762 | 0.429395 | 0.068308 | 0.035362 | 352.3 |
| `B_candidate_v3_2` | 2 | 0.368813 | 0.273276 | 0.741861 | 0.589649 | 460.9 |
| `B_candidate_v3_2` | 3 | 0.286894 | 0.258620 | 0.744607 | 0.593126 | 484.7 |
| `B_candidate_v3_2` | 4 | 0.266354 | 0.243895 | 0.760312 | 0.613309 | 496.7 |
| `B_candidate_v3_2` | 5 | 0.253432 | 0.234664 | 0.762607 | 0.616301 | 501.3 |

- `A_candidate_v3_1` completion: `FIVE_EPOCH_ARM_COMPLETE`; best epoch `4`
- `A_candidate_v3_1` peak GPU allocated/reserved: `6129.5` / `6270.0` MiB; mean epoch `457.5` s
- `A_candidate_v3_1` best checkpoint: `/mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC/probe/A_candidate_v3_1/best_checkpoint.pt`
- `A_candidate_v3_1` best checkpoint SHA-256: `e4b23eff8b033bc8258383ad80ef1da9eccb9d51d12512adfe15fbbaecce986d`
- `A_candidate_v3_1` last checkpoint: `/mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC/probe/A_candidate_v3_1/last_checkpoint.pt`
- `A_candidate_v3_1` last checkpoint SHA-256: `90ae9a21515e43cb524490c31e3c1276da7794c51dcf65c7d1a8dea27e690000`
- `B_candidate_v3_2` completion: `FIVE_EPOCH_ARM_COMPLETE`; best epoch `5`
- `B_candidate_v3_2` peak GPU allocated/reserved: `6129.5` / `6270.0` MiB; mean epoch `459.2` s
- `B_candidate_v3_2` best checkpoint: `/mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC/probe/B_candidate_v3_2/best_checkpoint.pt`
- `B_candidate_v3_2` best checkpoint SHA-256: `8e18ef2427ba3c32189c1c970528cbe6cecf599cf5fced36bdb7d17fb81328a8`
- `B_candidate_v3_2` last checkpoint: `/mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC/probe/B_candidate_v3_2/last_checkpoint.pt`
- `B_candidate_v3_2` last checkpoint SHA-256: `436e691cacddb5642a47e39e1cddb1777a2754f31c9cf02cc78cca98ff1f759c`

## Primary common-subset comparison

Selected thresholds: arm A `0.5`, arm B `0.3`.

| Metric | Arm A | Arm B | B minus A |
|---|---:|---:|---:|
| boundary_f1 | 0.794082542 | 0.795326897 | +0.001244356 |
| empty_prediction_rate | 0.000000000 | 0.000000000 | +0.000000000 |
| f1 | 0.764071775 | 0.763051238 | -0.001020537 |
| false_negative_rate | 0.256142505 | 0.263330146 | +0.007187642 |
| false_positive_rate | 0.000972394 | 0.000929105 | -0.000043289 |
| fragmentation_rate | 0.006070203 | 0.007389813 | +0.001319609 |
| macro_dice | 0.755154279 | 0.760142258 | +0.004987980 |
| macro_iou | 0.625736964 | 0.631122842 | +0.005385878 |
| merge_rate | 0.002250000 | 0.003256513 | +0.001006513 |
| micro_dice | 0.764071775 | 0.763051238 | -0.001020537 |
| micro_iou | 0.618216947 | 0.616881847 | -0.001335100 |
| opening_instance_f1 | 0.831942483 | 0.837424496 | +0.005482013 |
| opening_instance_precision | 0.810000000 | 0.816132265 | +0.006132265 |
| opening_instance_recall | 0.855106888 | 0.859857482 | +0.004750594 |
| positive_plan_dice | 0.755154279 | 0.760142258 | +0.004987980 |
| positive_plan_iou | 0.625736964 | 0.631122842 | +0.005385878 |
| precision | 0.785415387 | 0.791392325 | +0.005976938 |
| prediction_foreground_ratio | 0.004509940 | 0.004432630 | -0.000077310 |
| recall | 0.743857495 | 0.736669854 | -0.007187642 |
| validation_loss | 0.242749094 | 0.234662950 | -0.008086144 |

## Sensitivity references

| Reference | Arm | Threshold | Micro Dice | Micro IoU | Macro Dice | Macro IoU | Validation loss |
|---|---|---:|---:|---:|---:|---:|---:|
| `COMMON_CONSENSUS_VALIDATION_SUBSET` | `A_candidate_v3_1` | 0.5 | 0.764072 | 0.618217 | 0.755154 | 0.625737 | 0.242749 |
| `COMMON_CONSENSUS_VALIDATION_SUBSET` | `B_candidate_v3_2` | 0.3 | 0.763051 | 0.616882 | 0.760142 | 0.631123 | 0.234663 |
| `REFERENCE_V31` | `A_candidate_v3_1` | 0.5 | 0.764062 | 0.618204 | 0.754590 | 0.625261 | 0.243385 |
| `REFERENCE_V31` | `B_candidate_v3_2` | 0.3 | 0.763096 | 0.616940 | 0.759725 | 0.630721 | 0.235146 |
| `REFERENCE_V32` | `A_candidate_v3_1` | 0.5 | 0.764062 | 0.618204 | 0.754590 | 0.625261 | 0.243385 |
| `REFERENCE_V32` | `B_candidate_v3_2` | 0.3 | 0.763096 | 0.616940 | 0.759725 | 0.630721 | 0.235146 |

## Common-subset threshold sweep

| Threshold | A micro Dice | A micro IoU | B micro Dice | B micro IoU |
|---:|---:|---:|---:|---:|
| 0.1 | 0.762992 | 0.616805 | 0.762868 | 0.616642 |
| 0.2 | 0.763656 | 0.617672 | 0.762949 | 0.616748 |
| 0.3 | 0.763939 | 0.618043 | 0.763051 | 0.616882 |
| 0.4 | 0.763999 | 0.618122 | 0.762837 | 0.616601 |
| 0.5 | 0.764072 | 0.618217 | 0.762607 | 0.616301 |
| 0.6 | 0.763834 | 0.617906 | 0.762335 | 0.615946 |
| 0.7 | 0.763540 | 0.617521 | 0.761977 | 0.615479 |
| 0.8 | 0.763097 | 0.616942 | 0.761366 | 0.614682 |
| 0.9 | 0.762280 | 0.615874 | 0.760280 | 0.613267 |

Full arm comparison, per-plan metrics, and all 54 arm/reference/threshold summaries are in:

- `/mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC/evaluation/arm_comparison.csv`
- `/mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC/evaluation/per_plan_metrics.csv`
- `/mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC/evaluation/threshold_sweep.csv`

## Diagnostics, integrity, and limitations

- Training-fixture manifest: `/mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC/diagnostics/training_fixture_manifest.csv`
- Every fixture output is labeled `TRAINING-FIXTURE DIAGNOSTIC — NOT VALIDATION EVIDENCE`.
- Final artifact audit: `PASS`
- Checkpoint integrity: `True`
- Predictions universally empty: `{'A_candidate_v3_1': False, 'B_candidate_v3_2': False}`
- No test access: `true`
- No 30-epoch run: `true`

- Only eight of 4,600 sample masks differ, so small metric differences may reflect normal training variation.
- Validation references are provisional and are not human-reviewed gold.
- This five-epoch technical probe cannot prove candidate_v3.2 superior or authorize promotion.

Because only eight of 4,600 masks changed, small differences may be caused by normal training variation. The provisional results do not prove candidate_v3.2 superior and do not authorize promotion.

## Exact next recommended command

`cd /home/pmharris/dev/mitunet_phase3a2_shared_init_probe && PYTHONDONTWRITEBYTECODE=1 /home/pmharris/dev/mitunet/.venv/bin/python scripts/rescore_against_frozen_gold.py --run-dir /mnt/e/AI_Team/mitunet/phase3a2_shared_init_probe/phase3a2_v31_vs_v32_shared_init_probe_20260904_152111_UTC --phase probe --gold-manifest /mnt/e/AI_Team/mitunet/phase3a2_door_opening_512_ablation/phase3a2_v31_vs_v32_door_opening_512_20260903_152401_UTC/gold_validation/gold_manifest.csv --gold-hashes /mnt/e/AI_Team/mitunet/phase3a2_door_opening_512_ablation/phase3a2_v31_vs_v32_door_opening_512_20260903_152401_UTC/gold_validation/gold_hashes.json`
