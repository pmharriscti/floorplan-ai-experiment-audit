# INPUT_INVENTORY

Run `bim_bridge_v0_20260928_183649_UTC`. Everything below was verified on disk when the `inspect` stage ran. Machine-readable
copy: `input_inventory.json`.

## Selected input

Saved, thresholded predictions of the Phase 5 hierarchical multi-head run (audit entry 09), one validation sample.

| Item | Value |
| --- | --- |
| Upstream run | `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED` |
| Sample, split | `high_quality_architectural/333`, `val` |
| Source image | `/home/pmharris/dev/cubicasa5k_data/data/datasets/qmarva/cubicasa5k/versions/4/cubicasa5k/cubicasa5k/high_quality_architectural/333/F1_scaled.png` |
| Source image SHA-256 | `ac6be65c391069f75307a9b90c66240a0e94c9e75cadfd161ca14001bd6a88cc` (matches the upstream manifest: True) |
| Original size | [1319, 619] px |
| Letterbox | {"letterbox_scale": "0.38817285822592873", "letterbox_pad_top": "136", "letterbox_pad_left": "0", "letterbox_pad_bottom": "136", "letterbox_pad_right": "0", "input_width": "512", "input_height": "512"} |
| Prediction file | `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/masks/val/high_quality_architectural__333__heads.png` |
| Prediction SHA-256 | `4da6f6eb69c64ef721a30e7f81f74843348db831d3608b331fcc2dbd03f1f355` |
| Prediction kind | thresholded_mask (uint8 bitmask PNG); NOT a probability map and NOT a colour overlay |
| Checkpoint | `/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/checkpoints/best_gated_hierarchical_score.pth` (epoch 30) |
| Checkpoint SHA-256 | `c281b31974e194f216df3e2170eb5b2197d72a872713ed9176973940a95357ae` (matches audit entry 09: True) |
| Config snapshot SHA-256 | `ea6dda8b54aeba62c86ea2583d1e8392630b55ce341d13ba1292e7ad69f4cc35` |
| Manifest SHA-256 | `ea5b91ad8e455c2769f04ae9943dd9229f718657cba6a9e7b02666910877b10d` |

### Encoding, verified from two sources

The upstream `masks/README.md` says:

```
Thresholded prediction masks (512x512 letterbox space).

`<sample>__heads.png`: uint8, bit k set <=> head k positive, k = 0:structural_wall, 1:wall_boundary, 2:wall_centerline, 3:junction, 4:endpoint, 5:door_opening, 6:window_opening, 7:visible_wall
`<sample>__fixtures.png`: uint16, bit k set <=> fixture class k positive, k = 0:cabinetry_storage, 1:appliance, 2:toilet_urinal, 3:sink_tap, 4:sauna_bench, 5:fireplace, 6:bathtub_shower_jacuzzi, 7:chimney, 8:other_fixture
Thresholds: see audit/evaluate_summary.json -> thresholds.
```

The writer `_save_prediction_masks` in `/home/pmharris/dev/mitunet/mitunet_cubicasa/hierarchical_evaluation.py` packs the heads with
`heads |= layer << k` in the order of `BINARY_MASK_BITS`, which gives the same layout. The bridge reads bit
0 as `structural_wall` and bit 5 as `door_opening`, and refuses to run if the README
does not document the configured bits.

### Thresholds

Read from `audit/evaluate_summary.json`: `structural_wall` 0.05, `door_opening` 0.95.
They were selected on validation by the upstream run. This experiment selects and changes no threshold.

### Why this input

- Its lineage is complete: image, manifest, prediction file, thresholds, config snapshot and checkpoint are
  all on disk with hashes, and the checkpoint hash equals the one recorded in audit entry 09.
- It includes a `door_opening` head, so an aperture can come from the model and need not be supplied by hand.
- It is a saved prediction. No inference was run.
- The sample is a CubiCasa5K validation image that the audit repository already publishes.

It was not chosen for its metrics. No segmentation metric is claimed or compared by this experiment.

## Alternatives that were not selected

| Alternative | Evidence | Reason |
| --- | --- | --- |
| Phase 2 probability maps | 400 files | Probability maps exist and would make a raw, uncalibrated semantic score available. Not selected because the Phase 2 checkpoint hash is deferred in its manifest (unknown) and the Phase 2 wall quality regressed by 5 IoU points against its parent (audit entry 05). |
| Phase 2 `graphs/` | 0 files | Empty. The MitUNet pipeline persists no vector output. |
| floorplan3d outputs | 7 files | One wall-mass polygon (GeoJSON), a GLB and a DXF. No centrelines or thicknesses. Scale came from a CLI argument, not from evidence. |
| floorplan-synth `f-plan-1` vectors | predicted mask on disk: False | Segment-level vectors exist, but the predicted mask and the checkpoint that produced them are no longer on disk, so prediction lineage cannot be established. Used by the archived 0.1 prototype only. |

## Existing geometry and export code

| Code | Reused | Note |
| --- | --- | --- |
| floorplan_synth_vectorizer | yes | Run unmodified in a subprocess on the decoded predicted wall mask. Requires OpenCV 4.x. |
| floorplan_synth_dxf_exporter | no | Left untouched. DXF is not a prerequisite of this experiment. |
| floorplan3d_glb_exporter | no | Left untouched. Its default wall height 2.7 m is reused as a preview assumption. |
| ifc_code_upstream | no | No IFC code exists in any inspected repository. IfcOpenShell was not installed in any existing environment. |

## Target BIM application

No receiving application or accepted IFC schema is documented in the inspected repositories. IFC4 is a prototype choice; target compatibility is UNVERIFIED.

## Viewer availability

Blender is installed without an IFC add-on, and no other IFC viewer was found. No viewer inspection is possible in this environment.

## Audit repository

- Path: `/home/pmharris/dev/floorplan-ai-experiment-audit` (exists: True)
- HEAD: `703fcbc4e3482cf664a79d853ea268ddb583354e`; ['## main...origin/main']; worktree clean: True
- Existing experiments: 01_binary_mitunet, 02_hybrid_tiling, 03_deeplabv3, 04_phase1_wall_structure, 05_phase2_boundary_openings, 06_binary_mitunet_1024, 07_mitunet_512_adamw, 08_mitunet_1024_highres_runpod, 09_phase5_hierarchical_multihead_512, 10_phase3a2_door_opening_v31_vs_v32_512
- Next unused experiment number: **11**

## Conflicts and missing evidence

- Plan scale: NO documented evidence. The drawing has no dimension string and no scale bar. Only an apartment area label exists.
- Semantic confidence: NOT AVAILABLE. The selected run saved thresholded masks only (save_probability_maps: false; predictions/ is empty).
- Human review: NONE recorded for this geometry.
- Vertical dimensions: none exist in a plan drawing.
- Upstream code identity: the Phase 5 modules are untracked in the mitunet repository; audit entry 09 records their file hashes instead of a clean commit.
- Vectorizer identity: floorplan-synth is not a git repository; its source file hashes are recorded.
- The upstream structural_wall head predicts walls with openings NOT subtracted, so a predicted wall runs through its doors and windows.
