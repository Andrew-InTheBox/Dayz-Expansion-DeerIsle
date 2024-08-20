import os
import xml.etree.ElementTree as ET

def validate_xml(file_path):
    try:
        ET.parse(file_path)
        return True
    except ET.ParseError as e:
        print(f"Error in {file_path}: {e}")
        return False

def validate_xml_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                if validate_xml(file_path):
                    print(f"Valid XML: {file_path}")
                else:
                    print(f"Invalid XML: {file_path}")

if __name__ == "__main__":
    directory = "C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader"  # Replace with the actual directory path
    validate_xml_files(directory)