#!/usr/bin/env python3
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MISSION = ROOT / "mpmissions" / "Expansion.deerisle"

EVENT_FILES = [
    MISSION / "expansion_ce" / "expansion_events.xml",
    MISSION / "db" / "events.xml",
]

TYPE_FILES = [
    MISSION / "expansion_ce" / "expansion_types.xml",
    MISSION / "db" / "types.xml",
]

SPAWN_FILE = MISSION / "cfgeventspawns.xml"


def load_type_index(paths):
    index = {}
    for path in paths:
        root = ET.parse(path).getroot()
        for t in root.findall("type"):
            name = t.attrib["name"]
            nominal = int((t.findtext("nominal") or "0").strip())
            minimum = int((t.findtext("min") or "0").strip())
            index[name] = {
                "file": str(path.relative_to(ROOT)),
                "nominal": nominal,
                "min": minimum,
            }
    return index


def load_spawn_counts(path):
    counts = {}
    current = None
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        m = re.search(r'<event name="([^"]+)"', line)
        if m:
            current = m.group(1)
            counts.setdefault(current, 0)
            continue
        if current and line.startswith("<pos "):
            counts[current] += 1
        elif current and line.startswith("</event>"):
            current = None
    return counts


def load_active_vehicle_children(paths, spawn_counts):
    rows = []
    for path in paths:
        root = ET.parse(path).getroot()
        for event in root.findall("event"):
            event_name = event.attrib.get("name", "")
            if not event_name.startswith("Vehicle"):
                continue
            nominal = int((event.findtext("nominal") or "0").strip())
            minimum = int((event.findtext("min") or "0").strip())
            active = (event.findtext("active") or "0").strip()
            positions = spawn_counts.get(event_name, 0)
            if active != "1" or nominal <= 0 or positions <= 0:
                continue
            for child in event.findall("./children/child"):
                rows.append(
                    {
                        "event": event_name,
                        "event_file": str(path.relative_to(ROOT)),
                        "event_nominal": nominal,
                        "event_min": minimum,
                        "spawn_positions": positions,
                        "child_type": child.attrib["type"],
                    }
                )
    return rows


def main():
    type_index = load_type_index(TYPE_FILES)
    spawn_counts = load_spawn_counts(SPAWN_FILE)
    active_children = load_active_vehicle_children(EVENT_FILES, spawn_counts)

    results = []
    for row in active_children:
        t = type_index.get(row["child_type"])
        status = "ok"
        if not t:
            status = "missing_type_entry"
            result = {**row, "type_file": None, "type_nominal": None, "type_min": None, "status": status}
        else:
            if t["nominal"] <= 0 or t["min"] <= 0:
                status = "non_positive_nominal_or_min"
            result = {
                **row,
                "type_file": t["file"],
                "type_nominal": t["nominal"],
                "type_min": t["min"],
                "status": status,
            }
        results.append(result)

    bad = [r for r in results if r["status"] != "ok"]
    summary = {
        "spawned_vehicle_child_types_checked": len(results),
        "issues_found": len(bad),
        "issue_breakdown": {
            "missing_type_entry": sum(r["status"] == "missing_type_entry" for r in bad),
            "non_positive_nominal_or_min": sum(r["status"] == "non_positive_nominal_or_min" for r in bad),
        },
    }

    print(json.dumps({"summary": summary, "issues": bad}, indent=2))


if __name__ == "__main__":
    sys.exit(main())
