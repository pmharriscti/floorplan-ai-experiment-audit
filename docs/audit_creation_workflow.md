# How Experiment Audits Are Created

This document explains how a completed floor-plan AI experiment is converted into an evidence-backed entry in this repository. It describes the process used for experiments 01-08 as of 2026-09-24.

The central rule is simple:

> The audit records persisted evidence, not intentions, recollections, or a newly reconstructed result.

An audit is not a new training run. It is a compact, reviewable package that connects claims to source artifacts, preserves the important configuration and metrics, adds a small amount of visual evidence, and leaves large datasets and checkpoints in their original storage locations.

## End-to-End Flow

```text
historical run directories
        |
        v
inventory configs, reports, metrics, logs, manifests, and checkpoints
        |
        v
resolve conflicts and select the authoritative result
        |
        v
normalize README + config.yaml + metrics.json + provenance.json
        |
        v
generate or copy representative visual QA with per-image metadata
        |
        v
update the global index, scoreboard, and comparison pages
        |
        v
validate schemas, links, hashes, images, file policy, and Git diff
        |
        v
commit and publish the audit entry
```

## Repository Contract

Every experiment receives the same four core files:

```text
experiments/<NN_experiment_slug>/
|-- README.md
|-- config.yaml
|-- metrics.json
|-- provenance.json
`-- qa/
    `-- README.md
```

Optional directories are added only when supported by the source run:

