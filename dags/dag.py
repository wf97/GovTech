#%%
import sys
import os

import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

def process_data(**kwargs):
    data1 = pd.read_csv('./dags/dataset1.csv')
    data2 = pd.read_csv('./dags/dataset2.csv')
    data = pd.concat([data1, data2], axis=0, ignore_index=True)
    data = data.dropna(axis=0, subset=['name'])
    data['name'] = data['name'].replace(['Miss ','Mr\. ','Ms\. ', 'Mrs\. ', 'Dr\. '],'', regex=True)
    data[['first_name', 'last_name']] = data['name'].str.split(' ', 1, expand=True)
    data.to_csv('./dags/test.csv', index=False)

with DAG(
        dag_id="data_processing_pipeline",
        schedule_interval='0 1 * * *',
        default_args={
            "owner": "airflow",
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
            "start_date": datetime(2021, 1, 1),
        },
        catchup=False) as f:

    start = DummyOperator(
        task_id="start",
    )

    process_data = PythonOperator(
        task_id="process_data",
        # bash_command="python data_processing.py",
        python_callable=process_data,
        provide_context=True,
    )

start >> process_data