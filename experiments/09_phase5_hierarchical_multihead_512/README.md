# Phase 5 Hierarchical Multi-Head MitUNet 512

Phase 5 tested whether the 512 px binary-wall MitUNet baseline (experiment 01) can be extended into an eight-head model, with a shared MiT-B4 encoder, four task-group decoders and independent sigmoid heads, without losing the baseline's wall accuracy. The wall decoder is the baseline decoder, kept in its own group; the new heads add wall boundary, wall centerline, junctions, endpoints, door openings, window openings and nine fixture classes. Checkpoint selection is gated: an epoch is eligible only if its validation structural-wall IoU at the baseline threshold stays within `0.005` of the reproduced baseline.

The audited run is the fourth run of this design. The first three, all with the repository's current data augmentation enabled, failed the wall gate on every joint epoch. A wall-only ablation and a set of one-epoch diagnostics traced the regression to an augmentation mismatch with the June 2026 baseline, not to the multi-head design. The audited run repeats the fixed-weight configuration with augmentation disabled and passes the gate on all 26 joint epochs.

## Source Evidence

Source run directory: `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED`

Primary evidence files (all under the run directory unless noted):

- `artifacts/FINAL_REPORT.md` (copied to [results/source_FINAL_REPORT.md](results/source_FINAL_REPORT.md))
- `audit/evaluate_summary.json` (copied to [results/evaluate_summary.json](results/evaluate_summary.json))
- `audit/train_summary.json`, `audit/threshold_search.json` (copied under [results/](results/))
- `audit/reproduce-baseline_summary.json`, `audit/checkpoint-proof_summary.json`, `audit/label_validation.json`
- `audit/config_snapshot.yaml` and `audit/resolved_config.json`
- `metrics/training_history.csv` (copied to [results/training_history.csv](results/training_history.csv))
- `metrics/per_image_val_*.csv` and `masks/val/*` (visual QA source)
- `logs/commands_executed.txt` (records the launch and the post-reboot resume)
- Source repository `/home/pmharris/dev/mitunet`, config `configs/experiments/mitunet_hierarchical_multihead_512_noaug.yaml` (byte-identical to the run's config snapshot)

Related-run evidence (negative runs and root-cause diagnostics) is listed in [provenance.json](provenance.json) and copied under [results/related_runs/](results/related_runs/) and [results/diagnostics/](results/diagnostics/).

## Verified Configuration

Initialised from the experiment 01 checkpoint (`best_model.pth`, SHA-256 `fb966505...`), with the wall path proven logit-equivalent at initialisation (max absolute difference `0.0`) and the baseline reproduced by this run's evaluator to within `1e-6` IoU on validation and test.

Same CubiCasa5K v4 splits as the baseline (4200 / 400 / 400, manifests identical), 512 letterbox RGB, ImageNet normalisation, Adam, weight decay 0, batch 4, AMP, seed 42, Tversky α=0.6 β=0.4 on the wall head. The structural-wall target is pixel-identical to the baseline wall target.

Schedule: 4 warm-up epochs training only the new decoders and heads at LR `1e-4` with the encoder and wall path frozen, then 26 joint epochs with encoder and wall path at LR `1e-5` (linear ramp over the first joint epoch) and new paths at `1e-4`. Loss weighting was fixed (`--weighting fixed`; wall 0.40, boundary 0.08, centerline 0.12, junction 0.05, endpoint 0.03, door 0.12, window 0.12, fixtures 0.08). Data augmentation was disabled. The run completed all 30 epochs; the ReduceLROnPlateau scheduler never fired and early stopping never triggered.

The run was interrupted once by a host reboot after epoch 15 and resumed from `last.pth` with optimizer, scheduler, scaler and best-checkpoint state restored. Both commands are in the run's `commands_executed.txt`.

## Verified Metrics

Selected checkpoint: `best_gated_hierarchical_score.pth`, epoch 30, the last epoch and the best gated score. Selected thresholds: structural wall `0.05`, wall boundary `0.95`, centerline `0.95`, junction `0.85` (NMS radius 3), endpoint `0.8` (NMS radius 3), door opening `0.95`, window opening `0.9`, fixtures per class (see [config.yaml](config.yaml)).

Wall protection gate, validation, threshold `0.1`: reproduced baseline `0.8188460992164052`, floor `0.8138460992164052`, selected checkpoint `0.8161948635674233`. Gate met; 26 of 26 joint epochs passed.

| Head | Stage metric | Validation | Test |
| --- | --- | ---: | ---: |
| structural_wall | micro IoU at selected threshold 0.05 | `0.8163773956524429` | `0.8201544454854268` |
| structural_wall | micro Dice at selected threshold 0.05 | `0.8989072398791883` | `0.9011921461057063` |
| wall_boundary | boundary F1@2 px | `0.9545912416245511` | `0.9539204213294288` |
| wall_centerline | skeleton clDice | `0.49923712059981695` | `0.5035053752780867` |
| junction | F1@5 px | `0.7870734231563665` | `0.7667439205020895` |
| endpoint | F1@5 px | `0.33671869601605553` | `0.3173590605486322` |
| door_opening | object F1 | `0.8802919575908823` | `0.8751504111574657` |
| window_opening | object F1 | `0.8806236251106608` | `0.8557445328184917` |
| fixtures | macro IoU over 9 classes | `0.45816277648462456` | `0.45617858244392373` |
| hierarchical score | weighted composite | `0.7500312363606518` | `0.7467168595494466` |
| visible_wall (derived) | micro IoU | `0.788995454179994` | `0.793481305721754` |

Baseline comparison at threshold `0.1`: validation IoU delta `-0.0026512356489818423`, test IoU delta `-0.004426577768414819` versus the reproduced baseline (`0.8244330705186285` test IoU).

Fixture classes span a wide range: sauna bench, cabinetry and toilet reach validation IoU `0.75`, `0.70` and `0.63`, while chimney (`0.13`, 45 supporting samples) and other-fixture (`0.15`) are near failure. The wall-boundary head scores high on the 2 px tolerant metric but only `0.3023` pixel IoU with precision `0.3139`, so it paints a band roughly three times wider than the one-pixel target. The boundary threshold sweep is still rising at `0.95`, the top of its grid.

## Visual QA

Curated validation evidence is in [qa/README.md](qa/README.md): the three shared samples with source images, ground-truth and prediction masks for all seven binary heads plus the fixture union, TP/FP/FN overlays, a contact sheet and per-sample metadata. Predictions are decoded from the run's saved thresholded bitmasks; no new inference was performed. The per-image structural-wall IoU recomputed from those masks equals the run's per-image CSV for all three samples.

Training curves for this run and the three augmentation-on runs are in [plots/README.md](plots/README.md).

## Interpretation

This is a positive structural expansion with a small, verified wall cost. Versus the correct comparator, the reproduced baseline evaluated with the same code and thresholds, the wall lost `0.27` IoU points on validation and `0.44` on test, inside the declared `0.5` point tolerance but not zero. The wall peaked at `0.8230897318865986` at epoch 11 (above the baseline) and drifted down about `0.05` points per epoch afterwards while training loss kept falling; the score-based selection rule preferred the later epochs where the new heads were stronger. Checkpoints from both regimes are on disk.

Against prior phases on the same validation samples, using the same metric implementations: boundary F1@2 px rose from Phase 2's `0.9347893344704645` to `0.9545912416245511` (`+0.0198`), door object F1 from `0.7796991077953163` to `0.8802919575908823` (`+0.1006`), and junction F1@5 px from Phase 1's `0.769385212829412` to `0.7870734231563665` (`+0.0177`). Window openings, endpoints and fixtures have no prior-phase counterpart. The centerline value is not compared: Phase 1 reports hard clDice of the thresholded mask while this run reports skeleton clDice.

The endpoint head is the weakest output (`0.34` F1@5 px). It predicted nothing at all for the first fifteen epochs of every run and only became non-trivial late in joint training.

## Root Cause of the Earlier Failures

Three earlier runs of this design with `data.augmentation: true` (GradNorm weighting; fixed weighting; and a wall-only ablation with every new-head weight set to `0`) dropped validation wall IoU from `0.8188` to between `0.76` and `0.79` within one joint epoch and never recovered ([results/related_runs/](results/related_runs/)). Because the wall-only ablation regressed just as much with no gradient from any new head, the multi-head design and GradNorm were ruled out.

One-epoch diagnostics from the baseline initialisation ([results/diagnostics/diag_results.json](results/diagnostics/diag_results.json)) then showed: forward passes alone leave the wall unchanged (`0.8187`), so BatchNorm statistics are not the cause; freezing BatchNorm does not help (`0.7789`); training only the encoder (`0.7780`) or only the wall decoder (`0.7872`) each reproduce the drop; a 10x lower LR halves it (`0.8028`); and the same epoch with augmentation disabled raises the wall to `0.8220`. A loss probe explains why: the baseline model's training-split Tversky loss is `0.0860` without augmentation, matching its own logged `0.0909`, but `0.1422` under the repository's current augmentation set and `0.1533` under horizontal flips alone. The baseline, trained on 2026-06-25 before the repository's only git commit, was not trained with the current geometric augmentations. Fine-tuning it under flips and rotations moves it away from the un-augmented validation distribution.

The per-op entries inside `aug_loss_probe.json` are invalid (all four ops report the same value because the loader's persistent workers did not pick up the swapped transform). The corrected per-op probe ([results/diagnostics/aug_loss_probe_perop.json](results/diagnostics/aug_loss_probe_perop.json), baseline model, first 300 training batches, each op forced on) gives training loss `0.0970` with no augmentation, `0.0997` with brightness/contrast jitter, `0.1086` with transpose, `0.1486` with vertical flip, `0.1533` with horizontal flip, `0.1602` with a 90-degree rotation and `0.2047` with a 180-degree rotation. Photometric jitter is harmless; every geometric op is not.

## Missing Evidence and Non-Claims

- The Phase 5 modules, experiment script and configs are untracked in the source repository, so the recorded git commit `459778bd07b1a0b8a60413a2e681bbd4ff7bd829` does not identify the code alone; file SHA-256 values are recorded in [provenance.json](provenance.json).
- DVC status is not recorded by this pipeline (`UNKNOWN`).
- GradNorm was only run with augmentation on; whether it helps under the corrected recipe is untested.
- The wall-boundary head has not been compared against the trivial alternative of extracting the outline of the structural-wall prediction, so its 2 px F1 does not by itself show the head is necessary.
- Window and door opening targets coincide with their symbol footprints in `79.7%` and `93.9%` of samples (label validation); the source report warns that they must be read as symbol-derived targets, not corridor targets.
- The curated QA samples support visual diagnosis only; split-level metrics remain the basis for the result.

See [config.yaml](config.yaml), [metrics.json](metrics.json), and [provenance.json](provenance.json).
