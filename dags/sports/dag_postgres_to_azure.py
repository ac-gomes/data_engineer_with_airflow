from datetime import datetime, timedelta
import logging

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sensors.filesystem import FileSensor

from common.scripts.load_to_azure import upload_to_azure_bob
from common.scripts.file_manager import write_csv_file, remove_temp_file

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def postgres_to_local() -> None:

    hook = PostgresHook(postgres_conn_id='postgres_conn')

    try:
        with hook.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM players")
            write_csv_file(
                file_content=[i[0] for i in cursor.description],
                cursor=cursor,
                local_path='data/',
                file_name='players_hist.txt'
            )
            cursor.close()
    except Exception as exec:
        conn.rollback()
        print(exec)
    logger.info("writing data in local file!")


default_args = {
    'owner': 'Toni',
    'retries': 3,
    'retry': timedelta(minutes=5)
}


with DAG(
    dag_id='postgres_to_azure_v01.2',
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
        python_callable=postgres_to_local
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
