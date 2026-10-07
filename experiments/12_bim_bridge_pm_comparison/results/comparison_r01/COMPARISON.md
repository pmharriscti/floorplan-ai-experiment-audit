# Comparison: CubiCasa test plans vs AI-generated plans

Run `bim_bridge_pm_comparison_v0_20261006_130747_UTC`. Written 2026-10-06T13:32:14Z.

**Candidate, unreviewed IFC previews with an assumed scale. Twelve plans. An illustration of behaviour, not a benchmark.**

Open `COMPARISON_SHEET.png` for all rows, or `plans/<key>.png` for one plan.

## Accuracy per plan

CubiCasa rows use the dataset's labels. AI-generated rows use DRAFT labels made by an AI assistant and not reviewed by a person: agreement with draft labels, not verified accuracy.

| Plan | Labels | Mask wall IoU | IFC wall IoU | IFC wall precision | IFC wall recall | Doors found: mask | Doors found: IFC | Windows found: mask |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `cc-01` high_quality/4712 | dataset | 70.5% | 57.7% | 66.3% | 81.6% | 5/6 | 5/6 | 4/4 |
| `cc-02` high_quality_architectural/4847 | dataset | 87.7% | 56.2% | 72.5% | 71.4% | 6/7 | 3/7 | 6/6 |
| `cc-03` high_quality_architectural/2539 | dataset | 83.9% | 76.4% | 89.8% | 83.7% | 10/10 | 10/10 | 9/9 |
| `img-01` img-01 | draft, unreviewed | 81.3% | 72.9% | 85.5% | 83.1% | 5/6 | 2/6 | 9/9 |
| `img-02` img-02 | draft, unreviewed | 79.2% | 79.5% | 89.4% | 87.8% | 7/9 | 7/9 | 8/8 |
| `img-03` img-03 | draft, unreviewed | 79.0% | 71.3% | 88.4% | 78.6% | 6/6 | 6/6 | 6/6 |
| `img-04` img-04 | draft, unreviewed | 75.9% | 74.3% | 81.7% | 89.1% | 6/6 | 6/6 | 6/6 |
| `img-05` img-05 | draft, unreviewed | 81.0% | 80.0% | 92.8% | 85.3% | 3/3 | 1/3 | 3/3 |
| `img-06` img-06 | draft, unreviewed | 80.5% | 82.4% | 88.8% | 92.0% | 3/3 | 2/3 | 11/11 |
| `com-01` com-01 | draft, unreviewed | 61.7% | 60.3% | 73.2% | 77.3% | 11/11 | 10/11 | 12/14 |
| `com-02` com-02 | draft, unreviewed | 76.3% | 67.2% | 83.0% | 77.9% | 23/25 | 11/25 | 16/16 |
| `com-03` com-03 | draft, unreviewed | 77.3% | 76.7% | 86.4% | 87.2% | 17/17 | 15/17 | 10/10 |
| `com-04` com-04 | draft, unreviewed | 76.6% | 72.0% | 83.4% | 84.0% | 14/14 | 13/14 | 16/16 |
| `com-05` com-05 | draft, unreviewed | 68.3% | 75.6% | 88.1% | 84.2% | 12/12 | 11/12 | 16/16 |
| `com-06` com-06 | draft, unreviewed | 73.0% | 70.6% | 85.2% | 80.5% | 12/14 | 8/14 | 20/20 |

## Pooled by group

