import os
import json
import xml.etree.ElementTree as ET

def get_json_items(market_dir):
    json_items = set()
    for filename in os.listdir(market_dir):
        if filename.endswith('.json'):
            with open(os.path.join(market_dir, filename), 'r') as f:
                data = json.load(f)
                if 'Items' in data:
                    for item in data['Items']:
                        json_items.add(item['ClassName'].lower())
                        # Add variants
                        if 'Variants' in item:
                            for variant in item['Variants']:
                                json_items.add(variant.lower())
    return json_items

def get_xml_items(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return {type_elem.get('name').lower(): type_elem.get('name') 
            for type_elem in root.findall('.//type') 
            if not type_elem.get('name').lower().startswith('zmbm')}

def get_all_xml_items(base_dir, mmg_dir):
    xml_items = {}
    
    # Process main types.xml
    xml_items.update(get_xml_items(os.path.join(base_dir, 'types.xml')))
    
    # Process all XML files in mmg directory
    for filename in os.listdir(mmg_dir):
        if filename.endswith('.xml'):
            xml_items.update(get_xml_items(os.path.join(mmg_dir, filename)))
    
    return xml_items

def find_missing_items(json_items, xml_items):
    return {original_name for lower_name, original_name in xml_items.items() if lower_name not in json_items}

# Set up directories
market_dir = './config/ExpansionMod/Market'
base_dir = './mpmissions/Expansion.chernarusplus/db'
mmg_dir = os.path.join(base_dir, 'mmg')

# Get items from JSON and XML files
json_items = get_json_items(market_dir)
xml_items = get_all_xml_items(base_dir, mmg_dir)

# Find missing items
missing_items = find_missing_items(json_items, xml_items)

# Print results
print(f"Total items in JSON files: {len(json_items)}")
print(f"Total items in XML files (excluding zombies): {len(xml_items)}")
print(f"Number of missing items: {len(missing_items)}")
print("\nMissing items:")
for item in sorted(missing_items):
    print(item)

# Optionally, write missing items to a file
with open('missing_items.txt', 'w') as f:
    for item in sorted(missing_items):
        f.write(f"{item}\n")

print("\nMissing items have been written to 'missing_items.txt'")
