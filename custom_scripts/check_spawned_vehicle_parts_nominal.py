#!/usr/bin/env python3
import json
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MISSION = ROOT / "mpmissions" / "Expansion.deerisle"

EVENT_FILES = [
    MISSION / "expansion_ce" / "expansion_events.xml",
    MISSION / "db" / "events.xml",
]

SPAWNABLE_FILES = [
    MISSION / "expansion_ce" / "expansion_spawnabletypes.xml",
    MISSION / "cfgspawnabletypes.xml",
]

TYPE_FILES = [
    MISSION / "expansion_ce" / "expansion_types.xml",
    MISSION / "db" / "types.xml",
]

SPAWN_FILE = MISSION / "cfgeventspawns.xml"


def load_spawn_counts(path: Path):
    root = ET.parse(path).getroot()
    out = {}
    for event in root.findall("event"):
        out[event.attrib["name"]] = len(event.findall("pos"))
    return out


def load_active_vehicle_children(paths, spawn_counts):
    rows = []
    for path in paths:
        root = ET.parse(path).getroot()
        for event in root.findall("event"):
            name = event.attrib.get("name", "")
            if not name.startswith("Vehicle"):
                continue
            nominal = int((event.findtext("nominal") or "0").strip())
            active = (event.findtext("active") or "0").strip()
            if active != "1" or nominal <= 0 or spawn_counts.get(name, 0) <= 0:
                continue
            for child in event.findall("./children/child"):
                rows.append(
                    {
                        "event": name,
                        "event_file": str(path.relative_to(ROOT)),
                        "vehicle_class": child.attrib["type"],
                    }
                )
    return rows


def load_spawnable_index(paths):
    index = {}
    for path in paths:
        root = ET.parse(path).getroot()
        for t in root.findall("type"):
            items = []
            for attachments in t.findall("attachments"):
                for item in attachments.findall("item"):
                    items.append(item.attrib["name"])
            index[t.attrib["name"]] = {
                "file": str(path.relative_to(ROOT)),
                "items": items,
            }
    return index


def load_type_index(paths):
    index = {}
    for path in paths:
        root = ET.parse(path).getroot()
        for t in root.findall("type"):
            index[t.attrib["name"]] = {
                "file": str(path.relative_to(ROOT)),
                "nominal": int((t.findtext("nominal") or "0").strip()),
                "min": int((t.findtext("min") or "0").strip()),
            }
    return index


def main():
    spawn_counts = load_spawn_counts(SPAWN_FILE)
    active_children = load_active_vehicle_children(EVENT_FILES, spawn_counts)
    spawnable = load_spawnable_index(SPAWNABLE_FILES)
    types = load_type_index(TYPE_FILES)

    seen = set()
    issues = []
    summary = defaultdict(int)

    for row in active_children:
        vehicle_class = row["vehicle_class"]
        spawnable_info = spawnable.get(vehicle_class)
        if not spawnable_info:
            key = (row["event"], vehicle_class, "missing_spawnabletype")
            if key not in seen:
                seen.add(key)
                issues.append(
                    {
                        **row,
                        "part": None,
                        "spawnable_file": None,
                        "type_file": None,
                        "type_nominal": None,
                        "type_min": None,
                        "status": "missing_spawnabletype",
                    }
                )
                summary["missing_spawnabletype"] += 1
            continue

        for part in spawnable_info["items"]:
            key = (row["event"], vehicle_class, part)
            if key in seen:
                continue
            seen.add(key)
            type_info = types.get(part)
            if not type_info:
                issues.append(
                    {
                        **row,
                        "part": part,
                        "spawnable_file": spawnable_info["file"],
                        "type_file": None,
                        "type_nominal": None,
                        "type_min": None,
                        "status": "missing_type_entry",
                    }
                )
                summary["missing_type_entry"] += 1
                continue
            if type_info["nominal"] <= 0:
                issues.append(
                    {
                        **row,
                        "part": part,
                        "spawnable_file": spawnable_info["file"],
                        "type_file": type_info["file"],
                        "type_nominal": type_info["nominal"],
                        "type_min": type_info["min"],
                        "status": "non_positive_nominal",
                    }
                )
                summary["non_positive_nominal"] += 1

    print(
        json.dumps(
            {
                "summary": {
                    "active_vehicle_classes_checked": len(active_children),
                    "issues_found": len(issues),
                    **summary,
                },
                "issues": issues,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    sys.exit(main())
