import json

def transform_json(input_file, output_file):
    # Read input JSON
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Initialize output dictionary
    transformed_data = {}

    # Process each item
    for item in data['items']:
        station_icao = item['station_icao']
        if station_icao in transformed_data:
            print("Duplicate CCCC", item, "dengan", transformed_data[station_icao])
            return
        
        if station_icao == "":
            print("SKIP", item)
            continue
        
        transformed_data[station_icao] = {
            "station_name": item['station_name'],
            "url": f"{item['path']}/gts",  # Add '/gts' to the end of 'path'
            "wmo_id": item['station_wmo_id']
        }

    # Write the transformed data to an output JSON file
    with open(output_file, 'w') as file:
        json.dump(transformed_data, file, indent=4)

# File paths
input_file = './metadata/raw.json'
output_file = './metadata/output.json'

# Run the transformation
transform_json(input_file, output_file)
