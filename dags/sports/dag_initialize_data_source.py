from datetime import datetime, timedelta
import logging

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def insert_into_table() -> None:
    hook = PostgresHook(postgres_conn_id='postgres_conn')

    with hook.get_conn() as conn:
        hook.copy_expert("""COPY src_db.public.players  FROM stdin WITH CSV HEADER
                        DELIMITER as ',' """,
                         'dags/sports/includes/db_data.csv')
        conn.commit()
    logger.info("load data into src_db database!")


default_args = {
    'owner': 'Toni',
    'retries': 3,
    'retry': timedelta(minutes=5)
}


with DAG(
    dag_id='initialize_data_source_v01.0',
    default_args=default_args,
    description='Create source table and insert data into it',
    start_date=datetime(2023, 6, 12),
    schedule_interval='0 0 * * *',
    catchup=False,
    tags=['localdatabase', 'sourcetable', 'datagathering']

) as dag:
    start = EmptyOperator(
        task_id='Start'
    )
    is_database_available = PostgresOperator(
        task_id='is_database_available',
        postgres_conn_id='postgres_conn',
        sql="""
          DO $$
          BEGIN
          IF exists (SELECT datname FROM pg_database where datname ='src_db') THEN
          RAISE NOTICE  'data base already exists';
          ELSE
          RAISE NOTICE  'Run python3 -m init_database';
          END IF;
          END $$;
        """
    )
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_conn',
        sql="""
        CREATE TABLE IF NOT EXISTS players (
          ACCESS_DATETIME CHAR(25) NOT NULL,
          CUSTOMER_ID CHAR(10) NOT NULL,
          MODALITY CHAR(10),
          RAKE double precision NOT NULL
        )
        """
    )

    load_data_to_table = PythonOperator(
        task_id='load_data_to_table',
        python_callable=insert_into_table,
    )


start >> is_database_available >> create_table >> load_data_to_table
