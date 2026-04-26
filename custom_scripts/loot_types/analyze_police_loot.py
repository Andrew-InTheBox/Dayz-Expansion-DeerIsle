#!/usr/bin/env python3
"""Estimate Police loot supply versus map spawn capacity for a DayZ mission."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path


DEFAULT_MISSION = Path("mpmissions/Expansion.deerisle")
TYPE_FILES = ("db/types.xml", "expansion_ce/expansion_types.xml")


def as_int(value: str | None, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def parse_types(mission: Path, usage: str) -> list[dict]:
    items: list[dict] = []
    for rel_path in TYPE_FILES:
        path = mission / rel_path
        if not path.exists():
            continue

        root = ET.parse(path).getroot()
        for type_node in root.findall("type"):
            usages = [node.get("name", "") for node in type_node.findall("usage")]
            if usage not in usages:
                continue

            items.append(
                {
                    "file": rel_path,
                    "name": type_node.get("name", ""),
                    "nominal": as_int(type_node.findtext("nominal")),
                    "min": as_int(type_node.findtext("min")),
                    "categories": [node.get("name", "") for node in type_node.findall("category")],
                    "tags": [node.get("name", "") for node in type_node.findall("tag")],
                    "values": [node.get("name", "") for node in type_node.findall("value")],
                    "usages": usages,
                }
            )
    return items


def parse_proto(mission: Path) -> dict[str, dict]:
    groups: dict[str, dict] = {}
    root = ET.parse(mission / "mapgroupproto.xml").getroot()
    for group_node in root.findall("group"):
        containers = []
        for container_node in group_node.findall("container"):
            containers.append(
                {
                    "name": container_node.get("name", ""),
                    "lootmax": as_int(container_node.get("lootmax")),
                    "categories": [node.get("name", "") for node in container_node.findall("category")],
                    "tags": [node.get("name", "") for node in container_node.findall("tag")],
                    "points": len(container_node.findall("point")),
                }
            )

        name = group_node.get("name", "")
        groups[name] = {
            "name": name,
            "lootmax": as_int(group_node.get("lootmax"), 10),
            "usages": [node.get("name", "") for node in group_node.findall("usage")],
            "containers": containers,
            "points": sum(container["points"] for container in containers),
            "container_lootmax": sum(container["lootmax"] for container in containers),
        }
    return groups


def parse_map_positions(mission: Path) -> Counter[str]:
    root = ET.parse(mission / "mapgrouppos.xml").getroot()
    return Counter(node.get("name", "") for node in root.findall("group"))


def print_item_supply(items: list[dict], usage: str, limit: int) -> None:
    category_nominal = Counter()
    tag_nominal = Counter()
    value_nominal = Counter()
    usage_count = Counter()

    for item in items:
        usage_count[len(item["usages"])] += item["nominal"]
        for category in item["categories"] or ["(none)"]:
            category_nominal[category] += item["nominal"]
        for tag in item["tags"] or ["(none)"]:
            tag_nominal[tag] += item["nominal"]
        for value in item["values"] or ["(none)"]:
            value_nominal[value] += item["nominal"]

    print(f"{usage} item supply")
    print(f"  items: {len(items)}")
    print(f"  nominal sum: {sum(item['nominal'] for item in items)}")
    print(f"  min sum: {sum(item['min'] for item in items)}")
    print(f"  by file: {dict(Counter(item['file'] for item in items))}")
    print(f"  nominal by category: {dict(category_nominal.most_common())}")
    print(f"  nominal by tag: {dict(tag_nominal.most_common())}")
    print(f"  nominal by tier/value: {dict(value_nominal.most_common())}")
    print(f"  nominal shared by usage count: {dict(sorted(usage_count.items()))}")

    police_only = [item for item in items if item["usages"] == [usage]]
    print(f"  {usage}-only nominal: {sum(item['nominal'] for item in police_only)}")
    if police_only:
        print(f"  {usage}-only items:")
        for item in sorted(police_only, key=lambda i: (-i["nominal"], i["name"])):
            print(
                f"    {item['nominal']:4d} min {item['min']:4d} {item['name']} "
                f"cat={','.join(item['categories']) or '-'} tags={','.join(item['tags']) or '-'}"
            )

    print(f"  top {limit} nominal items:")
    for item in sorted(items, key=lambda i: (-i["nominal"], i["name"]))[:limit]:
        print(
            f"    {item['nominal']:4d} min {item['min']:4d} {item['name']} "
            f"cat={','.join(item['categories']) or '-'} tags={','.join(item['tags']) or '-'} "
            f"usages={','.join(item['usages'])}"
        )


def print_map_capacity(groups: dict[str, dict], instances: Counter[str], usage: str, limit: int) -> None:
    usage_groups = {name: group for name, group in groups.items() if usage in group["usages"]}
    placed = {name: count for name, count in instances.items() if name in usage_groups}

    group_capacity = sum(count * usage_groups[name]["lootmax"] for name, count in placed.items())
    container_capacity = sum(count * usage_groups[name]["container_lootmax"] for name, count in placed.items())
    points = sum(count * usage_groups[name]["points"] for name, count in placed.items())

    print()
    print(f"{usage} map capacity")
    print(f"  proto groups with usage: {len(usage_groups)}")
    print(f"  placed instances: {sum(placed.values())} across {len(placed)} distinct group names")
    print(f"  group lootmax capacity estimate: {group_capacity}")
    print(f"  container lootmax sum, before group cap: {container_capacity}")
    print(f"  spawn points: {points}")
    print(f"  top {limit} placed groups by group lootmax capacity:")

    for name, count in sorted(placed.items(), key=lambda item: -(item[1] * usage_groups[item[0]]["lootmax"]))[:limit]:
        group = usage_groups[name]
        print(
            f"    {count:4d}x cap {count * group['lootmax']:5d} "
            f"lootmax {group['lootmax']:3d} points {count * group['points']:5d} {name}"
        )


def print_station_breakdown(groups: dict[str, dict], instances: Counter[str]) -> None:
    print()
    print("Police station buildings")
    for name in sorted(group for group in groups if "PoliceStation" in group):
        group = groups[name]
        count = instances[name]
        print(
            f"  {name}: instances={count}, group_lootmax={group['lootmax']}, "
            f"group_capacity={count * group['lootmax']}"
        )
        for container in group["containers"]:
            print(
                f"    {container['name']}: lootmax={container['lootmax']} "
                f"points_per={container['points']} total_points={count * container['points']} "
                f"cats={','.join(container['categories']) or '-'} tags={','.join(container['tags']) or '-'}"
            )


def print_usage_comparison(groups: dict[str, dict], instances: Counter[str]) -> None:
    stats = defaultdict(lambda: {"instances": 0, "capacity": 0, "points": 0, "proto_groups": 0})

    for group in groups.values():
        for usage in group["usages"]:
            stats[usage]["proto_groups"] += 1

    for name, count in instances.items():
        group = groups.get(name)
        if not group:
            continue
        for usage in group["usages"]:
            stats[usage]["instances"] += count
            stats[usage]["capacity"] += count * group["lootmax"]
            stats[usage]["points"] += count * group["points"]

    print()
    print("Usage capacity comparison")
    for usage, stat in sorted(stats.items(), key=lambda item: -item[1]["capacity"]):
        print(
            f"  {usage:<18} instances={stat['instances']:5d} "
            f"capacity={stat['capacity']:6d} points={stat['points']:7d} "
            f"proto_groups={stat['proto_groups']:4d}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mission", type=Path, default=DEFAULT_MISSION)
    parser.add_argument("--usage", default="Police")
    parser.add_argument("--top", type=int, default=30)
    args = parser.parse_args()

    mission = args.mission
    items = parse_types(mission, args.usage)
    groups = parse_proto(mission)
    instances = parse_map_positions(mission)

    print_item_supply(items, args.usage, args.top)
    print_map_capacity(groups, instances, args.usage, args.top)
    print_station_breakdown(groups, instances)
    print_usage_comparison(groups, instances)


if __name__ == "__main__":
    main()
