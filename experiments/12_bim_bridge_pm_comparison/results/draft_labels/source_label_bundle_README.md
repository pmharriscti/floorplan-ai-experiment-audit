# Synthetic floor-plan structure labels — draft v0.1

**Status: DRAFT ANNOTATIONS, NOT INDEPENDENTLY VERIFIED GROUND TRUTH.**

This bundle supplies usable reference-label candidates for the generated floor-plan PNGs in this conversation. The annotations were inferred from the raster drawings; no original CAD/SVG scene geometry or human-approved answer key was available. All 12 images remain unreviewed by an independent human. Geometry and class assignment can still be wrong even where no ignore region is marked.

The scope is **walls and openings**. This is not a complete fixture, room, 13-class, or fire-sprinkler annotation dataset. No model inference or model-accuracy evaluation has been run as part of this delivery.

## Start here

1. Open `review/index.html` in a browser after extracting the whole folder. It works offline. Review the original, colored overlay, and label visualization at native size. Orange regions are explicitly unresolved and excluded from metric pixels.
2. Correct labels in `annotation_spec.json` as needed. The `wall_guides` rectangles constrain the wall-pixel extractor. Door/window `polygon` points define their opening footprints. `wall_additions` and `wall_exclusions` accept polygons for explicit corrections. `ignore_regions` are rectangles.
3. After edits, run the commands below to regenerate masks and refresh the review page. Record actual human review in the page, then export `review_decisions.json`. The evaluator checks review identities, version hashes, source hashes, and label hashes rather than silently accepting stale reviews.

```bash
python -m pip install -r requirements.txt
python scripts/regenerate.py
python scripts/check_dataset.py
python scripts/build_review.py
```

Editing exported SVGs or masks alone does not update the specification. Put corrections into the specification and regenerate, or integrate the provided mask files into your own versioned annotation workflow. Do not simply approve an image because the colored overlay looks plausible at thumbnail size.

## Which images are included?

There are 12 distinct individual plans in the conversation, not 10. The collage and the duplicate `imagegen.png` were excluded.

`manifests/assumed_10.txt` is an explicit selection assumption: the nine commercial plans plus the apartment. `commercial_9.txt` contains only commercial plans. `all_12.txt` also includes the two single-family plans. These are **selection lists, not train/validation/test splits**.

| ID | Plan | Draft door openings | Draft window openings | Assumed 10 |
|---|---|---:|---:|---|
| fp01_office | Office suite | 6 | 6 | Yes |
| fp02_retail | Retail store | 3 | 3 | Yes |
| fp03_restaurant | Restaurant | 3 | 11 | Yes |
| fp04_warehouse | Warehouse / distribution center | 15 | 14 | Yes |
| fp05_hotel | Hotel guest-room floor | 27 | 16 | Yes |
| fp06_clinic | Medical clinic | 17 | 10 | Yes |
| fp07_school | School classroom wing | 14 | 16 | Yes |
| fp08_grocery | Grocery store | 16 | 18 | Yes |
| fp09_manufacturing | Light manufacturing plant | 14 | 20 | Yes |
| fp10_apartment | Two-bedroom apartment | 7 | 6 | Yes |
| fp11_house_ground | Single-family home, first floor | 7 | 9 | Extra |
| fp12_house_upper | Single-family home, second floor | 10 | 8 | Extra |
| **Total** | **12 images** | **139** | **137** | **10 selected** |

These are counts of annotations, not independently verified counts of actual architectural elements. Some candidates intersect ignored regions. The ten-image subset contains 122 draft door openings and 120 draft window openings.

## Label definitions and encoding

Every source image and raster label is **1254 × 1254 pixels**. Originals were copied byte-for-byte. No resizing, letterboxing, geometric augmentation, or coordinate remapping was applied.

Coordinates have origin at the top left; x increases rightward and y downward. Rectangles are half-open `[x0, y0, x1, y1]` pixel-edge coordinates. Opening polygons are rasterized by pixel-center containment. Do not treat printed room dimensions or scale bars as verified physical dimensions.

### Separate binary targets

