from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any


TASK_BINARY_WALL = "binary_wall"
TASK_CUBICASA_MULTICLASS = "cubicasa_multiclass"
IGNORE_INDEX = 255
MASK_SCHEMA_VERSION = "cubicasa-two-head-v1"


@dataclass(frozen=True)
class ClassDef:
    id: int
    name: str


STRUCTURE_CLASSES: tuple[ClassDef, ...] = (
    ClassDef(0, "background"),
    ClassDef(1, "wall"),
)

OPTIONAL_STRUCTURE_CLASSES: tuple[ClassDef, ...] = (
    ClassDef(2, "railing"),
    ClassDef(3, "stairs"),
)

ICON_CLASSES: tuple[ClassDef, ...] = (
    ClassDef(0, "empty"),
    ClassDef(1, "window"),
    ClassDef(2, "door"),
    ClassDef(3, "cabinetry_storage"),
    ClassDef(4, "appliance"),
    ClassDef(5, "toilet_urinal"),
    ClassDef(6, "sink_tap"),
    ClassDef(7, "sauna_bench"),
    ClassDef(8, "fireplace"),
    ClassDef(9, "bathtub_shower_jacuzzi"),
    ClassDef(10, "chimney"),
    ClassDef(11, "other_fixture"),
)

STRUCTURE_SOURCE_TO_TARGET: dict[str, str] = {
    "Wall": "wall",
    "Railing": "railing",
    "Stairs": "stairs",
}

ICON_SOURCE_TO_TARGET: dict[str, str] = {
    "Window": "window",
    "Door": "door",
    "Closet": "cabinetry_storage",
    "ClosetRound": "cabinetry_storage",
    "ClosetTriangle": "cabinetry_storage",
    "CoatCloset": "cabinetry_storage",
    "CoatRack": "cabinetry_storage",
    "CounterTop": "cabinetry_storage",
    "Housing": "cabinetry_storage",
    "BaseCabinet": "cabinetry_storage",
    "BaseCabinetRound": "cabinetry_storage",
    "BaseCabinetTriangle": "cabinetry_storage",
    "WallCabinet": "cabinetry_storage",
    "ElectricalAppliance": "appliance",
    "WoodStove": "appliance",
    "GasStove": "appliance",
    "SaunaStove": "appliance",
    "WashingMachine": "appliance",
    "IntegratedStove": "appliance",
    "Dishwasher": "appliance",
    "GeneralAppliance": "appliance",
    "Refrigerator": "appliance",
    "DoubleRefrigerator": "appliance",
    "TumbleDryer": "appliance",
    "Heater": "appliance",
    "HighHeater": "appliance",
    "SpaceForAppliance": "appliance",
    "SpaceForAppliance2": "appliance",
    "IntegratedStoveSmall": "appliance",
    "Fan": "appliance",
    "Stove": "appliance",
    "GEARound": "appliance",
    "SaunaStoveRound": "appliance",
    "Round": "appliance",
    "Toilet": "toilet_urinal",
    "Urinal": "toilet_urinal",
    "SideSink": "sink_tap",
    "Sink": "sink_tap",
    "RoundSink": "sink_tap",
    "CornerSink": "sink_tap",
    "DoubleSink": "sink_tap",
    "DoubleSinkRight": "sink_tap",
    "WaterTap": "sink_tap",
    "SaunaBench": "sauna_bench",
    "SaunaBenchHigh": "sauna_bench",
    "SaunaBenchLow": "sauna_bench",
    "SaunaBenchMid": "sauna_bench",
    "Fireplace": "fireplace",
    "FireplaceCorner": "fireplace",
    "FireplaceRound": "fireplace",
    "PlaceForFireplace": "fireplace",
    "PlaceForFireplaceCorner": "fireplace",
    "PlaceForFireplaceRound": "fireplace",
    "Bathtub": "bathtub_shower_jacuzzi",
    "BathtubRound": "bathtub_shower_jacuzzi",
    "Shower": "bathtub_shower_jacuzzi",
    "ShowerCab": "bathtub_shower_jacuzzi",
    "ShowerPlatform": "bathtub_shower_jacuzzi",
    "ShowerScreen": "bathtub_shower_jacuzzi",
    "ShowerScreenRoundLeft": "bathtub_shower_jacuzzi",
    "ShowerScreenRoundRight": "bathtub_shower_jacuzzi",
    "Jacuzzi": "bathtub_shower_jacuzzi",
    "Chimney": "chimney",
    "Misc": "other_fixture",
}


