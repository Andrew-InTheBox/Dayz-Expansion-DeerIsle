import json
import os
import sys

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {file_path}: {str(e)}")
        return None

def save_json(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Successfully saved data to {file_path}")
    except Exception as e:
        print(f"Error saving to {file_path}: {str(e)}")

import re

def match_weapons_and_mags(weapons_data, mags_data):
    if not weapons_data or not mags_data:
        print("Error: Weapons or mags data is None")
        return None

    weapon_classnames = [item['ClassName'] for item in weapons_data['Items']]
    mag_classnames = [item['ClassName'] for item in mags_data['Items']]

    for weapon in weapons_data['Items']:
        weapon_name = weapon['ClassName'].replace('SNAFU', '').replace('_GUN', '')
        matching_mags = []

        # Create a regex pattern to match the weapon name more precisely
        pattern = re.compile(rf"{re.escape(weapon_name)}.*?Mag", re.IGNORECASE)

        for mag in mag_classnames:
            if pattern.search(mag):
                matching_mags.append(mag)

        if matching_mags:
            if 'SpawnAttachments' not in weapon:
                weapon['SpawnAttachments'] = []
            weapon['SpawnAttachments'].extend(matching_mags)

    return weapons_data


def main():
    input_dir = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServerChernaTrader\config\ExpansionMod\Market"
    weapons_file = os.path.join(input_dir, "Snafu_Weapons.json")
    mags_file = os.path.join(input_dir, "Snafu_Mags.json")
    output_file = os.path.join(input_dir, "Snafu_Weapons_modified.json")

    print(f"Loading weapons data from {weapons_file}")
    weapons_data = load_json(weapons_file)
    print(f"Loading mags data from {mags_file}")
    mags_data = load_json(mags_file)

    if weapons_data and mags_data:
        print("Matching weapons and mags")
        modified_weapons_data = match_weapons_and_mags(weapons_data, mags_data)

        if modified_weapons_data:
            print(f"Saving modified weapons data to {output_file}")
            save_json(modified_weapons_data, output_file)
        else:
            print("Error: Failed to match weapons and mags")
    else:
        print("Error: Failed to load weapons or mags data")

if __name__ == "__main__":
    main()
