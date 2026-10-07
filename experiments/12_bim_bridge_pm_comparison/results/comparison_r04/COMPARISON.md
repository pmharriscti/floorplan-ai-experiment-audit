# Comparison: CubiCasa test plans vs AI-generated plans

Run `bim_bridge_pm_comparison_v0_20261006_130747_UTC`. Written 2026-10-06T19:18:54Z.

**Candidate, unreviewed IFC previews with an assumed scale. Export revision `r04`, candidates `candidates_r04`. An illustration of behaviour, not a benchmark.**

Open `COMPARISON_SHEET.png` for all rows, or `plans/<key>.png` for one plan.

## Accuracy per plan

CubiCasa rows use the dataset's labels. AI-generated rows use DRAFT labels made by an AI assistant and not reviewed by a person: agreement with draft labels, not verified accuracy.

| Plan | Labels | Mask wall IoU | IFC wall IoU | IFC wall precision | IFC wall recall | Doors found: mask | Doors found: IFC | Windows found: mask |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `cc-01` high_quality/4712 | dataset | 70.5% | 66.4% | 67.6% | 97.4% | 5/6 | 5/6 | 4/4 |
| `cc-02` high_quality_architectural/4847 | dataset | 87.7% | 59.6% | 71.8% | 77.8% | 6/7 | 4/7 | 6/6 |
| `cc-03` high_quality_architectural/2539 | dataset | 83.9% | 82.9% | 91.7% | 89.6% | 10/10 | 10/10 | 9/9 |
| `img-01` img-01 | draft, unreviewed | 81.3% | 79.3% | 83.6% | 94.0% | 5/6 | 5/6 | 9/9 |
| `img-02` img-02 | draft, unreviewed | 79.2% | 84.1% | 91.1% | 91.7% | 7/9 | 7/9 | 8/8 |
| `img-03` img-03 | draft, unreviewed | 79.0% | 82.6% | 90.1% | 90.8% | 6/6 | 6/6 | 6/6 |
| `img-04` img-04 | draft, unreviewed | 75.9% | 79.5% | 81.7% | 96.7% | 6/6 | 6/6 | 6/6 |
| `img-05` img-05 | draft, unreviewed | 81.0% | 88.1% | 91.6% | 95.8% | 3/3 | 3/3 | 3/3 |
| `img-06` img-06 | draft, unreviewed | 80.5% | 83.6% | 86.7% | 95.9% | 3/3 | 3/3 | 11/11 |
| `com-01` com-01 | draft, unreviewed | 61.7% | 59.2% | 67.2% | 83.2% | 11/11 | 10/11 | 12/14 |
| `com-02` com-02 | draft, unreviewed | 76.3% | 74.3% | 84.0% | 86.6% | 23/25 | 14/25 | 16/16 |
| `com-03` com-03 | draft, unreviewed | 77.3% | 81.2% | 85.5% | 94.2% | 17/17 | 16/17 | 10/10 |
| `com-04` com-04 | draft, unreviewed | 76.6% | 85.0% | 91.1% | 92.6% | 14/14 | 14/14 | 16/16 |
| `com-05` com-05 | draft, unreviewed | 68.3% | 76.7% | 84.5% | 89.2% | 12/12 | 11/12 | 16/16 |
| `com-06` com-06 | draft, unreviewed | 73.0% | 74.9% | 85.1% | 86.3% | 12/14 | 9/14 | 20/20 |

## Pooled by group

| Group | Plans | Labels | Mask wall IoU | IFC wall IoU | Doors found: mask | Doors found: IFC |
| --- | --- | --- | --- | --- | --- | --- |
| cubicasa_test | 3 | dataset | 79.8% | 71.1% | 21/23 | 19/23 |
| synth_images_prior_run | 6 | draft, unreviewed | 79.3% | 82.7% | 30/33 | 30/33 |
| synth_images_commercial | 6 | draft, unreviewed | 73.5% | 76.5% | 89/93 | 74/93 |

## CubiCasa context

| | Wall IoU | Boundary F1 (2 px) | Door object F1 | Window object F1 |
| --- | --- | --- | --- | --- |
| `cc-01` high_quality/4712 | 70.5% | 85.4% | 71.4% | 80.0% |
| `cc-02` high_quality_architectural/4847 | 87.7% | 97.5% | 92.3% | 100.0% |
| `cc-03` high_quality_architectural/2539 | 83.9% | 97.1% | 100.0% | 100.0% |
| All 400 CubiCasa test plans (mean) | 81.1% | 95.4% | 87.5% | 85.6% |

## What reached the IFC, all plans

