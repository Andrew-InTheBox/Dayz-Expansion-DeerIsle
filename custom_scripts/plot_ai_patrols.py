import json
import matplotlib.pyplot as plt
from datetime import datetime
import os
import numpy as np

# Get script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Input file path
file_path = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\mpmissions\Expansion.deerisle\expansion\settings\AIPatrolSettings.json'

# Generate output filename with timestamp
output_filename = f"{datetime.now().strftime('%Y%m%d%H%M')}_patrols.png"
output_path = os.path.join(script_dir, output_filename)

# Load the JSON data from the file
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract data for plotting
patrols = data.get("Patrols", [])
plot_data = []

for patrol in patrols:
    name = patrol.get("Name", "Unknown")
    waypoints = patrol.get("Waypoints", [])
    coords = [(wp[0], wp[2]) for wp in waypoints]
    if coords:
        plot_data.append((name, coords))

# Plot the data
plt.figure(figsize=(12, 10))
for name, coords in plot_data:
    x_coords, z_coords = zip(*coords)
    plt.scatter(x_coords, z_coords, label=name)
    
    # Calculate geometric center (centroid) of waypoints
    centroid_x = np.mean(x_coords)
    centroid_z = np.mean(z_coords)
    
    # Add label at the centroid
    plt.annotate(name, 
                (centroid_x, centroid_z),
                xytext=(0, 0), 
                textcoords='offset points',
                ha='center',
                va='center',
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=2),
                fontsize=9)

# Customize the plot
plt.title("Patrol Waypoints (X and Z Coordinates)")
plt.xlabel("X Coordinate")
plt.ylabel("Z Coordinate")
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()

# Save the plot
plt.savefig(output_path, bbox_inches='tight', dpi=300)
plt.close()

print(f"Plot saved as: {output_path}")