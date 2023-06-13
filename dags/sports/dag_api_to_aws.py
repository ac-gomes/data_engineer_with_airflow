import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.sensors.filesystem import FileSensor


from sports.services.get_data_api import GetAPIData
from common.scripts.load_to_aws import AWSUploader
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


def upload_to_aws(bucket_name, filename, key):
    load_to_s3 = AWSUploader

    load_to_s3.upload_to_s3_bucket(
        bucket_name=bucket_name,
        filename=filename,
        key=key
    )
    logger.info("loading data to AWS s3 bucket")


with DAG(
    dag_id='API_to_aws_v1.0',
    default_args=default_args,
    description='This will to get data from sports API',
    start_date=datetime(2023, 6, 6),
    schedule_interval=timedelta(minutes=30),
    catchup=False,
    tags=['apitos3', 'aws']
) as dag:
    start = EmptyOperator(
        task_id='start'
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

    load_sports_s3_bucket = PythonOperator(
        task_id='load_sports_s3_bucket',
        python_callable=upload_to_aws,
        op_kwargs={
            'bucket_name': 's3-airflow-dev',
            'filename': 'data/sports.json',
            'key': 'sport/sports.json'
        }
    )
    load_scores_s3_bucket = PythonOperator(
        task_id='load_scores_s3_bucket',
        python_callable=upload_to_aws,
        op_kwargs={
            'bucket_name': 's3-airflow-dev',
            'filename': 'data/scores.json',
            'key': 'score/scores.json'
        }
    )
    Clear_tmp_files = PythonOperator(
        task_id='Clear_tmp_files',
        python_callable=remove_temp_file
    )

    end = EmptyOperator(
        task_id='end'
    )

[start >> fetch_sport_data >> is_sports_available >> load_sports_s3_bucket,
 start >> fetch_scores_data >> is_scores_available >> load_scores_s3_bucket] >> Clear_tmp_files >> end