All binary PNGs use **uint8 values 0 and 1**, not 0 and 255. They will look almost black in a normal image viewer. Use `overlays/` or `visualizations/` for visual inspection. Do not divide these target values by 255.

| Folder under `masks/` | Positive pixels mean |
|---|---|
| `visible_wall/` | Draft visible opaque wall footprint. Door/window cuts are subtracted. |
| `structural_wall/` | Visible wall plus the annotated opening footprints, as a continuous 2D support convention. |
| `door_opening/` | Jamb-to-jamb opening through the wall band; not the full door leaf or swing symbol. |
| `window_opening/` | Window opening through the wall band; not all glazing, frame, or nearby symbol strokes. |
| `valid/` | Pixel may be used in a draft/reviewed experiment under the chosen label contract. Zero means explicitly ignored. |

For the raw binary targets:

```text
visible_wall AND (door_opening OR window_opening) = empty
structural_wall = visible_wall OR door_opening OR window_opening
```

The word “structural” describes this dataset's **2D target convention**, not load-bearing classification and not solid material filling a 3D doorway. Mask unions do not establish an IFC-ready wall graph. No host-wall IDs or individual wall-entity instances were assigned.

`valid=1` does not mean an independent reviewer confirmed that pixel. It means no explicit unresolved region was marked there. All drafts still require review.

### Four-class structure mask

`masks/semantic_structure4/<id>.png` is a single-channel uint8 target:

| ID | Meaning |
|---:|---|
| 0 | Non-structural: rooms, text, furniture, fixtures, floor finishes, exterior background, and other unannotated content |
| 1 | Visible wall |
| 2 | Window opening |
| 3 | Door opening |
| 255 | Ignore |

Class 0 is **not equivalent to your full 13-class background**. Fixtures were not labeled. Do not feed this mask into the existing 13-class model as a fully annotated target.

`masks/partial13_structure_only/` is an optional partial-label representation: only structure-positive IDs 1/2/3 are retained and **everything else is 255**, including unannotated fixtures. It is not a complete 13-class answer key and provides no full background coverage. Verify both numeric IDs and opening/wall semantics against your exact training configuration before any use.

### Instance and vector representations

`instances/door_opening/` and `instances/window_opening/` are **uint16** instance maps. Zero is none; positive IDs are local to the image and class. Each double-door assembly is normally one architectural opening, not two leaf instances. Multi-panel glazing may be grouped as one opening; ambiguous movable/fixed distinctions require review.

`annotations/openings_coco.json` contains draft door/window polygons, boxes, areas and IDs. Categories are 2=window_opening and 3=door_opening. Extra `attributes` record review status and ignored-region overlap. A generic COCO loader may not honor those extra attributes or pixel-level ignore masks; explicitly apply the supplied valid masks or exclude unresolved instances. No wall-instance ground truth is claimed.

Per-image `annotations/<id>.json` includes exact uncompressed, column-major binary RLE for visible/structural walls, opening data, ignore regions and review notes. Wall connected components are **not** individual architectural walls.

`vectors/<id>.svg` contains colored annotation geometry with even-odd wall contours and separate door/window/ignore groups. These are traced label overlays, not recovered source drawings. The PNG/RLE masks are authoritative; simplified SVG contours can differ at pixel boundaries and do not provide verified metric CAD geometry.

## How these drafts were produced

The assistant visually inspected all source plans, specified wall-guide bands and opening polygons, and used a fixed non-ML raster procedure to extract dark wall regions inside those guides. The procedure uses grayscale threshold `<155`, a 5×5 morphological opening to suppress thin symbol/fixture strokes, removal of components smaller than 9 pixels, and filling of enclosed holes of at most 16 pixels. Explicit opening masks are then removed from visible walls and added to structural support.

This is an **assistant-guided raster annotation draft**, not output from your segmentation model and not a source-geometry-derived ground truth. It can miss very thin/light walls, retain dark fixtures, or place a jamb incorrectly. Wall thickness, window extents, sliding/overhead door interpretations and ambiguous partitions deserve close review. No calibrated confidence scores were invented.

