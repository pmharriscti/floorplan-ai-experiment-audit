# Shared Validation Samples

The visual QA pass uses the same three validation sample identities across all five experiments.

| Sample | Role | 01 | 02 | 03 | 04 | 05 |
| --- | --- | --- | --- | --- | --- | --- |
| high_quality_architectural/333 | typical_clean_validation_case | [metadata](../../experiments/01_binary_mitunet/qa/high_quality_architectural__333/metadata.json) | [metadata](../../experiments/02_hybrid_tiling/qa/high_quality_architectural__333/metadata.json) | [metadata](../../experiments/03_deeplabv3/qa/high_quality_architectural__333/metadata.json) | [metadata](../../experiments/04_phase1_wall_structure/qa/high_quality_architectural__333/metadata.json) | [metadata](../../experiments/05_phase2_boundary_openings/qa/high_quality_architectural__333/metadata.json) |
| high_quality_architectural/3015 | strong_high_resolution_case | [metadata](../../experiments/01_binary_mitunet/qa/high_quality_architectural__3015/metadata.json) | [metadata](../../experiments/02_hybrid_tiling/qa/high_quality_architectural__3015/metadata.json) | [metadata](../../experiments/03_deeplabv3/qa/high_quality_architectural__3015/metadata.json) | [metadata](../../experiments/04_phase1_wall_structure/qa/high_quality_architectural__3015/metadata.json) | [metadata](../../experiments/05_phase2_boundary_openings/qa/high_quality_architectural__3015/metadata.json) |
| high_quality_architectural/5559 | difficult_failure_case | [metadata](../../experiments/01_binary_mitunet/qa/high_quality_architectural__5559/metadata.json) | [metadata](../../experiments/02_hybrid_tiling/qa/high_quality_architectural__5559/metadata.json) | [metadata](../../experiments/03_deeplabv3/qa/high_quality_architectural__5559/metadata.json) | [metadata](../../experiments/04_phase1_wall_structure/qa/high_quality_architectural__5559/metadata.json) | [metadata](../../experiments/05_phase2_boundary_openings/qa/high_quality_architectural__5559/metadata.json) |

Direct visual comparison should account for task differences: experiments 01-03 are binary wall-region models, Phase 1 adds centerline and junction heads, and Phase 2 adds wall-boundary and door-opening heads.
