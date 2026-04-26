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
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
heatmap_folder = os.path.join(base_path, 'config', 'Heatmap')
background_img_path = os.path.join(base_path, 'custom_scripts', 'assets', 'deer_isle_background.png')
roamer_plots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

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
    datetime_match = re.match(r'autosave_(\d{4})_(\d{1,2})_(\d{1,2})_(\d{1,2})_(\d{1,2})_Heatmap\.json', filename)
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
    fig, ax = plt.subplots(figsize=(10, 8))  # Increased figure size to accommodate legend
    background_img = plt.imread(background_img_path)
    ax.imshow(background_img, extent=[0, 16300, 0, 16300])

    colors = list(mcolors.TABLEAU_COLORS.values())
    
    # Find the maximum length of all paths for animation frames
    ai_max_frames = max(len(path) for path in data['m_AIWayPoints'])
    player_max_frames = max(len(path) for path in data['m_WayPoints']) if data['m_WayPoints'] else 0
    max_frames = max(ai_max_frames, player_max_frames)
    
    # Calculate start datetime (2 minutes per frame backwards from end_datetime)
    start_datetime = end_datetime - timedelta(minutes=2 * (max_frames - 1))
    logger.info(f"Calculated start datetime: {start_datetime}")

    # Initialize empty line and point collections for AI paths
    ai_lines = []
    ai_points = [] 
    for i, waypoints in enumerate(data['m_AIWayPoints']):
        color = colors[i % len(colors)]
        # Create empty line for AI
        line, = ax.plot([], [], 
                       linestyle='-',
                       linewidth=2,
                       color=color,
                       alpha=0.7) # Removed label for AI bots
        ai_lines.append(line)
        # Create empty point for AI
        point, = ax.plot([], [],
                        marker='o',
                        markersize=6,
                        markeredgewidth=2,
                        color=color)
        ai_points.append(point)

    # Initialize empty line and point collections for player paths with labels
    player_lines = []
    player_points = []
    for i, waypoints in enumerate(data['m_WayPoints']):
        color = colors[(i + len(data['m_AIWayPoints'])) % len(colors)]
        # Create empty line for player
        line, = ax.plot([], [], 
                       linestyle='--',  # Dashed line for players
                       linewidth=2,
                       color=color,
                       alpha=0.7,
                       label=f'Player {i+1}')  # Keep label for players only
        player_lines.append(line)
        # Create empty point for player
        point, = ax.plot([], [],
                        marker='*',  # Star marker for players
                        markersize=12,  # Larger marker
                        markeredgewidth=2,
                        color=color)
        player_points.append(point)

    # Add legend for players only
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))

    ax.set_xlim(0, 16300)
    ax.set_ylim(0, 16300)
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    
    # Create main title and subtitle with better spacing
    main_title = ax.set_title('AI and Player Movement on Deer Isle Map', pad=30, y=1.05)
    subtitle = ax.text(0.5, 1.02, '', horizontalalignment='center', transform=ax.transAxes)

    # Add grey color for inactive entities
    inactive_color = '#808080'  # Grey color for inactive entities

    # Animation update function
    def update(frame):
        current_datetime = start_datetime + timedelta(minutes=2 * frame)
        subtitle.set_text(current_datetime.strftime('%Y-%m-%d %H:%M'))

        # Update AI positions
        for i, waypoints in enumerate(data['m_AIWayPoints']):
            waypoints = np.array(waypoints)
            current_points = min(frame + 1, len(waypoints))
            
            if current_points > 0:
                # Check if AI has reached its final position
                is_inactive = current_points >= len(waypoints)
                current_color = inactive_color if is_inactive else colors[i % len(colors)]
                
                # Update line
                ai_lines[i].set_data(
                    waypoints[:current_points, 0],
                    waypoints[:current_points, 2]
                )
                ai_lines[i].set_color(current_color)
                ai_lines[i].set_alpha(0.4 if is_inactive else 0.7)
                
                # Update point
                ai_points[i].set_data(
                    [waypoints[current_points-1, 0]],
                    [waypoints[current_points-1, 2]]
                )
                ai_points[i].set_color(current_color)
                ai_points[i].set_alpha(0.4 if is_inactive else 1.0)
            else:
                ai_lines[i].set_data([], [])
                ai_points[i].set_data([], [])

        # Update player positions
        for i, waypoints in enumerate(data['m_WayPoints']):
            waypoints = np.array(waypoints)
            current_points = min(frame + 1, len(waypoints))
            
            if current_points > 0:
                player_lines[i].set_data(
                    waypoints[:current_points, 0],
                    waypoints[:current_points, 2]
                )
                player_points[i].set_data(
                    [waypoints[current_points-1, 0]],
                    [waypoints[current_points-1, 2]]
                )
            else:
                player_lines[i].set_data([], [])
                player_points[i].set_data([], [])
        
        return ai_lines + ai_points + player_lines + player_points + [subtitle]

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
    output_mp4_path = os.path.join(roamer_plots_dir, f"movement_animation_{datetime_str}.mp4")
    
    writer = FFMpegWriter(
        fps=4,  # frames per second
        metadata=dict(artist='DayZ Movement Plot'),
        bitrate=2000  # Controlling video quality (2000 kbps)
    )
    animation.save(output_mp4_path, writer=writer)
    
    plt.close()
    logger.info(f"Successfully saved animation to: {output_mp4_path}")

except Exception as e:
    logger.error(f"An error occurred: {e}")
    raise