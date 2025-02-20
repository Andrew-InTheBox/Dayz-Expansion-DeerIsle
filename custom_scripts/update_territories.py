import xml.etree.ElementTree as ET
import math

def is_inside_circle(x, z, circle_x, circle_z, circle_radius):
    distance = math.sqrt((x - circle_x)**2 + (z - circle_z)**2)
    return distance <= circle_radius

def update_xml_values(file_path, multiplier, circle_x, circle_z, circle_radius):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    skipped_count = 0
    adjusted_count = 0

    for zone in root.findall('.//zone'):
        x = float(zone.get('x'))
        z = float(zone.get('z'))

        # Only update if the point is outside the circle
        if not is_inside_circle(x, z, circle_x, circle_z, circle_radius):
            dmin = int(zone.get('dmin'))
            dmax = int(zone.get('dmax'))

            new_dmin = math.ceil(dmin * multiplier)
            new_dmax = math.ceil(dmax * multiplier)

            zone.set('dmin', str(new_dmin))
            zone.set('dmax', str(new_dmax))
            adjusted_count += 1
        else:
            skipped_count += 1

    tree.write(file_path, encoding='UTF-8', xml_declaration=True)
    return skipped_count, adjusted_count

# Example usage
file_path = r'C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\mpmissions\Expansion.deerisle\env\zombie_territories.xml'
multiplier = 1.25  # Set your desired multiplier here

# Define the circle (center point and radius)
circle_x = 6900  # Example center x-coordinate
circle_z = 1400  # Example center z-coordinate
circle_radius = 1500  # Example radius

skipped, adjusted = update_xml_values(file_path, multiplier, circle_x, circle_z, circle_radius)
print(f"XML file updated with multiplier {multiplier}")
print(f"Zones inside circle (skipped): {skipped}")
print(f"Zones outside circle (adjusted): {adjusted}")
print(f"Total zones processed: {skipped + adjusted}")