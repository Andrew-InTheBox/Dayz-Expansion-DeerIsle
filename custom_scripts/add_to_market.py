import json
import os

def insert_items_into_market(market_file, items_to_insert):
    # Load the existing JSON file
    with open(market_file, 'r') as f:
        market_data = json.load(f)
    
    # Ensure 'Items' key exists
    if 'Items' not in market_data:
        market_data['Items'] = []
    
    # Insert new items
    for item, base_price in items_to_insert:
        new_item = {
            "ClassName": item,
            "MaxPriceThreshold": int(base_price * 1.5),  # 50% more than base price
            "MinPriceThreshold": int(base_price * 0.5),  # 50% less than base price
            "SellPricePercent": -1.0,  # Use default sell price
            "MaxStockThreshold": 100,  # Default max stock
            "MinStockThreshold": 1,    # Default min stock
            "QuantityPercent": -1,     # Default quantity
            "SpawnAttachments": [],
            "Variants": []
        }
        market_data['Items'].append(new_item)
    
    # Write updated data back to the file
    with open(market_file, 'w') as f:
        json.dump(market_data, f, indent=4)

def main():
    # Specify the directory containing market JSON files
    market_dir = './config/ExpansionMod/Market'
    
    # Get the category (JSON file) to update
    category = input("Enter the category (JSON file name without .json) to update: ")
    market_file = os.path.join(market_dir, f"{category}.json")
    
    if not os.path.exists(market_file):
        print(f"Error: {market_file} does not exist.")
        return
    
    # Get items to insert
    items_to_insert = []
    while True:
        item = input("Enter item name (or press Enter to finish): ")
        if not item:
            break
        base_price = float(input(f"Enter base price for {item}: "))
        items_to_insert.append((item, base_price))
    
    # Insert items into the market file
    insert_items_into_market(market_file, items_to_insert)
    print(f"Items have been inserted into {market_file}")

if __name__ == "__main__":
    main()
