import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
from airflow.operators.empty import EmptyOperator
from airflow.sensors.filesystem import FileSensor

from sports.services.get_data_api import GetAPIData
from common.scripts.file_manager import write_json_file, remove_temp_file

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

default_args = {
    'owner': 'Toni',
    'retries': 3,
    'retry': timedelta(minutes=5)
}


def sports(local_path, file_name):
    retrive_sports = GetAPIData('sports')
    response = retrive_sports.data_request()
    logger.info("fetching sport data from API")

    write_json_file(response, local_path, file_name)
    logger.info("creating file on local system")


def scores(local_path, file_name):
    retrive_scores = GetAPIData('scores')
    response = retrive_scores.data_request()
    logger.info("fetching score data from API")

    write_json_file(response, local_path, file_name)
    logger.info("creating file on local system")


def load_to_azure_blob(file_name, container_name, blob_name):
    Wasb_Hook = WasbHook(wasb_conn_id='az-blob-conn')

    Wasb_Hook.load_file(
        file_path=file_name,
        container_name=container_name,
        blob_name=blob_name,
        overwrite=True,
    )
    logger.info("loading data to Azur blob storage")


with DAG(
    dag_id='API_to_azure_v1.0',
    default_args=default_args,
    description='This will to get data from sports API',
    start_date=datetime(2023, 6, 6),
    schedule_interval='0 0 * * *',
    catchup=False,
    tags=['apitoazure', 'azure', 'blobstorage']
) as dag:
    Start = EmptyOperator(
        task_id='Start'
    )

    fetch_sport_data = PythonOperator(
        task_id='fetch_sport_data',
        python_callable=sports,
        op_kwargs={
            'local_path': 'data',
            'file_name': 'sports.json'
        }
    )

    is_sports_available = FileSensor(
        task_id='is_sports_available',
        filepath='scores.json',
        fs_conn_id='local_file_system',
        poke_interval=5
    )

    fetch_scores_data = PythonOperator(
        task_id='fetch_scores_data',
        python_callable=scores,
        op_kwargs={
            'local_path': 'data',
            'file_name': 'scores.json'
        }
    )

    is_scores_available = FileSensor(
        task_id='is_scores_available',
        filepath='scores.json',
        fs_conn_id='local_file_system',
        poke_interval=5
    )

    load_sports_to_azure = PythonOperator(
        task_id='load_sports_to_azure',
        python_callable=load_to_azure_blob,
        op_kwargs={
            'file_name': 'data/sports.json',
            'blob_name': 'sports/sports.json',
            'container_name': 'raw',
        }
    )

    load_scores_to_azure = PythonOperator(
        task_id='load_scores_to_azure',
        python_callable=load_to_azure_blob,
        op_kwargs={
            'file_name': 'data/sports.json',
            'blob_name': 'scores/scores.json',
            'container_name': 'raw',
        }
    )

    clear_tmp_files = PythonOperator(
        task_id='Clear_tmp_files',
        python_callable=remove_temp_file
    )

    End = EmptyOperator(
        task_id='End'
    )
[Start >> fetch_sport_data >> is_sports_available >> load_sports_to_azure,
 Start >> fetch_scores_data >> is_scores_available >> load_scores_to_azure] >> clear_tmp_files >> End
