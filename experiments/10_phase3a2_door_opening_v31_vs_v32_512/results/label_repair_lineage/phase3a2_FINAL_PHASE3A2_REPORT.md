# Final Phase 3A.2 Report

Final status: `candidate_v3.2 generated`; `Family A focused human re-review required`; `training blocked pending human review`.

New run directory: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC`
Phase 3A source run: `/mnt/e/AI_Team/mitunet/phase3a_opening_source_class_repair/experiments/mitunet_phase3a_opening_source_class_repair_20260812_224352_UTC`
Phase 3A.1 source run: `/mnt/e/AI_Team/mitunet/phase3a1_opening_rule_repair/experiments/mitunet_phase3a1_opening_rule_repair_20260824_144755_UTC`
candidate_v3.2 target path: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/targets/candidate_v3_2`

## Root-cause diagnosis

The v3.1 Family A repair did not confirm jamb-supported source geometry. It inferred a local wall orientation with PCA over nearby wall pixels, synthesized a rectangle from the old seed span, and snapped the rectangle center to the nearest wall pixel. Near corners, stacked doors, and image borders this can select a nearby or perpendicular wall. The review app then displayed full-plan green pixels that could be attributed to the wrong source instance.

Tangent/normal inversion was not confirmed as a single global 90-degree bug. The confirmed code defect is a host-wall inference and provenance failure: v3.1 could replace a valid source threshold with a synthetic rectangle aligned to the wrong nearby wall. No row/column or width/height parser bug was found in the generator, but the review UI had a flat-vs-nested bbox parsing bug that hid bbox values.

## Results

Family A instances audited: `10`
candidate_v3.2 tangent-aligned rows: `10`
candidate_v3.2 normal-aligned rows: `0`
Stale legacy orientation metadata rows: `10`
Legacy tangent/normal naming ambiguity rows: `10`
Actual v3.2 geometric disagreement rows: `0`
Instance provenance rows: `10`
Focused re-review rows: `44`
Generated samples: `42`
Mechanical invariant violations: `0`
Pixel-preservation violations: `0`

## Implementation and tests

Files added:

- `scripts/run_phase3a2_opening_axis_repair.py`
- `tests/test_phase3a2_opening_axis_repair.py`

Files modified:

- `mitunet_cubicasa/target_integrity/opening_derivation_v3.py`
- `mitunet_cubicasa/phase3a_review/manifests.py`
- `mitunet_cubicasa/phase3a_review/images.py`
- `mitunet_cubicasa/phase3a_review/constants.py`
- `tests/test_phase3a_review_core.py`

Python libraries used: `numpy`, `Pillow`, `xml.dom.minidom`, standard `csv/json/random/shutil/subprocess/datetime/pathlib`, and existing project validators; tests use `pytest`.

Math used: PCA/SVD for source polygon tangent estimation, modulo-180 axis-angle comparison, tangent/normal decomposition, bbox width/height checks, boolean mask set operations for provenance, connected-component/mechanical validation, and pixel-preservation resize audits.

Metadata audit: the legacy `wall_orientation` field is preserved as Phase 3A provenance and the focused re-review manifest now exposes `legacy_wall_orientation`, `legacy_wall_orientation_degrees`, `v3_2_wall_tangent_angle`, `v3_2_wall_normal_angle`, and `v3_2_opening_axis_angle` separately.

Tests added: synthetic tangent/normal semantics, wrong-nearby-wall rejection, diagonal modulo-180 axis equivalence, real-sample regressions for `10543/door_0003`, `10620/door_0005`, and `11709/door_0012`-`door_0014`, plus flat bbox parser coverage.

Tests run:

```bash
.venv/bin/python -m pytest tests/test_phase3a2_opening_axis_repair.py tests/test_phase3a_review_core.py -q
.venv/bin/python -m pytest tests/test_phase3a2_opening_axis_repair.py tests/test_phase3a1_opening_rule_repairs.py tests/test_phase3a_review_core.py tests/test_phase3a_review_manifest.py tests/test_phase3a_runner.py tests/test_opening_wall_association.py tests/test_opening_derivation_v3.py tests/test_source_class_evidence.py tests/test_svg_coordinate_mapping.py -q
```

Test results: first run `30 passed`; broader focused run `45 passed`. Warnings were limited to the existing albumentations network-version check and floortrans NumPy matrix pending-deprecation warnings.

## Required artifacts

- Family A axis-audit CSV: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/debug/family_a_axis_audit.csv`
- Family A axis-audit report: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/reports/FAMILY_A_AXIS_AUDIT.md`
- Orientation metadata audit CSV: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/debug/family_a_orientation_metadata_audit.csv`
- Orientation metadata audit report: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/reports/ORIENTATION_METADATA_AUDIT.md`
- Family A geometry trace: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/debug/family_a_geometry_trace.csv`
- Instance-pixel provenance table: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/debug/instance_pixel_provenance.csv`
- Three-way overlays: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/overlays/family_a_three_way`
- Focused re-review manifest: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/review/candidate_v3_2_family_a_re_review_manifest.csv`
- Superseding findings: `/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC/review/superseding_human_findings_v3_1.csv`

## Updated Gradio Launch Command

```bash
cd /home/pmharris/dev/mitunet
RUN_DIR=/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC
./.venv/bin/python scripts/gradio_phase3a_target_review.py \
  --review-manifest "$RUN_DIR/review/candidate_v3_2_plan_review_manifest.csv" \
  --class-review-manifest "$RUN_DIR/review/phase3a1_snapshot/snapshots/class_review_manifest.phase3a.csv" \
  --opening-review-manifest "$RUN_DIR/review/candidate_v3_2_family_a_re_review_manifest.csv" \
  --host 127.0.0.1 \
  --port 7894 \
  --reviewer "$USER"
```

## Known unresolved cases and limitations

- Human re-review remains required; no automated PASS is asserted.
- `10620 / door_0005` is clipped at the image bottom boundary, so the source SVG wall thickness is recorded even though the rasterized opening has one row in the native target.
- Controls are included for regression review, but the v3.2 source-threshold repair is only applied to configured Family A instances.
- No canary, probe, or full training was launched.
