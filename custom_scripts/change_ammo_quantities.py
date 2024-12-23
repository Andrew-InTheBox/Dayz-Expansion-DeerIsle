import json
import os
import argparse

def modify_ammo_quantities(json_file):
    # Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Function to recursively search and modify ammo entries
    def modify_ammo_recursive(item):
        modified = False
        if isinstance(item, dict):
            # Check if this is an ammo entry
            if "ClassName" in item and isinstance(item["ClassName"], str) and item["ClassName"].startswith("Ammo"):
                if "Quantity" in item:
                    item["Quantity"]["Min"] = 0.6
                    item["Quantity"]["Max"] = 0.8
                    modified = True

            # Continue searching through all keys
            for key, value in item.items():
                if isinstance(value, (dict, list)):
                    if modify_ammo_recursive(value):
                        modified = True
                        
        elif isinstance(item, list):
            for sub_item in item:
                if modify_ammo_recursive(sub_item):
                    modified = True
                    
        return modified

    # Start the recursive search from the root of the JSON
    if modify_ammo_recursive(data):
        # Write the modified JSON back to the file
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Modified ammo quantities in {json_file}")
    else:
        print(f"No ammo entries found in {json_file}")

def process_directory(directory_path, target_file=None):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # If target file is specified, only process that file
            if target_file and file != target_file:
                continue
                
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                try:
                    modify_ammo_quantities(json_file)
                except Exception as e:
                    print(f"Error processing {json_file}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Modify ammo quantities in DayZ configuration files.')
    parser.add_argument('--directory', '-d', 
                        default=r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\config\ExpansionMod\Loadouts',
                        help='Directory containing loadout files')
    parser.add_argument('--file', '-f', help='Specific JSON file to process (filename only)')

    args = parser.parse_args()

    process_directory(
        args.directory,
        target_file=args.file
    )

if __name__ == "__main__":
    main()