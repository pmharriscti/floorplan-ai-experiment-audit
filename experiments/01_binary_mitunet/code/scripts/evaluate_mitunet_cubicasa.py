#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import torch
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitunet_cubicasa.dataset import CubiCasaMultiClassDataset, CubiCasaWallDataset, prepare_dataset
from mitunet_cubicasa.engine import evaluate_model, evaluate_model_multiclass, save_evaluation_outputs, save_multiclass_evaluation_outputs
from mitunet_cubicasa.model import load_model_from_checkpoint
from mitunet_cubicasa.ontology import TASK_CUBICASA_MULTICLASS
from mitunet_cubicasa.utils import collect_environment, detect_device, save_json, setup_logging, timestamp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a MitUNet CubiCasa5K checkpoint.")
    parser.add_argument("--data-root", default="/home/pmharris/dev/cubicasa5k_data")
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--split", choices=["train", "val", "test"], default="test")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--cache-dir", default="artifacts/cubicasa5k_wall_cache")
    parser.add_argument("--floortrans-root", default=None)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--also-threshold-05", action="store_true")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    checkpoint_path = Path(args.checkpoint)
    output_dir = Path(args.output_dir) if args.output_dir else Path("experiments/cubicasa5k_mitunet_evaluations") / timestamp()
    output_dir.mkdir(parents=True, exist_ok=True)
    logger = setup_logging(output_dir / "run.log")
    device, device_info = detect_device()
    environment = collect_environment(device_info)
    save_json(environment, output_dir / "environment.json")

    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    loaded = load_model_from_checkpoint(checkpoint, map_location=device)
    model = loaded.model.eval()
    preprocessing = checkpoint.get("preprocessing", {})
    input_size = int(preprocessing.get("image_size", preprocessing.get("input_size", 512)))
    resize_mode = preprocessing.get("resize_mode", "letterbox")
    task_mode = checkpoint.get("task_mode") or checkpoint.get("architecture", {}).get("task_mode")
    include_optional_structure = bool(checkpoint.get("architecture", {}).get("include_optional_structure", False))
    if task_mode == TASK_CUBICASA_MULTICLASS:
        prepared = prepare_dataset(
            data_root=args.data_root,
            output_dir=output_dir,
            cache_dir=args.cache_dir,
            floortrans_root=args.floortrans_root,
            preview_count=0,
            task_mode=TASK_CUBICASA_MULTICLASS,
            include_optional_structure=include_optional_structure,
        )
        ds = CubiCasaMultiClassDataset(
            prepared.manifest_paths[args.split],
            args.split,
            image_size=input_size,
            resize_mode=resize_mode,
            augment=False,
            limit=args.limit,
            include_optional_structure=include_optional_structure,
        )
        loader = DataLoader(
            ds,
            batch_size=args.batch_size,
            shuffle=False,
            num_workers=args.num_workers,
            pin_memory=device.type == "cuda",
        )
        results = evaluate_model_multiclass(
            model,
            loader,
            device,
            amp_enabled=device.type == "cuda",
            overlay_dir=output_dir / f"{args.split}_prediction_panels",
            max_overlays=20,
            include_optional_structure=include_optional_structure,
        )
        save_multiclass_evaluation_outputs(results, output_dir, args.split)
        save_json(
            {
                "checkpoint": str(checkpoint_path),
                "split": args.split,
                "task_mode": TASK_CUBICASA_MULTICLASS,
                "metrics": results,
            },
            output_dir / "metrics.json",
        )
        logger.info("multiclass evaluation complete: %s", output_dir)
        return
    subtract_openings = bool(preprocessing.get("subtract_openings", False))
    threshold = float(args.threshold if args.threshold is not None else checkpoint.get("threshold", 0.5))
    thresholds = sorted(set([0.5, threshold])) if args.also_threshold_05 else [threshold]

    prepared = prepare_dataset(
        data_root=args.data_root,
        output_dir=output_dir,
        cache_dir=args.cache_dir,
        floortrans_root=args.floortrans_root,
        subtract_openings=subtract_openings,
        preview_count=0,
    )
    ds = CubiCasaWallDataset(
        prepared.manifest_paths[args.split],
        args.split,
        image_size=input_size,
        resize_mode=resize_mode,
        augment=False,
        limit=args.limit,
    )
    loader = DataLoader(
        ds,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=device.type == "cuda",
    )
    amp_enabled = device.type == "cuda"
    results = evaluate_model(
        model,
        loader,
        device,
        thresholds=thresholds,
        amp_enabled=amp_enabled,
        overlay_dir=output_dir / f"{args.split}_prediction_overlays",
        overlay_threshold=threshold,
        max_overlays=20,
    )
    save_evaluation_outputs(results, output_dir, args.split)
    save_json(
        {
            "checkpoint": str(checkpoint_path),
            "split": args.split,
            "thresholds": thresholds,
            "metrics": {f"{t:.2f}": {k: v for k, v in r.items() if k != "per_image"} for t, r in results.items()},
        },
        output_dir / "metrics.json",
    )
    logger.info("evaluation complete: %s", output_dir)


if __name__ == "__main__":
    main()
