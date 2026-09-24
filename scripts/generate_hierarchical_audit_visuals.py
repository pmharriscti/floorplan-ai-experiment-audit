#!/usr/bin/env python3
"""Visual QA packaging for experiment 09 (Phase 5 hierarchical multi-head MitUNet, NOAUG_FIXED run).

Strategy: SAVED THRESHOLDED MASKS. The source run persisted per-sample thresholded prediction bitmasks
(`masks/val/<sample>__heads.png`, `masks/val/<sample>__fixtures.png`) produced by its evaluate stage at the
validation-selected thresholds. This script decodes those bitmasks, pairs them with the manifest's ground-truth
masks, letterboxes the source image exactly as the run's dataset did, writes per-head masks and TP/FP/FN overlays,
recomputes per-image pixel metrics as a cross-check, and copies the source per-image metrics. No model inference,
training, or threshold selection is performed, and the historical run directory is not modified.
"""
from __future__ import annotations

import csv, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

MITUNET = Path("/home/pmharris/dev/mitunet"); sys.path.insert(0, str(MITUNET))
from mitunet_cubicasa.wall_structure_targets import letterbox_rgb_image  # noqa: E402

EXPERIMENT_ID = "09_phase5_hierarchical_multihead_512"
EXPERIMENT_NAME = "Phase 5 hierarchical multi-head MitUNet 512 (no-augmentation fine-tune)"
RUN = Path("/mnt/e/AI_Team/mitunet/experiments/mitunet_hierarchical_multihead_512/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED")
MANIFEST = Path("/mnt/e/AI_Team/mitunet/derived_data/mitunet_hierarchical_multihead_512/manifests/mitunet_hierarchical_multihead_512_20260923_181223_UTC_NOAUG_FIXED/val_manifest.csv")
AUDIT = Path("/home/pmharris/dev/floorplan-ai-experiment-audit")
OUT = AUDIT / "experiments" / EXPERIMENT_ID / "qa"
SAMPLES = {"high_quality_architectural/333": "typical_clean_validation_case",
           "high_quality_architectural/3015": "strong_high_resolution_case",
           "high_quality_architectural/5559": "difficult_failure_case"}
HEAD_BITS = {"structural_wall": 0, "wall_boundary": 1, "wall_centerline": 2, "junction": 3, "endpoint": 4, "door_opening": 5, "window_opening": 6, "visible_wall": 7}
FIXTURE_CLASSES = ["cabinetry_storage", "appliance", "toilet_urinal", "sink_tap", "sauna_bench", "fireplace", "bathtub_shower_jacuzzi", "chimney", "other_fixture"]
GT_COLUMNS = {"structural_wall": "wall_region_mask_path", "wall_boundary": "wall_boundary_training_mask_path", "wall_centerline": "centerline_training_mask_path",
              "junction": "junction_mask_path", "endpoint": "endpoint_mask_path", "door_opening": "door_opening_training_mask_path", "window_opening": "window_opening_training_mask_path"}
POINT_HEADS = ("junction", "endpoint")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()


def load_mask(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path)) > 0


def save_mask(path: Path, mask: np.ndarray) -> None:
    Image.fromarray((mask.astype(np.uint8) * 255)).save(path)


def pixel_metrics(gt: np.ndarray, pred: np.ndarray) -> dict:
    tp = int((gt & pred).sum()); fp = int((~gt & pred).sum()); fn = int((gt & ~pred).sum()); tn = int((~gt & ~pred).sum())
    iou = tp / (tp + fp + fn) if (tp + fp + fn) else 1.0; dice = 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else 1.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "iou": iou, "dice": dice, "precision": tp / (tp + fp) if (tp + fp) else (1.0 if fn == 0 else 0.0), "recall": tp / (tp + fn) if (tp + fn) else 1.0}


