import xml.etree.ElementTree as ET
import pandas as pd
import os

def safe_get_text(element, default='0'):
    """Safely get text from an XML element with a default value if None"""
    if element is not None:
        return element.text or default
    return default

def parse_dayz_loot_xml(xml_files, output_dir):
    """
    Parse DayZ types.xml files into normalized dataframes and save as CSVs
    
    Parameters:
    xml_files: dict - Dictionary of {filename: filepath} for types.xml files
    output_dir: str - Directory to save CSV files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Lists to store our data
    types_data = []
    usages = set()
    values = set()
    type_usage_relations = []
    type_value_relations = []
    
    # Process each input file
    for source_name, xml_path in xml_files.items():
        print(f"Processing {source_name}...")
        
        # Parse XML
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Parse each type element
        for type_elem in root.findall('type'):
            type_name = type_elem.get('name')
            
            # Extract base type attributes to match original structure exactly
            type_data = {
                'type_id': type_name,
                'source_file': source_name,  # Only new field added
                'nominal': int(safe_get_text(type_elem.find('nominal'))),
                'lifetime': int(safe_get_text(type_elem.find('lifetime'))),
                'restock': int(safe_get_text(type_elem.find('restock'))),
                'min': int(safe_get_text(type_elem.find('min'))),
                'cost': int(safe_get_text(type_elem.find('cost'))),
                'category': type_elem.find('category').get('name') if type_elem.find('category') is not None else None,
                'crafted': type_elem.find('flags').get('crafted') if type_elem.find('flags') is not None else None,
                'deloot': type_elem.find('flags').get('deloot') if type_elem.find('flags') is not None else None
            }
            
            types_data.append(type_data)
            
            # Collect usage locations (optional)
            for usage in type_elem.findall('usage'):
                usage_name = usage.get('name')
                if usage_name:
                    usages.add(usage_name)
                    type_usage_relations.append({
                        'type_id': type_name,
                        'source_file': source_name,
                        'usage_name': usage_name
                    })
                
            # Collect tier values (optional)
            for value in type_elem.findall('value'):
                value_name = value.get('name')
                if value_name:
                    values.add(value_name)
                    type_value_relations.append({
                        'type_id': type_name,
                        'source_file': source_name,
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
    
    print("\nSummary:")
    print(f"Generated {len(types_df)} total type records:")
    for source in sorted(types_df['source_file'].unique()):
        source_df = types_df[types_df['source_file'] == source]
        print(f"  {len(source_df)} from {source}")
        print(f"    Categories: {source_df['category'].nunique()} unique")
        print(f"    Usage relations: {len(type_usage_bridge_df[type_usage_bridge_df['source_file'] == source])}")
        print(f"    Value relations: {len(type_value_bridge_df[type_value_bridge_df['source_file'] == source])}")
    
    print(f"\nFound {len(usages_df)} unique usage locations")
    print(f"Found {len(values_df)} unique tier values")
    
    return {
        'types': types_df,
        'usages': usages_df,
        'values': values_df,
        'type_usage_bridge': type_usage_bridge_df,
        'type_value_bridge': type_value_bridge_df
    }

if __name__ == "__main__":
    base_path = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader"
    
    input_files = {
        'types': os.path.join(base_path, 'mpmissions', 'Expansion.deerisle', 'db', 'types.xml'),
        'mmg': os.path.join(base_path, 'mpmissions', 'Expansion.deerisle', 'db', 'mmg', 'mmg_bare_types.xml'),
        'expansion': os.path.join(base_path, 'mpmissions', 'Expansion.deerisle', 'expansion_ce', 'expansion_types.xml'),
        'snafu': os.path.join(base_path, 'mpmissions', 'Expansion.deerisle', 'db', 'snafu', 'SNAFU_bare_types.xml')
    }
    
    output_dir = os.path.join(base_path, 'custom_scripts', 'dim_types')
    
    try:
        results = parse_dayz_loot_xml(input_files, output_dir)
        print(f"\nFiles successfully created in {output_dir}")
    except Exception as e:
        import traceback
        print(f"Error processing files: {str(e)}")
        print(traceback.format_exc())