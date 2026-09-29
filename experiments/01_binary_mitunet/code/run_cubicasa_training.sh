#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-.venv/bin/python}"
DATA_ROOT="${DATA_ROOT:-/home/pmharris/dev/cubicasa5k_data}"
CONFIG="${CONFIG:-configs/cubicasa5k_mitunet.yaml}"

"${PYTHON_BIN}" scripts/validate_cubicasa.py \
  --data-root "${DATA_ROOT}" \
  --output-dir artifacts/cubicasa_validation

"${PYTHON_BIN}" scripts/train_mitunet_cubicasa.py \
  --data-root "${DATA_ROOT}" \
  --config "${CONFIG}"
