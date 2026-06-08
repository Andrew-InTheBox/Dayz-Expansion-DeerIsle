#!/usr/bin/env python3
"""
Plot animal territory zones from cfgenvironment.xml on the Deer Isle map.
"""

import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle


SCRIPT_DIR = Path(__file__).resolve().parent
CUSTOM_SCRIPTS_DIR = SCRIPT_DIR.parent
SERVER_DIR = CUSTOM_SCRIPTS_DIR.parent
MPMISSIONS_DIR = SERVER_DIR / "mpmissions"
PREFERRED_MISSION_DIR = MPMISSIONS_DIR / "Expansion.deerisle"

DEFAULT_MAP_SIZE = 16400.0
DEFAULT_EXTENT = (0.0, DEFAULT_MAP_SIZE, 0.0, DEFAULT_MAP_SIZE)
DEFAULT_BACKGROUND_IMAGE = CUSTOM_SCRIPTS_DIR / "assets" / "deer_isle_background.png"
DEFAULT_BACKGROUND_WORLD_BOUNDS = DEFAULT_EXTENT

PREDATOR_TERRITORIES = {
    "AmbientBear",
    "AmbientPolarbear",
    "AnimalArcticWolf",
    "AnimalWolf",
    "ArcticWolf",
    "Wolf",
}

ANIMAL_COLORS = {
    "AmbientHen": "#f2c94c",
    "AmbientCow": "#56ccf2",
    "AmbientDeer": "#27ae60",
    "AmbientRoeDeer": "#6fcf97",
    "AmbientGoat": "#bb6bd9",
    "AmbientSheep": "#f2994a",
    "AmbientPig": "#eb5757",
    "AmbientWildBoar": "#8d5a2b",
    "AnimalWolf": "#2f80ed",
    "Wolf": "#2f80ed",
    "AnimalArcticWolf": "#00a3ff",
    "ArcticWolf": "#00a3ff",
    "AmbientBear": "#4f4f4f",
    "AmbientPolarbear": "#bdbdbd",
}


def resolve_environment_path():
    preferred = PREFERRED_MISSION_DIR / "cfgenvironment.xml"
    if preferred.exists():
        return preferred

    candidates = sorted(MPMISSIONS_DIR.glob("*/cfgenvironment.xml"))
    return candidates[0] if candidates else None


def compact_label(territory_name):
    return (
        territory_name.removeprefix("Ambient")
        .removeprefix("Animal")
        .replace("RoeDeer", "Roe Deer")
        .replace("WildBoar", "Wild Boar")
        .replace("Polarbear", "Polar Bear")
        .replace("ArcticWolf", "Arctic Wolf")
    )


def load_animal_zones(environment_path, exclude_predators=False):
    mission_dir = Path(environment_path).parent
    root = ET.parse(environment_path).getroot()

    zones = []
    for territory in root.findall("./territories/territory"):
        territory_name = territory.attrib.get("name", "")
        territory_type = territory.attrib.get("type", "")
        if territory_name == "ZombieTest":
            continue
        if exclude_predators and territory_name in PREDATOR_TERRITORIES:
            continue

        file_node = territory.find("./file")
        if file_node is None:
            continue

        usable_name = file_node.attrib.get("usable")
        if not usable_name:
            continue

        territory_path = mission_dir / "env" / f"{usable_name}.xml"
        if not territory_path.exists():
            print(f"Skipping missing territory file for {territory_name}: {territory_path}")
            continue

        territory_root = ET.parse(territory_path).getroot()
        for index, zone in enumerate(territory_root.findall(".//zone"), start=1):
            x = zone.attrib.get("x")
            z = zone.attrib.get("z")
            radius = zone.attrib.get("r")
            if x is None or z is None or radius is None:
                continue

            zones.append(
                {
                    "territory_name": territory_name,
                    "territory_type": territory_type,
                    "label": compact_label(territory_name),
                    "file": territory_path.name,
                    "zone_name": zone.attrib.get("name", ""),
                    "zone_index": index,
                    "x": float(x),
                    "z": float(z),
                    "radius": float(radius),
                    "smin": zone.attrib.get("smin", ""),
                    "smax": zone.attrib.get("smax", ""),
                    "dmin": zone.attrib.get("dmin", ""),
                    "dmax": zone.attrib.get("dmax", ""),
                }
            )

    return zones


