from datetime import datetime, timedelta
import logging

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor

from common.scripts.load_to_azure import upload_to_azure_bob
from sports.services.get_data_db import postgres_to_local
from common.scripts.file_manager import remove_temp_file

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


with DAG(
    dag_id='postgres_to_azure_v01.0',
    default_args=default_args,
    description='This will to get data from postgers and azure datalake',
    start_date=datetime(2023, 6, 12),
    schedule_interval='0 0 * * *',
    catchup=False,
    tags=['postgrestoazure', 'azure', 'blobstorage']

) as dag:
    start = EmptyOperator(
        task_id='Start'
    )

    get_data_from_postgres = PythonOperator(
        task_id='get_data_from_postgres',
        python_callable=postgres_to_local,
        op_kwargs={
            'postgres_conn_id': 'postgres_conn',
            'local_path': 'data/',
            'file_name': 'players_hist.txt',
            'query_statement': "SELECT * FROM players"
        }
    )

    is_players_hist_available = FileSensor(
        task_id='is_players_hist_available',
        filepath='players_hist.txt',
        fs_conn_id='local_file_system',
        poke_interval=5
    )

    load_players_hist_to_azure = PythonOperator(
        task_id='load_players_hist_to_azure',
        python_callable=upload_to_azure_bob,
        op_kwargs={
            'file_name': 'data/players_hist.txt',
            'blob_name': 'players/players_hist.txt',
            'container_name': 'raw',
            'wasb_conn_id': 'az-blob-conn'
        }
    )

    clear_tmp_files = PythonOperator(
        task_id='clear_tmp_files',
        python_callable=remove_temp_file
    )

    end = EmptyOperator(
        task_id='End'
    )

start >> get_data_from_postgres >> is_players_hist_available >> load_players_hist_to_azure >> clear_tmp_files >> end
