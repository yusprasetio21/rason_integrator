import pandas as pd
import json

with open("./metadata/output.json", 'r') as file:
    data = json.load(file)
    # Convert JSON to DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index.name = 'station_icao'
    df.reset_index(inplace=True)
    df.rename(columns={'wmo_id': 'station_wmo_id'}, inplace=True)

    # Save to CSV
    csv_path = './metadata/station_data_bmkgsoft.csv'
    df.to_csv(csv_path, index=False)
