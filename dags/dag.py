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
    # Drop rows with NA values in name column
    data = data.dropna(axis=0, subset=['name'])
    # Remove Salutations
    data['name'] = data['name'].replace(['Miss ','Mr\. ','Ms\. ', 'Mrs\. ', 'Dr\. '],'', regex=True)
    # Split by 1st occurrence of ' ', suffixes such as 'Jr.' goes into last name as well
    data[['first_name', 'last_name']] = data['name'].str.split(' ', 1, expand=True)
    # Save file
    data['price'] = data['price'].astype('float')
    data['above_100'] = data['price'].apply(lambda x: True if x > 100 else False)
    data.to_csv('./dags/test.csv', index=False)

with DAG(
        dag_id="data_processing_pipeline",
        schedule_interval='0 1 * * *', # Schedule at 1 am everyday
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
        python_callable=process_data,
        provide_context=True,
    )

start >> process_data