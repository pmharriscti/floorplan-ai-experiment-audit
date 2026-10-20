# Integration Plan

The normalized [config.yaml](config.yaml) is a design specification. Implement it in the scientific source workspace using the inspected Phase 5 and Phase 3A helpers. This audit entry does not provide a verified combined training entry point.

## Inspected Integration Points

Paths below are relative to `/home/pmharris/dev/mitunet` unless another workspace is named.

| Module | Current behavior | Experiment-14 adaptation |
| --- | --- | --- |
| `hierarchical_model.py` | Preserves the baseline wall path, copies decoder groups, adds named sigmoid heads; task constant includes `512` | Load experiment 06; verify 1024 wall identity and output shapes; version task/checkpoint metadata |
| `hierarchical_targets.py` | Reads Phase 1/2 cache masks and checks their shape; dependencies include Phase 2 door hashes | Regenerate 1024 parents and add explicit versioned door/window providers and cache keys |
| `hierarchical_dataset.py` | Loads final-space mask paths and requires configured shapes | Bind every path to the new 1024 bundle; reject stale mixed-resolution rows |
| `target_integrity/opening_derivation_v3.py` | Implements source association and scoped v3.2 repair | Freeze flags, nonempty scope, source dispositions and native geometry traces |
| `scripts/run_phase3a2_opening_axis_repair.py` | Creates native candidates, scope, traces, audit tables and review evidence | Materialize native labels, then pass the validated paths through the combined adapter |
| `hierarchical_losses.py` | Phase 5 task losses/positive weighting | Recompute train-only statistics from final masks; preserve explicit fixed weights |
| `scripts/run_hierarchical_multihead_experiment.py` | Supports warm-up/joint groups and accumulation; default names/reports assume 512; reproduction stage iterates val and test | Update task/config identity; split reproduction into validation-only selection and final frozen test evaluation |
| `hierarchical_evaluation.py` | Uses 2 px boundary/5 px point metrics and fixed prediction bit layout | Add named evaluation coordinate profiles, full fixture outputs and a versioned encoding |
| `hierarchical_label_validation.py` | Validates final masks and class-bit storage | Run on the new bundle; extend scoped geometry and transform invariants |
| `target_integrity/validate_model_compatibility.py` | Explicitly recognizes older modes; generic fallback treats an unknown mode as binary | Validate all eight heads and 16 channels directly |

The preceding filenames refer to `mitunet_cubicasa/` except the two script paths. Source hashes are recorded in the inventory. Relevant earlier compiler modules and 512 materializer files are inventoried as references, not drop-in replacements.

## 1. Freeze The Scientific Inputs

Record code commit plus all modified/untracked dependency hashes, environment, dataset version, sample IDs, source image/SVG hashes, parent checkpoint hash, target mapping/derivation contracts, source dispositions, geometry repair keys and fixture class order. Copy the resolved configuration and input identities into a new timestamped run directory.

Resolve sample IDs to official split membership independently of CSV path spelling. Keep the E-drive results root separate from the source tree. On a cloud GPU, copy immutable inputs to pod-local storage, verify hashes there, and persist epoch checkpoints and records to durable storage.

## 2. Build Native And Model-Space Targets

1. Generate the baseline structural-wall masks from the same native SVG definition as experiment 06.
2. Generate source/symbol masks and door/window openings using the declared Phase 3A policies, frozen dispositions and exact v3.2 door scope.
3. Store native target hashes and per-instance traces before resizing.
4. Create new 1024 letterbox masks and record exact source/model transforms.
5. Derive 1024 boundaries, skeletons, clustered junctions and endpoints; create training bands separately.
6. Encode nine fixture masks with the frozen source-class order and inspect upstream overlap handling.
7. Fill all hierarchical manifest paths, metadata paths and dependency hashes. Remove reliance on immutable 512 Phase 1/2 mask paths for this run.
8. Run whole-mask and per-instance survivability audits plus semantic/mechanical checks on the final masks.

The new cache key must contain source image/SVG hashes, target contract, repair scope, source dispositions, generator implementation, output size, rounding/interpolation/padding policy, band radii, class order and relevant dependency hashes. Changing any one of these invalidates the target entry. Retaining a stale `phase2_door_opening_raw_sha256` under a new version name is insufficient.

## 3. Verify Initialization

Build the binary experiment-06 model and the new hierarchical model with the same dependency versions. Strictly load/remap encoder, wall decoder and wall-head tensors; write missing/unexpected keys and shape differences. Check parameter counts and raw-logit outputs on several representative 1024 inputs in evaluation mode, with a declared numerical tolerance (initial proposal: max absolute error `1e-6` in a deterministic float32 check).

