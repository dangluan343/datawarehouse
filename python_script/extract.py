import pyart

import csv

def transform(value): 
    if(value == '--'):
        return None
    else: 
        return value

# Define the file path for the CSV file
csv_file_path = '/Users/luanluan/Documents/Data/dw_airflow/data/radar/2020/Pro-Raw(1-8)T7-2020/01/NHB200701001009.RAWXPS9.csv'

# Đọc dữ liệu từ tệp radar
radar = pyart.io.read('/Users/luanluan/Documents/Data/dw_airflow/data/radar/2020/Pro-Raw(1-8)T7-2020/01/NHB200701001009.RAWXPS9')

# Trích xuất thông tin về vị trí và chiếu
gate_longitude = radar.gate_latitude['data']
gate_latitude = radar.gate_longitude['data']
gate_altitude = radar.gate_altitude['data']
reflectivity_data = radar.fields['reflectivity']['data']
total_power_data = radar.fields['total_power']['data']
velocity_data = radar.fields['velocity']['data']
spectrum_width_data = radar.fields['spectrum_width']['data']
times = radar.time['data']
timestamp = pyart.util.datetime_from_radar(radar)


#flat 
data_frames = []
first_level_len = len(gate_longitude)
second_level_len = len(gate_latitude[0])
for first_level in range(first_level_len): 
    time = times[first_level]
    for second_level in range(second_level_len): 
        longitude = gate_longitude[first_level][second_level]
        latitude = gate_latitude[first_level][second_level]
        altitude = gate_altitude[first_level][second_level]
        reflectivity = reflectivity_data[first_level][second_level]
        total_power = total_power_data[first_level][second_level]
        velocity = velocity_data[first_level][second_level]
        spectrum_width = spectrum_width_data[first_level][second_level]

        data_frame = {
            'longitude': transform(str(longitude)),
            'latitude': transform(str(latitude)),
            'altitude': transform(str(altitude)),
            'reflectivity': transform(str(reflectivity)),
            'total_power': transform(str(total_power)),
            'velocity': transform(str(velocity)),
            'spectrum_width': transform(str(spectrum_width)),
            'time': transform(str(time))
        }
        data_frames.append(data_frame)

field_names = ['longitude', 'latitude', 'altitude', 'reflectivity', 'total_power', 'velocity', 'spectrum_width', 'time']


print('timestamp', timestamp)
# Write data into CSV file
# with open(csv_file_path, 'w', newline='') as csv_file:
#     writer = csv.DictWriter(csv_file, fieldnames=field_names)
#     writer.writeheader()
#     for data_frame in data_frames:
#         writer.writerow(data_frame)

# print("Data has been written to", csv_file_path)