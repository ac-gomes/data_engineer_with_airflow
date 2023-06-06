from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.providers.http.sensors.http import HttpSensor


from sports.services.get_data_api import GetAPIData


default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry': timedelta(minutes=5)
}


def sports():
    retrive_sports = GetAPIData('sports')
    response = retrive_sports.data_request()
    print(response)


def scores():
    retrive_scores = GetAPIData('scores')
    response = retrive_scores.data_request()
    print(response)


with DAG(
    dag_id='GetAPIdata_v01.02',
    default_args=default_args,
    description='This will to get data from sports API',
    start_date=datetime(2023, 6, 6),
    schedule_interval=timedelta(minutes=30),
    catchup=False
) as dag:
    get_sports = PythonOperator(
        task_id='get_sports',
        python_callable=sports
    )
    get_scores = PythonOperator(
        task_id='get_scores',
        python_callable=scores
    )

get_sports >> get_scores
