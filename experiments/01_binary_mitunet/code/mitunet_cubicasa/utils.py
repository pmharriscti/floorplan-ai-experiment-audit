from __future__ import annotations

import csv
import importlib.metadata
import json
import logging
import os
import platform
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch
import yaml


LOGGER_NAME = "mitunet_cubicasa"


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(path: str | Path) -> Path:
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out


def load_yaml(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping in {path}")
    return data


def save_yaml(data: dict[str, Any], path: str | Path) -> None:
    with Path(path).open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def save_json(data: Any, path: str | Path) -> None:
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def write_csv(rows: list[dict[str, Any]], path: str | Path, fieldnames: list[str] | None = None) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def setup_logging(log_path: str | Path | None = None, verbose: bool = True) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    if verbose:
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        logger.addHandler(stream)
    if log_path is not None:
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.propagate = False
    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)


def progress_disabled() -> bool:
    for name in ("MITUNET_DISABLE_PROGRESS", "TQDM_DISABLE"):
        value = os.environ.get(name, "").strip().lower()
        if value in {"1", "true", "yes", "on"}:
            return True
    return False


def seed_everything(seed: int, deterministic: bool = True) -> list[str]:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    notes = []
    if deterministic:
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
        try:
            torch.use_deterministic_algorithms(True, warn_only=True)
        except Exception as exc:  # pragma: no cover - version dependent
            notes.append(f"torch deterministic algorithms unavailable: {exc}")
    notes.append("Some operations in PyTorch/SMP/Albumentations may remain nondeterministic depending on device kernels.")
    return notes


def detect_device(prefer_cuda: bool = True) -> tuple[torch.device, dict[str, Any]]:
    info: dict[str, Any] = {
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "mps_available": hasattr(torch.backends, "mps") and torch.backends.mps.is_available(),
        "selected_device": "cpu",
        "gpu_model": None,
        "gpu_vram_total_bytes": None,
        "gpu_vram_available_bytes": None,
    }
    if prefer_cuda and torch.cuda.is_available():
        device = torch.device("cuda")
        info["selected_device"] = "cuda"
        try:
            idx = torch.cuda.current_device()
            props = torch.cuda.get_device_properties(idx)
            info["gpu_model"] = props.name
            info["gpu_vram_total_bytes"] = props.total_memory
            free, total = torch.cuda.mem_get_info(idx)
            info["gpu_vram_available_bytes"] = free
            info["gpu_vram_total_bytes"] = total
        except Exception as exc:
            info["gpu_probe_error"] = str(exc)
        return device, info
    if info["mps_available"]:
        info["selected_device"] = "mps"
        return torch.device("mps"), info
    return torch.device("cpu"), info


def package_versions(extra: list[str] | None = None) -> dict[str, str | None]:
    names = [
        "torch",
        "torchvision",
        "segmentation-models-pytorch",
        "albumentations",
        "opencv-python-headless",
        "numpy",
        "pandas",
        "Pillow",
        "pyyaml",
        "scikit-image",
        "svgpathtools",
    ]
    if extra:
        names.extend(extra)
    out: dict[str, str | None] = {}
    for name in names:
        try:
            out[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            out[name] = None
    return out


def collect_environment(device_info: dict[str, Any] | None = None) -> dict[str, Any]:
    env = {
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "cwd": os.getcwd(),
        "packages": package_versions(),
    }
    if device_info:
        env["device"] = device_info
    return env


def merge_config(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    for key, value in overrides.items():
        if value is not None:
            merged[key] = value
    return merged