def plot_animal_spawns(
    environment_path,
    output_dir,
    label_zones=False,
    focus_region=None,
    background_bounds=None,
    exclude_predators=False,
):
    zones = load_animal_zones(environment_path, exclude_predators=exclude_predators)
    if not zones:
        print(f"No animal territory zones found in: {environment_path}")
        return None

    fig, ax = plt.subplots(figsize=(13, 11), dpi=150)
    image_bounds = background_bounds if background_bounds is not None else DEFAULT_BACKGROUND_WORLD_BOUNDS

    if DEFAULT_BACKGROUND_IMAGE.exists():
        background = plt.imread(DEFAULT_BACKGROUND_IMAGE)
        ax.imshow(background, extent=image_bounds, origin="upper")
    else:
        print(f"Background image not found: {DEFAULT_BACKGROUND_IMAGE}")

    territory_names = sorted({zone["territory_name"] for zone in zones})
    fallback_colors = plt.get_cmap("tab20", len(territory_names))
    colors_by_territory = {
        territory_name: ANIMAL_COLORS.get(territory_name, fallback_colors(index))
        for index, territory_name in enumerate(territory_names)
    }

    for zone in zones:
        color = colors_by_territory[zone["territory_name"]]
        circle = Circle(
            (zone["x"], zone["z"]),
            zone["radius"],
            fill=True,
            facecolor=color,
            edgecolor=color,
            linewidth=0.75,
            alpha=0.18,
            zorder=4,
        )
        ax.add_patch(circle)

    for territory_name in territory_names:
        territory_zones = [
            zone for zone in zones if zone["territory_name"] == territory_name
        ]
        ax.scatter(
            [zone["x"] for zone in territory_zones],
            [zone["z"] for zone in territory_zones],
            label=compact_label(territory_name),
            c=[colors_by_territory[territory_name]],
            s=18,
            alpha=0.9,
            edgecolors="black",
            linewidth=0.35,
            zorder=5,
        )

    if label_zones:
        for zone in zones:
            ax.annotate(
                zone["label"],
                (zone["x"], zone["z"]),
                fontsize=5,
                xytext=(3, 3),
                textcoords="offset points",
                bbox=dict(facecolor="white", alpha=0.68, edgecolor="none", pad=1.0),
                zorder=6,
            )

    if focus_region:
        min_x, max_x, min_z, max_z = focus_region
    else:
        min_x, max_x, min_z, max_z = image_bounds

    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_z, max_z)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_xlabel("X Coordinate (meters)")
    ax.set_ylabel("Z Coordinate (meters)")
    ax.set_title("Deer Isle Animal Territory Spawn Zones")

    counts_by_territory = Counter(zone["territory_name"] for zone in zones)
    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor=colors_by_territory[territory_name],
            markeredgecolor="black",
            markersize=6,
            label=f"{compact_label(territory_name)} ({counts_by_territory[territory_name]})",
        )
        for territory_name in territory_names
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        fontsize=6,
        title="Animal Zones",
        title_fontsize=7,
        framealpha=0.9,
    )

    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    suffix = "-no-predators" if exclude_predators else ""
    output_path = Path(output_dir) / f"AnimalSpawns{suffix}-{timestamp}.png"

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Plot saved to: {output_path}")
    print(f"Total animal territory zones plotted: {len(zones)}")
    for territory_name, count in sorted(counts_by_territory.items()):
        radii = [
            zone["radius"] for zone in zones if zone["territory_name"] == territory_name
        ]
        print(
            f"{territory_name}: {count} zones, radius {min(radii):g}-{max(radii):g}m"
        )

    return output_path


def main():
    parser = ArgumentParser(description="Plot Deer Isle animal territory zones.")
    parser.add_argument(
        "--environment",
        type=Path,
        default=resolve_environment_path(),
        help="Path to cfgenvironment.xml.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=SCRIPT_DIR / "output",
        help="Directory to save the output image.",
    )
    parser.add_argument(
        "--label-zones",
        action="store_true",
        help="Label individual territory zones. This can clutter the full-map plot.",
    )
    parser.add_argument(
        "--exclude-predators",
        action="store_true",
        help="Skip wolf and bear territory zones.",
    )
    parser.add_argument(
        "--focus-region",
        nargs=4,
        type=float,
        metavar=("MIN_X", "MAX_X", "MIN_Z", "MAX_Z"),
        help="Zoom to a specific map region.",
    )
    parser.add_argument(
        "--background-bounds",
        nargs=4,
        type=float,
        metavar=("MIN_X", "MAX_X", "MIN_Z", "MAX_Z"),
        help="World-coordinate bounds to map the background image onto.",
    )
    args = parser.parse_args()

    if args.environment is None:
        raise FileNotFoundError(f"No cfgenvironment.xml found under: {MPMISSIONS_DIR}")

    plot_animal_spawns(
        environment_path=args.environment,
        output_dir=args.output_dir,
        label_zones=args.label_zones,
        focus_region=tuple(args.focus_region) if args.focus_region else None,
        background_bounds=tuple(args.background_bounds) if args.background_bounds else None,
        exclude_predators=args.exclude_predators,
    )


if __name__ == "__main__":
    main()
