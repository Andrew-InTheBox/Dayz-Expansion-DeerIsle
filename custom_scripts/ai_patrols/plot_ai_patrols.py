import json
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from datetime import datetime
from pathlib import Path
import numpy as np
from argparse import ArgumentParser

# Get script directory
script_dir = Path(__file__).resolve().parent

# Input file paths (relative to repo root; prefer Deer Isle for this server)
mpmissions_dir = script_dir.parents[1] / 'mpmissions'
preferred_mission_dir = mpmissions_dir / 'Expansion.deerisle'

DEFAULT_MAP_SIZE = 16400.0
DEFAULT_EXTENT = (0.0, DEFAULT_MAP_SIZE, 0.0, DEFAULT_MAP_SIZE)
DEFAULT_BACKGROUND_IMAGE = script_dir.parent / 'assets' / 'deer_isle_background.png'
# The image pixel dimensions do not need to match the DayZ world size.
# Matplotlib stretches the image into these world coordinates via `extent`.
# Deer Isle's world coordinate range is 0..16400 meters on X and Z, so the
# background should occupy the same extent as the raw patrol coordinates.
DEFAULT_BACKGROUND_WORLD_BOUNDS = DEFAULT_EXTENT


def resolve_settings_path(filename):
    preferred = preferred_mission_dir / 'expansion' / 'settings' / filename
    if preferred.exists():
        return preferred

    candidates = sorted(mpmissions_dir.glob(f'*/expansion/settings/{filename}'))
    return candidates[0] if candidates else None

# Generate output filename with timestamp
output_filename = f"{datetime.now().strftime('%Y%m%d%H%M')}_patrols.png"
output_path = script_dir / 'output' / output_filename

