# Use weapon tiering config file and tier lookup config file
# to remap tiering for weapons across tiers 1-9 in deer isle 5.9

import xml.etree.ElementTree as ET
import csv
from typing import Dict, List, Set
import os

def load_weapon_ratings(csv_file: str) -> Dict[str, int]:
    """Load weapon ratings from CSV file"""
    weapon_ratings = {}
    with open(csv_file, 'r', encoding='UTF-8-sig') as f:  # Note the UTF-8-sig to handle BOM
        reader = csv.DictReader(f)
        for row in reader:
            try:
                weapon_name = row['type_id'].lower()  # Convert to lowercase
                rating = int(row['Rating (4 is best)'])
                weapon_ratings[weapon_name] = rating
            except (ValueError, KeyError) as e:
                print(f"Warning: Skipping invalid entry: {row.get('type_id', 'Unknown')} - {str(e)}")
    
    # Add debug info
    print(f"\nLoaded {len(weapon_ratings)} weapons from CSV")
    print("Sample of loaded weapons:")
    sample = list(weapon_ratings.items())[:5]
    for weapon, rating in sample:
        print(f"  {weapon}: {rating}")
    
    return weapon_ratings

def load_rating_tier_mapping(csv_file: str) -> Dict[int, List[int]]:
    """Load rating to tier mapping from CSV"""
    rating_map = {}
    with open(csv_file, 'r', encoding='UTF-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                rating = int(row['Weapon  Rating'])
                tier = int(row['xml types tier'])
                
                # Initialize the list if this rating isn't in the map yet
                if rating not in rating_map:
                    rating_map[rating] = []
                
                # Only append if this tier isn't already in the list
                if tier not in rating_map[rating]:
                    rating_map[rating].append(tier)
            except (ValueError, KeyError) as e:
                print(f"Warning: Skipping invalid rating mapping: {str(e)}")
    
    # Add debug info
    print("\nRating to Tier mappings:")
    for rating, tiers in rating_map.items():
        print(f"Rating {rating} -> Tiers {sorted(tiers)}")
        
    return rating_map

def indent_xml(elem: ET.Element, level: int = 0):
    """Add proper indentation to the XML elements"""
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent_xml(subelem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def process_xml_file(input_file: str, output_file: str, weapon_ratings: Dict[str, int], rating_tier_map: Dict[int, List[int]]):
    """Process XML file and update weapon tiers"""
    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    weapons_processed = 0
    weapons_skipped = 0

    # Process each type element
    for type_elem in root.findall('type'):
        weapon_name = type_elem.get('name')
        weapon_name_lower = weapon_name.lower()  # Convert to lowercase for comparison
        
        # Skip if weapon not in ratings
        if weapon_name_lower not in weapon_ratings:
            weapons_skipped += 1
            continue

        # Get the weapon's rating and corresponding tiers
        rating = weapon_ratings[weapon_name_lower]  # Use lowercase version for lookup
        new_tiers = rating_tier_map.get(rating, [1])  # Default to tier 1 if mapping not found

        # Remove existing tier values
        for value in type_elem.findall("value[@name]"):
            if value.get('name', '').startswith('Tier'):
                type_elem.remove(value)

        # Add new tier values
        for new_tier in new_tiers:
            new_value = ET.Element('value')
            new_value.set('name', f'Tier{new_tier}')
            type_elem.append(new_value)

        weapons_processed += 1

    # Apply proper indentation
    indent_xml(root)

    # Write the modified XML to a new file
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)

    # Read the file back and add proper spacing
    with open(output_file, 'r', encoding='UTF-8') as f:
        content = f.read()
    
    # Format the content
    content = content.replace('/><', '/>\n<')
    
    # Write the formatted content back
    with open(output_file, 'w', encoding='UTF-8') as f:
        f.write(content)

    return weapons_processed, weapons_skipped

def main():
    # Base paths
    server_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    mission_base = os.path.join(server_base, "mpmissions", "Expansion.deerisle")
    
    # Input files
    types_xml = os.path.join(mission_base, "db", "types.xml")
    expansion_types_xml = os.path.join(mission_base, "expansion_ce", "expansion_types.xml")
    snafu_types_xml = os.path.join(mission_base, "db", "snafu", "SNAFU_bare_types.xml")
    
    # Output files - maintain same directory structure
    output_base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_base, exist_ok=True)
    output_types_xml = os.path.join(output_base, "types_new.xml")
    output_expansion_types_xml = os.path.join(output_base, "expansion_types_new.xml")
    output_snafu_types_xml = os.path.join(output_base, "SNAFU_bare_types_new.xml")
    
    # CSV files
    weapon_ratings_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weapon_ratings", "weapon_ratings.csv")
    rating_tiers_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weapon_ratings", "rating_to_tiers.csv")

    try:
        # Load weapon ratings and rating-to-tier mapping
        print(f"Loading weapon ratings from: {weapon_ratings_csv}")
        weapon_ratings = load_weapon_ratings(weapon_ratings_csv)
        print(f"Loading rating-to-tier mappings from: {rating_tiers_csv}")
        rating_tier_map = load_rating_tier_mapping(rating_tiers_csv)
        
        print(f"Loaded {len(weapon_ratings)} weapon ratings")
        print(f"Loaded rating-to-tier mappings for {len(rating_tier_map)} ratings")

        # Process types.xml
        if os.path.exists(types_xml):
            print(f"\nProcessing: {types_xml}")
            processed, skipped = process_xml_file(types_xml, output_types_xml, weapon_ratings, rating_tier_map)
            print(f"Output written to: {output_types_xml}")
            print(f"  - Weapons processed: {processed}")
            print(f"  - Weapons skipped: {skipped}")
        else:
            print(f"Warning: {types_xml} not found")

        # Process expansion_types.xml
        if os.path.exists(expansion_types_xml):
            print(f"\nProcessing: {expansion_types_xml}")
            processed, skipped = process_xml_file(expansion_types_xml, output_expansion_types_xml, weapon_ratings, rating_tier_map)
            print(f"Output written to: {output_expansion_types_xml}")
            print(f"  - Weapons processed: {processed}")
            print(f"  - Weapons skipped: {skipped}")
        else:
            print(f"Warning: {expansion_types_xml} not found")
        
        # Process SNAFU_bare_types.xml
        if os.path.exists(snafu_types_xml):
            print(f"\nProcessing: {snafu_types_xml}")
            processed, skipped = process_xml_file(snafu_types_xml, output_snafu_types_xml, weapon_ratings, rating_tier_map)
            print(f"Output written to: {output_snafu_types_xml}")
            print(f"  - Weapons processed: {processed}")
            print(f"  - Weapons skipped: {skipped}")
        else:
            print(f"Warning: {snafu_types_xml} not found")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()