# Final Repair Report

Final status: `candidate_v3.1 generated`; `focused human re-review required`; `training blocked pending human review`.

New run directory: `/mnt/e/AI_Team/mitunet/phase3a1_opening_rule_repair/experiments/mitunet_phase3a1_opening_rule_repair_20260824_144755_UTC`
Immutable Phase 3A source run: `/mnt/e/AI_Team/mitunet/phase3a_opening_source_class_repair/experiments/mitunet_phase3a_opening_source_class_repair_20260812_224352_UTC`
candidate_v3.1 target path: `/mnt/e/AI_Team/mitunet/phase3a1_opening_rule_repair/experiments/mitunet_phase3a1_opening_rule_repair_20260824_144755_UTC/targets/candidate_v3_1`

## Root causes

1. Family A: door source polygons could represent leaf/symbol geometry; v3 used them as opening seeds.
2. Family B: false, malformed, or border-collapsed source instances could enter the opening pipeline after clipping.
3. Family C: wall association required direct wall foreground overlap and rejected openings located in wall gaps.

## Code paths changed

- `mitunet_cubicasa/target_integrity/opening_derivation_v3.py`
- `mitunet_cubicasa/target_integrity/opening_association.py`
- `mitunet_cubicasa/phase3a_review/filtering.py`
- `scripts/gradio_phase3a_target_review.py`
- `scripts/run_phase3a1_opening_rule_repair.py`
- `tests/test_phase3a1_opening_rule_repairs.py`

## Results

Warnings clustered: `84`
Resolved: `42`
Excluded as false source instance: `2`
Improved but still review-required: `0`
Unchanged: `16`
Insufficient evidence: `24`
Mechanical invariant violations: `0`
Pixel-preservation violations: `0`

Clean controls were regenerated in the focused subset and remain queued for human re-review; no human PASS is fabricated.

## Human reviewer must examine next

- All explicit examples and saved Phase 3A human-reviewed warnings.
- Cluster representatives, all unresolved empty-source cases, and clean door/window controls.
- Any v3.1 source-instance exclusion or changed target geometry.

## Launch command

```bash
cd /home/pmharris/dev/mitunet
RUN_DIR=/mnt/e/AI_Team/mitunet/phase3a1_opening_rule_repair/experiments/mitunet_phase3a1_opening_rule_repair_20260824_144755_UTC
./.venv/bin/python scripts/gradio_phase3a_target_review.py \
  --review-manifest "$RUN_DIR/review/candidate_v3_1_plan_review_manifest.csv" \
  --class-review-manifest "$RUN_DIR/review/snapshots/class_review_manifest.phase3a.csv" \
  --opening-review-manifest "$RUN_DIR/review/candidate_v3_1_re_review_manifest.csv" \
  --host 127.0.0.1 \
  --port 7893 \
  --reviewer "$USER"
```

## Automated verification

Commands run:

```bash
.venv/bin/python -m pytest tests/test_phase3a1_opening_rule_repairs.py tests/test_opening_wall_association.py tests/test_opening_derivation_v3.py tests/test_phase3a_review_core.py tests/test_phase3a_review_manifest.py -q
.venv/bin/python -m pytest tests/test_phase3a1_opening_rule_repairs.py tests/test_phase3a_review_core.py tests/test_phase3a_review_manifest.py tests/test_phase3a_runner.py tests/test_opening_wall_association.py tests/test_opening_derivation_v3.py tests/test_source_class_evidence.py tests/test_svg_coordinate_mapping.py -q
```

Results: first focused run `22 passed`; final focused/review-app run `25 passed`. Both runs emitted only the existing albumentations network-version-check warning in the restricted environment.

Review-app manifest smoke: `candidate_v3_1_plan_review_manifest.csv` loads as 81 plan rows, `candidate_v3_1_re_review_manifest.csv` loads as 105 opening rows, and the `candidate_v3.1 focused re-review` queue contains 105 rows. Opening decisions resolve to `review/opening_human_decisions_v3_1.csv`.

## Known unresolved cases and limitations

- 24 warning rows remain unresolved because their Phase 3A seed is empty or unrenderable; they have source-instance evidence sheets and remain in the focused human queue.
- 16 warning rows remain unchanged after the automated repairs and are queued for focused human review.
- Wrong-wall association safety is not declared by automation; the human reviewer must inspect the before/after sheets.
- No training, canary training, or probe training was launched.

