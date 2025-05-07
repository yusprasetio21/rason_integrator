import pandas as pd

# Load both CSV files
first_csv = pd.read_csv('./metadata/station_data_aviation.csv')
second_csv = pd.read_csv('./metadata/station_data_bmkgsoft.csv')

# Find entries in first CSV that are not in the second based on 'station_icao'
missing_in_second = first_csv[~first_csv['station_icao'].isin(second_csv['station_icao'])]

# Save the result to a new CSV file or print it
missing_in_second.to_csv('./metadata/missing_in_bmkgsoft.csv', index=False)
print("Stations missing in bmkgsoft CSV:")
print(missing_in_second)