#!/usr/bin/env python3
"""
Plot AI roaming locations from AILocationSettings.json on the Deer Isle map.
"""

import json
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle


SCRIPT_DIR = Path(__file__).resolve().parent
MPMISSIONS_DIR = SCRIPT_DIR.parents[1] / "mpmissions"
PREFERRED_MISSION_DIR = MPMISSIONS_DIR / "Expansion.deerisle"
DEFAULT_MAP_SIZE = 16400.0
DEFAULT_EXTENT = (0.0, DEFAULT_MAP_SIZE, 0.0, DEFAULT_MAP_SIZE)
DEFAULT_BACKGROUND_IMAGE = SCRIPT_DIR.parent / "assets" / "deer_isle_background.png"
# The image pixel dimensions do not need to match the DayZ world size.
# Matplotlib stretches the image into these world coordinates via `extent`.
DEFAULT_BACKGROUND_WORLD_BOUNDS = DEFAULT_EXTENT


def resolve_settings_path(filename):
    preferred = PREFERRED_MISSION_DIR / "expansion" / "settings" / filename
    if preferred.exists():
        return preferred

    candidates = sorted(MPMISSIONS_DIR.glob(f"*/expansion/settings/{filename}"))
    return candidates[0] if candidates else None


def parse_area_entries(entries):
    points = []
    for location in entries:
        position = location.get("Position", [])
        if len(position) < 3:
            continue

        points.append(
            {
                "name": location.get("Name", "Unknown"),
                "x": position[0],
                "z": position[2],
                "radius": location.get("Radius", 100.0),
            }
        )

    return points


def load_location_settings(json_file_path):
    with open(json_file_path, "r") as file_handle:
        data = json.load(file_handle)

    return {
        "roaming_locations": parse_area_entries(data.get("RoamingLocations", [])),
        "no_go_areas": parse_area_entries(data.get("NoGoAreas", [])),
    }


def plot_ai_locations(
    json_file_path,
    output_dir,
    label_locations=True,
    focus_region=None,
    background_bounds=None,
):
    settings = load_location_settings(json_file_path)
    locations = settings["roaming_locations"]
    no_go_areas = settings["no_go_areas"]

    if not locations:
        print("No roaming locations found in the JSON file.")
        return

    fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
    image_bounds = background_bounds if background_bounds is not None else DEFAULT_BACKGROUND_WORLD_BOUNDS

    if DEFAULT_BACKGROUND_IMAGE.exists():
        background = plt.imread(DEFAULT_BACKGROUND_IMAGE)
        ax.imshow(background, extent=image_bounds, origin="upper")
    else:
        print(f"Background image not found: {DEFAULT_BACKGROUND_IMAGE}")

    for location in locations:
        circle = Circle(
            (location["x"], location["z"]),
            location["radius"],
            fill=False,
            edgecolor="red",
            linewidth=1.2,
            alpha=0.85,
        )
        ax.add_patch(circle)

    for area in no_go_areas:
        circle = Circle(
            (area["x"], area["z"]),
            area["radius"],
            fill=True,
            facecolor="grey",
            edgecolor="dimgray",
            linewidth=1.0,
            alpha=0.35,
            zorder=3,
        )
        ax.add_patch(circle)

    ax.scatter(
        [location["x"] for location in locations],
        [location["z"] for location in locations],
        c="red",
        s=16,
        alpha=0.85,
        edgecolors="black",
        linewidth=0.4,
        zorder=5,
    )

    if no_go_areas:
        ax.scatter(
            [area["x"] for area in no_go_areas],
            [area["z"] for area in no_go_areas],
            c="grey",
            s=16,
            alpha=0.85,
            edgecolors="black",
            linewidth=0.4,
            zorder=5,
        )

    if label_locations:
        for location in locations:
            ax.annotate(
                location["name"],
                (location["x"], location["z"]),
                fontsize=6,
                xytext=(3, 3),
                textcoords="offset points",
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=1.5),
                zorder=6,
            )

        for area in no_go_areas:
            ax.annotate(
                area["name"],
                (area["x"], area["z"]),
                fontsize=6,
                xytext=(3, 3),
                textcoords="offset points",
                bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", pad=1.5),
                color="dimgray",
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
    ax.set_title("Deer Isle AI Roaming Areas and No-Go Areas")

    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    output_path = Path(output_dir) / f"AILocationsPlots-{timestamp}.png"

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Plot saved to: {output_path}")
    print(f"Total locations plotted: {len(locations)}")
    print(f"Total no-go areas plotted: {len(no_go_areas)}")


def main():
    parser = ArgumentParser(description="Plot AI roaming areas for Deer Isle.")
    parser.add_argument(
        "--json",
        type=Path,
        default=resolve_settings_path("AILocationSettings.json"),
        help="Path to AILocationSettings.json.",
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
        help="Do not label location names.",
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
        help="World-coordinate bounds to map the background image onto. "
             "Use this to calibrate a background image that has margins or is not edge-to-edge.",
    )
    args = parser.parse_args()

    if args.json is None:
        raise FileNotFoundError(f"No AILocationSettings.json found under: {MPMISSIONS_DIR}")

    plot_ai_locations(
        json_file_path=args.json,
        output_dir=args.output_dir,
        label_locations=not args.no_labels,
        focus_region=tuple(args.focus_region) if args.focus_region else None,
        background_bounds=tuple(args.background_bounds) if args.background_bounds else None,
    )


if __name__ == "__main__":
    main()
