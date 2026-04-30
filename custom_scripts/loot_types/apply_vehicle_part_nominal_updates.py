#!/usr/bin/env python3
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
HEADLIGHT_OVERRIDE = ("HeadlightH7", 40, 35)
BODY_PART_TOTAL_MIN = 10
BODY_PART_TOTAL_MAX = 25


def clamp(value, low, high):
    return max(low, min(high, value))


def load_spawn_counts():
    root = ET.parse(SPAWN_FILE).getroot()
    return {event.attrib["name"]: len(event.findall("pos")) for event in root.findall("event")}


def load_spawnables():
    spawnables = {}
    for path in SPAWNABLE_FILES:
        root = ET.parse(path).getroot()
        for t in root.findall("type"):
            items = []
            for attachments in t.findall("attachments"):
                for item in attachments.findall("item"):
                    items.append((item.attrib["name"], float(item.attrib.get("chance", "1"))))
            spawnables[t.attrib["name"]] = items
    return spawnables


def load_type_index():
    index = {}
    for path in TYPE_FILES:
        root = ET.parse(path).getroot()
        for t in root.findall("type"):
            name = t.attrib["name"]
            index[name] = {
                "file": path,
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


def distribute_total(total, parts):
    if not parts:
        return {}

    base = total // len(parts)
    remainder = total % len(parts)
    return {part: base + (1 if idx < remainder else 0) for idx, part in enumerate(sorted(parts))}


def active_vehicle_rows(spawn_counts):
    rows = []
    for path in EVENT_FILES:
        root = ET.parse(path).getroot()
        for event in root.findall("event"):
            event_name = event.attrib.get("name", "")
            if not event_name.startswith("Vehicle"):
                continue

            nominal = int((event.findtext("nominal") or "0").strip())
            minimum = int((event.findtext("min") or "0").strip())
            active = (event.findtext("active") or "0").strip()
            if active != "1" or nominal <= 0 or spawn_counts.get(event_name, 0) <= 0:
                continue

            children = [child.attrib["type"] for child in event.findall("./children/child")]
            if children:
                rows.append(
                    {
                        "event": event_name,
                        "nominal": nominal,
                        "min": minimum,
                        "children": children,
                    }
                )
    return rows


def compute_updates():
    spawn_counts = load_spawn_counts()
    spawnables = load_spawnables()
    type_index = load_type_index()
    expected = defaultdict(float)
    body_groups = {}

    for row in active_vehicle_rows(spawn_counts):
        per_variant = row["nominal"] / len(row["children"])
        for child in row["children"]:
            for part, chance in spawnables.get(child, []):
                slot = body_part_slot(part)
                if slot:
                    body_groups.setdefault(
                        (row["event"], slot),
                        {
                            "nominal": row["nominal"],
                            "min": row["min"],
                            "parts": set(),
                        },
                    )["parts"].add(part)
                else:
                    expected[part] += per_variant * chance

    updates = defaultdict(dict)

    for group in body_groups.values():
        target_nominal = clamp(round(group["nominal"]), BODY_PART_TOTAL_MIN, BODY_PART_TOTAL_MAX)
        event_min_ratio = group["min"] / group["nominal"] if group["nominal"] > 0 else 0.75
        target_min = clamp(round(target_nominal * event_min_ratio), 1, target_nominal)

        nominal_by_part = distribute_total(target_nominal, group["parts"])
        min_by_part = distribute_total(target_min, group["parts"])
        for part in group["parts"]:
            if part not in type_index:
                continue
            nominal = nominal_by_part[part]
            minimum = min_by_part[part]
            if type_index[part]["nominal"] == nominal and type_index[part]["min"] == minimum:
                continue
            updates[type_index[part]["file"]][part] = (nominal, minimum)

    for part, exp_count in expected.items():
        if part not in type_index:
            continue
        if part == HEADLIGHT_OVERRIDE[0]:
            nominal, minimum = HEADLIGHT_OVERRIDE[1], HEADLIGHT_OVERRIDE[2]
        else:
            if type_index[part]["nominal"] > 0:
                continue
            nominal = max(1, round(exp_count))
            minimum = max(1, round(nominal * 0.75))

        if type_index[part]["nominal"] == nominal and type_index[part]["min"] == minimum:
            continue

        updates[type_index[part]["file"]][part] = (nominal, minimum)

    return updates


def update_type_block(text: str, type_name: str, nominal: int, minimum: int) -> str:
    escaped = re.escape(type_name)
    pattern = re.compile(
        rf'(<type name="{escaped}">.*?<nominal>)(\d+)(</nominal>.*?<min>)(\d+)(</min>)',
        re.DOTALL,
    )

    def repl(match):
        return f"{match.group(1)}{nominal}{match.group(3)}{minimum}{match.group(5)}"

    new_text, count = pattern.subn(repl, text, count=1)
    if count != 1:
        raise RuntimeError(f"Failed to update type block for {type_name}")
    return new_text


def apply_updates(updates):
    for path, mapping in updates.items():
        text = path.read_text()
        for type_name, (nominal, minimum) in sorted(mapping.items()):
            text = update_type_block(text, type_name, nominal, minimum)
        path.write_text(text)


def main():
    updates = compute_updates()
    total = sum(len(v) for v in updates.values())
    print(f"Planned updates: {total}")
    for path, mapping in updates.items():
        print(f"{path.relative_to(ROOT)}: {len(mapping)}")
        for type_name, (nominal, minimum) in sorted(mapping.items()):
            print(f"  {type_name}: nominal={nominal} min={minimum}")
    if "--apply" in sys.argv:
        apply_updates(updates)
        print("Applied updates.")


if __name__ == "__main__":
    sys.exit(main())
