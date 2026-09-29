#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mitunet_cubicasa.dataset import prepare_dataset
from mitunet_cubicasa.utils import save_json, setup_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate local CubiCasa5K data and generate binary wall masks.")
    parser.add_argument("--data-root", default="/home/pmharris/dev/cubicasa5k_data")
    parser.add_argument("--output-dir", default="artifacts/cubicasa_validation")
    parser.add_argument("--cache-dir", default="artifacts/cubicasa5k_wall_cache")
    parser.add_argument("--floortrans-root", default=None)
    parser.add_argument("--subtract-openings", action="store_true")
    parser.add_argument("--preview-count", type=int, default=20)
    parser.add_argument("--allow-invalid-over-1pct", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    logger = setup_logging(output_dir / "run.log")
    prepared = prepare_dataset(
        data_root=args.data_root,
        output_dir=output_dir,
        cache_dir=args.cache_dir,
        floortrans_root=args.floortrans_root,
        subtract_openings=args.subtract_openings,
        preview_count=args.preview_count,
        allow_invalid_over_1pct=args.allow_invalid_over_1pct,
    )
    save_json(prepared.layout, output_dir / "detected_layout.json")
    logger.info("Detected dataset root: %s", prepared.dataset_root)
    for split, stats in prepared.summary["splits"].items():
        logger.info(
            "%s valid=%s invalid=%s wall_prevalence=%.6f empty_masks=%s",
            split,
            stats["valid_samples"],
            stats["invalid_samples"],
            stats["wall_pixel_prevalence"],
            stats["empty_masks"],
        )
    logger.info("Wrote manifests and summary to %s", output_dir)


if __name__ == "__main__":
    main()
