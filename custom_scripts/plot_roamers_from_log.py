import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import glob
from datetime import datetime

def get_newest_log_file(log_dir):
    # Get all ExpLog files in the directory
    log_pattern = os.path.join(log_dir, 'ExpLog_*.log')
    log_files = glob.glob(log_pattern)
    
    if not log_files:
        raise FileNotFoundError("No log files found in specified directory")
    
    # Get the most recent file
    newest_log = max(log_files, key=os.path.getctime)
    return newest_log

def extract_datetime_from_filename(filepath):
    # Extract datetime string from filename (ExpLog_2025-02-01_16-01-25.log)
    filename = os.path.basename(filepath)
    date_time_str = filename.replace('ExpLog_', '').replace('.log', '')
    # Parse the datetime string
    dt = datetime.strptime(date_time_str, '%Y-%m-%d_%H-%M-%S')
    return dt

def plot_ai_patrol_coords(log_file_path, map_image_path, output_dir, dot_color='yellow', scale=16365):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read log file
    with open(log_file_path, 'r') as file:
        log_data = file.read()

    # Extract coordinates using regex
    coordinates = re.findall(r'<(\d+\.\d+),\s*(-?\d+\.\d+),\s*(\d+\.\d+)>', log_data)

    # Convert to float and separate X and Y (Y represented by third value)
    x_coords = [float(coord[0]) for coord in coordinates]
    y_coords = [float(coord[2]) for coord in coordinates]

    # Load map image
    img = mpimg.imread(map_image_path)

    # Get formatted datetime for title
    dt = extract_datetime_from_filename(log_file_path)
    formatted_datetime = dt.strftime('%m/%d/%Y %H:%M')

    # Plotting with background map
    plt.figure(figsize=(10, 10))
    plt.imshow(img, extent=[0, scale, 0, scale])
    plt.scatter(x_coords, y_coords, color=dot_color, marker='o')
    plt.title(f'AI Patrol Coordinates - {formatted_datetime}\n({dot_color.capitalize()} Dots, Scaled to {scale})')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.xlim(0, scale)
    plt.ylim(0, scale)
    plt.grid(False)

    # Generate output filename using datetime from log filename
    output_filename = f'roamer_plot_{dt.strftime("%Y-%m-%d_%H-%M-%S")}.png'
    output_path = os.path.join(output_dir, output_filename)
    
    # Save the plot
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def main():
    # Define paths
    log_dir = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\config\ExpansionMod\Logs'
    map_image_path = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\custom_scripts\deer_isle_background.png'  # Update this path
    output_dir = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\custom_scripts\roamer_plots'

    try:
        # Get the newest log file
        newest_log = get_newest_log_file(log_dir)
        
        # Generate and save the plot
        output_path = plot_ai_patrol_coords(
            newest_log,
            map_image_path,
            output_dir,
            dot_color='yellow',
            scale=16365
        )
        print(f"Plot saved successfully to: {output_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()