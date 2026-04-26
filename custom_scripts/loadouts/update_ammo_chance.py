import json
import os

def update_ammo_chance(json_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Function to recursively search and update ammo chances
    def update_ammo_recursive(item):
        if isinstance(item, dict):
            if "ClassName" in item and "ammo" in item["ClassName"].lower():
                item["Chance"] = 0.33
            for value in item.values():
                update_ammo_recursive(value)
        elif isinstance(item, list):
            for sub_item in item:
                update_ammo_recursive(sub_item)

    # Start the recursive search from the root of the JSON
    update_ammo_recursive(data)

    # Write the modified JSON back to the file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Updated ammo chances in {json_file}")

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                try:
                    update_ammo_chance(json_file)
                except Exception as e:
                    print(f"Error processing {json_file}: {str(e)}")

# Usage
directory_path = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\config\ExpansionMod\Loadouts'
process_directory(directory_path)
