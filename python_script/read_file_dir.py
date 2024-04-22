import os
def read_data_dir():
    # Define the folder path where your files are located
    radar_path = '/Users/luanluan/Documents/Data/dw_airflow/data/radar'
    
    # Get a list of files in the folder
    years = os.listdir(radar_path)
    
    # Initialize a PostgreSQL hook
    # pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    for year in years:
        if(year == '.DS_Store'):
            continue
        print('year: ', year)

        month_path = radar_path + '/' + year
        months = os.listdir(month_path)

        for month in months: 
            if(month == '.DS_Store'):
                continue
            print('month: ', month)

            day_path = radar_path + '/' + year + '/' + month
            days = os.listdir(day_path)

            for day in days: 
                if(day == '.DS_Store'):
                    continue
                print('day: ', day)

        # Assuming each file contains data to be inserted into PostgreSQL
        # with open(os.path.join(folder_path, file_name), 'r') as file:
            # Read data from the file (assuming each line represents a record)
            
            # for line in file:
            #     # Insert data into PostgreSQL
            #     pg_hook.run(f"INSERT INTO your_table_name (column1, column2, ...) VALUES ({line});")

read_data_dir()