```text
|-- plots/                 # Small historical or derived training plots
|-- results/               # Small original JSON/CSV result files
|-- source_provenance/     # Original provenance, environment, and checksum files
`-- src/                   # Source availability notes or small runner files
```

The repository-wide views are:

- [README.md](../README.md): human-readable overview and current conclusions.
- [EXPERIMENT_INDEX.md](../EXPERIMENT_INDEX.md): source locations and the evidence files inspected for each experiment.
- [EXPERIMENT_SCOREBOARD.csv](../EXPERIMENT_SCOREBOARD.csv): one normalized comparison row per experiment.
- [metrics definitions](metrics_definitions.md): interpretation of the reported metrics.
- [reproducibility notes](reproducibility.md): artifact roots and rerun requirements.
- `docs/visual_comparisons/`: links that make representative outputs easy to compare.

## 1. Define the Audit Question

The first step is to state what the run actually tested. The name must describe the treatment, comparator, or model family without claiming more than the evidence supports.

Examples include:

- a 512 px binary-wall baseline;
- a model-architecture comparator;
- an optimizer substitution;
- a structural-head expansion;
- a whole-plan 1024 run;
- a native-1024-crop treatment evaluated on 512 whole plans.

This distinction matters because similarly named runs can have different spatial formulations. Experiment 06 and experiment 08 both involve 1024 px input, but experiment 06 is a whole-plan high-resolution run while experiment 08 trains on native crops and validates on whole-plan 512 letterboxes. Their results cannot be presented as interchangeable.

Before extracting numbers, the audit identifies:

- the scientific question;
- the treatment and comparator;
- the prediction targets;
- the train, validation, and test presentations;
- the selection metric and split;
- whether the run is complete, partial, exploratory, or a comparator;
- the claims the available evidence does not support.

## 2. Inventory the Source Evidence

Source experiment directories are treated as read-only evidence. The audit searches the supplied roots for the smallest authoritative set of files needed to understand and reproduce the result.

Typical evidence includes:

| Evidence type | Examples | Purpose |
| --- | --- | --- |
| Final reports | `FINAL_REPORT.md`, `EXPERIMENT_SUMMARY.md`, `summary.json` | Run status, selected checkpoint, final conclusions |
| Evaluation outputs | `metrics.json`, `test_metrics.json`, `validation_metrics.json` | Aggregate model quality |
| Selection artifacts | `threshold_search.csv`, locked-selection JSON | Threshold and checkpoint selection |
| Training history | `history.csv`, `training_history.csv`, `history.json` | Best epoch, final epoch, loss, timing, learning rate |
| Resolved configuration | YAML/JSON config, command file | Actual model, data, optimizer, loss, and runtime settings |
| Data manifests | train/validation/test CSVs and checksums | Split membership, counts, and sample identity |
| Reproducibility records | environment files, git state, DVC/MLflow metadata | Code and environment identity |
| Large artifacts | checkpoints, probability maps | Inference source or externally retained evidence |
| Visual outputs | overlays, masks, plots | Qualitative review and failure analysis |
| Logs | complete run log, launch log | Operational facts not present in structured outputs |

The evidence inventory is recorded in both the experiment README and `provenance.json`. The global index records the source roots so a reviewer can return to the historical run.

## 3. Rank Evidence and Resolve Conflicts

The audit uses persisted artifacts in roughly this order:

1. Final selected-checkpoint evaluation and locked-selection artifacts.
2. Structured final summaries and resolved configurations.
3. Per-epoch histories, manifests, and environment records.
4. Run logs for operational details.
5. User-supplied narrative summaries for context that is not available elsewhere.

When artifacts disagree, the discrepancy is not silently averaged away. The most direct final artifact wins, and the competing value is either explained or omitted.

Examples:

- A peak metric in training history is not substituted for final selected-checkpoint evaluation.
- A configured threshold is not substituted for a validation-selected threshold.
- A report describing an intended 1024 run does not override a resolved config that verifies `image_size: 512`.
- Rounded comparison values from a supplied summary are labeled as rounded or approximate.
- A test result is not inferred when the run explicitly disabled test inference.

### Evidence Status

`VERIFIED` means the value was found in a persisted source artifact during the audit.

`UNKNOWN` means the field may exist elsewhere, but the inspected evidence did not establish it. CSV uses `UNKNOWN`; JSON uses `null` where appropriate.

`NOT YET VERIFIED` is reserved for a plausible claim that still needs source confirmation. Missing visual assets may also receive a `NOT_YET_AVAILABLE` marker rather than a fabricated replacement.

## 4. Normalize the Configuration

`config.yaml` is a compact map of the settings that materially define the experiment. It is not a verbatim copy of every source option.

The normalized config usually records:

- experiment ID, name, status, and source directory;
- target type and target-generation policy;
- dataset version, split counts, image size, and resize/crop strategy;
- architecture, encoder, pretrained weights, output heads, and activation policy;
- epochs, batch size, gradient accumulation, optimizer, learning rate, loss, scheduler, seed, and AMP;
- selected thresholds and postprocessing;
- checkpoint path and SHA-256 when available;
- code commit and source-tree state;
- environment or infrastructure facts that affect interpretation;
- explicit unknowns and limitations.

Configuration is taken from resolved run artifacts whenever possible. Proposal configs and remembered launch commands are secondary evidence because they may not describe what actually ran.

## 5. Normalize the Metrics

`metrics.json` preserves exact machine-readable values. The README may round values for readability, but JSON keeps the source precision.

Every metrics file identifies:

- the experiment and evidence status;
- the primary split;
- the primary scoreboard metrics;
- the selected thresholds;
- best epoch and completion state;
- validation and test details when present;
- comparisons and deltas when valid;
- sample counts and any confidence intervals available in the source.

### Primary Metric Selection

The scoreboard contains one row per experiment, so each entry must choose one primary result consistently:

- Baseline and architecture runs use the source run's selected or best validation result.
- A locked hyperparameter sweep uses the locked validation selection.
- An optimizer experiment may use held-out test metrics when its source comparison is explicitly test-based.
- Structural experiments use the final evaluation corresponding to their selected structural checkpoint.
- A run without test inference remains validation-only.

Best-epoch and final-epoch values can both appear in `metrics.json`, but they are labeled separately. The audit does not move a metric between validation and test or between micro and macro aggregation.

### Comparison Guardrails

A delta is meaningful only when the compared runs align on the relevant contract. The audit checks:

- dataset split and membership;
- target definition;
- input presentation and resize/crop strategy;
- threshold and postprocessing;
- metric aggregation;
- checkpoint-selection rule;
- whether test data influenced selection.

If these differ, the README explains the confounder. Experiment 08 is therefore described as a negative crop treatment, not proof that image resolution itself is harmful.

## 6. Build Provenance

`provenance.json` connects the normalized audit back to the historical evidence. It is the chain-of-custody record for the entry.

Depending on availability, it contains:

- absolute source run and source repository paths;
- the exact files inspected;
- source-file SHA-256 values;
- checkpoint paths, sizes, and hashes or hash status;
- train/validation/test manifest counts and hashes;
- source commit, dirty-tree state, and file hashes when a commit is unavailable;
- DVC and MLflow status;
- environment and package records;
- visual-evidence sources and generation method;
- missing artifacts and reproducibility limits;
- confirmation that large artifacts were not committed.

Large checkpoint hashes may come from an existing manifest or be calculated directly when practical. If hashing was deferred by the source run, the audit says so rather than inventing an identifier.

When a copied text artifact requires a mechanical transformation, both identities are retained. For example, experiment 08 normalizes one CSV from CRLF to LF and records the source hash, the transformation, and the audit-copy hash.

## 7. Create Visual QA

Visual evidence is intentionally small and inspectable. It is meant to reveal geometry and failure modes that aggregate metrics hide, not to replace split-level evaluation.

All audit-generated error overlays use the same palette:

- green: true-positive pixels;
- red: false-positive pixels;
- blue: false-negative pixels.

Masks are saved with nearest-neighbor semantics and checked for binary values. Source images are saved as RGB. Each generated sample receives metadata describing its identity, split, checkpoint or probability-map source, threshold, source paths, hashes, metrics, dimensions, and generation method.

### Visual-Evidence Strategies

| Strategy | Experiments | What the audit does |
| --- | --- | --- |
| Checkpoint inference | 01, 02, 03, 06 | Load the verified checkpoint, reconstruct the validation item from its manifest, apply the recorded threshold, save masks and overlays, and recompute per-image pixel metrics as a cross-check. |
| Structural checkpoint inference | 04 | Regenerate wall-region, centerline, and junction outputs from the Phase 1 checkpoint. Junction points are rendered as masks only for visualization; historical point-matching metrics remain authoritative. |
| Saved probability maps | 05 | Apply recorded thresholds to historical Phase 2 validation probability maps for wall, centerline, junction, boundary, and door/opening outputs. No new model inference is performed. |
| Historical comparison copy | 07 | Copy the source run's six representative Adam-vs-AdamW test comparisons, masks, and overlays. No training or inference is performed. |
| Historical composite copy | 08 | Copy four composites from the best RunPod epoch. Each already contains input, target, prediction, and TP/FP/FN panels. No training or inference is performed. |

The core visual generator is [generate_audit_overlay.py](../scripts/generate_audit_overlay.py). It uses three shared validation samples across experiments 01-06:

- `high_quality_architectural/333`: typical clean validation case;
- `high_quality_architectural/3015`: strong high-resolution case;
- `high_quality_architectural/5559`: difficult failure case.

Using the same sample identities makes model and task differences easier to inspect. The generator also creates contact sheets and [the shared comparison index](visual_comparisons/shared_validation_samples.md).

The AdamW copy-only workflow is implemented in [generate_adamw_audit_visuals.py](../scripts/generate_adamw_audit_visuals.py). Its six samples are source-selected roles such as strongest clean case, difficult case, false-positive-heavy case, false-negative-heavy case, sparse target, and dense target.

The RunPod entry preserves the source composites directly because they are already self-contained historical evidence. Its image list and hashes are recorded in [experiment 08 QA metadata](../experiments/08_mitunet_1024_highres_runpod/qa/metadata.json).

### What Visual Generation Never Does

- It does not train or fine-tune a model.
- It does not alter the historical run directory.
- It does not select a new aggregate threshold from the curated examples.
- It does not promote a per-image observation into a split-level claim.
- It does not silently regenerate an unavailable artifact and label it historical.

## 8. Write the Experiment Report

The experiment README is the human-readable synthesis. It normally contains:

1. The tested question and experiment identity.
2. Source locations and primary evidence files.
3. Verified configuration.
4. Verified primary and supporting metrics.
5. Links to visual QA and plots.
6. Interpretation relative to the correct comparator.
7. Missing evidence, confounders, and unsupported claims.
8. Links to normalized config, metrics, and provenance.

Interpretation labels such as `negative_comparator` or `positive_structural_expansion` are compact audit categories. They describe the observed result; they are not substitute scientific metrics.

## 9. Update Repository-Wide Views

A new experiment is not complete until it is visible from the repository root.

The audit updates:

- the experiment table and findings in the root README;
- the source-evidence row in `EXPERIMENT_INDEX.md`;
- one schema-compatible row in `EXPERIMENT_SCOREBOARD.csv`;
- the outcome-label definitions when a new category is introduced;
- visual-comparison documentation when the experiment has review images;
- reproducibility notes when it introduces a new artifact root or restoration requirement.

The scoreboard row must match the experiment's `metrics.json` and `provenance.json`, especially experiment ID, primary split, metrics, threshold, checkpoint identity, code identity, source location, and evidence status.

## 10. Enforce the Small-Artifact Policy

The audit repository intentionally excludes heavy or operationally sensitive material:

- model checkpoints such as `.pth`, `.pt`, and `.ckpt`;
- datasets and caches;
- NumPy prediction dumps and full probability-map collections;
- complete generated output trees;
- large videos or uncurated media;
- secrets, credentials, and private keys.

Checkpoints stay in their external archive and are referenced by path, byte size, SHA-256, and availability status. Curated PNG/JPEG evidence is explicitly allowed by `.gitignore` only under audit QA, plot, and visual-comparison locations.

Small original JSON, CSV, environment, checksum, and provenance files may be copied when they materially improve reviewability. Copy-only artifacts keep their source path and hash in provenance.

## 11. Validate Before Publishing

Validation scales with the evidence added, but a completed audit normally checks all of the following.

### Structured Data

- Every JSON file parses.
- Every YAML file parses.
- CSV headers and row counts are valid.
- Experiment IDs are unique.
- The scoreboard contains exactly one row for each experiment.
- Primary scoreboard values equal the corresponding `metrics.json` values.
- Normalized best/final metrics agree with the original history and summary files.

### Provenance

- Source paths exist when they are expected to be local.
- Copied artifact hashes match the source or document any transformation.
- Checkpoint hashes agree with source checksum files or manifests.
- Code commits are checked for local availability.
- Dirty or non-Git source trees are reported rather than hidden.

### Visual Integrity

- Referenced assets exist.
- Images open successfully and have the recorded dimensions and mode.
- Ground-truth and prediction masks are binary.
- Related source, target, prediction, and overlay dimensions align.
- Image hashes match per-sample metadata.
- Contact sheets and Markdown links resolve.

### Repository Hygiene

- No checkpoint or forbidden large-artifact suffix is staged.
- No newly added file exceeds the review-size limit used for the audit pass.
- A secret-pattern scan has no findings.
- `git diff --check` passes.
- Copied files do not accidentally retain executable mode.
- The worktree contains no unrelated changes from the audit.
- The final commit is pushed and the branch is synchronized with its remote.

The current repository performs these checks with focused shell and Python validation commands. A generalized schema validator has not yet been added, so the validation evidence is procedural rather than one reusable command.

## Current Automation and Manual Work

| Activity | Current state |
| --- | --- |
| Source artifact discovery | Manual, using the paths supplied for each experiment |
| Conflict resolution and primary-metric choice | Manual audit judgment |
| Core visual QA for experiments 01-06 | Automated by `scripts/generate_audit_overlay.py` |
| AdamW visual packaging | Automated by `scripts/generate_adamw_audit_visuals.py` |
| RunPod historical-composite packaging | Manual copy with recorded hashes |
| Normalized README/config/metrics/provenance | Manually authored from verified evidence |
| JSON/YAML/link/image/hash validation | Scripted during each audit pass, but not yet centralized |
| Scoreboard and index updates | Manual with cross-file validation |

The visual scripts contain explicit experiment paths and thresholds. They are reproducibility tools for the known audits, not a generic experiment-ingestion framework.

## Common Failure Modes

### Treating a planned setting as an executed setting

Always prefer the resolved config, final log, or checkpoint metadata over a proposal document.

### Reporting the wrong split

Validation selection and held-out test evaluation are different claims. Keep the split attached to every metric.

### Mixing best and final values

Training history may peak before the last epoch. Record both when useful and label the selected result.

### Comparing incompatible formulations

Resolution, cropping, context, threshold, task heads, and postprocessing can all change the experiment. A numerical delta without this context can be misleading.

### Recreating historical evidence without labeling it

Regenerated predictions must say which checkpoint, manifest, transform, and threshold produced them. Copied historical images must retain source hashes.

### Treating curated samples as aggregate evaluation

The examples support visual diagnosis only. Split-level metrics remain the basis for experiment ranking.

### Committing large model artifacts

Reference checkpoints externally and preserve checksums. Normal Git is not used as checkpoint storage in this repository.

## Checklist for a New Audit

- [ ] Define the exact experiment question, treatment, comparator, and non-claims.
- [ ] Confirm the source run directory and source repository.
- [ ] Inventory final reports, metrics, histories, configs, manifests, logs, and checkpoints.
- [ ] Resolve conflicting values using the evidence hierarchy.
- [ ] Select and label the primary split and metric.
- [ ] Create `README.md`, `config.yaml`, `metrics.json`, and `provenance.json`.
- [ ] Record checkpoint path, size, hash, and hash source/status.
- [ ] Record code commit or file hashes and dirty-tree state.
- [ ] Add representative visual QA using the appropriate evidence strategy.
- [ ] Record per-image source paths, hashes, thresholds, metrics, and integrity checks.
- [ ] Update the root README, experiment index, scoreboard, and comparison docs.
- [ ] Parse all structured files and validate cross-file metric consistency.
- [ ] Check links, images, mask integrity, file sizes, forbidden suffixes, and secrets.
- [ ] Run `git diff --check` and inspect file modes.
- [ ] Commit only the audit changes, push, and confirm a clean synchronized branch.

## Definition of Done

An audit is complete when another reviewer can answer these questions without reopening the entire experiment workspace:

1. What was tested?
2. What data, model, training, and evaluation settings actually ran?
3. Which checkpoint and threshold produced the selected result?
4. What are the primary metrics, on which split, and at what precision?
5. How does the result compare with the correct baseline or predecessor?
6. What do representative successes and failures look like?
7. Where are the original artifacts and large files stored?
8. Which code, data manifests, and environment records identify the run?
9. What evidence is missing or ambiguous?
10. What claims would go beyond the available evidence?

That is the standard these audit entries are designed to meet.
