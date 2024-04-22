import os
def read_data_dir():
    # Define the folder path where your files are located
    radar_path = '/Users/luanluan/Documents/Data/dw_airflow/data/radar/2020/Pro-Raw(1-8)T7-2020/02'
    years = os.listdir(radar_path)

    print('count',len(years) )
read_data_dir()