| Group | Plans | Labels | Mask wall IoU | IFC wall IoU | Doors found: mask | Doors found: IFC |
| --- | --- | --- | --- | --- | --- | --- |
| cubicasa_test | 3 | dataset | 79.8% | 64.8% | 21/23 | 18/23 |
| synth_images_prior_run | 6 | draft, unreviewed | 79.3% | 76.4% | 30/33 | 24/33 |
| synth_images_commercial | 6 | draft, unreviewed | 73.5% | 71.0% | 89/93 | 68/93 |

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
| `cc-01` high_quality/4712 | cubicasa_test | 23 | 7 | 8 | 6 (0 exported) | 81.8% | PASS; run-specific 8/8; web-ifc PASS |
| `cc-02` high_quality_architectural/4847 | cubicasa_test | 12 | 3 | 6 | 6 (0 exported) | 72.0% | PASS; run-specific 8/8; web-ifc PASS |
| `cc-03` high_quality_architectural/2539 | cubicasa_test | 18 | 10 | 10 | 9 (0 exported) | 86.8% | PASS; run-specific 8/8; web-ifc PASS |
| `img-01` img-01 | synth_images_prior_run | 25 | 3 | 9 | 11 (0 exported) | 81.6% | PASS; run-specific 8/8; web-ifc PASS |
| `img-02` img-02 | synth_images_prior_run | 21 | 8 | 9 | 8 (0 exported) | 90.4% | PASS; run-specific 8/8; web-ifc PASS |
| `img-03` img-03 | synth_images_prior_run | 22 | 10 | 10 | 10 (0 exported) | 80.6% | PASS; run-specific 8/8; web-ifc PASS |
| `img-04` img-04 | synth_images_prior_run | 17 | 6 | 6 | 6 (0 exported) | 87.6% | PASS; run-specific 8/8; web-ifc PASS |
| `img-05` img-05 | synth_images_prior_run | 11 | 1 | 3 | 3 (0 exported) | 82.8% | PASS; run-specific 8/8; web-ifc PASS |
| `img-06` img-06 | synth_images_prior_run | 15 | 2 | 3 | 11 (0 exported) | 87.5% | PASS; run-specific 8/8; web-ifc PASS |
| `com-01` com-01 | synth_images_commercial | 22 | 10 | 14 | 19 (0 exported) | 78.6% | PASS; run-specific 8/8; web-ifc PASS |
| `com-02` com-02 | synth_images_commercial | 45 | 15 | 28 | 16 (0 exported) | 78.5% | PASS; run-specific 8/8; web-ifc PASS |
| `com-03` com-03 | synth_images_commercial | 29 | 15 | 17 | 10 (0 exported) | 83.7% | PASS; run-specific 8/8; web-ifc PASS |
| `com-04` com-04 | synth_images_commercial | 22 | 13 | 14 | 16 (0 exported) | 84.2% | PASS; run-specific 8/8; web-ifc PASS |
| `com-05` com-05 | synth_images_commercial | 21 | 16 | 20 | 20 (0 exported) | 76.4% | PASS; run-specific 8/8; web-ifc PASS |
| `com-06` com-06 | synth_images_commercial | 20 | 8 | 12 | 24 (0 exported) | 74.8% | PASS; run-specific 8/8; web-ifc PASS |

## How to read it

- Mask wall IoU is the model's own accuracy. It equals the upstream evaluation for each plan.
- IFC wall IoU measures the walls as they ended up in the IFC file, read back from the file. The gap between the two is what the mask-to-IFC step loses.
- A door counts as found when a predicted region shares at least one pixel with it. This is a loose detection count, not a shape score.
- Windows are predicted but never exported; the preview profile has no window height.
- The draft labels were traced from dark pixels inside hand-placed guide bands. The model also follows dark ink, so agreement may overstate true accuracy.
- Wall pixels are scored on the model's 512 grid (labels reduced by area coverage). Doors and windows are counted on the labels' own full-resolution instance maps. Label ignore regions are left out.
- Thresholds were chosen on the CubiCasa validation split. Nothing was tuned on these plans.

## IFC files

- `cc-01`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\cc-01\export_candidate_preview_whole_plan_r01\cc-high-quality--4712-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `cc-02`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\cc-02\export_candidate_preview_whole_plan_r01\cc-high-quality-architectural--4847-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `cc-03`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\cc-03\export_candidate_preview_whole_plan_r01\cc-high-quality-architectural--2539-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `img-01`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-01\export_candidate_preview_whole_plan_r01\synth-img-01-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `img-02`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-02\export_candidate_preview_whole_plan_r01\synth-img-02-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `img-03`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-03\export_candidate_preview_whole_plan_r01\synth-img-03-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `img-04`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-04\export_candidate_preview_whole_plan_r01\synth-img-04-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `img-05`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-05\export_candidate_preview_whole_plan_r01\synth-img-05-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `img-06`: `E:\AI_Team\mitunet\experiments\bim_bridge_synth_images_v0\bim_bridge_synth_images_v0_20261002_200115_UTC\samples\img-06\export_candidate_preview_whole_plan_r01\synth-img-06-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `com-01`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-01\export_candidate_preview_whole_plan_r01\com-com-01-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `com-02`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-02\export_candidate_preview_whole_plan_r01\com-com-02-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `com-03`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-03\export_candidate_preview_whole_plan_r01\com-com-03-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `com-04`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-04\export_candidate_preview_whole_plan_r01\com-com-04-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `com-05`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-05\export_candidate_preview_whole_plan_r01\com-com-05-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
- `com-06`: `E:\AI_Team\mitunet\experiments\bim_bridge_pm_comparison_v0\bim_bridge_pm_comparison_v0_20261006_130747_UTC\samples\com-06\export_candidate_preview_whole_plan_r01\com-com-06-p01__CANDIDATE_UNREVIEWED_PREVIEW__WHOLE_PLAN_ATTEMPT__SCALE_ASSUMED_FOR_PREVIEW__r01.ifc`
