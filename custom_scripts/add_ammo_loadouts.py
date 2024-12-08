import json
import os

IGNORE_FILES = [
    "FireFighterLoadout.json",
    "PlayerFemaleSuitLoadout.json",
    "PlayerMaleSuitLoadout.json",
    "PlayerSurvivorLoadout.json"
]

def create_ammo_entry(classname):
    # Template for ammo entry
    return {
        "ClassName": classname,
        "Include": "",
        "Chance": 1.0,  # You can adjust this value
        "Quantity": {
            "Min": 1.0,  # You can adjust this value
            "Max": 1.0   # You can adjust this value
        },
        "Health": [
            {
                "Min": 1.0,
                "Max": 1.0,
                "Zone": ""
            }
        ],
        "InventoryAttachments": [],
        "InventoryCargo": [],
        "ConstructionPartsBuilt": [],
        "Sets": []
    }

def get_ammo_types(ammo_list_file):
    with open(ammo_list_file, 'r') as file:
        content = file.read()
        # Split by comma and strip whitespace
        ammo_types = [ammo.strip() for ammo in content.split(',')]
    return ammo_types

def add_ammo_entries(json_file, ammo_types):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Create ammo entries for each type
    ammo_entries = [create_ammo_entry(ammo_type) for ammo_type in ammo_types]

    # Function to recursively search for guaranteed spawn clothing items in the Body slot 
    def add_ammo_recursive(item):
        if isinstance(item, dict):
            # Check if this is a Body slot with Items
            if (item.get("SlotName") == "Body" and 
                "Items" in item):
                # Add ammo to each guaranteed spawn clothing item
                items_modified = False
                for clothing_item in item["Items"]:
                    # Only add to items with 100% spawn chance
                    if clothing_item.get("Chance") == 1.0:
                        if "InventoryCargo" not in clothing_item:
                            clothing_item["InventoryCargo"] = []
                        # Only add if ammo entries don't already exist
                        if not any(entry["ClassName"] in ammo_types for entry in clothing_item["InventoryCargo"]):
                            clothing_item["InventoryCargo"].extend(ammo_entries)
                            items_modified = True
                return items_modified

            # Continue searching through all keys
            for key, value in item.items():
                if isinstance(value, (dict, list)):
                    if add_ammo_recursive(value):
                        return True
                        
        elif isinstance(item, list):
            for sub_item in item:
                if add_ammo_recursive(sub_item):
                    return True
        return False

    # Start the recursive search from the root of the JSON
    if add_ammo_recursive(data):
        # Write the modified JSON back to the file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Added ammo entries to {json_file}")
    else:
        print(f"No eligible Body slots found in {json_file}")

def process_directory(directory_path, ammo_list_file):
    # Get list of ammo types
    ammo_types = get_ammo_types(ammo_list_file)
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # Skip files in the ignore list
            if file in IGNORE_FILES:
                print(f"Skipping ignored file: {file}")
                continue
                
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                try:
                    add_ammo_entries(json_file, ammo_types)
                except Exception as e:
                    print(f"Error processing {json_file}: {str(e)}")

# Usage
directory_path = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerSakhal\config\ExpansionMod\Loadouts'
ammo_list_file = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerSakhal\custom_scripts\ammo_list.txt'
process_directory(directory_path, ammo_list_file)