def main():
    parser = ArgumentParser(description="Plot AI patrol waypoints and AI location radii.")
    parser.add_argument(
        "--locations-only",
        action="store_true",
        help="Plot only AILocationSettings.json circles and label them by Name.",
    )
    parser.add_argument(
        "--label-locations",
        action="store_true",
        help="Label AILocationSettings.json circles by Name while still plotting patrol data.",
    )
    parser.add_argument(
        "--label-locations-instead-of-patrols",
        action="store_true",
        help="Label AILocationSettings.json circles by Name and suppress AIPatrolSettings.json labels.",
    )
    parser.add_argument(
        "--no-location-circles",
        action="store_true",
        help="Do not draw AILocationSettings.json circles.",
    )
    parser.add_argument(
        "--no-patrol-labels",
        action="store_true",
        help="Do not draw patrol name labels.",
    )
    parser.add_argument(
        "--focus-region",
        nargs=4,
        type=float,
        metavar=("MIN_X", "MAX_X", "MIN_Z", "MAX_Z"),
        help="Zoom to a specific map region.",
    )
    parser.add_argument(
        "--focus-center",
        nargs=2,
        type=float,
        metavar=("X", "Z"),
        help="Center point for zoom region.",
    )
    parser.add_argument(
        "--focus-size",
        nargs=2,
        type=float,
        metavar=("WIDTH", "HEIGHT"),
        help="Width/height for --focus-center region in meters (default: 800 800).",
    )
    parser.add_argument(
        "--background-bounds",
        nargs=4,
        type=float,
        metavar=("MIN_X", "MAX_X", "MIN_Z", "MAX_Z"),
        help="World-coordinate bounds to map the background image onto. "
             "Defaults to the full Deer Isle 0..16400m X/Z coordinate range.",
    )
    parser.add_argument(
        "--offset",
        nargs=2,
        type=float,
        metavar=("DX", "DZ"),
        default=(0.0, 0.0),
        help="Offset to apply to plotted X/Z coordinates after reading them.",
    )
    args = parser.parse_args()

    if args.label_locations_instead_of_patrols:
        args.label_locations = True
        args.no_patrol_labels = True

    if args.focus_region and args.focus_center:
        parser.error("Use either --focus-region or --focus-center, not both.")

    if args.focus_size and not args.focus_center:
        parser.error("--focus-size requires --focus-center.")

    background_bounds = tuple(args.background_bounds) if args.background_bounds else DEFAULT_BACKGROUND_WORLD_BOUNDS
    dx, dz = args.offset

    patrol_file_path = None
    if not args.locations_only:
        patrol_file_path = resolve_settings_path('AIPatrolSettings.json')
        if patrol_file_path is None:
            raise FileNotFoundError(
                f"No AIPatrolSettings.json found under: {mpmissions_dir}"
            )

    ai_locations_path = None if args.no_location_circles else resolve_settings_path('AILocationSettings.json')
    if ai_locations_path is None and args.locations_only:
        raise FileNotFoundError(
            f"No AILocationSettings.json found under: {mpmissions_dir}"
        )

    plot_data = []
    if patrol_file_path is not None:
        with open(patrol_file_path, 'r') as file:
            data = json.load(file)

        patrols = data.get("Patrols", [])
        for patrol in patrols:
            name = patrol.get("Name", "Unknown")
            waypoints = patrol.get("Waypoints", [])
            coords = [(wp[0] + dx, wp[2] + dz) for wp in waypoints if len(wp) >= 3]
            if coords:
                plot_data.append((name, coords))

    ai_locations = []
    if ai_locations_path is not None:
        with open(ai_locations_path, 'r') as file:
            locations_data = json.load(file)
        ai_locations = locations_data.get('RoamingLocations', [])

    # Plot the data
    fig, ax = plt.subplots(figsize=(12, 10))

    # Draw background image if present
    if DEFAULT_BACKGROUND_IMAGE.exists():
        bg = plt.imread(DEFAULT_BACKGROUND_IMAGE)
        ax.imshow(
            bg,
            extent=background_bounds,
            origin='upper'
        )
    else:
        print(f"Background image not found: {DEFAULT_BACKGROUND_IMAGE}")

    for name, coords in plot_data:
        x_coords, z_coords = zip(*coords)
        ax.scatter(x_coords, z_coords, label=name)

        # Calculate geometric center (centroid) of waypoints
        centroid_x = np.mean(x_coords)
        centroid_z = np.mean(z_coords)

        if not args.no_patrol_labels:
            # Add patrol label at the centroid
            ax.annotate(name,
                        (centroid_x, centroid_z),
                        xytext=(0, 6),
                        textcoords='offset points',
                        ha='center',
                        va='bottom',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2),
                        fontsize=6)

    # Overlay AI location radii (open red circles)
    if ai_locations:
        for location in ai_locations:
            position = location.get('Position', [])
            radius = location.get('Radius', 0)
            name = location.get('Name', 'Unknown')
            if len(position) >= 3 and radius > 0:
                circle = Circle(
                    (position[0] + dx, position[2] + dz),
                    radius,
                    fill=False,
                    edgecolor='red',
                    linewidth=1.0,
                    alpha=0.8
                )
                ax.add_patch(circle)
                if args.locations_only or args.label_locations:
                    ax.annotate(
                        name,
                        (position[0] + dx, position[2] + dz),
                        xytext=(0, 6),
                        textcoords='offset points',
                        ha='center',
                        va='bottom',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2),
                        fontsize=6
                    )

    # Customize the plot
    ax.set_title("Deer Isle AI Patrols and Roaming Areas")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Z Coordinate")
    if plot_data:
        ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')
    if args.focus_region:
        min_x, max_x, min_z, max_z = args.focus_region
    elif args.focus_center:
        width, height = (args.focus_size if args.focus_size else (800.0, 800.0))
        center_x, center_z = args.focus_center
        min_x = center_x - (width / 2.0)
        max_x = center_x + (width / 2.0)
        min_z = center_z - (height / 2.0)
        max_z = center_z + (height / 2.0)
    else:
        min_x, max_x, min_z, max_z = background_bounds

    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_z, max_z)
    plt.tight_layout()

    # Save the plot
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"Plot saved as: {output_path}")


if __name__ == '__main__':
    main()