| Plan | Group | Walls | Openings | Predicted doors | Predicted windows | Predicted wall covered by IFC walls | File checks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `cc-01` high_quality/4712 | cubicasa_test | 14 | 7 | 8 | 6 (0 exported) | 95.9% | PASS; run-specific 8/8; web-ifc PASS |
| `cc-02` high_quality_architectural/4847 | cubicasa_test | 8 | 4 | 6 | 6 (0 exported) | 78.1% | PASS; run-specific 8/8; web-ifc PASS |
| `cc-03` high_quality_architectural/2539 | cubicasa_test | 16 | 10 | 10 | 9 (0 exported) | 93.7% | PASS; run-specific 8/8; web-ifc PASS |
| `img-01` img-01 | synth_images_prior_run | 17 | 7 | 9 | 11 (0 exported) | 94.8% | PASS; run-specific 8/8; web-ifc PASS |
| `img-02` img-02 | synth_images_prior_run | 19 | 8 | 9 | 8 (0 exported) | 94.9% | PASS; run-specific 8/8; web-ifc PASS |
| `img-03` img-03 | synth_images_prior_run | 16 | 10 | 10 | 10 (0 exported) | 94.4% | PASS; run-specific 8/8; web-ifc PASS |
| `img-04` img-04 | synth_images_prior_run | 10 | 6 | 6 | 6 (0 exported) | 97.7% | PASS; run-specific 8/8; web-ifc PASS |
| `img-05` img-05 | synth_images_prior_run | 7 | 3 | 3 | 3 (0 exported) | 96.8% | PASS; run-specific 8/8; web-ifc PASS |
| `img-06` img-06 | synth_images_prior_run | 8 | 3 | 3 | 11 (0 exported) | 99.0% | PASS; run-specific 8/8; web-ifc PASS |
| `com-01` com-01 | synth_images_commercial | 13 | 11 | 14 | 19 (0 exported) | 90.8% | PASS; run-specific 8/8; web-ifc PASS |
| `com-02` com-02 | synth_images_commercial | 35 | 18 | 28 | 16 (0 exported) | 89.1% | PASS; run-specific 8/8; web-ifc PASS |
| `com-03` com-03 | synth_images_commercial | 23 | 16 | 17 | 10 (0 exported) | 96.3% | PASS; run-specific 8/8; web-ifc PASS |
| `com-04` com-04 | synth_images_commercial | 16 | 14 | 14 | 16 (0 exported) | 93.3% | PASS; run-specific 8/8; web-ifc PASS |
| `com-05` com-05 | synth_images_commercial | 19 | 17 | 20 | 20 (0 exported) | 83.9% | PASS; run-specific 8/8; web-ifc PASS |
| `com-06` com-06 | synth_images_commercial | 17 | 9 | 12 | 24 (0 exported) | 85.8% | PASS; run-specific 8/8; web-ifc PASS |

## How to read it

- Mask wall IoU is the model's own accuracy. It equals the upstream evaluation for each plan.
- IFC wall IoU measures the walls as they ended up in the IFC file, read back from the file. The gap between the two is what the mask-to-IFC step loses.
- A door counts as found when a predicted region shares at least one pixel with it. This is a loose detection count, not a shape score.
- Windows are predicted but never exported; the preview profile has no window height.
- The draft labels were traced from dark pixels inside hand-placed guide bands. The model also follows dark ink, so agreement may overstate true accuracy.
- Wall pixels are scored on the model's 512 grid (labels reduced by area coverage). Doors and windows are counted on the labels' own full-resolution instance maps. Label ignore regions are left out.
- Thresholds were chosen on the CubiCasa validation split. Nothing was tuned on these plans.

## IFC files

- `cc-01`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\cc-01\export_candidate_preview_whole_plan_r04\cc-high-quality--4712-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `cc-02`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\cc-02\export_candidate_preview_whole_plan_r04\cc-high-quality-architectural--4847-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `cc-03`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\cc-03\export_candidate_preview_whole_plan_r04\cc-high-quality-architectural--2539-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `img-01`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-01\export_candidate_preview_whole_plan_r04\synth-img-01-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `img-02`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-02\export_candidate_preview_whole_plan_r04\synth-img-02-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `img-03`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-03\export_candidate_preview_whole_plan_r04\synth-img-03-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `img-04`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-04\export_candidate_preview_whole_plan_r04\synth-img-04-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `img-05`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-05\export_candidate_preview_whole_plan_r04\synth-img-05-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `img-06`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-06\export_candidate_preview_whole_plan_r04\synth-img-06-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `com-01`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-01\export_candidate_preview_whole_plan_r04\com-com-01-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `com-02`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-02\export_candidate_preview_whole_plan_r04\com-com-02-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `com-03`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-03\export_candidate_preview_whole_plan_r04\com-com-03-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `com-04`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-04\export_candidate_preview_whole_plan_r04\com-com-04-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `com-05`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-05\export_candidate_preview_whole_plan_r04\com-com-05-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
- `com-06`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-06\export_candidate_preview_whole_plan_r04\com-com-06-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r04.ifc`
