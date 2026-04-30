#!/usr/bin/env python3
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
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
BODY_PART_TOTAL_MIN = 10
BODY_PART_TOTAL_MAX = 25


def clamp(value, low, high):
    return max(low, min(high, value))


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
            minimum = int((event.findtext("min") or "0").strip())
            for child in event.findall("./children/child"):
                rows.append(
                    {
                        "event": name,
                        "event_file": str(path.relative_to(ROOT)),
                        "event_nominal": nominal,
                        "event_min": minimum,
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


def body_part_slot(part):
    if "Wheel" in part:
        return None

    match = re.match(r"^(.+?Door(?:s)?_(?:\d_\d|Driver|CoDriver))(?:_.+)?$", part)
    if match:
        return match.group(1)

    match = re.match(r"^(.+?(?:Hood|Trunk))(?:_.+)?$", part)
    if match:
        return match.group(1)

    return None


def main():
    spawn_counts = load_spawn_counts(SPAWN_FILE)
    active_children = load_active_vehicle_children(EVENT_FILES, spawn_counts)
    spawnable = load_spawnable_index(SPAWNABLE_FILES)
    types = load_type_index(TYPE_FILES)

    seen = set()
    issues = []
    body_groups = {}
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

            slot = body_part_slot(part)
            if slot:
                body_groups.setdefault(
                    (row["event"], slot),
                    {
                        "event": row["event"],
                        "slot": slot,
                        "event_nominal": row["event_nominal"],
                        "event_min": row["event_min"],
                        "parts": set(),
                    },
                )["parts"].add(part)

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
            if not slot and type_info["nominal"] <= 0:
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

    for group in body_groups.values():
        parts = sorted(group["parts"])
        present_parts = [part for part in parts if part in types]
        missing_parts = [part for part in parts if part not in types]
        total_nominal = sum(types[part]["nominal"] for part in present_parts)
        total_min = sum(types[part]["min"] for part in present_parts)
        target_nominal = clamp(round(group["event_nominal"]), BODY_PART_TOTAL_MIN, BODY_PART_TOTAL_MAX)
        event_min_ratio = group["event_min"] / group["event_nominal"] if group["event_nominal"] > 0 else 0.75
        target_min = clamp(round(target_nominal * event_min_ratio), 1, target_nominal)

        if missing_parts or total_nominal != target_nominal or total_min != target_min:
            status = "body_part_group_total_mismatch"
            if missing_parts:
                status = "body_part_group_missing_type_entry"
            issues.append(
                {
                    "event": group["event"],
                    "slot": group["slot"],
                    "event_nominal": group["event_nominal"],
                    "event_min": group["event_min"],
                    "target_total_nominal": target_nominal,
                    "target_total_min": target_min,
                    "actual_total_nominal": total_nominal,
                    "actual_total_min": total_min,
                    "parts": parts,
                    "missing_parts": missing_parts,
                    "status": status,
                }
            )
            summary[status] += 1

    print(
        json.dumps(
            {
                "summary": {
                    "active_vehicle_classes_checked": len(active_children),
                    "body_part_groups_checked": len(body_groups),
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
