import datetime as dt

from airflow import DAG
# python operator to define task by python code
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

import os
import sys

path = '/Users/luanluan/Documents/Data/dw_airflow/lib'
sys.path.append(path)

from etl_radar import handle_data_radar

ingestion_dag = DAG(
    dag_id="radar_ingestion_module", 
    schedule="0 0 * * *", 
    start_date=dt.datetime(2024, 4, 26),
    tags=["example"], 
    description='Extract data from sigmet format and import into staging database',
    catchup=False # do not run past DAG if it was paused
)

start = DummyOperator(task_id='start', dag=ingestion_dag)
load_radar_data_task = PythonOperator(
    task_id='load_radar_data',
    python_callable=handle_data_radar,
    dag=ingestion_dag,
)
end = DummyOperator(task_id='end', dag=ingestion_dag)


start>> load_radar_data_task>>end