During warm-up, verify no inherited parameter or running buffer changes and that new decoder/head parameters do change. Keep inherited modules in eval mode so BatchNorm/dropout/drop-path cannot alter the protected path while frozen. Resume must restore the phase and these mode settings.

## 4. Resource And Optimization Preflight

Profile all eight heads and all losses at physical batch 1, accumulation 4, AMP. Record allocated/reserved VRAM, step time, data wait, examples/s, finite losses, nonzero gradients, task weights, all three LR groups and optimizer update counts. Include rare fixtures, an empty-opening case, a dense plan and a border opening.

Run a warm-up step and a joint step; memory use can differ. A preflight that only forwards the wall path does not measure the integrated workload. The proposed workload has more decoders than experiment 06 and larger activations than experiment 09; no hardware capacity is inferred from either parent's run alone.

The main Phase 5 loop already accumulates gradients. Check incomplete accumulation windows when using diagnostic sample limits; its inspected loop divides each microbatch by the configured accumulation count even for a short final window. The full proposed train split has 4200 physical batches and 1050 updates at batch 1/accumulation 4, but limited probes need their own correct normalization and counters. Existing diagnostic paths that step every batch must report that difference.

Retain the source's joint normalization behavior initially and record it. If batch-1 normalization or memory requires a change, version that change and apply it equally to paired controls. Gradient accumulation does not duplicate batch-4 BatchNorm statistics or nonlinear batch-reduced loss behavior.

## 5. Train And Select

Use the proposed four warm-up and 26 joint epochs, fixed task weights, Adam, AMP and explicit LR groups. The wall floor comes from the validation-only reproduction of experiment 06. Write per-epoch per-head losses, pixel prevalence, gradient diagnostics, LR, wall gate, hierarchical score and timing.

Persist best gated hierarchical, best wall, best ungated and last recovery states. Recovery state contains optimizer, scheduler, scaler, RNG, sampler/epoch position, phase, bests, freeze/mode state, class order, configuration and manifest identities. Save at epoch boundaries or an explicitly documented interval; avoid a large durable checkpoint write on every batch.

Run the short probe before full training and check wall retention, learnability, target survival, memory and recovery. A probe is an engineering gate; its ranking is not a final performance result.

## 6. Version The Inference Contract

Record preprocessing, image dimensions, padding, probability interpolation, activation, per-head thresholds, NMS, point coordinate space, fixture order, prediction storage dtype and model/target/checkpoint identity. Store per-head probabilities outside this audit repository so threshold and downstream checks remain reproducible.

Proposed combined prediction encoding is `uint16`: bits 0-6 for structural wall, boundary, centerline, junction, endpoint, door and window; bits 7-15 for the nine fixture classes in config order. This is sixteen binary planes. Do not cast this encoding into the old Phase 5 `uint8` format, whose fixture bit is only a union.

Downstream readers must require the new contract version, dtype, shape and letterbox transform before reading the bit layout. Preserve source-to-model-to-output coordinate maps, units/scale evidence, probabilities and review provenance for IFC work. The bridge's wall/door bit positions can be retained, but a matching bit number alone does not prove compatible coordinates or semantics.

## Implementation Checks Before A Run

| Area | Required checks |
| --- | --- |
| Source labels | Exact frozen native inputs, source dispositions and scoped repair keys |
| Transform | Asymmetric padding, non-square inputs, border instances, exact instance/aggregate mapping |
| Wall identity | New 1024 wall target and inherited logits match the experiment-06 reference |
| Target version | Toggling v3.1/v3.2 changes only declared door instances; windows held fixed in that comparison |
| Windows | Symbol/opening separation, host evidence, explicit policy version |
| Small objects | Per-instance nonempty-to-empty and component changes; no dilation hiding canonical loss |
| Fixtures | Nine-channel order, `uint16` round trip, unknown-class handling and overlap audit |
| Training | Warm-up buffer identity, new-head updates, LR groups, full/partial accumulation, resume |
| Selection | Validation-only parent reproduction, correct 1024 wall floor, no below-floor selection |
| Evaluation | Common reference labels, coordinate/tolerance profiles, matching and empty-target policy |
| Export | Full 16-plane round trip and rejection of an incompatible old reader/contract |

The 56 local labeling tests recorded in this proposal cover existing helpers. The checks above describe additional coverage required by the new integration.