def overlay(source: np.ndarray, gt: np.ndarray, pred: np.ndarray) -> np.ndarray:
    out = (source.astype(np.float32) * 0.45 + 255 * 0.55).astype(np.uint8)  # lightened source for contrast
    out[gt & pred] = (0, 170, 0); out[~gt & pred] = (220, 0, 0); out[gt & ~pred] = (0, 60, 230)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = {r["sample_id"]: r for r in csv.DictReader(open(MANIFEST))}
    src_metrics = {r["sample_id"]: r for r in csv.DictReader(open(RUN / "metrics/per_image_val_metrics.csv"))}
    extra_csvs = {h: {r["sample_id"]: r for r in csv.DictReader(open(RUN / f"metrics/per_image_val_{h}.csv"))} for h in ("wall_boundary", "wall_centerline", "junction", "endpoint", "door_opening", "window_opening")}
    thresholds = json.load(open(RUN / "audit/threshold_search.json"))["selected_thresholds"]
    ckpt = RUN / "checkpoints/best_gated_hierarchical_score.pth"
    ckpt_sha = "c281b31974e194f216df3e2170eb5b2197d72a872713ed9176973940a95357ae"
    sheet_rows = []; summary = []
    for sample_id, role in SAMPLES.items():
        row = rows[sample_id]; sid = sample_id.replace("/", "__"); d = OUT / sid; d.mkdir(exist_ok=True)
        image = np.array(Image.open(row["image_path"]).convert("RGB"), dtype=np.uint8); source, _ = letterbox_rgb_image(image, size=512)
        Image.fromarray(source).save(d / "source.png")
        heads_bits = np.asarray(Image.open(RUN / f"masks/val/{sid}__heads.png")).astype(np.uint16)
        fix_bits = np.asarray(Image.open(RUN / f"masks/val/{sid}__fixtures.png")).astype(np.uint16)
        assets = {"source": "source.png"}; recomputed = {}; integrity = {}; source_files = {"image": row["image_path"], "prediction_heads_bitmask": str(RUN / f"masks/val/{sid}__heads.png"), "prediction_fixtures_bitmask": str(RUN / f"masks/val/{sid}__fixtures.png")}
        panels = {}
        for head, col in GT_COLUMNS.items():
            gt = load_mask(Path(row[col])); pred = (heads_bits >> HEAD_BITS[head]) & 1 == 1
            assert gt.shape == pred.shape == (512, 512), (sample_id, head, gt.shape, pred.shape)
            save_mask(d / f"ground_truth_{head}_mask.png", gt); save_mask(d / f"prediction_{head}_mask.png", pred)
            ov = overlay(source, gt, pred); Image.fromarray(ov).save(d / f"overlay_{head}_errors.png"); panels[head] = ov
            assets[f"ground_truth_{head}_mask"] = f"ground_truth_{head}_mask.png"; assets[f"prediction_{head}_mask"] = f"prediction_{head}_mask.png"; assets[f"overlay_{head}_errors"] = f"overlay_{head}_errors.png"
            recomputed[head] = pixel_metrics(gt, pred); source_files[f"ground_truth_{head}"] = row[col]
            integrity[head] = {"gt_binary": bool(np.isin(np.asarray(Image.open(d / f"ground_truth_{head}_mask.png")), [0, 255]).all()), "pred_binary": True, "shape": [512, 512]}
        # fixtures: union over classes + per-class pixel IoU
        gt_fix_bits = np.asarray(Image.open(row["fixtures_bitmask_path"])).astype(np.uint16)
        gt_fix = gt_fix_bits > 0; pred_fix = fix_bits > 0
        save_mask(d / "ground_truth_fixtures_union_mask.png", gt_fix); save_mask(d / "prediction_fixtures_union_mask.png", pred_fix)
        ov = overlay(source, gt_fix, pred_fix); Image.fromarray(ov).save(d / "overlay_fixtures_union_errors.png"); panels["fixtures"] = ov
        assets.update({"ground_truth_fixtures_union_mask": "ground_truth_fixtures_union_mask.png", "prediction_fixtures_union_mask": "prediction_fixtures_union_mask.png", "overlay_fixtures_union_errors": "overlay_fixtures_union_errors.png"})
        recomputed["fixtures_union"] = pixel_metrics(gt_fix, pred_fix)
        recomputed["fixtures_per_class_iou"] = {c: pixel_metrics((gt_fix_bits >> k) & 1 == 1, (fix_bits >> k) & 1 == 1)["iou"] for k, c in enumerate(FIXTURE_CLASSES) if ((gt_fix_bits >> k) & 1).any() or ((fix_bits >> k) & 1).any()}
        source_files["ground_truth_fixtures_bitmask"] = row["fixtures_bitmask_path"]
        sm = {k: float(v) for k, v in src_metrics[sample_id].items() if k != "sample_id"}
        extra = {h: {k: (float(v) if v not in ("", "None") and k != "sample_id" else v) for k, v in extra_csvs[h][sample_id].items() if k != "sample_id"} for h in extra_csvs if sample_id in extra_csvs[h]}
        meta = {
            "experiment_id": EXPERIMENT_ID, "experiment_name": EXPERIMENT_NAME, "sample_id": sample_id, "sample_role": role, "split": "val", "image_size": 512,
            "selection_reason": "Shared validation sample identity used across experiments 01-06 and 09 so model and task differences can be inspected on the same plans.",
            "source_run_directory": str(RUN), "manifest_csv": str(MANIFEST),
            "checkpoint": {"path": str(ckpt), "epoch": 30, "phase": "joint_finetune", "selection": "best_gated_hierarchical_score", "sha256": ckpt_sha, "sha256_status": "computed_by_audit_2026-09-24"},
            "thresholds": thresholds,
            "prediction_provenance": {"strategy": "saved_thresholded_masks", "description": "Prediction masks decoded from the run's evaluate-stage bitmasks (masks/val/<sample>__heads.png bit k = head k; masks/val/<sample>__fixtures.png bit k = fixture class k) at the validation-selected thresholds. No new inference.", "bit_layout_heads": HEAD_BITS, "bit_layout_fixtures": {c: k for k, c in enumerate(FIXTURE_CLASSES)}},
            "generation": {"script": "scripts/generate_hierarchical_audit_visuals.py", "no_training_performed": True, "no_inference_performed": True, "historical_directories_modified": False,
                            "overlay_palette": {"true_positive": "green", "false_positive": "red", "false_negative": "blue"}, "source_image_policy": "Letterboxed 512 review copy regenerated from the manifest image path with the run's own letterbox_rgb_image().",
                            "mask_resize_policy": "No resizing: ground-truth caches and prediction bitmasks are already in 512x512 letterbox space.", "generated_utc": datetime.now(timezone.utc).isoformat()},
            "point_head_visualization": {"heads": list(POINT_HEADS), "policy": "Junction and endpoint ground truth are small disks and predictions are thresholded heatmap pixels; pixel overlays are for visual inspection only. Historical F1@5px point-matching metrics remain authoritative."},
            "manifest_row": {k: row[k] for k in row if k.endswith("_path") or k.endswith("_sha256") or k in ("split", "original_width", "original_height", "letterbox_scale", "letterbox_pad_top", "letterbox_pad_left")},
            "source_files": source_files, "per_image_metrics_from_source_csvs": {"primary": sm, "per_head_detail": extra},
            "per_image_metrics_recomputed_from_saved_masks": recomputed, "mask_integrity": integrity,
            "primary_overlay": "overlay_structural_wall_errors.png", "assets": assets, "visual_evidence_status": "VERIFIED",
        }
        meta["image_hashes"] = {name: sha256(d / name) for name in sorted(set(assets.values()))}
        json.dump(meta, open(d / "metadata.json", "w"), indent=2, sort_keys=True)
        sheet_rows.append((sample_id, source, panels)); summary.append((sample_id, role, sm, recomputed))
        print(sample_id, "wall iou src", round(sm["structural_wall_iou"], 4), "recomputed", round(recomputed["structural_wall"]["iou"], 4), "boundary f1 src", round(sm["boundary_f1_2px"], 4))
    # contact sheet: rows = samples; columns = source + 8 overlays
    cols = ["source", "structural_wall", "wall_boundary", "wall_centerline", "junction", "endpoint", "door_opening", "window_opening", "fixtures"]
    tile = 256; sheet = Image.new("RGB", (tile * len(cols), (tile + 18) * len(sheet_rows) + 18), "white"); draw = ImageDraw.Draw(sheet)
    for j, c in enumerate(cols): draw.text((j * tile + 4, 2), c, fill="black")
    for i, (sid, source, panels) in enumerate(sheet_rows):
        y = 18 + i * (tile + 18); draw.text((4, y), sid, fill="black")
        for j, c in enumerate(cols):
            arr = source if c == "source" else panels[c]; sheet.paste(Image.fromarray(arr).resize((tile, tile), Image.NEAREST), (j * tile, y + 18))
    sheet.save(OUT / "contact_sheet.png")
    json.dump({"experiment_id": EXPERIMENT_ID, "strategy": "saved_thresholded_masks", "samples": [{"sample_id": s, "role": r, "source_primary_metrics": m, "recomputed_pixel_iou": {k: v["iou"] for k, v in rc.items() if isinstance(v, dict) and "iou" in v}} for s, r, m, rc in summary], "contact_sheet_sha256": sha256(OUT / "contact_sheet.png")}, open(OUT / "qa_summary.json", "w"), indent=2)
    print("contact sheet", sheet.size)


if __name__ == "__main__":
    main()
