
import os
# get dag directory path
dag_path = os.getcwd()
#pyart
import pyart
import psycopg2 #postgresql package
from psycopg2 import sql


def handle_data_radar(): 
    data = transform_data()
    load_data(data)


def transform_data():
    # Đọc dữ liệu từ tệp radar
    radar = pyart.io.read_sigmet(f"{dag_path}/data/radar/2020/Pro-Raw(1-8)T7-2020/01/NHB200701000010.RAWXPS3")
    
    # Trích xuất thông tin về vị trí và chiếu
    gate_longitude = radar.gate_latitude['data']
    gate_latitude = radar.gate_longitude['data']
    gate_altitude = radar.gate_altitude['data']
    reflectivity_data = radar.fields['reflectivity']['data']
    total_power_data = radar.fields['total_power']['data']
    velocity_data = radar.fields['velocity']['data']
    spectrum_width_data = radar.fields['spectrum_width']['data']
    times = radar.time['data']

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
                'longitude': str(longitude),
                'latitude': str(latitude),
                'altitude': str(altitude),
                'reflectivity': str(reflectivity),
                'total_power': str(total_power),
                'velocity': str(velocity),
                'spectrum_width': str(spectrum_width),
                'time': str(time)
            }
            data_frames.append(data_frame)
    
    return data_frames

def load_data(data_frames):
    database_name = 'staging_area'
    user = 'luanluan'
    password = '123'
    host = 'localhost'
    port = '5432'
    conn = psycopg2.connect(
        dbname=database_name,
        user=user,
        password=password,
        host=host,
        port=port
    )     

    cursor = conn.cursor()

    table_name = 'radar'

    # Insert the image data into the database
    # data_frames = kwargs['ti'].xcom_pull(task_ids='transform_data', key='transformed_data')


    for data_frame in data_frames:
        cursor.execute(sql.SQL("""
            INSERT INTO {} (longitude, latitude, altitude, reflectivity, total_power, velocity, spectrum_width, time) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """).format(sql.Identifier(table_name)), 
        (data_frame['longitude'], data_frame['latitude'], data_frame['altitude'], data_frame['reflectivity'], 
        data_frame['total_power'], data_frame['velocity'], data_frame['spectrum_width'], data_frame['time']))
    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()  

