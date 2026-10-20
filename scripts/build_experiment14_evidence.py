#!/usr/bin/env python3
"""Snapshot inspected source identities and parent facts for the experiment-14 proposal."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ENTRY = REPO / "experiments/14_mitunet_1024_hierarchical_phase3a2"
MITUNET = Path("/home/pmharris/dev/mitunet")
MULTIHEAD = Path("/home/pmharris/dev/mitunet_multihead")
MATCHED = Path("/home/pmharris/dev/mitunet_phase3a2_512")
PHASE3A2 = Path("/mnt/e/AI_Team/mitunet/phase3a2_opening_axis_repair/experiments/mitunet_phase3a2_opening_axis_repair_20260826_142837_UTC")
CONTRACTS = (
    "target_contract_v1.yaml",
    "candidate_target_mapping_v3.yaml",
    "opening_derivation_v3.yaml",
    "fixture_target_mapping_v2.yaml",
    "source_class_taxonomy_v1.yaml",
)
SOURCE_FILES = {
    MITUNET: (
        "mitunet_cubicasa/hierarchical_model.py",
        "mitunet_cubicasa/hierarchical_dataset.py",
        "mitunet_cubicasa/hierarchical_targets.py",
        "mitunet_cubicasa/hierarchical_evaluation.py",
        "mitunet_cubicasa/hierarchical_losses.py",
        "mitunet_cubicasa/hierarchical_label_validation.py",
        "mitunet_cubicasa/cubicasa_parser.py",
        "mitunet_cubicasa/ontology.py",
        "mitunet_cubicasa/transforms.py",
        "mitunet_cubicasa/wall_structure_targets.py",
        "mitunet_cubicasa/wall_structure_phase2_targets.py",
        "scripts/run_hierarchical_multihead_experiment.py",
        "scripts/run_phase3a1_opening_rule_repair.py",
        "scripts/run_phase3a2_opening_axis_repair.py",
        "scripts/audit_run_labels_to_mlflow.py",
        "scripts/gradio_phase3a_target_review.py",
        "configs/experiments/mitunet_hierarchical_multihead_512_noaug.yaml",
        "configs/experiments/mitunet_phase1_wall_region_centerline_junctions.yaml",
        "configs/experiments/mitunet_phase2_wall_boundary_door_openings.yaml",
        *(f"configs/targets/{name}" for name in CONTRACTS),
        *(f"mitunet_cubicasa/target_integrity/{name}.py" for name in (
            "contracts", "source_mapping", "source_taxonomy", "source_class_evidence",
            "opening_derivation_v3", "opening_association", "derive_walls", "derive_topology",
            "derive_fixtures", "structural_wall_repair", "transforms", "geometry",
            "validate_pixel_preservation", "validate_mechanical", "validate_semantic",
            "validate_model_compatibility", "gold_freeze", "gold_validation", "review_adjudication",
        )),
        *(f"mitunet_cubicasa/phase3a_review/{name}.py" for name in (
            "manifests", "filtering", "images", "persistence", "constants", "metrics",
        )),
        *(f"tests/{name}.py" for name in (
            "test_target_contract", "test_source_class_taxonomy", "test_door_symbol_opening_separation",
            "test_window_symbol_opening_separation", "test_opening_wall_association",
            "test_opening_derivation_v3", "test_phase3a1_opening_rule_repairs",
            "test_phase3a2_opening_axis_repair", "test_target_resize_alignment", "test_pixel_preservation",
            "test_target_determinism", "test_fixture_target_derivation", "test_model_target_compatibility",
            "test_phase3a_review_core", "test_phase3a_review_skip_guard",
        )),
    ),
    MULTIHEAD: (
        "README.md",
        *(f"mitunet_multihead/{name}.py" for name in (
            "svg_inspection", "wall_extraction", "symbol_extraction", "opening_cuts", "final_geometries",
            "rasterize_masks", "validation/label_validation", "data/manifest_builder",
        )),
    ),
    MATCHED: ("phase3a2_512/constants.py", "phase3a2_512/resize.py", "scripts/build_matched_targets.py"),
}


def identity(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path), "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    source_root = ENTRY / "source_provenance"
    copies = []
    for name in CONTRACTS:
        source = MITUNET / "configs/targets" / name
        dest = source_root / "contracts" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        copies.append({"source": str(source), "copy": str(dest.relative_to(ENTRY)), **identity(source)})

    scope_source = PHASE3A2 / "review/candidate_v3_2_family_a_re_review_manifest.csv"
    with scope_source.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    keys = ("sample_id", "source_instance_id", "target_name", "split")
    scope = [{key: row[key] for key in keys} for row in rows if row["repair_family"] == "A"]
    if len(scope) != 10 or len({row["sample_id"] for row in scope}) != 8:
        raise ValueError("The source repair scope changed; review the proposal before refreshing it.")
    write_json(source_root / "phase3a2_repair_scope.json", {
        "kind": "historical_explicit_repair_scope",
        "source": identity(scope_source),
        "instance_count": len(scope),
        "plan_count": len({row["sample_id"] for row in scope}),
        "door_tangent_normal_repair_instances": scope,
        "note": "Scope identity only; no reviewer decisions or notes are copied.",
    })

    entries = []
    for workspace, files in SOURCE_FILES.items():
        for relative in files:
            entries.append({"workspace": str(workspace), "relative_path": relative, **identity(workspace / relative)})
    audit_sources = []
    parent_facts = {}
    for slug in (
        "01_binary_mitunet", "06_binary_mitunet_1024", "09_phase5_hierarchical_multihead_512",
        "10_phase3a2_door_opening_v31_vs_v32_512", "13_phase3a_human_review_tool",
    ):
        folder = REPO / "experiments" / slug
        for name in ("config.yaml", "metrics.json", "provenance.json"):
            audit_sources.append({"relative_path": str((folder / name).relative_to(REPO)), **identity(folder / name)})
        metrics = json.loads((folder / "metrics.json").read_text())
        facts = {"source": str((folder / "metrics.json").relative_to(REPO)), "evidence_kind": "parent_only"}
        if slug.startswith(("01_", "06_")):
            facts.update({"primary_metrics": metrics["primary_metrics"], "test_at_selected_threshold": metrics["test_at_selected_threshold"]})
            if "validation_at_selected_threshold" in metrics:
                facts["validation_at_selected_threshold"] = metrics["validation_at_selected_threshold"]
        elif slug.startswith("09_"):
            facts.update({"primary_metrics": metrics["primary_metrics"], "wall_protection_gate": metrics["wall_protection_gate"]})
        elif slug.startswith("13_"):
            facts["phase3a2_geometry_audit"] = metrics["phase3a2_geometry_audit"]
        else:
            facts["reference"] = "Scoped label geometry and paired model evidence documented in the source entry; no combined-model result."
        parent_facts[slug] = facts
    write_json(ENTRY / "results/parent_evidence.json", {
        "kind": "parent_results_only",
        "experiment_14_measured_results": None,
        "parents": parent_facts,
    })
    write_json(source_root / "source_inventory.json", {
        "inspection_date": "2026-10-20",
        "purpose": "Evidence identity for the experiment-14 proposal; scientific sources are read-only.",
        "source_files": entries,
        "copied_contracts": copies,
        "parent_audit_sources": audit_sources,
        "refresh_command": "python3 scripts/build_experiment14_evidence.py",
    })
    print(f"Inventoried {len(entries)} source files, {len(copies)} contracts and {len(scope)} repair instances.")


if __name__ == "__main__":
    main()
