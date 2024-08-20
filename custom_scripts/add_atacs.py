import xml.etree.ElementTree as ET
import json
import os

# File paths
xml_path = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServerChernaTrader\mpmissions\Expansion.chernarusplus\db\mmg\mmg_types_atacs.xml"
json_output_path = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServerChernaTrader\config\ExpansionMod\Market\MMG_ATACS_Market.json"

# Read the XML file
tree = ET.parse(xml_path)
root = tree.getroot()

# Initialize the market data structure
market_data = {
    "m_Version": 12,
    "DisplayName": "MMG ATACS Items",
    "Icon": "Deliver",
    "Color": "FBFCFEFF",
    "IsExchange": 0,
    "InitStockPercent": 75.0,
    "Items": []
}

# Placeholder values
placeholder_values = {
    "MaxPriceThreshold": 1500,
    "MinPriceThreshold": 1000,
    "SellPricePercent": -1.0,
    "MaxStockThreshold": 1,
    "MinStockThreshold": 1,
    "QuantityPercent": -1,
}

# Iterate through the XML and extract ATACS item class names
for item_type in root.findall('.//type'):
    class_name = item_type.get('name')
    if 'atacs' in class_name.lower():
        item_data = {
            "ClassName": class_name,
            "SpawnAttachments": [],
            "Variants": []
        }
        item_data.update(placeholder_values)
        market_data["Items"].append(item_data)

# Ensure the output directory exists
os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

# Write the market data to a JSON file
with open(json_output_path, 'w') as json_file:
    json.dump(market_data, json_file, indent=4)

print(f"Market JSON file '{json_output_path}' has been created.")
