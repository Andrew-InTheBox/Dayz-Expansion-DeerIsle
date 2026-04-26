import json
import os

IGNORE_FILES = [
    "FireFighterLoadout.json",
    "PlayerFemaleSuitLoadout.json",
    "PlayerMaleSuitLoadout.json",
    "PlayerSurvivorLoadout.json"
]

def duplicate_ammo_entry(json_file, ammo_classname):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    changes_made = 0

    def duplicate_entry_recursive(item):
        nonlocal changes_made
        modifications_made = False

        if isinstance(item, list):
            # Use a separate index because we'll be modifying the list
            i = 0
            while i < len(item):
                entry = item[i]
                if isinstance(entry, dict):
                    # Check if this is an ammo entry
                    if entry.get("ClassName") == ammo_classname:
                        # Create a duplicate of the entry
                        duplicate = entry.copy()
                        # Set quantity and chance to 1.0
                        duplicate["Quantity"] = {
                            "Min": 1.0,
                            "Max": 1.0
                        }
                        duplicate["Chance"] = 1.0
                        # Insert the duplicate right after the original entry
                        item.insert(i + 1, duplicate)
                        changes_made += 1
                        modifications_made = True
                        i += 2  # Skip over both the original and the duplicate
                        continue
                    
                    # Continue searching through nested structures
                    if duplicate_entry_recursive(entry):
                        modifications_made = True
                
                i += 1
                        
        elif isinstance(item, dict):
            for value in item.values():
                if isinstance(value, (dict, list)):
                    if duplicate_entry_recursive(value):
                        modifications_made = True

        return modifications_made

    # Start the recursive search from the root of the JSON
    if duplicate_entry_recursive(data):
        # Write the modified JSON back to the file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Duplicated {changes_made} {ammo_classname} entries in {json_file}")
    else:
        print(f"No {ammo_classname} entries found in {json_file}")

def process_directory(directory_path, ammo_classname):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # Skip files in the ignore list
            if file in IGNORE_FILES:
                print(f"Skipping ignored file: {file}")
                continue
                
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                try:
                    duplicate_ammo_entry(json_file, ammo_classname)
                except Exception as e:
                    print(f"Error processing {json_file}: {str(e)}")

# Usage
directory_path = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerSakhal\config\ExpansionMod\Loadouts'
ammo_classname = "Ammo_556x45"
process_directory(directory_path, ammo_classname)
