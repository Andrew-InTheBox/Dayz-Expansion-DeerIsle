import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os
from datetime import datetime, timedelta
import logging
from matplotlib.animation import FuncAnimation, FFMpegWriter
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define paths
base_path = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader'
heatmap_folder = os.path.join(base_path, 'config', 'Heatmap')
background_img_path = os.path.join(base_path, 'custom_scripts', 'deer_isle_background.png')
roamer_plots_dir = os.path.join(base_path, 'custom_scripts', 'roamer_plots')

# Ensure the output directory exists
try:
    os.makedirs(roamer_plots_dir, exist_ok=True)
    logger.info(f"Output directory confirmed: {roamer_plots_dir}")
except Exception as e:
    logger.error(f"Failed to create output directory: {e}")
    raise

# Function to get the newest JSON file from the directory
def get_newest_json_file(directory):
    try:
        json_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]
        if not json_files:
            raise FileNotFoundError("No JSON files found in the given directory.")
        latest_file = max(json_files, key=os.path.getmtime)
        logger.info(f"Found latest JSON file: {latest_file}")
        return latest_file
    except Exception as e:
        logger.error(f"Error finding JSON file: {e}")
        raise

try:
    # Get the newest JSON file
    json_file_path = get_newest_json_file(heatmap_folder)

    # Parse datetime from filename
    filename = os.path.basename(json_file_path)
    datetime_match = re.match(r'autosave_(\d{4})_(\d{2})_(\d{2})_(\d{2})_(\d{2})_Heatmap\.json', filename)
    if datetime_match:
        year, month, day, hour, minute = map(int, datetime_match.groups())
        end_datetime = datetime(year, month, day, hour, minute)
        logger.info(f"Parsed end datetime: {end_datetime}")
    else:
        raise ValueError(f"Could not parse datetime from filename: {filename}")

    # Load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    logger.info("Successfully loaded JSON data")

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    background_img = plt.imread(background_img_path)
    ax.imshow(background_img, extent=[0, 16300, 0, 16300])

    colors = list(mcolors.TABLEAU_COLORS.values())
    
    # Find the maximum length of all paths for animation frames
    max_frames = max(len(path) for path in data['m_AIWayPoints'])
    
    # Calculate start datetime (2 minutes per frame backwards from end_datetime)
    start_datetime = end_datetime - timedelta(minutes=2 * (max_frames - 1))
    logger.info(f"Calculated start datetime: {start_datetime}")

    # Initialize empty line and point collections for each path
    lines = []
    points = []
    for i, waypoints in enumerate(data['m_AIWayPoints']):
        color = colors[i % len(colors)]
        # Create empty line
        line, = ax.plot([], [], 
                       linestyle='-',
                       linewidth=2,
                       color=color,
                       alpha=0.7)
        lines.append(line)
        # Create empty point
        point, = ax.plot([], [],
                        marker='o',
                        markersize=6,
                        markeredgewidth=2,
                        color=color)
        points.append(point)

    ax.set_xlim(0, 16300)
    ax.set_ylim(0, 16300)
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    
    # Create main title and subtitle with better spacing
    main_title = ax.set_title('AI Waypoints Progress on Deer Isle Map', pad=30, y=1.05)
    subtitle = ax.text(0.5, 1.02, '', horizontalalignment='center', transform=ax.transAxes)

    # Animation update function
    def update(frame):
        # Calculate current datetime for this frame
        current_datetime = start_datetime + timedelta(minutes=2 * frame)
        subtitle.set_text(current_datetime.strftime('%Y-%m-%d %H:%M'))

        for i, waypoints in enumerate(data['m_AIWayPoints']):
            waypoints = np.array(waypoints)
            
            # Only show up to current frame number of points
            current_points = min(frame + 1, len(waypoints))
            
            if current_points > 0:
                # Update line data
                lines[i].set_data(
                    waypoints[:current_points, 0],
                    waypoints[:current_points, 2]
                )
                # Update current position point
                points[i].set_data(
                    [waypoints[current_points-1, 0]],
                    [waypoints[current_points-1, 2]]
                )
            else:
                lines[i].set_data([], [])
                points[i].set_data([], [])
        
        return lines + points + [subtitle]

    fig.set_dpi(150)

    # Create animation
    animation = FuncAnimation(
        fig,
        update,
        frames=max_frames,
        interval=250,  # 250ms between frames
        blit=True,
        repeat=True
    )

    # Save animation as MP4
    datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_mp4_path = os.path.join(roamer_plots_dir, f"roamer_animation_{datetime_str}.mp4")
    
    writer = FFMpegWriter(
        fps=4,  # frames per second
        metadata=dict(artist='DayZ Roamer Plot'),
        bitrate=2000  # Controlling video quality (2000 kbps)
    )
    animation.save(output_mp4_path, writer=writer)
    
    plt.close()
    logger.info(f"Successfully saved animation to: {output_mp4_path}")

except Exception as e:
    logger.error(f"An error occurred: {e}")
    raise