Examples of explicit unresolved areas include warehouse docks, hotel elevator doors, grocery-store loading/cooler/glazed boundaries, apartment balcony glazing and some closet/pass-through connections. Sample-specific notes are in the manifest and review page. Missing door symbols are not automatically “repaired” into invented doors.

## Run a model experiment

First choose whether your checkpoint predicts **visible wall** or **structural support**. The wrong target semantics can make a correct prediction look wrong. Freeze the checkpoint and preprocessing for a useful comparison. Keep these images out of training while using them for evaluation.

Your predictions must be mapped back to the original 1254×1254 coordinates, including reversal of any letterboxing/cropping. Prediction PNG filenames must match the IDs, e.g. `fp01_office.png`. The included evaluator will reject mismatched shapes rather than silently resize them.

For initial debugging against the unreviewed drafts:

```bash
python scripts/evaluate.py \
  --pred-dir /path/to/native_resolution_predictions \
  --target structural_wall \
  --subset assumed_10 \
  --allow-draft-labels \
  --output draft_wall_agreement.json
```

Binary predictions must contain 0/1. Four-class predictions must contain 0/1/2/3. Colored overlays, probabilities and 0/255 binary predictions are rejected.

After actual human review, replace `--allow-draft-labels` with:

```bash
--review-decisions review_decisions.json
```

The script computes per-image and aggregated per-class IoU/Dice only on valid pixels. Aggregation sums TP/FP/FN across included images; empty unions produce null rather than an artificial perfect score. The draft mode marks results `DRAFT_ANNOTATION_AGREEMENT_ONLY`. It does not label them verified model accuracy.

Minimal binary-label loading:

```python
from pathlib import Path
import numpy as np
from PIL import Image

root = Path("synthetic_floorplan_labels_v0_1")
sample_id = "fp01_office"
image = np.asarray(Image.open(root / "images" / f"{sample_id}.png").convert("RGB"))
target = np.asarray(Image.open(root / "masks/structural_wall" / f"{sample_id}.png"), dtype=np.uint8)
valid = np.asarray(Image.open(root / "masks/valid" / f"{sample_id}.png"), dtype=np.uint8).astype(bool)
assert image.shape[:2] == target.shape == valid.shape
assert set(np.unique(target)) <= {0, 1}
# Apply your normal input preprocessing. Transform targets/valid masks identically
# with nearest-neighbor sampling, and exclude valid==False pixels from loss/metrics.
```

## What QA established — and what it did not

`qa_report.json` records shape/dtype/value checks, source/mask hashes, mask-union invariants, door/window non-overlap, instance-ID projection checks, RLE round-trips, subset sizes and COCO ID/count checks. These checks passed for the delivered files. The report also records the runtime package versions.

**Passing these checks proves file consistency, not annotation accuracy or construction validity.** Independent human review remains necessary. This delivery does not include any measured model results.

All plans are synthetic and share a generated drawing style. Agreement on this small set does not establish performance on real sprinkler-company drawings or other independent external data. Printed dimensions can be inconsistent. No real-world scale, ceiling height, hazard classification, pipe network, sprinkler-head placement, hydraulic calculations, code compliance or deployable IFC geometry was established.

## File map

```text
annotation_spec.json                 Editable source annotation specification
README.md                            Definitions, limitations and commands
requirements.txt                     Regeneration/checking dependencies
images/                              Unmodified original PNGs, stable sample IDs
dataset_manifest.json                Source names, hashes, counts, notes and subsets
manifests/                           assumed_10, commercial_9, all_12 ID lists
masks/                               Binary, valid, 4-class and partial-label targets
instances/                           16-bit door/window instance maps
annotations/                         Per-image wall RLE/contours and COCO openings
vectors/                             Traced SVG annotation overlays
visualizations/                      Color masks; not numerical training labels
overlays/                            Labels blended over original images
review_contact_sheet.png             All 12 overlays at a glance
review/index.html                    Offline viewer and human review log exporter
scripts/                             Regeneration, QA, review-page build, evaluation
qa_report.json                       Mechanical QA and environment versions
```
