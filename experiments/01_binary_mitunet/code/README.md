# Code snapshot for the binary MitUNet baseline

**This is a reference snapshot. It is not proven to be the code that trained the baseline.**

| Fact | Value |
| --- | --- |
| Baseline training run | 2026-06-25, from a working tree that was not committed |
| This snapshot | commit `459778bd07b1` of the local `mitunet` repository, dated 2026-07-23 |
| Relation | The earliest recorded code state that contains the baseline training code. It is about four weeks later than the run. |

Every file here is byte-identical to the file at that commit. Hashes are in [../provenance.json](../provenance.json).

## What is known about the match

- The model definition matches. A model built from `mitunet_cubicasa/model.py` has the same 954 tensors, with the
  same names and shapes, as the baseline checkpoint. See [../results/code_checkpoint_consistency.json](../results/code_checkpoint_consistency.json).
- The configuration keys do not all match. The run's own configuration uses `input_size` and `augment`; the
  configuration file at this commit uses `image_size` and has no `augment` key. The code changed between the run and the commit.
- The augmentation that trained the baseline is not recorded. The run records `augment: true` only. Experiment 09
  found that the baseline checkpoint regresses when fine-tuned with flips and 90-degree rotations, which
  `mitunet_cubicasa/transforms.py` in this snapshot applies. Do not assume the baseline was trained with them.

## Files

| Path | Purpose |
| --- | --- |
| `mitunet_cubicasa/model.py` | Builds the model: U-Net decoder with SCSE attention on a MiT-B4 encoder, one output channel, raw logits |
| `mitunet_cubicasa/losses.py` | Asymmetric Tversky loss |
| `mitunet_cubicasa/metrics.py` | IoU, Dice and related pixel metrics |
| `mitunet_cubicasa/dataset.py`, `cubicasa_parser.py`, `ontology.py` | CubiCasa5K reading, wall targets from the SVG annotations, class mapping |
| `mitunet_cubicasa/transforms.py` | Resize or letterbox, augmentation, normalisation |
| `mitunet_cubicasa/engine.py` | Training and evaluation loops, threshold search |
| `mitunet_cubicasa/audit.py`, `observability.py`, `utils.py` | Dataset checks, training plots, helpers |
| `scripts/train_mitunet_cubicasa.py` | Training entry point |
| `scripts/evaluate_mitunet_cubicasa.py`, `predict_mitunet.py`, `validate_cubicasa.py` | Evaluation, prediction, dataset validation |
| `configs/cubicasa5k_mitunet.yaml` | 512 px baseline configuration at this commit |
| `tests/` | Three unit test files for model, metrics and dataset |
| `requirements.txt`, `requirements-cubicasa.txt`, `run_cubicasa_training.sh`, `README_CUBICASA_TRAINING.md` | Environment and run instructions from the source repository |

Not included: `mitunet_cubicasa/hybrid.py`, which belongs to experiment 02. The package `__init__.py` lists it in
`__all__`; the baseline scripts do not import it.

## Drift since this commit

11 of 26 files differ from the current working tree of the source repository: `mitunet_cubicasa/cubicasa_parser.py`, `mitunet_cubicasa/dataset.py`, `mitunet_cubicasa/engine.py`, `mitunet_cubicasa/losses.py`, `mitunet_cubicasa/metrics.py`, `mitunet_cubicasa/model.py`, `mitunet_cubicasa/ontology.py`, `scripts/evaluate_mitunet_cubicasa.py`, `scripts/train_mitunet_cubicasa.py`, `tests/test_dataset.py`, `tests/test_model.py`.
The current tree carries later experiments. It is not published here.

## Licence and origin

The local repository was cloned from <https://github.com/aliasstudio/mitunet>, which is under the MIT licence. Its
licence text is [LICENSE](LICENSE) and its citation file is [CITATION.cff](CITATION.cff). The files under
`mitunet_cubicasa/`, `scripts/`, `configs/` and `tests/` were added to the local clone in commit `459778bd07b1`.
They use `segmentation_models_pytorch` for the network.

## Not included

No dataset, no checkpoint, no cache and no prediction output. CubiCasa5K has its own licence and is not redistributed here.
