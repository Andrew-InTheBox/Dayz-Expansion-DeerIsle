#!/usr/bin/env python3
"""Generate an HTML matrix report for DayZ Expansion AI patrol settings."""

from __future__ import annotations

import argparse
import collections
import html
import json
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = REPO_ROOT / "mpmissions/Expansion.deerisle/expansion/settings/AIPatrolSettings.json"
DEFAULT_OUTPUT = REPO_ROOT / "custom_scripts/output/ai_patrol_matrix_report.html"

KEY_FIELDS = [
    "Faction",
    "Behaviour",
    "Formation",
    "FormationScale",
    "FormationLooseness",
    "Loadout",
    "NumberOfAI",
    "NumberOfAIMax",
    "LootingBehaviour",
    "Speed",
    "UnderThreatSpeed",
    "DefaultStance",
    "CanBeLooted",
    "UnlimitedReload",
    "AccuracyMin",
    "AccuracyMax",
    "ThreatDistanceLimit",
    "NoiseInvestigationDistanceLimit",
    "MaxFlankingDistance",
    "EnableFlankingOutsideCombat",
    "DamageMultiplier",
    "DamageReceivedMultiplier",
    "HeadshotResistance",
    "CanSpawnInContaminatedArea",
    "CanBeTriggeredByAI",
    "MinDistRadius",
    "MaxDistRadius",
    "DespawnRadius",
    "MinSpreadRadius",
    "MaxSpreadRadius",
    "Chance",
    "DespawnTime",
    "RespawnTime",
    "LoadBalancingCategory",
    "ObjectClassName",
    "WaypointInterpolation",
    "UseRandomWaypointAsStartPoint",
]

MATRIX_FIELDS = [
    "Name",
    "Group",
    "Behaviour",
    "Faction",
    "Loadout",
    "NumberOfAI",
    "NumberOfAIMax",
    "Formation",
    "Speed",
    "CanBeLooted",
    "UnlimitedReload",
    "CanSpawnInContaminatedArea",
    "MinDistRadius",
    "MaxDistRadius",
    "DespawnRadius",
    "DespawnTime",
    "RespawnTime",
    "DamageMultiplier",
    "DamageReceivedMultiplier",
    "LoadBalancingCategory",
    "ObjectClassName",
    "WaypointCount",
]


def esc(value: Any) -> str:
    if value == "":
        return '<span class="empty">blank</span>'
    if value is None:
        return '<span class="empty">null</span>'
    return html.escape(str(value))


def patrol_group(patrol: dict[str, Any]) -> str:
    name = patrol["Name"]
    behaviour = patrol["Behaviour"]
    if name.startswith(("Wreck-", "Contam-")) or name == "Contam-area-static":
        return "Heli / police / contam"
    if behaviour == "ROAMING":
        return "Standard ROAMING"
    if behaviour == "ROAMING_LOCAL":
        return "ROAMING_LOCAL"
    return "Regular multi-waypoint"


def compact_counts(values: list[Any]) -> str:
    counter = collections.Counter(values)
    return ", ".join(f"{esc(value)} x {count}" for value, count in counter.most_common())


def variant_class(value: Any, group_patrols: list[dict[str, Any]], field: str) -> str:
    if field in {"Name", "Group", "ObjectClassName"}:
        return ""
    values = [len(p.get("Waypoints") or []) if field == "WaypointCount" else p.get(field) for p in group_patrols]
    if len(set(map(repr, values))) <= 1:
        return "same"
    baseline = collections.Counter(values).most_common(1)[0][0]
    return "variant" if value != baseline else "baseline"


def cell_value(patrol: dict[str, Any], field: str, group_name: str) -> Any:
    if field == "Group":
        return group_name
    if field == "WaypointCount":
        return len(patrol.get("Waypoints") or [])
    return patrol.get(field)


