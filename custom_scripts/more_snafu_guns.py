import xml.etree.ElementTree as ET
import os

# Specify the full path to the XML file
file_path = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\mpmissions\Expansion.deerisle\db\snafu\SNAFU_types.xml"

# Check if the file exists
if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    exit()

# Parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

# Iterate through all 'type' elements
for type_elem in root.findall('type'):
    name = type_elem.get('name')
    
    # Check if 'Gun' is in the name attribute
    if 'Mag' in name:
        # Find and update the 'nominal' element
        nominal_elem = type_elem.find('nominal')
        if nominal_elem is not None:
            nominal_elem.text = '5'
        
        # Find and update the 'min' element
        min_elem = type_elem.find('min')
        if min_elem is not None:
            min_elem.text = '3'

# Prepare the output file path
output_path = os.path.join(os.path.dirname(file_path), 'SNAFU_types_modified.xml')

# Save the modified XML back to file
tree.write(output_path, encoding='UTF-8', xml_declaration=True)

print(f"XML file has been modified and saved as '{output_path}'")
