import os
import csv
import json

def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = json.load(file)
    return flatten_json(content, file_path)

def flatten_json(data, file_path, parent_element='', slot_name='none'):
    rows = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'ClassName':
                rows.append({'filename': file_path, 'className': value, 'parent-element': parent_element, 'slotName': slot_name})
            elif key == 'SlotName':
                slot_name = value
            rows.extend(flatten_json(value, file_path, parent_element=key, slot_name=slot_name))
    elif isinstance(data, list):
        for index, element in enumerate(data):
            rows.extend(flatten_json(element, file_path, parent_element=f"{parent_element}[{index}]", slot_name=slot_name))
    return rows

def main():
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_directory = os.path.join(base_path, 'config', 'ExpansionMod', 'Loadouts')
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_csv = os.path.join(output_dir, 'loadouts_output.csv')


    all_rows = []
    for root, _, filenames in os.walk(input_directory):
        for filename in filenames:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                all_rows.extend(process_json_file(file_path))

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'className', 'parent-element', 'slotName']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f'CSV file "{output_csv}" created successfully with {len(all_rows)} entries.')

if __name__ == '__main__':
    main()