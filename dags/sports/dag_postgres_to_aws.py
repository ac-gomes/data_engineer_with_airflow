from datetime import datetime, timedelta
import logging

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor

from common.scripts.file_manager import remove_temp_file
from common.scripts.load_to_aws import AWSUploader
from sports.services.get_data_db import postgres_to_local

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


def upload_to_aws(bucket_name, filename, key):
    load_to_s3 = AWSUploader
    load_to_s3.upload_to_s3_bucket(
        bucket_name=bucket_name,
        filename=filename,
        key=key
    )
    logger.info("loading data to AWS s3 bucket")


with DAG(
    dag_id='postgres_to_aws_v01.0',
    default_args=default_args,
    description='This will to get data from postgers and write into s3 buckt',
    start_date=datetime(2023, 6, 6),
    schedule_interval='0 0 * * *',
    catchup=False,
    tags=['postgrestoaws', 'aws', 's3buckt']
) as dag:
    start = EmptyOperator(
        task_id='start'
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

    load_players_hist_s3_bucket = PythonOperator(
        task_id='load_players_hist_s3_bucket',
        python_callable=upload_to_aws,
        op_kwargs={
            'bucket_name': 's3-airflow-dev',
            'filename': 'data/players_hist.txt',
            'key': 'players/players_hist.txt'
        }
    )

    clear_tmp_files = PythonOperator(
        task_id='clear_tmp_files',
        python_callable=remove_temp_file
    )

    end = EmptyOperator(
        task_id='end'
    )

start >> get_data_from_postgres >> is_players_hist_available >> load_players_hist_s3_bucket >> clear_tmp_files >> end
