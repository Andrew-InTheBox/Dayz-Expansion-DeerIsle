import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import os
from datetime import datetime
import logging

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

    # Load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    logger.info("Successfully loaded JSON data")

    # Load the background image
    background_img = plt.imread(background_img_path)
    logger.info("Successfully loaded background image")

    # Plot settings
    plt.figure(figsize=(12, 12))
    plt.imshow(background_img, extent=[0, 16300, 0, 16300])

    colors = list(mcolors.TABLEAU_COLORS.values())

    # Plot each array of AI waypoints
    for i, waypoints in enumerate(data['m_AIWayPoints']):
        waypoints = np.array(waypoints)
        plt.plot(
            waypoints[:, 0], waypoints[:, 2],
            marker='o', 
            linestyle='-', 
            markersize=5,       # Increased from 5 to 12
            markeredgewidth=2,   # Added edge width to markers
            linewidth=2,
            color=colors[i % len(colors)], 
            alpha=0.7
        )

    plt.xlim(0, 16300)
    plt.ylim(0, 16300)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('AI Waypoints on Deer Isle Map')

    # Save the plot
    datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_image_path = os.path.join(roamer_plots_dir, f"roamer_plots_{datetime_str}.png")
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Successfully saved plot to: {output_image_path}")

except Exception as e:
    logger.error(f"An error occurred: {e}")
    raise