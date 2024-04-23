import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pyart


#read data from a file
def readDataFromFile(file_path):
    radar = pyart.io.read_sigme(file_path)
    gate_longitude = radar.gate_latitude['data']
    gate_latitude = radar.gate_longitude['data']
    gate_altitude = radar.gate_altitude['data']
    reflectivity_data = radar.fields['reflectivity']['data']
    total_power_data = radar.fields['total_power']['data']
    velocity_data = radar.fields['velocity']['data']
    spectrum_width_data = radar.fields['spectrum_width']['data']
    times = radar.time['data']
    return gate_longitude,gate_latitude,gate_altitude,reflectivity_data,total_power_data,velocity_data,spectrum_width_data,times

def createRadarObj(radar):
    new_radar = pyart.core.Radar(
        time=radar.time,
        _range=radar.range,  # Thay range_data bằng dữ liệu về khoảng cách
        fields={'reflectivity': {'data': reflectivity_data},
                'total_power': {'data': total_power_data},
                'velocity': {'data': velocity_data},
                'spectrum_width': {'data': spectrum_width_data}},
        metadata={'instrument_name': 'Your Radar Name'},
        scan_type='ppi',  # Loại quét radar, ví dụ: 'ppi' (phổ cung) hoặc 'rhi' (phổ chiều)
        latitude=radar.latitude,  # Vĩ độ của cổng radar
        longitude=radar.longitude,  # Kinh độ của cổng radar
        altitude=radar.altitude,  # Độ cao của cổng radar
        sweep_number=radar.sweep_number,  # Số lần quét
        sweep_mode=radar.sweep_mode,  # Chế độ quét
        fixed_angle=radar.fixed_angle,  # Góc cố định
        sweep_start_ray_index=radar.sweep_start_ray_index,  # Chỉ số của ray bắt đầu của mỗi lần quét
        sweep_end_ray_index=radar.sweep_end_ray_index,  # Chỉ số của ray kết thúc của mỗi lần quét
        azimuth=radar.azimuth,  # Góc azimuth
        elevation=radar.elevation  # Góc nâng
    )
    return new_radar

#handle with -- value
def transform(value): 
    if(value == '--'):
        return None
    else: 
        return value

def combineRadarField(
    gate_longitude,
    gate_latitude,
    gate_altitude,
    reflectivity_data,
    total_power_data,
    velocity_data,
    spectrum_width_data,
    times
):
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


# convert radar object to image
def convertRadarToImage(radar):
    fig = plt.figure(figsize=(12, 4))
    display = pyart.graph.RadarMapDisplay(radar)

    ax = plt.subplot(121, projection=ccrs.PlateCarree())

    display.plot_ppi_map(
        "reflectivity",
        sweep=0,
        ax=ax,
        colorbar_label="Equivalent Relectivity ($Z_{e}$) \n (dBZ)",
        vmin=-20,
        vmax=60,
    )

# Write data into CSV file
def write_data_to_CSV(
        field_names, 
        #str[] ==> ['longitude', 'latitude', 'altitude', 'reflectivity', 'total_power', 'velocity', 'spectrum_width', 'time']
        data, 
        # obj[] ==> [{}, {}]
        file_path
        #str
    ):
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        for data_frame in data_frames:
            writer.writerow(data_frame)
