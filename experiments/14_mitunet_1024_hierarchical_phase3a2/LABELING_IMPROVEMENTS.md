# Labeling Improvements From The Local Development Work

This document records the label engineering to carry into experiment 14. It covers the source work under `/home/pmharris/dev`, names its files, and distinguishes inspected implementations from adaptations proposed for the integrated 1024 model. Exact file hashes are in [source_provenance/source_inventory.json](source_provenance/source_inventory.json).

## Source Workspaces

| Workspace | Contribution | Identity |
| --- | --- | --- |
| `/home/pmharris/dev/mitunet` | Phase 3/3A contracts, source taxonomy, opening repairs, topology, fixture masks, audits, review tool and Phase 5 dataset | Inspected HEAD `aebca12e284aa17ddef08d45327e191773e0f07a`; dirty tree, per-file hashes required |
| `/home/pmharris/dev/mitunet_multihead` | Earlier openings-aware vector label compiler, rasterization, validation and manifest builder | Git initialized with no commits; per-file hashes required |
| `/home/pmharris/dev/mitunet_phase3a2_512` | Matched target materialization, exact nearest-neighbor instance mapping, changed-pixel and disappearance reports | Separate 512-specific preparation implementation; source files pinned in the inventory |

The local directories `phase5_hierarchical_mitunet` and `human_review` were empty at inspection. The active Phase 5 and Phase 3A implementations described here live under `mitunet`.

## 1. Explicit Meaning For Each Target

The local contracts separate concepts that had previously been easy to conflate:

| Concept | Required meaning in experiment 14 |
| --- | --- |
| `structural_wall` | Baseline SVG Wall definition before subtracting openings |
| `visible_wall` | Structural wall after subtracting the union of raw validated openings |
| `door_opening` | Source-supported doorway corridor |
| `window_opening` | Source-supported window corridor |
| `door_symbol` | Visual leaf, swing, panel or outline evidence |
| `window_symbol` | Visual frame, glazing, mullion or stroke evidence |
| Centerline | Skeleton derived from the declared structural-wall target |
| Junction/endpoint | Points tied to that skeleton and its 8-connected graph, preserving the declared corner/branch convention |
| Fixture class | Explicit source-class mapping, with lineage preserved |

Sources: `configs/targets/target_contract_v1.yaml`, `candidate_target_mapping_v3.yaml`, `opening_derivation_v3.yaml`, and `mitunet_cubicasa/target_integrity/{contracts,derive_walls,derive_topology}.py`. Copies of the YAML policies are preserved under [source_provenance/](source_provenance/).

The structural-wall target used by the parent checkpoint must remain pixel-identical when materialized with the same transform. `structural_wall_repair.py` contains a local bridge helper for a different reconstruction use case; enabling it on this wall target would create an additional wall-label treatment. Global closing is excluded from the proposed primary contract.

## 2. Source-Class Inventory And Conservative Mapping

`source_taxonomy.py`, `source_mapping.py` and `source_class_evidence.py` preserve raw class strings, normalize them for analysis, inspect parent/child context and geometry, and assign one of `map`, `ignore`, `unsupported` or `review_required`.

The taxonomy names door leaf, swing, jamb, threshold, sliding/pocket/double symbols, window frame/glazing/sill/mullion, structural sources, fixture classes, text, dimensions and decorative/non-target geometry. A class name alone is insufficient evidence for a mapping.

Carry into experiment 14:

- Raw class, normalized class, element/instance ID, parent/child classes, source geometry, mapped target, action and mapping version.
- Explicit exclusion of room labels, dimensions, hidden controls and unrelated decorations from opening targets.
- Unknown fixture-like classes retain evidence and an explicit disposition; they are not silently relabeled `other_fixture`.
- A report of unsupported/malformed/out-of-bounds geometry, distinct from a valid absence of an object.

The legacy parser contains permissive fallback mappings. The new adapter must check actual emitted source classes against the frozen taxonomy; copying a policy YAML alone does not enforce that policy.

## 3. Structural And Visible Walls

Both the earlier compiler and the Phase 3A code represent the formula explicitly:

```text
opening_all = door_opening OR window_opening
visible_wall = structural_wall AND NOT opening_all
```

The earlier vector compiler also checks union/difference area relationships and disjointness before rasterization. Reuse those validation ideas alongside the Phase 3A mask checks.

Experiment 14 keeps the structural-wall head as the protected task and derives visible wall from the predicted masks. Raw openings are used for this derivation; training dilation must not redefine visible-wall geometry. Preserve opening pixels outside the wall as a reported support discrepancy rather than silently modifying the structural target to make a formula pass.

## 4. Symbols And Openings Are Separate Artifacts