def group_summaries(patrols: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    order = [
        "Heli / police / contam",
        "Standard ROAMING",
        "ROAMING_LOCAL",
        "Regular multi-waypoint",
    ]
    by_group: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for patrol in patrols:
        by_group[patrol_group(patrol)].append(patrol)
    return [(name, by_group[name]) for name in order if by_group[name]]


def render_value_sets(patrols: list[dict[str, Any]]) -> str:
    rows = []
    for field in KEY_FIELDS + ["WaypointCount"]:
        values = [
            len(patrol.get("Waypoints") or []) if field == "WaypointCount" else patrol.get(field)
            for patrol in patrols
        ]
        if len(set(map(repr, values))) == 1:
            rows.append(
                f"<tr><th>{esc(field)}</th><td>{esc(values[0])}</td><td><span class=\"ok\">same</span></td></tr>"
            )
        else:
            rows.append(
                f"<tr><th>{esc(field)}</th><td>{compact_counts(values)}</td><td><span class=\"warn\">varies</span></td></tr>"
            )
    return "\n".join(rows)


def render_difference_rows(patrols: list[dict[str, Any]]) -> str:
    rows = []
    ignored = {"Name", "ObjectClassName"}
    for field in KEY_FIELDS + ["WaypointCount"]:
        if field in ignored:
            continue
        values_by_repr: dict[str, tuple[Any, list[str]]] = {}
        for patrol in patrols:
            value = len(patrol.get("Waypoints") or []) if field == "WaypointCount" else patrol.get(field)
            key = repr(value)
            values_by_repr.setdefault(key, (value, []))[1].append(patrol["Name"])
        if len(values_by_repr) <= 1:
            continue
        detail = []
        for value, names in values_by_repr.values():
            detail.append(f"<strong>{esc(value)}</strong>: {esc(', '.join(names))}")
        rows.append(f"<tr><th>{esc(field)}</th><td>{'<br>'.join(detail)}</td></tr>")
    return "\n".join(rows) or '<tr><td colspan="2">No differences inside this group.</td></tr>'


def render_matrix(groups: list[tuple[str, list[dict[str, Any]]]]) -> str:
    all_grouped = {patrol["Name"]: (name, group_patrols) for name, group_patrols in groups for patrol in group_patrols}
    headers = "".join(f"<th>{esc(field)}</th>" for field in MATRIX_FIELDS)
    rows = []
    for group_name, patrols in groups:
        rows.append(f'<tr class="group-row"><th colspan="{len(MATRIX_FIELDS)}">{esc(group_name)} ({len(patrols)})</th></tr>')
        for patrol in patrols:
            _, group_patrols = all_grouped[patrol["Name"]]
            cells = []
            for field in MATRIX_FIELDS:
                value = cell_value(patrol, field, group_name)
                cls = variant_class(value, group_patrols, field)
                cells.append(f'<td class="{cls}">{esc(value)}</td>')
            rows.append(f"<tr>{''.join(cells)}</tr>")
    return f"<table><thead><tr>{headers}</tr></thead><tbody>{''.join(rows)}</tbody></table>"


def render_report(input_path: Path, patrols: list[dict[str, Any]]) -> str:
    groups = group_summaries(patrols)
    generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    group_cards = []
    diff_cards = []
    for group_name, group_patrols in groups:
        waypoint_counts = collections.Counter(len(p.get("Waypoints") or []) for p in group_patrols)
        group_cards.append(
            f"""
            <section>
              <h2>{esc(group_name)} <span>{len(group_patrols)} patrols</span></h2>
              <p>Waypoint counts: {compact_counts(list(waypoint_counts.elements()))}</p>
              <table>
                <thead><tr><th>Setting</th><th>Values</th><th>Status</th></tr></thead>
                <tbody>{render_value_sets(group_patrols)}</tbody>
              </table>
            </section>
            """
        )
        diff_cards.append(
            f"""
            <section>
              <h2>{esc(group_name)} differences</h2>
              <table>
                <thead><tr><th>Setting</th><th>Patrol values</th></tr></thead>
                <tbody>{render_difference_rows(group_patrols)}</tbody>
              </table>
            </section>
            """
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Patrol Matrix Report</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f5;
      --ink: #202422;
      --muted: #5f6763;
      --line: #cfd5d1;
      --head: #e7ece8;
      --baseline: #eef6f0;
      --variant: #fff2bf;
      --same: #f8faf8;
      --accent: #0f6b58;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ max-width: 100%; overflow-x: hidden; }}
    body {{ margin: 0; font: 14px/1.45 system-ui, -apple-system, Segoe UI, sans-serif; color: var(--ink); background: var(--bg); }}
    header {{ padding: 28px 32px 18px; border-bottom: 1px solid var(--line); background: #ffffff; }}
    main {{ padding: 24px 32px 40px; min-width: 0; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    h2 {{ margin: 0 0 12px; font-size: 18px; }}
    h2 span {{ color: var(--muted); font-weight: 500; }}
    p {{ margin: 0 0 14px; color: var(--muted); }}
    section {{ margin: 0 0 24px; min-width: 0; }}
    .stats {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 16px; }}
    .stat {{ border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; background: #fff; min-width: 180px; }}
    .stat strong {{ display: block; font-size: 22px; }}
    .matrix {{ display: block; width: 100%; max-width: 100%; overflow-x: scroll; overflow-y: auto; border: 1px solid var(--line); border-radius: 8px; background: white; -webkit-overflow-scrolling: touch; overscroll-behavior-x: contain; }}
    table {{ width: 100%; border-collapse: collapse; background: white; }}
    .matrix table {{ width: max-content; min-width: 100%; }}
    th, td {{ border: 1px solid var(--line); padding: 7px 9px; vertical-align: top; white-space: nowrap; }}
    th {{ background: var(--head); text-align: left; }}
    .matrix thead th {{ position: sticky; top: 0; z-index: 1; }}
    .group-row th {{ position: static; background: #dce7e1; color: #18372f; font-size: 15px; }}
    .baseline {{ background: var(--baseline); }}
    .variant {{ background: var(--variant); font-weight: 650; }}
    .same {{ background: var(--same); }}
    .empty {{ color: #8a6b00; font-style: italic; }}
    .ok {{ color: var(--accent); font-weight: 650; }}
    .warn {{ color: #966200; font-weight: 650; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 18px; align-items: start; }}
    code {{ background: #eef1ee; padding: 1px 4px; border-radius: 4px; }}
    @media (max-width: 700px) {{
      header, main {{ padding-left: 14px; padding-right: 14px; }}
      .grid {{ grid-template-columns: 1fr; }}
      th, td {{ white-space: normal; }}
      .matrix th, .matrix td {{ white-space: nowrap; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>AI Patrol Matrix Report</h1>
    <p>Source: <code>{esc(input_path)}</code>. Generated: {esc(generated)}.</p>
    <p>Yellow cells are fields that differ from the most common value inside that patrol family. Green cells are the common value for fields that vary inside that family.</p>
    <div class="stats">
      <div class="stat"><strong>{len(patrols)}</strong>Total patrols</div>
      {''.join(f'<div class="stat"><strong>{len(group_patrols)}</strong>{esc(group_name)}</div>' for group_name, group_patrols in groups)}
    </div>
  </header>
  <main>
    <section>
      <h2>Patrol Matrix</h2>
      <div class="matrix">{render_matrix(groups)}</div>
    </section>
    <section>
      <h2>Major Differences</h2>
      <div class="grid">{''.join(diff_cards)}</div>
    </section>
    <section>
      <h2>Group Setting Summary</h2>
      <div class="grid">{''.join(group_cards)}</div>
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    with args.input.open(encoding="utf-8-sig") as handle:
        data = json.load(handle)
    patrols = data["Patrols"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_report(args.input, patrols), encoding="utf-8")
    print(f"Wrote {args.output} ({len(patrols)} patrols)")


if __name__ == "__main__":
    main()
