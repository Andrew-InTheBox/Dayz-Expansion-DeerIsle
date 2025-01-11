import xml.etree.ElementTree as ET
from typing import Set, List
import os
from xml.dom import minidom

def map_tiers_to_new_system(old_tiers: Set[int]) -> List[int]:
    """Map old tiers (1-4) to new tier system (1-9)"""
    new_tiers = set()
    for old_tier in old_tiers:
        if old_tier == 1:
            new_tiers.add(1)
        elif old_tier == 2:
            new_tiers.add(2)
        elif old_tier == 3:
            new_tiers.add(3)
        elif old_tier == 4:
            new_tiers.update([4, 5, 6, 7, 8, 9])
    return sorted(new_tiers)

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

def process_xml_file(input_file: str, output_file: str):
    # Ensure output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Process each type element
    for type_elem in root.findall('type'):
        # Find all value elements that specify tiers
        tier_values = type_elem.findall("value[@name]")
        old_tiers = set()
        
        # Collect old tiers
        for value in tier_values[:]:  # Create a copy of the list to safely remove elements
            if value.get('name', '').startswith('Tier'):
                try:
                    tier_num = int(value.get('name')[4:])  # Extract number from 'Tier1', 'Tier2', etc.
                    old_tiers.add(tier_num)
                    type_elem.remove(value)  # Remove old tier value
                except ValueError:
                    continue

        # If we found any tiers, map them to new system
        if old_tiers:
            new_tiers = map_tiers_to_new_system(old_tiers)
            
            # Add new tier values
            for new_tier in new_tiers:
                new_value = ET.Element('value')
                new_value.set('name', f'Tier{new_tier}')
                type_elem.append(new_value)

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

def main():
    input_file = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServerChernaTrader\mpmissions\Expansion.chernarusplus\expansion_ce\expansion_types.xml"
    output_file = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\mpmissions\Expansion.deerisle\expansion_ce\new_types.xml"
    
    try:
        process_xml_file(input_file, output_file)
        print(f"Successfully processed file.")
        print(f"Input: {input_file}")
        print(f"Output: {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()