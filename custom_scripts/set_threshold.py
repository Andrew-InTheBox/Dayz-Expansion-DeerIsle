import os
import json

def update_stock_thresholds(file_path, max_threshold, min_threshold):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Update thresholds
        for item in data.get("Items", []):
            item["MaxStockThreshold"] = max_threshold
            item["MinStockThreshold"] = min_threshold

        # Write updated data back to file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"Updated {file_path}")

    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from {file_path}: {e}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    directory = './config/ExpansionMod/Market/'
    file_name = 'Snafu_Ammo.json'
    file_path = os.path.join(directory, file_name)
    max_threshold = 1
    min_threshold = 1

    update_stock_thresholds(file_path, max_threshold, min_threshold)
