import pyart

data_path = '/Users/luanluan/Documents/Data/dw_airflow/data/radar/2020/Pro-Raw(1-8)T7-2020/01/'
file = 'NHB200701001009.RAWXPS9'
# Đọc dữ liệu từ tệp radar
radar = pyart.io.read_sigmet(data_path + file)

# Trích xuất thông tin về dữ liệu đo được theo vị trí và thời gian
gate_longitude = radar.gate_longitude['data']
gate_latitude = radar.gate_latitude['data']
gate_altitude = radar.gate_altitude['data']
reflectivity_data = radar.fields['reflectivity']['data']
total_power_data = radar.fields['total_power']['data']
velocity_data = radar.fields['velocity']['data']
spectrum_width_data = radar.fields['spectrum_width']['data']
time = radar.time['data']
timestamps = pyart.util.datetimes_from_radar(radar)

print((timestamps[100]))