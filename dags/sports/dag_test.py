from datetime import datetime, timedelta
import pathlib
import json

from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.providers.http.sensors.http import HttpSensor


from sports.services.get_data_api import GetAPIData
from common.scripts.load_to_azure import AzureUploader


default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry': timedelta(minutes=5)
}


def sports():
    TEMP_FILE_PATH: pathlib.Path = 'data/sports.json'

    retrive_sports = GetAPIData('sports')
    response = retrive_sports.data_request()

    print(response)
    with open(TEMP_FILE_PATH, "w+") as f:
        sports_data = json.loads(response.json())

        f.write(json.dumps(sports_data, ensure_ascii=False))


def scores():
    retrive_scores = GetAPIData('scores')
    response = retrive_scores.data_request()
    print(response)


def load_to_azure_blob():
    upload_blob = AzureUploader()

    upload_blob.upload_to_bob(
        blob_name='sports',
        file_name='data/sports.json',
        container_name='raw',
        azure_conn_id='adls-blob-only-key'
    )


def load_to_azure_lake():
    upload_Adls = AzureUploader()

    upload_Adls.upload_to_azure_datalake(
        azure_data_lake_conn_id='adls-gen2-conn-string',
        local_path='data/sports.json',
        remote_path='raw/sports/'
    )


with DAG(
    dag_id='GetAPIdata_v01.08',
    default_args=default_args,
    description='This will to get data from sports API',
    start_date=datetime(2023, 6, 6),
    schedule_interval=timedelta(minutes=30),
    catchup=False,
    tags=['apitoazure', 'azure']
) as dag:
    # get_sports = PythonOperator(
    #     task_id='get_sports',
    #     python_callable=sports
    # )

    # load_azure = PythonOperator(
    #     task_id='load_sports_to_azure',
    #     python_callable=load_to_azure_blob
    # )

    load_azure_lake = PythonOperator(
        task_id='load_sports_to_azure_lake',
        python_callable=load_to_azure_lake
    )
    # get_scores = PythonOperator(
    #     task_id='get_scores',
    #     python_callable=scores
    # )

load_azure_lake
