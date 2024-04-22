from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

def read_files_and_insert_to_postgres(**kwargs):
    # Define the folder path where your files are located
    folder_path = '/path/to/your/folder'
    
    # Get a list of files in the folder
    files = os.listdir(folder_path)
    
    # Initialize a PostgreSQL hook
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    
    for file_name in files:
        # Assuming each file contains data to be inserted into PostgreSQL
        with open(os.path.join(folder_path, file_name), 'r') as file:
            # Read data from the file (assuming each line represents a record)
            for line in file:
                # Insert data into PostgreSQL
                pg_hook.run(f"INSERT INTO your_table_name (column1, column2, ...) VALUES ({line});")

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'read_files_and_insert_to_postgres',
    default_args=default_args,
    description='A DAG to read files from a folder and insert data into PostgreSQL',
    schedule_interval=timedelta(days=1),
)

# Define the task to read files and insert data into PostgreSQL
read_files_task = PythonOperator(
    task_id='read_files_and_insert_to_postgres',
    python_callable=read_files_and_insert_to_postgres,
    provide_context=True,  # This allows passing additional context to the function
    dag=dag,
)

# Set task dependencies
read_files_task
