import numpy as np
import matplotlib.pyplot as plt
import pyart

# Define the file path for the CSV file
csv_file_path = '/Users/luanluan/Documents/Data/dw_airflow/data/radar/2020/Pro-Raw(1-8)T7-2020/01/NHB200701001009.RAWXPS9.csv'

# Đọc dữ liệu từ tệp radar
radar = pyart.io.read('/Users/luanluan/Documents/Data/dw_airflow/data/radar/2020/Pro-Raw(1-8)T7-2020/01/NHB200701001009.RAWXPS9')

# Extract data
data = radar.fields['reflectivity']['data']  # Assuming 'reflectivity' is the field you're interested in
lon = radar.gate_longitude['data']
lat = radar.gate_latitude['data']
altitude = radar.gate_altitude['data']

# Set up a regular grid of interpolated data points
lon_min, lon_max = lon.min(), lon.max()
lat_min, lat_max = lat.min(), lat.max()
lon_grid, lat_grid = np.meshgrid(np.linspace(lon_min, lon_max, 100), np.linspace(lat_min, lat_max, 100))

# Interpolate data onto regular grid
grid = pyart.map.grid_from_radars(
    (radar,), grid_shape=(1, 100, 100),
    grid_limits=((0, 0), (200, 200)),
    fields=['reflectivity'],
    gridding_algo='map_gates_to_grid',
    weighting_function='Barnes2',
    roi_func='constant', constant_roi=500)

# Plotting using matplotlib
plt.figure(figsize=(8, 6))
plt.imshow(grid.fields['reflectivity']['data'][0], origin='lower', extent=(lon_min, lon_max, lat_min, lat_max))
plt.colorbar(label='Reflectivity (dBZ)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Reflectivity')
plt.show()
