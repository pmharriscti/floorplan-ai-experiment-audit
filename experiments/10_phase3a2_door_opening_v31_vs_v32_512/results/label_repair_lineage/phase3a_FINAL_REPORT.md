# Final Report

Executive verdict: **blocked**

Phase 3A implemented `candidate_v3`, inventoried source SVG classes, separated symbol and opening targets, and stopped at the human-review gate. No training process was launched.

## Evidence

- Full source inventory samples: `5000`.
- Observed raw source classes: `318`.
- Review-required source classes: `153`.
- Pilot mechanical violations: `0`.
- Pilot semantic violations: `0`.
- Unexplained exact symbol/opening equality cases: `0`.
- Pilot pixel-preservation violations: `0`.
- Human review passed: `False`.

## Target Repair

- `candidate_v2` was not modified or overwritten.
- `candidate_v3` derives opening masks only after wall association and clips them to structural wall support.
- Door/window symbol masks are generated from visual outlines/strokes, not by blindly copying filled opening polygons.
- Ambiguous openings and classes remain `review_required`; this is an acceptable blocked result.

## Artifact Locations

- Run directory: `/mnt/e/AI_Team/mitunet/phase3a_opening_source_class_repair/experiments/mitunet_phase3a_opening_source_class_repair_20260812_224352_UTC`.
- Source inventory: `/mnt/e/AI_Team/mitunet/phase3a_opening_source_class_repair/experiments/mitunet_phase3a_opening_source_class_repair_20260812_224352_UTC/reports/source_class_inventory.csv`.
- Candidate v3 manifest: `/mnt/e/AI_Team/mitunet/phase3a_opening_source_class_repair/experiments/mitunet_phase3a_opening_source_class_repair_20260812_224352_UTC/targets/candidate_v3/manifests`.
- Review manifest: `/mnt/e/AI_Team/mitunet/phase3a_opening_source_class_repair/experiments/mitunet_phase3a_opening_source_class_repair_20260812_224352_UTC/review/review_manifest.csv`.
- Class review manifest: `/mnt/e/AI_Team/mitunet/phase3a_opening_source_class_repair/experiments/mitunet_phase3a_opening_source_class_repair_20260812_224352_UTC/review/class_review_manifest.csv`.
- Opening review manifest: `/mnt/e/AI_Team/mitunet/phase3a_opening_source_class_repair/experiments/mitunet_phase3a_opening_source_class_repair_20260812_224352_UTC/review/opening_review_manifest.csv`.

## Next Gate

Complete class-centric and plan-centric human review before any canary, probe, or training run.
