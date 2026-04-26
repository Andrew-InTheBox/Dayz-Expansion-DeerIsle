import xml.etree.ElementTree as ET
import math

# Define the file path
file_path = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerSakhal\mpmissions\dayzOffline.sakhal\db\types.xml'

# Load the XML file
tree = ET.parse(file_path)
root = tree.getroot()
print("XML file loaded successfully.")

# Iterate through each <type> node
for type_element in root.findall('type'):
    # Get the 'name' attribute
    type_name = type_element.get('name')
    
    # Check if the <nominal> value is greater than 0
    nominal = type_element.find('nominal')
    if nominal is not None and float(nominal.text) > 0:
        # Multiply the <nominal> value by 1.3 and round to the nearest whole number, then convert to string
        new_nominal_value = str(round(float(nominal.text) * 1.3))
        # Set the new value back to the <nominal> node
        nominal.text = new_nominal_value
        print(f"Updated nominal value for type: {type_name}")

    # Check if the <min> attribute exists and its value is greater than 0
    min_element = type_element.find('min')
    if min_element is not None and float(min_element.text) > 0:
        # Multiply the <min> value by 1.3 and round to the nearest whole number, then convert to string
        new_min_value = str(round(float(min_element.text) * 1.3))
        # Set the new value back to the <min> node
        min_element.text = new_min_value
        print(f"Updated min value for type: {type_name}")

# Save the modified XML back to the same file
tree.write(file_path)
print(f"Modified XML saved to {file_path}")
