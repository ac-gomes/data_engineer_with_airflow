from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


from sports.services.get_data_api import GetAPIData
from common.scripts.load_to_aws import AWSUploader
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


def upload_to_aws(bucket_name, filename, key):
    load_to_s3 = AWSUploader

    load_to_s3.upload_to_s3_bucket(
        bucket_name=bucket_name,
        filename=filename,
        key=key
    )


with DAG(
    dag_id='APIdata_aws_01.3',
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

    upload_sports_s3_bucket = PythonOperator(
        task_id='upload_sports_s3_bucket',
        python_callable=upload_to_aws,
        op_kwargs={
            'bucket_name': 's3-airflow-dev',
            'filename': 'data/sports.json',
            'key': 'sport/sports.json'
        }
    )
    upload_scores_s3_bucket = PythonOperator(
        task_id='upload_scores_s3_bucket',
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

start >> get_sports >> get_scores >> [
    upload_sports_s3_bucket, upload_scores_s3_bucket] >> end
