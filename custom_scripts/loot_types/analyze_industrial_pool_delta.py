#!/usr/bin/env python3
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FILES = [
    Path("mpmissions/Expansion.deerisle/db/types.xml"),
    Path("mpmissions/Expansion.deerisle/expansion_ce/expansion_types.xml"),
]


def parse_types(xml_text: str):
    root = ET.fromstring(xml_text)
    rows = {}
    for t in root.findall("type"):
        name = t.attrib["name"]
        nominal = int((t.findtext("nominal") or "0").strip())
        minimum = int((t.findtext("min") or "0").strip())
        usages = {u.attrib.get("name") for u in t.findall("usage")}
        rows[name] = {
            "nominal": nominal,
            "min": minimum,
            "industrial": "Industrial" in usages,
        }
    return rows


def read_head_version(relpath: Path):
    proc = subprocess.run(
        ["git", "show", f"HEAD:{relpath.as_posix()}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout


def load_versions():
    current = {}
    baseline = {}
    for relpath in FILES:
        current.update(parse_types((ROOT / relpath).read_text()))
        baseline.update(parse_types(read_head_version(relpath)))
    return baseline, current


def summarize(rows):
    industrial = {k: v for k, v in rows.items() if v["industrial"]}
    return {
        "type_count": len(industrial),
        "nominal_sum": sum(v["nominal"] for v in industrial.values()),
        "positive_nominal_count": sum(v["nominal"] > 0 for v in industrial.values()),
    }


def main():
    baseline, current = load_versions()
    base_summary = summarize(baseline)
    current_summary = summarize(current)

    deltas = []
    for name, cur in current.items():
        if not cur["industrial"]:
            continue
        old = baseline.get(name, {"nominal": 0, "min": 0, "industrial": False})
        if cur["nominal"] != old["nominal"] or cur["min"] != old["min"]:
            deltas.append(
                {
                    "name": name,
                    "nominal_before": old["nominal"],
                    "nominal_after": cur["nominal"],
                    "nominal_delta": cur["nominal"] - old["nominal"],
                    "min_before": old["min"],
                    "min_after": cur["min"],
                    "industrial": True,
                }
            )

    deltas.sort(key=lambda x: (-x["nominal_delta"], x["name"]))

    result = {
        "baseline": base_summary,
        "current": current_summary,
        "delta": {
            "nominal_sum": current_summary["nominal_sum"] - base_summary["nominal_sum"],
            "positive_nominal_count": current_summary["positive_nominal_count"] - base_summary["positive_nominal_count"],
        },
        "changed_industrial_types": deltas,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
