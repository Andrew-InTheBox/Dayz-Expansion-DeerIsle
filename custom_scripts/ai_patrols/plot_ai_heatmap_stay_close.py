import json
import math
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


# Get script directory
script_dir = Path(__file__).resolve().parent

# Inputs (relative to repo root)
heatmap_dir = script_dir.parents[1] / 'config' / 'Heatmap'
background_image_path = script_dir.parent / 'assets' / 'hashima-map-background.png'

# Map extent for background image (min_x, max_x, min_z, max_z) in meters
background_extent = (0, 5200, 0, 5200)

# Analysis settings
max_radius_m = 120.0

# Output file
output_filename = f"{datetime.now().strftime('%Y%m%d%H%M')}_ai_tracks_within_{int(max_radius_m)}m.png"
output_path = script_dir / 'output' / output_filename


def iter_ai_tracks(heatmap_path):
    with open(heatmap_path, 'r') as file:
        data = json.load(file)
    ai_tracks = data.get('m_AIWayPoints', [])
    for track_index, track in enumerate(ai_tracks):
        if not track:
            continue
        yield track_index, track


def track_within_radius(track, radius_m):
    if len(track) < 2:
        return False
    # Use first point as spawn location
    first = track[0]
    if len(first) < 3:
        return False
    origin_x, origin_z = first[0], first[2]

    for point in track:
        if len(point) < 3:
            continue
        dx = point[0] - origin_x
        dz = point[2] - origin_z
        if math.hypot(dx, dz) > radius_m:
            return False
    return True


def main():
    if not heatmap_dir.exists():
        raise FileNotFoundError(f"Heatmap directory not found: {heatmap_dir}")

    qualifying_tracks = []
    total_tracks = 0

    # Use the most recent heatmap file larger than 20KB
    heatmap_files = [p for p in heatmap_dir.glob('*.json') if p.is_file()]
    large_files = [p for p in heatmap_files if p.stat().st_size > 20 * 1024]
    if not large_files:
        raise FileNotFoundError(
            f"No heatmap JSON files larger than 20KB found in: {heatmap_dir}"
        )
    heatmap_path = max(large_files, key=lambda p: p.stat().st_mtime)
    print(f"Using heatmap file: {heatmap_path.name}")

    for track_index, track in iter_ai_tracks(heatmap_path):
        total_tracks += 1
        if track_within_radius(track, max_radius_m):
            qualifying_tracks.append((heatmap_path.name, track_index, track))

    print(f"Total AI tracks found: {total_tracks}")
    print(f"Tracks within {max_radius_m}m: {len(qualifying_tracks)}")

    fig, ax = plt.subplots(figsize=(12, 10))

    # Draw background image if present
    if background_image_path.exists():
        bg = plt.imread(background_image_path)
        ax.imshow(
            bg,
            extent=background_extent,
            origin='upper'
        )
    else:
        print(f"Background image not found: {background_image_path}")

    # Plot qualifying tracks
    for _, _, track in qualifying_tracks:
        xs = []
        zs = []
        for point in track:
            if len(point) < 3:
                continue
            xs.append(point[0])
            zs.append(point[2])
        if len(xs) >= 2:
            ax.plot(xs, zs, color='blue', linewidth=1.5, alpha=0.7)
        elif len(xs) == 1:
            ax.scatter(xs, zs, color='blue', s=10, alpha=0.7)

    ax.set_title(f"AI Tracks Staying Within {int(max_radius_m)}m of Spawn")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Z Coordinate")
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(background_extent[0], background_extent[1])
    ax.set_ylim(background_extent[2], background_extent[3])
    ax.grid(True)

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"Plot saved as: {output_path}")


if __name__ == '__main__':
    main()