Phase 3A generates symbol masks from visual outlines/strokes and opening masks after wall association. This supports direct audits of exact symbol/opening equality, off-wall openings and incorrect source interpretation.

Sources: `opening_derivation_v3.py`, `opening_association.py`, `candidate_target_mapping_v3.yaml`, `test_door_symbol_opening_separation.py`, and `test_window_symbol_opening_separation.py`.

Retain the evidence masks even though experiment 14 does not add symbol prediction heads. A swing arc or a thick frame is useful context for a reviewer, but its full footprint is not doorway/window width.

## 5. Phase 3A.1 Repairs

| Family | Implemented improvement | Preserve in experiment 14 |
| --- | --- | --- |
| A | Door-seed interpretation | Keep source evidence; use the v3.2 override on its explicit repair keys |
| B | Source-instance classification/localization, including border-collapsed cases and explicit dispositions | Preserve classifications and source geometry; no invented positive for an unsupported instance |
| C | Gap-aware host-wall association | Preserve host evidence and accepted/rejected candidates, with native-coordinate search parameters |

The source runner's native-pixel parameters are maximum association distance `3`, minimum overlap `0.05`, seed-repair minimum overlap `0.02`, local seed radius `48`, and gap search radius `36`. These operate in native image coordinates and must not be doubled just because the model input becomes 1024.

The source runner also carries explicit source-instance dispositions. The adapter must freeze those dispositions with its configuration, not only copy the boolean flags.

## 6. Phase 3A.2 Source-Supported Door Axes

The v3.1 Family A repair could synthesize a rectangle and snap it to a nearby wall. The v3.2 path uses the source `Door` threshold polygon and its parent `Wall` polygon, estimates tangent with PCA/SVD, derives the normal and compares axes modulo 180 degrees. It retains jamb endpoints and rejects incompatible host-axis evidence.

Required generator settings:

```yaml
target_generator_version_override: candidate_v3.2
repair_door_opening_tangent_normal_semantics: true
repair_door_opening_seed_semantics: true
repair_source_instance_classification_and_localization: true
repair_opening_host_wall_association: true
door_tangent_normal_axis_tolerance_degrees: 15.0
```

This excerpt must be combined with the exact native-pixel parameters, dispositions, and a **nonempty** `door_tangent_normal_repair_instances` list. The historical list is frozen in [phase3a2_repair_scope.json](source_provenance/phase3a2_repair_scope.json). The current helper treats an absent/empty list as unrestricted, so experiment 14's adapter must reject that accidental broadening.

Preserve these fields separately: legacy orientation, source threshold bbox, source host bbox, tangent angle/vector, normal angle/vector, opening angle/vector, jamb endpoints, angular disagreement, association evidence, source IDs, and added/removed pixels by source instance.

The historical scoped audit has ten tangent-aligned instances, zero wrong-wall cases and zero missing-jamb cases. The special axis repair is door-specific. Experiment 14 separately declares adopting the Phase 3A window-opening contract with inherited association repairs; it does not call that a v3.2 window-axis repair.

## 7. Shared SVG/Image/Mask Transforms

The earlier `mitunet_multihead` compiler implements conservative SVG inspection, nested translate/scale/rotate/matrix transforms, vector extraction, hole preservation and a shared raster transform stored in label metadata.

Its selected adoption points are:

- Rasterize in the source image's known canvas, preserving SVG viewBox/transform identity.
- Preserve polygon holes and per-class geometry.
- Apply the same resize/padding transform to image, masks and point metadata.
- Store source dimensions, scaled dimensions, scale and all four padding values.
- Keep masks lossless and categorical. Normalize compiler `0/255` masks to the model contract's `0/1` values explicitly.

The earlier compiler can fall back to geometry bounds when the canvas is unknown. That fallback does not establish image alignment and is excluded from the primary materialization. Its nearest-wall projection and optional rotated-rectangle regularization are also excluded from the source-supported Phase 3A.2 path.

## 8. Resize And Pixel-Preservation Audits

`validate_pixel_preservation.py` records native/processed positive pixels, expected area scaling, connected-component counts, categorical-value checks and nonempty-to-empty conversion. The separate `phase3a2_512/resize.py` and `build_matched_targets.py` add exact per-instance nearest-neighbor mapping, scoped changed-pixel checks and disappearance reports.

The historical 512 audit found an opening on `high_quality_architectural/5981` disappearing from its target. Increasing model resolution is a reason to remeasure survival, not proof of recovery.

For the new materializer:

1. Generate native masks and retain source-instance identity.
2. Transform each instance with the exact same mapping used for the aggregate mask.
3. Report native and model-space pixels, components, bbox and survival for each opening.
4. Separate object absent, invalid source, excluded instance, failed generation and vanished positive.
5. Compare legacy/repaired arms outside the declared scope; unexpected pixel changes are a failure.
6. Store raw labels separately from training bands. Dilation must not conceal a vanished canonical opening.

