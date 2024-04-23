#%%
import pyart
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

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

# vẽ biểu đồ trên dữ liệu cũ
fig = plt.figure(figsize=(12, 4))
display = pyart.graph.RadarMapDisplay(new_radar)

ax = plt.subplot(121, projection=ccrs.PlateCarree())

display.plot_ppi_map(
    "reflectivity",
    sweep=0,
    ax=ax,
    colorbar_label="Equivalent Relectivity ($Z_{e}$) \n (dBZ) OLD",
    vmin=-20,
    vmax=60,
)


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

# vẽ biểu đồ trên dữ liệu mới

fig = plt.figure(figsize=(12, 4))
display = pyart.graph.RadarMapDisplay(new_radar)

ax = plt.subplot(121, projection=ccrs.PlateCarree())

display.plot_ppi_map(
    "reflectivity",
    sweep=0,
    ax=ax,
    colorbar_label="Equivalent Relectivity ($Z_{e}$) \n (dBZ) NEW",
    vmin=-20,
    vmax=60,
)



# %%
