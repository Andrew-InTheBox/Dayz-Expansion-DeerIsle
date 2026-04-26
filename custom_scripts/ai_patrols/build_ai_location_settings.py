#!/usr/bin/env python3
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOCATIONS_INPUT = ROOT / "docs" / "ai-locations-input.txt"
NO_GO_INPUT = ROOT / "docs" / "ai-locations-no-go-inputs.txt"
SETTINGS_PATH = ROOT / "mpmissions" / "Expansion.deerisle" / "expansion" / "settings" / "AILocationSettings.json"

DEFAULT_NO_GO_HEIGHT = 150.0
ROAMING_TYPE = ""
MIN_RADIUS = 25.0
MAX_ROAMING_RADIUS = 200.0

POINT_RE = re.compile(r"<\s*([-0-9.]+)\s*,\s*([-0-9.]+)\s*,\s*([-0-9.]+)\s*>")


@dataclass
class Entry:
    name: str
    edge1_label: str
    edge1: tuple[float, float, float]
    edge2_label: str
    edge2: tuple[float, float, float]


@dataclass
class NormalizationResult:
    entry: Entry
    notes: list[str]


def point_has_repeated_xyz(point: tuple[float, float, float]) -> bool:
    return point[0] == point[1] == point[2]


def normalize_entry(entry: Entry) -> NormalizationResult:
    edge1 = entry.edge1
    edge2 = entry.edge2
    notes: list[str] = []

    if point_has_repeated_xyz(edge1) and not point_has_repeated_xyz(edge2):
        edge1 = infer_typo_point(entry.edge1_label, edge1, edge2)
        notes.append(f"{entry.name}: repaired {entry.edge1_label} repeated X/Y/Z typo using the opposite edge.")
    if point_has_repeated_xyz(edge2) and not point_has_repeated_xyz(edge1):
        edge2 = infer_typo_point(entry.edge2_label, edge2, edge1)
        notes.append(f"{entry.name}: repaired {entry.edge2_label} repeated X/Y/Z typo using the opposite edge.")

    return NormalizationResult(Entry(entry.name, entry.edge1_label, edge1, entry.edge2_label, edge2), notes)


def infer_typo_point(label: str, typo_point: tuple[float, float, float], other_point: tuple[float, float, float]) -> tuple[float, float, float]:
    lowered = label.lower()
    if "left" in lowered or "right" in lowered:
        return (typo_point[0], other_point[1], other_point[2])
    if "top" in lowered or "bottom" in lowered:
        return (other_point[0], other_point[1], typo_point[2])
    return typo_point


def parse_entries(path: Path) -> list[Entry]:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    lines = [line for line in lines if line]
    entries: list[Entry] = []
    parse_entries.notes = []
    i = 0
    while i < len(lines):
        if i + 4 >= len(lines):
            raise ValueError(f"Incomplete entry near line {i + 1} in {path}")
        name = lines[i]
        edge1_label = lines[i + 1]
        edge1 = parse_point(lines[i + 2], path, i + 3)
        edge2_label = lines[i + 3]
        edge2 = parse_point(lines[i + 4], path, i + 5)
        normalized = normalize_entry(Entry(name, edge1_label, edge1, edge2_label, edge2))
        entries.append(normalized.entry)
        parse_entries.notes.extend(normalized.notes)
        i += 5
    return entries


def parse_point(line: str, path: Path, line_number: int) -> tuple[float, float, float]:
    match = POINT_RE.fullmatch(line)
    if not match:
        raise ValueError(f"Invalid point at {path}:{line_number}: {line!r}")
    return tuple(float(group) for group in match.groups())


def midpoint(a: tuple[float, float, float], b: tuple[float, float, float]) -> list[float]:
    return [
        (a[0] + b[0]) / 2.0,
        (a[1] + b[1]) / 2.0,
        (a[2] + b[2]) / 2.0,
    ]


def radius_with_buffer(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    horizontal_distance = math.dist((a[0], a[2]), (b[0], b[2]))
    radius = (horizontal_distance / 2.0) * 1.05
    return max(radius, MIN_RADIUS)


def build_roaming_locations(entries: list[Entry]) -> list[dict]:
    locations = []
    for entry in entries:
        radius = min(radius_with_buffer(entry.edge1, entry.edge2), MAX_ROAMING_RADIUS)
        locations.append(
            {
                "Name": entry.name,
                "Position": midpoint(entry.edge1, entry.edge2),
                "Radius": radius,
                "Type": ROAMING_TYPE,
                "Enabled": 1,
            }
        )
    return locations


def build_no_go_areas(entries: list[Entry]) -> list[dict]:
    areas = []
    for entry in entries:
        areas.append(
            {
                "Name": entry.name,
                "Position": midpoint(entry.edge1, entry.edge2),
                "Radius": radius_with_buffer(entry.edge1, entry.edge2),
                "Height": DEFAULT_NO_GO_HEIGHT,
            }
        )
    return areas


def load_excluded_buildings() -> list[str]:
    current = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    return current.get("ExcludedRoamingBuildings", [])


def collect_warnings(entries: list[Entry], label: str) -> list[str]:
    warnings = []
    for entry in entries:
        horizontal_distance = math.dist((entry.edge1[0], entry.edge1[2]), (entry.edge2[0], entry.edge2[2]))
        if horizontal_distance == 0:
            warnings.append(f"{label}: {entry.name} has identical edge points; applied minimum radius {MIN_RADIUS}.")
        if point_has_repeated_xyz(entry.edge1):
            warnings.append(f"{label}: {entry.name} first point repeats the same X/Y/Z value {entry.edge1[0]}.")
        if point_has_repeated_xyz(entry.edge2):
            warnings.append(f"{label}: {entry.name} second point repeats the same X/Y/Z value {entry.edge2[0]}.")
    return warnings


def main() -> None:
    roaming_entries = parse_entries(LOCATIONS_INPUT)
    roaming_notes = parse_entries.notes
    no_go_entries = parse_entries(NO_GO_INPUT)
    no_go_notes = parse_entries.notes

    output = {
        "m_Version": 4,
        "RoamingLocations": build_roaming_locations(roaming_entries),
        "ExcludedRoamingBuildings": load_excluded_buildings(),
        "NoGoAreas": build_no_go_areas(no_go_entries),
    }

    SETTINGS_PATH.write_text(json.dumps(output, indent=4) + "\n", encoding="utf-8")

    warnings = collect_warnings(roaming_entries, "Roaming") + collect_warnings(no_go_entries, "NoGo")
    notes = roaming_notes + no_go_notes
    print(f"Wrote {SETTINGS_PATH}")
    print(f"RoamingLocations: {len(roaming_entries)}")
    print(f"NoGoAreas: {len(no_go_entries)}")
    if notes:
        print("Notes:")
        for note in notes:
            print(f"- {note}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")


if __name__ == "__main__":
    main()
