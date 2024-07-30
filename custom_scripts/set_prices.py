import json
import sys
import os

def adjust_prices(input_file):
    # Read the JSON file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Iterate through items and adjust prices
    for item in data.get('Items', []):
        # Multiply MaxPriceThreshold by 3
        max_price = item.get('MaxPriceThreshold', 0) * 3.2
        
        # Set MinPriceThreshold to 75% of new MaxPriceThreshold
        min_price = max_price * 0.80

        # Ensure neither value is zero and min is less than max
        max_price = max(1, max_price)
        min_price = max(1, min(min_price, max_price - 1))

        # Update the values in the item dictionary
        item['MaxPriceThreshold'] = round(max_price)
        item['MinPriceThreshold'] = round(min_price)

    # Write the modified data back to the file
    with open(input_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Prices adjusted in {input_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python set_prices.py <input_filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    
    # Define possible paths
    possible_paths = [
        os.path.join(os.getcwd(), "..", "config", "ExpansionMod", "Market", input_filename),
        os.path.join(os.getcwd(), "config", "ExpansionMod", "Market", input_filename),
        os.path.join(os.path.dirname(os.getcwd()), "config", "ExpansionMod", "Market", input_filename)
    ]

    # Try each possible path
    for path in possible_paths:
        if os.path.exists(path):
            adjust_prices(path)
            break
    else:
        print(f"Error: File {input_filename} not found in any of the expected locations.")
        print("Searched in:")
        for path in possible_paths:
            print(f"- {path}")
        sys.exit(1)
