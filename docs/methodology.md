# Audit Methodology

The audit records evidence, not intentions. A value is included only when it was found in a persisted artifact such as JSON, CSV, YAML, Markdown report, checkpoint manifest, or metadata file.

## Evidence Levels

`VERIFIED` means the value was located in one or more source artifacts during the initial audit pass.

`UNKNOWN` means the value may exist elsewhere, but it was not found in the inspected artifacts.

`NOT YET VERIFIED` is reserved for claims that look plausible from context but were not checked against an artifact. This initial repo avoids using such values in the scoreboard.

## Extraction Rules

- Source experiment directories are read-only evidence sources.
- Large artifacts are referenced by path, size, and hash status only.
- If the source reports a checkpoint SHA-256, the hash is copied. If the manifest says hashing was deferred, this repo records `UNKNOWN`.
- If a historical claim conflicts with a located final report, the located final report wins.
- If training history contains a better intermediate value than final evaluation, both may be recorded in detailed metrics, but the scoreboard uses the final or selected primary metric.

## Primary Metric Convention

The scoreboard uses one primary split per experiment:

- Baseline, DeepLabV3, Phase 1, and Phase 2 use validation or final validation evaluation metrics from the inspected artifacts.
- Hybrid tiling uses the locked validation selection because the selection artifact explicitly records validation selection and states that test was not used for selection.
- Test metrics, where available, are retained inside the experiment-level `metrics.json` files.

## Interpretation Labels

Outcome categories are short audit labels, not new scientific claims:

- `baseline_positive`: a successful baseline run.
- `mixed_positive`: a useful result with an important qualification.
- `negative_comparator`: a completed comparator that underperformed the baseline.
- `positive_structural_expansion`: a completed expansion that introduced new validated structure metrics.
- `mixed_phase2_expansion`: a completed expansion with both improvements and regressions.
- `negative_optimizer_comparator`: a completed optimizer substitution that underperformed its control.
- `positive_high_resolution_baseline`: a completed higher-resolution whole-plan run that improved over its baseline.
- `negative_high_resolution_crop_treatment`: a completed high-resolution crop treatment that underperformed its supplied whole-plan control, with formulation caveats.
- `positive_gated_hierarchical_expansion`: a completed multi-head expansion that met its declared wall-protection gate (baseline minus a fixed tolerance) on every eligible epoch while adding validated new-head metrics; the small residual wall regression inside the tolerance is recorded, not hidden.
- `inconclusive_label_version_ablation`: a controlled target-version (label) ablation whose training completed but whose evidence cannot separate the two label versions from ordinary training variation, either because the label difference is too small, because the deciding evaluation was never run, or because the labels themselves are still unadjudicated. It is recorded as process evidence, not as a ranking of the versions.
