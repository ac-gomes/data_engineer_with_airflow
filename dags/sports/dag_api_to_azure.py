from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.operators.empty import EmptyOperator

from sports.services.get_data_api import GetAPIData
from common.scripts.file_manager import write_json_file, remove_temp_file


default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry': timedelta(minutes=5)
}


def sports(local_path, file_name):
    retrive_sports = GetAPIData('sports')
    response = retrive_sports.data_request()
    write_json_file(response, local_path, file_name)


def scores(local_path, file_name):
    retrive_scores = GetAPIData('scores')
    response = retrive_scores.data_request()
    write_json_file(response, local_path, file_name)


def load_to_azure_blob(file_name, container_name, blob_name):
    Wasb_Hook = WasbHook(wasb_conn_id='az-blob-conn')

    Wasb_Hook.load_file(
        file_path=file_name,
        container_name=container_name,
        blob_name=blob_name,
        overwrite=True,
    )


with DAG(
    dag_id='APIdata_azure_01.5',
    default_args=default_args,
    description='This will to get data from sports API',
    start_date=datetime(2023, 6, 6),
    schedule_interval=timedelta(minutes=30),
    catchup=False,
    tags=['apitoazure', 'azure']
) as dag:
    Start = EmptyOperator(
        task_id='Start'
    )

    get_sports = PythonOperator(
        task_id='get_sports',
        python_callable=sports,
        op_kwargs={
            'local_path': 'data',
            'file_name': 'sports.json'
        }
    )

    get_scores = PythonOperator(
        task_id='get_scores',
        python_callable=scores,
        op_kwargs={
            'local_path': 'data',
            'file_name': 'scores.json'
        }
    )

    load_sports_to_azure_lake = PythonOperator(
        task_id='load_sports_to_azure_lake',
        python_callable=load_to_azure_blob,
        op_kwargs={
            'file_name': 'data/sports.json',
            'blob_name': 'sports/sports.json',
            'container_name': 'raw',
        }
    )

    load_scores_to_azure_lake = PythonOperator(
        task_id='load_scores_to_azure_lake',
        python_callable=load_to_azure_blob,
        op_kwargs={
            'file_name': 'data/sports.json',
            'blob_name': 'scores/scores.json',
            'container_name': 'raw',
        }
    )

    Clear_tmp_files = PythonOperator(
        task_id='Clear_tmp_files',
        python_callable=remove_temp_file
    )

    End = EmptyOperator(
        task_id='End'
    )
Start >> get_sports >> get_scores >> [
    load_sports_to_azure_lake, load_scores_to_azure_lake] >> Clear_tmp_files >> End
