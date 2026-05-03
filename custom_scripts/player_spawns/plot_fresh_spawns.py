#!/usr/bin/env python3
"""
Plot fresh player spawn bubbles from cfgplayerspawnpoints.xml on the Deer Isle map.
"""

import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


SCRIPT_DIR = Path(__file__).resolve().parent
CUSTOM_SCRIPTS_DIR = SCRIPT_DIR.parent
SERVER_DIR = CUSTOM_SCRIPTS_DIR.parent
MPMISSIONS_DIR = SERVER_DIR / "mpmissions"
PREFERRED_MISSION_DIR = MPMISSIONS_DIR / "Expansion.deerisle"

DEFAULT_MAP_SIZE = 16400.0
DEFAULT_EXTENT = (0.0, DEFAULT_MAP_SIZE, 0.0, DEFAULT_MAP_SIZE)
DEFAULT_BACKGROUND_IMAGE = CUSTOM_SCRIPTS_DIR / "assets" / "deer_isle_background.png"
DEFAULT_BACKGROUND_WORLD_BOUNDS = DEFAULT_EXTENT


def resolve_spawnpoints_path():
    preferred = PREFERRED_MISSION_DIR / "cfgplayerspawnpoints.xml"
    if preferred.exists():
        return preferred

    candidates = sorted(MPMISSIONS_DIR.glob("*/cfgplayerspawnpoints.xml"))
    return candidates[0] if candidates else None


def load_spawn_bubbles(xml_file_path, section="fresh"):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    points = []
    for index, pos in enumerate(root.findall(f"./{section}/generator_posbubbles/pos"), start=1):
        points.append(
            {
                "index": index,
                "x": float(pos.attrib["x"]),
                "z": float(pos.attrib["z"]),
            }
        )

    generator_params = root.find(f"./{section}/generator_params")
    grid_width = 40.0
    grid_height = 40.0
    if generator_params is not None:
        width_node = generator_params.find("grid_width")
        height_node = generator_params.find("grid_height")
        if width_node is not None and width_node.text:
            grid_width = float(width_node.text)
        if height_node is not None and height_node.text:
            grid_height = float(height_node.text)

    return points, grid_width, grid_height


def plot_spawn_bubbles(
    xml_file_path,
    output_dir,
    section="fresh",
    label_points=True,
    focus_region=None,
    background_bounds=None,
):
    points, grid_width, grid_height = load_spawn_bubbles(xml_file_path, section)
    if not points:
        print(f"No {section} spawn bubbles found in: {xml_file_path}")
        return

    fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
    image_bounds = background_bounds if background_bounds is not None else DEFAULT_BACKGROUND_WORLD_BOUNDS

    if DEFAULT_BACKGROUND_IMAGE.exists():
        background = plt.imread(DEFAULT_BACKGROUND_IMAGE)
        ax.imshow(background, extent=image_bounds, origin="upper")
    else:
        print(f"Background image not found: {DEFAULT_BACKGROUND_IMAGE}")

    half_width = grid_width / 2.0
    half_height = grid_height / 2.0
    for point in points:
        rect = Rectangle(
            (point["x"] - half_width, point["z"] - half_height),
            grid_width,
            grid_height,
            fill=False,
            edgecolor="dodgerblue",
            linewidth=1.1,
            alpha=0.85,
            zorder=4,
        )
        ax.add_patch(rect)

    ax.scatter(
        [point["x"] for point in points],
        [point["z"] for point in points],
        c="deepskyblue",
        s=24,
        alpha=0.9,
        edgecolors="black",
        linewidth=0.45,
        zorder=5,
    )

    if label_points:
        for point in points:
            ax.annotate(
                str(point["index"]),
                (point["x"], point["z"]),
                fontsize=6,
                xytext=(3, 3),
                textcoords="offset points",
                bbox=dict(facecolor="white", alpha=0.75, edgecolor="none", pad=1.2),
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
    ax.set_title(f"Deer Isle {section.title()} Player Spawn Bubbles")

    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    output_path = Path(output_dir) / f"PlayerSpawnBubbles-{section}-{timestamp}.png"

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Plot saved to: {output_path}")
    print(f"Total {section} spawn bubbles plotted: {len(points)}")
    print(f"Spawn bubble grid size: {grid_width:g}m x {grid_height:g}m")


def main():
    parser = ArgumentParser(description="Plot player spawn bubbles for Deer Isle.")
    parser.add_argument(
        "--xml",
        type=Path,
        default=resolve_spawnpoints_path(),
        help="Path to cfgplayerspawnpoints.xml.",
    )
    parser.add_argument(
        "--section",
        default="fresh",
        choices=("fresh", "hop", "travel"),
        help="Spawn point section to plot.",
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
        help="Do not label spawn bubbles.",
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
        raise FileNotFoundError(f"No cfgplayerspawnpoints.xml found under: {MPMISSIONS_DIR}")

    plot_spawn_bubbles(
        xml_file_path=args.xml,
        output_dir=args.output_dir,
        section=args.section,
        label_points=not args.no_labels,
        focus_region=tuple(args.focus_region) if args.focus_region else None,
        background_bounds=tuple(args.background_bounds) if args.background_bounds else None,
    )


if __name__ == "__main__":
    main()