The 512 helper imports a fixed `MODEL_SIZE`; the new adapter must generalize it to 1024 and verify equivalence to the selected library's nearest-neighbor mapping. A generic nearest-neighbor claim alone does not guarantee identical sample rounding between implementations.

## 9. Topology And Model-Space Radii

`derive_topology.py` defines graph degree under 8-connectivity: degree 1 for endpoints, degree at least 3 for branch-junction candidates. Phase 1's generator additionally includes corners, with a 45-degree corner parameter and 15-degree straight-line tolerance, and supplies junction clustering and point metadata. Experiment 14 preserves that Phase 1/Phase 5 corner, T, cross and multi-branch convention while excluding endpoints from junction labels. Directly substituting the simpler degree-only helper would change the junction task. Carry the established clustering logic into the regenerated targets rather than counting every high-degree skeleton pixel as an independent junction.

Regenerate the skeleton and graph in the selected model space; upscaling an old skeleton does not preserve topology. The proposal uses a 512-equivalent radius policy: training dilation `1 -> 2`, junction/endpoint disk `3 -> 6`, junction cluster `3 -> 6`, and initial NMS `3 -> 6` when moving from 512 to 1024. These model-space values are proposed scale choices and require inspection. Boundary raw masks remain derived edges, and raw centerlines remain skeletons.

## 10. Fixtures And Overlap

Keep the nine fixture classes and explicit mappings in `fixture_target_mapping_v2.yaml`. The frozen channel order follows the source `FIXTURE_TARGETS` list:

```text
0 cabinetry_storage
1 appliance
2 toilet_urinal
3 sink_tap
4 sauna_bench
5 fireplace
6 bathtub_shower_jacuzzi
7 chimney
8 other_fixture
```

Training consumes nine independent channels. Preserve the `uint16` fixture bitmask and round-trip tests. This storage can represent overlap, but it cannot restore overlap already discarded by an upstream single-class rasterizer; audit that stage and record any resolution policy. Report class support and overlaps, including rare-class behavior. A binary fixture-obstacle union can remain a derived diagnostic without replacing the class head or adding another trained task.

## 11. Mechanical, Semantic And Manifest Validation

The local implementations add final-mask validation and MLflow-linked audit artifacts, including `hierarchical_label_validation.py` and `scripts/audit_run_labels_to_mlflow.py`. The earlier compiler supplies vector/raster checks and validation-aware manifest building.

Required artifacts for the combined target bundle:

- Shape/value/file validation for every raw/training mask and fixture bitmask.
- Structural/visible-wall formula checks, source-supported opening checks, symbol/opening equality flags, topology support and fixture-class coverage.
- Source image/SVG hashes, exact sample/split membership, target/config hashes and target provenance per row.
- Split leakage checks, duplicate keys, missing-path reports and class-prevalence reports.
- Separate validated inclusion/exclusion decisions and reasons. Keep the nominal official split membership stable; if samples are excluded, publish the exact evaluated subset and do not silently claim full `4200/400/400` coverage.
- Label validation on the final tensors consumed by the loss, not only on native SVG output.

The existing generic model-compatibility auditor recognizes older task modes. Its fallback is binary, so a compatible-looking report is insufficient for the new mode; add explicit checks for all eight heads, fixture channels, overlap policy and target keys.

## 12. Human Evidence And Frozen Labels

The Phase 3A review application contributes opening/source-class/plan workflows, source/SVG/mask comparison, controlled decision vocabularies, exact-key persistence, conflict detection, atomic saves, backups and append-only audit history. Keep review decisions separate from automated checks and copy their identities into frozen training/evaluation bundles.

`gold_freeze.py`, `gold_validation.py`, `review_adjudication.py` and the Phase 3B protocol describe versioned adjudicated references and common evaluation targets. Reuse these principles: evaluate paired models against the same frozen reference; record supported corrections, reviewer identity/time, source evidence and hashes. A filename containing `gold` or a manifest status does not itself supply a decision.

This audit publishes source contracts, aggregate facts and non-personal example images. It references mutable reviewer files by identity without republishing their notes.

## Verification Recorded For This Entry

On `2026-10-20`, the existing `mitunet` source suite passed **56 tests** across target contracts, source taxonomy, door/window separation, association, v3 derivation, v3.1/v3.2 repairs, resize alignment, pixel preservation, determinism, fixture mapping, model compatibility and review persistence/Skip protection. There were 78 existing FloorTrans NumPy matrix deprecation warnings.

The test invocation is recorded in [provenance.json](provenance.json). This result applies to the inspected local helper implementations. The new 1024 adapter, target bundle and combined checkpoint require the implementation checks in [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md).
