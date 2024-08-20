import json
import os

def add_ammo_entry(json_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # New ammo entry to add
    new_ammo = {
        "ClassName": "ammo_expansion_338",
        "Chance": 0.45,
        "Quantity": {
            "Min": 0.2,
            "Max": 0.5
        },
        "Health": [
            {
                "Min": 1.0,
                "Max": 1.0,
                "Zone": ""
            }
        ]
    }

    # Function to recursively search and add the new ammo entry
    def add_ammo_recursive(item):
        if isinstance(item, dict):
            if "ClassName" in item and item["ClassName"] == "AmmoBox_308Win_20Rnd":
                return True
            for key, value in item.items():
                if isinstance(value, list):
                    for i, sub_item in enumerate(value):
                        if add_ammo_recursive(sub_item):
                            value.insert(i + 1, new_ammo)
                            return False
        elif isinstance(item, list):
            for sub_item in item:
                if add_ammo_recursive(sub_item):
                    return True
        return False

    # Start the recursive search from the root of the JSON
    add_ammo_recursive(data)

    # Write the modified JSON back to the file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Added new ammo entry to {json_file}")

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                try:
                    add_ammo_entry(json_file)
                except Exception as e:
                    print(f"Error processing {json_file}: {str(e)}")

# Usage
directory_path = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\config\ExpansionMod\Loadouts'
process_directory(directory_path)