def _classes_to_dict(classes: tuple[ClassDef, ...]) -> dict[str, int]:
    return {item.name: item.id for item in classes}


STRUCTURE_NAME_TO_ID = _classes_to_dict(STRUCTURE_CLASSES)
OPTIONAL_STRUCTURE_NAME_TO_ID = _classes_to_dict(OPTIONAL_STRUCTURE_CLASSES)
ICON_NAME_TO_ID = _classes_to_dict(ICON_CLASSES)


def enabled_structure_classes(include_optional: bool = False) -> tuple[ClassDef, ...]:
    if include_optional:
        return STRUCTURE_CLASSES + OPTIONAL_STRUCTURE_CLASSES
    return STRUCTURE_CLASSES


def class_names(classes: tuple[ClassDef, ...]) -> list[str]:
    return [item.name for item in classes]


def id_to_name(classes: tuple[ClassDef, ...]) -> dict[int, str]:
    return {item.id: item.name for item in classes}


def name_to_id(classes: tuple[ClassDef, ...]) -> dict[str, int]:
    return {item.name: item.id for item in classes}


def fixed_furniture_tokens(class_attr: str) -> list[str]:
    parts = class_attr.split()
    if not parts or parts[0] != "FixedFurniture":
        return []
    return parts[1:]


def fixed_furniture_target(tokens: list[str]) -> str:
    if not tokens:
        return "other_fixture"
    if tokens[0] == "ElectricalAppliance":
        return "appliance"
    for token in tokens:
        target = ICON_SOURCE_TO_TARGET.get(token)
        if target is not None:
            return target
    return "other_fixture"


def structure_target_id(raw_name: str, include_optional: bool = False) -> int | None:
    target = STRUCTURE_SOURCE_TO_TARGET.get(raw_name)
    if target is None:
        return None
    classes = enabled_structure_classes(include_optional=include_optional)
    return name_to_id(classes).get(target)


def icon_target_id(raw_name: str, class_attr: str | None = None) -> int | None:
    if raw_name in {"Window", "Door"}:
        return ICON_NAME_TO_ID[ICON_SOURCE_TO_TARGET[raw_name]]
    tokens = fixed_furniture_tokens(class_attr or raw_name)
    if tokens:
        return ICON_NAME_TO_ID[fixed_furniture_target(tokens)]
    target = ICON_SOURCE_TO_TARGET.get(raw_name)
    if target is None:
        return None
    return ICON_NAME_TO_ID[target]


def mapping_payload(include_optional_structure: bool = False) -> dict[str, Any]:
    structure_classes = enabled_structure_classes(include_optional_structure)
    return {
        "mask_schema_version": MASK_SCHEMA_VERSION,
        "ignore_index": IGNORE_INDEX,
        "structure_classes": [{"id": item.id, "name": item.name} for item in structure_classes],
        "icon_classes": [{"id": item.id, "name": item.name} for item in ICON_CLASSES],
        "structure_source_to_target": STRUCTURE_SOURCE_TO_TARGET,
        "icon_source_to_target": ICON_SOURCE_TO_TARGET,
        "notes": {
            "training_targets": ["structure_mask", "icon_mask"],
            "unified_export": "lossy; icons/openings overwrite structural classes for visualization/export only",
            "optional_structure_classes": [item.name for item in OPTIONAL_STRUCTURE_CLASSES],
        },
    }


def mapping_hash(include_optional_structure: bool = False) -> str:
    payload = mapping_payload(include_optional_structure=include_optional_structure)
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def deterministic_palette(classes: tuple[ClassDef, ...]) -> dict[str, list[int]]:
    palette: dict[str, list[int]] = {}
    for item in classes:
        if item.id == 0:
            palette[item.name] = [0, 0, 0]
            continue
        digest = hashlib.sha256(f"{MASK_SCHEMA_VERSION}:{item.id}:{item.name}".encode("utf-8")).digest()
        palette[item.name] = [
            int(48 + digest[0] % 176),
            int(48 + digest[1] % 176),
            int(48 + digest[2] % 176),
        ]
    return palette


def validate_indexed_mask_values(mask_values: set[int], num_classes: int, ignore_index: int = IGNORE_INDEX) -> None:
    invalid = sorted(v for v in mask_values if v != ignore_index and (v < 0 or v >= num_classes))
    if invalid:
        raise ValueError(f"Mask contains class IDs outside configured range 0..{num_classes - 1}: {invalid}")
