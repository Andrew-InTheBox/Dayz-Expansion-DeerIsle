import xml.etree.ElementTree as ET
import os
import math
import sys
import argparse

def process_types_xml(item_type=None):
    # Hard-coded input path
    input_path = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\mpmissions\Expansion.deerisle\expansion_ce\expansion_types.xml"
    
    print(f"Checking file at: {input_path}")
    
    # Check if file exists
    if not os.path.exists(input_path):
        print("Error: File does not exist at specified path")
        return
    
    print("File found, parsing XML...")
    
    # Parse the XML file
    tree = ET.parse(input_path)
    root = tree.getroot()
    
    print(f"Root tag: {root.tag}")
    print(f"Number of type elements found: {len(root.findall('type'))}")
    
    # Determine which types to process
    types_to_process = ['Military', 'Police'] if item_type is None else [item_type]
    print(f"Processing items of type(s): {', '.join(types_to_process)}")
    
    modified_count = 0
    
    # For each type element in the file
    for type_elem in root.findall('type'):
        # Find usage element
        usage = type_elem.find('usage')
        
        # Check if usage matches our criteria
        if usage is not None and usage.get('name') in types_to_process:
            name = type_elem.get('name', 'Unknown')
            item_type = usage.get('name')
            print(f"\nProcessing {item_type} item: {name}")
            
            # Get nominal and min elements
            nominal_elem = type_elem.find('nominal')
            min_elem = type_elem.find('min')
            
            if nominal_elem is not None and min_elem is not None:
                # Convert to float, multiply by 1.4, round to nearest whole number
                old_nominal = nominal_elem.text
                old_min = min_elem.text
                new_nominal = round(float(nominal_elem.text) * 1.4)
                new_min = round(float(min_elem.text) * 1.4)
                
                # Update the values
                nominal_elem.text = str(new_nominal)
                min_elem.text = str(new_min)
                
                print(f"Modified {name}: nominal {old_nominal}->{new_nominal}, min {old_min}->{new_min}")
                modified_count += 1
    
    print(f"\nTotal items modified: {modified_count}")
    
    # Generate output path in same directory
    output_dir = os.path.dirname(input_path)
    output_path = os.path.join(output_dir, 'new_types.xml')
    
    print(f"Writing to: {output_path}")
    
    # Write the modified XML to the new file
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Successfully created new_types.xml in {output_dir}")

if __name__ == "__main__":
    try:
        print("Script starting...")
        
        # Set up argument parser
        parser = argparse.ArgumentParser(description='Process military and/or police items in types.xml')
        parser.add_argument('--type', choices=['Military', 'Police'], 
                          help='Specify item type to process (Military or Police). If not specified, both will be processed.')
        
        args = parser.parse_args()
        
        # Run the processor with the specified type (or None for both)
        process_types_xml(args.type)
        print("Script completed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    # Keep console window open
    input("Press Enter to exit...")