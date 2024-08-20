import xml.etree.ElementTree as ET

def update_chance_values(file_path, old_value="0.10", new_value="0.80"):
    # Load and parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Find all 'item' elements and update 'chance' attribute
    for item in root.findall(".//item"):
        chance = item.get('chance')
        if chance == old_value:
            item.set('chance', new_value)
    
    # Write the updated XML back to file
    tree.write(file_path)

if __name__ == "__main__":
    file_path = 'c:\\Program Files (x86)\\Steam\\steamapps\\common\\DayZServerDITrader\\mpmissions\\Expansion.deerisle\\db\\rfheli\\rfheli_spawnabletypes.xml'
    update_chance_values(file_path)
    print(f"Updated 'chance' values from 0.10 to 0.80 in {file_path}")
