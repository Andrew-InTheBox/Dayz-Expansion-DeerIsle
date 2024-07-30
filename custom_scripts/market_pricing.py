import json
import os
import xml.etree.ElementTree as ET

def load_nominal_values(types_xml_path, additional_types_dir):
    nominal_values = {}

    def parse_xml(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        for item in root.findall('.//type'):
            class_name = item.get('name').lower()  # Convert to lowercase
            nominal = item.find('nominal')
            if nominal is not None:
                nominal_values[class_name] = int(nominal.text)

    # Load the main types.xml file
    parse_xml(types_xml_path)

    # Load additional types XML files
    for filename in os.listdir(additional_types_dir):
        if "types" in filename and filename.endswith('.xml'):
            parse_xml(os.path.join(additional_types_dir, filename))

    return nominal_values

def calculate_price_multiplier(nominal_value, max_nominal=130, min_nominal=1):
    inverted_value = max_nominal - nominal_value + min_nominal
    return 1 + (inverted_value / max_nominal) * 2

def round_to_nearest_10(value):
    return round(value / 10) * 10

def update_market_prices(input_directory, output_directory, types_xml_path, additional_types_dir, base_price_multiplier, min_stock_threshold, default_multiplier, analysis_mode):
    nominal_values = load_nominal_values(types_xml_path, additional_types_dir)
    
    if analysis_mode:
        os.makedirs(output_directory, exist_ok=True)
    
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            input_filepath = os.path.join(input_directory, filename)
            output_filepath = os.path.join(output_directory, filename) if analysis_mode else input_filepath
            
            with open(input_filepath, 'r') as file:
                data = json.load(file)
            
            if 'Items' in data:
                for item in data['Items']:
                    class_name = item['ClassName'].lower()  # Convert to lowercase
                    if class_name in nominal_values:
                        nominal_value = nominal_values[class_name]
                        price_multiplier = base_price_multiplier * calculate_price_multiplier(nominal_value)
                    else:
                        price_multiplier = base_price_multiplier * default_multiplier
                    
                    item['MaxPriceThreshold'] = round_to_nearest_10(item['MaxPriceThreshold'] * price_multiplier)
                    item['MinPriceThreshold'] = round_to_nearest_10(item['MinPriceThreshold'] * price_multiplier)
                    item['MinStockThreshold'] = max(item['MinStockThreshold'], min_stock_threshold)
                    
                    if item['SellPricePercent'] != -1.0:
                        item['SellPricePercent'] = 0.75
            
            with open(output_filepath, 'w') as file:
                json.dump(data, file, indent=4)

# Usage
input_directory = './config/ExpansionMod/Market'
output_directory = './config/ExpansionMod/Market_Analysis'
types_xml_path = './mpmissions/Expansion.chernarusplus/db/types.xml'
additional_types_dir = './mpmissions/Expansion.chernarusplus/db/mmg'
base_price_multiplier = 1.75
min_stock_threshold = 1
default_multiplier = 1.5
analysis_mode = True  # Set to False for production changes

update_market_prices(input_directory, output_directory, types_xml_path, additional_types_dir, base_price_multiplier, min_stock_threshold, default_multiplier, analysis_mode)

print(f"Process completed. Output written to: {'analysis directory' if analysis_mode else 'original files'}")
