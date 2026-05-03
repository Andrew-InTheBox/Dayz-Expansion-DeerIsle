#!/usr/bin/env python3
"""
Plot Vehicle* event spawn coordinates from cfgeventspawns.xml on the Deer Isle map.
"""

import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


SCRIPT_DIR = Path(__file__).resolve().parent
CUSTOM_SCRIPTS_DIR = SCRIPT_DIR.parent
SERVER_DIR = CUSTOM_SCRIPTS_DIR.parent
MPMISSIONS_DIR = SERVER_DIR / "mpmissions"
PREFERRED_MISSION_DIR = MPMISSIONS_DIR / "Expansion.deerisle"

DEFAULT_MAP_SIZE = 16400.0
DEFAULT_EXTENT = (0.0, DEFAULT_MAP_SIZE, 0.0, DEFAULT_MAP_SIZE)
DEFAULT_BACKGROUND_IMAGE = CUSTOM_SCRIPTS_DIR / "assets" / "deer_isle_background.png"
DEFAULT_BACKGROUND_WORLD_BOUNDS = DEFAULT_EXTENT


def resolve_eventspawns_path():
    preferred = PREFERRED_MISSION_DIR / "cfgeventspawns.xml"
    if preferred.exists():
        return preferred

    candidates = sorted(MPMISSIONS_DIR.glob("*/cfgeventspawns.xml"))
    return candidates[0] if candidates else None


def compact_vehicle_label(event_name):
    label = event_name.removeprefix("Vehicle")
    if label.endswith("Helicopter"):
        label = label.removesuffix("Helicopter").strip()
        return f"{label} Heli" if label else "Heli"
    return label or event_name


def load_vehicle_spawns(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    points = []
    for event in root.findall("./event"):
        event_name = event.attrib.get("name", "")
        if not event_name.startswith("Vehicle"):
            continue

        for pos in event.findall("./pos"):
            x = pos.attrib.get("x")
            z = pos.attrib.get("z")
            if x is None or z is None:
                continue

            points.append(
                {
                    "event_name": event_name,
                    "label": compact_vehicle_label(event_name),
                    "x": float(x),
                    "z": float(z),
                    "a": pos.attrib.get("a"),
                }
            )

    return points


def plot_vehicle_spawns(
    xml_file_path,
    output_dir,
    label_points=True,
    focus_region=None,
    background_bounds=None,
    label_full_names=False,
):
    points = load_vehicle_spawns(xml_file_path)
    if not points:
        print(f"No Vehicle* spawn points found in: {xml_file_path}")
        return

    fig, ax = plt.subplots(figsize=(13, 11), dpi=150)
    image_bounds = background_bounds if background_bounds is not None else DEFAULT_BACKGROUND_WORLD_BOUNDS

    if DEFAULT_BACKGROUND_IMAGE.exists():
        background = plt.imread(DEFAULT_BACKGROUND_IMAGE)
        ax.imshow(background, extent=image_bounds, origin="upper")
    else:
        print(f"Background image not found: {DEFAULT_BACKGROUND_IMAGE}")

    event_names = sorted({point["event_name"] for point in points})
    color_map = plt.get_cmap("tab20", len(event_names))
    colors_by_event = {
        event_name: color_map(index)
        for index, event_name in enumerate(event_names)
    }

    for event_name in event_names:
        event_points = [point for point in points if point["event_name"] == event_name]
        ax.scatter(
            [point["x"] for point in event_points],
            [point["z"] for point in event_points],
            label=compact_vehicle_label(event_name),
            c=[colors_by_event[event_name]],
            s=28,
            alpha=0.9,
            edgecolors="black",
            linewidth=0.45,
            zorder=5,
        )

    if label_points:
        for index, point in enumerate(points):
            # Spread label anchors slightly so stacked or nearby points remain inspectable.
            offset_x = 4 + (index % 3) * 6
            offset_y = 4 + ((index // 3) % 3) * 5
            label = point["event_name"] if label_full_names else point["label"]
            ax.annotate(
                label,
                (point["x"], point["z"]),
                fontsize=5.5,
                xytext=(offset_x, offset_y),
                textcoords="offset points",
                bbox=dict(facecolor="white", alpha=0.72, edgecolor="none", pad=1.1),
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
    ax.set_title("Deer Isle Vehicle Event Spawns")
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        fontsize=6,
        title="Vehicle Type",
        title_fontsize=7,
        framealpha=0.9,
    )

    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    output_path = Path(output_dir) / f"VehicleSpawns-{timestamp}.png"

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()

    counts_by_event = Counter(point["event_name"] for point in points)
    print(f"Plot saved to: {output_path}")
    print(f"Total Vehicle* spawn points plotted: {len(points)}")
    for event_name, count in sorted(counts_by_event.items()):
        print(f"{event_name}: {count}")


def main():
    parser = ArgumentParser(description="Plot Vehicle* event spawns for Deer Isle.")
    parser.add_argument(
        "--xml",
        type=Path,
        default=resolve_eventspawns_path(),
        help="Path to cfgeventspawns.xml.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=SCRIPT_DIR / "output",
        help="Directory to save the output image.",
    )
    parser.add_argument(
        "--no-labels",
        action="store_true",
        help="Do not label individual vehicle spawn points.",
    )
    parser.add_argument(
        "--full-labels",
        action="store_true",
        help="Use full event names for point labels.",
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

    if args.xml is None:
        raise FileNotFoundError(f"No cfgeventspawns.xml found under: {MPMISSIONS_DIR}")

    plot_vehicle_spawns(
        xml_file_path=args.xml,
        output_dir=args.output_dir,
        label_points=not args.no_labels,
        focus_region=tuple(args.focus_region) if args.focus_region else None,
        background_bounds=tuple(args.background_bounds) if args.background_bounds else None,
        label_full_names=args.full_labels,
    )


if __name__ == "__main__":
    main()
