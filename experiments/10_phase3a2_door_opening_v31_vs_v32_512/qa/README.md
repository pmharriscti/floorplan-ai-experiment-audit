# Visual QA — Phase 3A.2 door-opening target ablation

**EXPLORATORY — NOT HUMAN-GOLD VALIDATED.** Every image here is a historical copy from a source run. This audit performed no training and no inference, and did not re-render any overlay. Curated samples support visual diagnosis only; the split-level metrics in [../metrics.json](../metrics.json) remain the basis for the result.

## 1. Label repair — what the experimental variable actually is

Three-way panels produced by the Phase 3A.2 repair run, showing source SVG evidence alongside `candidate_v3.1` and `candidate_v3.2` for the same instance. These are the label versions being compared, not model outputs.

Source: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/overlays/family_a_three_way`

| Image | Instance | Why it is here |
| --- | --- | --- |
| [high_quality_architectural__8690__door_0005.png](label_repair/high_quality_architectural__8690__door_0005.png) | `8690 / door_0005` | The **only validation plan** whose two targets differ; the entire validation-side experimental variable |
| [high_quality_architectural__10543__door_0003.png](label_repair/high_quality_architectural__10543__door_0003.png) | `10543 / door_0003` | Reviewer marked v3.1 `Critical issue`: foreground added at the wrong location/orientation |
| [high_quality_architectural__10620__door_0005.png](label_repair/high_quality_architectural__10620__door_0005.png) | `10620 / door_0005` | Reviewer marked v3.1 `Critical issue`: exterior door lies in the bottom horizontal wall, v3.1 added a vertical segment |
| [high_quality_architectural__11709__door_0012.png](label_repair/high_quality_architectural__11709__door_0012.png) | `11709 / door_0012` | Reviewer note: v3.2 generates the opening vertically between the two jambs; v3.1 used incorrect horizontal geometry |
| [high_quality_architectural__13827__door_0004.png](label_repair/high_quality_architectural__13827__door_0004.png) | `13827 / door_0004` | The one Family A row carrying a clean human `Correct` verdict preferring the candidate |

All five panels are `1320x1078` RGB.

## 2. Model diagnostics on the two special validation plans

Source: `.../diagnostics/{probe,full}`. Each instance is shown at **both** 5 epochs and 30 epochs, because the two differ in a way that matters.

**Changed instance `8690 / door_0005`** — the only validation plan whose two label versions disagree.

- [changed_instance_8690_door_0005__probe_5ep.png](diagnostics/changed_instance_8690_door_0005__probe_5ep.png) — at 5 epochs **both** arms predict nothing here (0 TP, 70 FN, Dice `0.0` against both references).
- [changed_instance_8690_door_0005__full_30ep.png](diagnostics/changed_instance_8690_door_0005__full_30ep.png) — at 30 epochs, threshold `0.1`, the control still predicts nothing, while the treatment predicts 16 pixels that are **16 TP against candidate_v3.2 and 16 FP against candidate_v3.1** (Dice `0.372093` vs its own version, `0.0` vs the other). The treatment model learned its own label version's geometry exactly. This does not say which version is correct; each arm is scored against the labels it trained on, and the source still records `PROVISIONAL_DIAGNOSTIC_NO_WINNER`.

**Vanished instance `5981 / door_0007`** — the 512 target-survivability failure, where the opening disappears from the target in both versions (20 reference pixels in the ROI).

- [vanished_instance_5981_door_0007__probe_5ep.png](diagnostics/vanished_instance_5981_door_0007__probe_5ep.png) — at 5 epochs arm A predicts 0 pixels in the ROI, arm B predicts 46.
- [vanished_instance_5981_door_0007__full_30ep.png](diagnostics/vanished_instance_5981_door_0007__full_30ep.png) — at 30 epochs **both** arms predict it confidently (39 and 35 pixels, maximum probability `1.0` each). The models recover an opening the 512 target pipeline lost. Excluded from primary positive-instance metrics; neither dilated nor restored.

## 3. Shared validation samples

Both arms on the three sample identities used by experiments 01-06 and 09, so door-opening behaviour can be compared against the wall and structural entries on the same plans. Source: `.../diagnostics/full/representative_common_overlays/<arm>`. All `512x512` RGB, **30-epoch** checkpoints at the validation-selected threshold `0.1`.

| Sample | A (`candidate_v3.1`) | B (`candidate_v3.2`) |
| --- | --- | --- |
| `high_quality_architectural/333` | [A](shared_samples/A_candidate_v3_1__high_quality_architectural__333.png) | [B](shared_samples/B_candidate_v3_2__high_quality_architectural__333.png) |
| `high_quality_architectural/3015` | [A](shared_samples/A_candidate_v3_1__high_quality_architectural__3015.png) | [B](shared_samples/B_candidate_v3_2__high_quality_architectural__3015.png) |
| `high_quality_architectural/5559` | [A](shared_samples/A_candidate_v3_1__high_quality_architectural__5559.png) | [B](shared_samples/B_candidate_v3_2__high_quality_architectural__5559.png) |

These three plans are in the 398-plan common subset, so their two targets are byte-identical and any visible difference between the arms is a model difference, not a label difference.

## Integrity

Every file above was opened and verified by the audit; recorded dimensions, mode and SHA-256 are in [../provenance.json](../provenance.json) under `visual_evidence.files`. No prediction masks, probability dumps or checkpoints are committed.

## What is not here

No test-split imagery: the test split was never loaded, scored, visualized or predicted. Section 1 is label evidence with no model involved; sections 2 and 3 are model outputs at the epochs stated.
