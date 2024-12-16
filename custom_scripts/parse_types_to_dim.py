import xml.etree.ElementTree as ET
import pandas as pd
import os

def parse_dayz_loot_xml(xml_path, output_dir):
    """
    Parse DayZ types.xml into normalized dataframes and save as CSVs
    
    Parameters:
    xml_path: str - Path to types.xml
    output_dir: str - Directory to save CSV files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Lists to store our data
    types_data = []
    usages = set()
    values = set()
    type_usage_relations = []
    type_value_relations = []
    
    # Parse each type element
    for type_elem in root.findall('type'):
        type_name = type_elem.get('name')
        
        # Extract base type attributes
        type_data = {
            'type_id': type_name,
            'nominal': int(type_elem.find('nominal').text),
            'lifetime': int(type_elem.find('lifetime').text),
            'restock': int(type_elem.find('restock').text),
            'min': int(type_elem.find('min').text),
            'cost': int(type_elem.find('cost').text),
            'category': type_elem.find('category').get('name') if type_elem.find('category') is not None else None,
            'crafted': type_elem.find('flags').get('crafted'),
            'deloot': type_elem.find('flags').get('deloot')
        }
        types_data.append(type_data)
        
        # Collect usage locations
        for usage in type_elem.findall('usage'):
            usage_name = usage.get('name')
            usages.add(usage_name)
            type_usage_relations.append({
                'type_id': type_name,
                'usage_name': usage_name
            })
            
        # Collect tier values
        for value in type_elem.findall('value'):
            value_name = value.get('name')
            values.add(value_name)
            type_value_relations.append({
                'type_id': type_name,
                'value_name': value_name
            })
    
    # Create dataframes
    types_df = pd.DataFrame(types_data)
    usages_df = pd.DataFrame({'usage_name': list(usages)})
    values_df = pd.DataFrame({'value_name': list(values)})
    type_usage_bridge_df = pd.DataFrame(type_usage_relations)
    type_value_bridge_df = pd.DataFrame(type_value_relations)
    
    # Save to CSV files
    types_df.to_csv(os.path.join(output_dir, 'dim_types.csv'), index=False)
    usages_df.to_csv(os.path.join(output_dir, 'dim_usages.csv'), index=False)
    values_df.to_csv(os.path.join(output_dir, 'dim_values.csv'), index=False)
    type_usage_bridge_df.to_csv(os.path.join(output_dir, 'bridge_type_usage.csv'), index=False)
    type_value_bridge_df.to_csv(os.path.join(output_dir, 'bridge_type_value.csv'), index=False)
    
    print(f"Generated {len(types_df)} type records")
    print(f"Found {len(usages_df)} unique usage locations")
    print(f"Found {len(values_df)} unique tier values")
    print(f"Generated {len(type_usage_bridge_df)} type-usage relationships")
    print(f"Generated {len(type_value_bridge_df)} type-value relationships")
    
    return {
        'types': types_df,
        'usages': usages_df,
        'values': values_df,
        'type_usage_bridge': type_usage_bridge_df,
        'type_value_bridge': type_value_bridge_df
    }

if __name__ == "__main__":
    input_path = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\mpmissions\Expansion.deerisle\db\types.xml"
    output_dir = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader\custom_scripts\dim_types"
    
    try:
        results = parse_dayz_loot_xml(input_path, output_dir)
        print(f"\nFiles successfully created in {output_dir}")
    except Exception as e:
        print(f"Error processing file: {str(e)}")