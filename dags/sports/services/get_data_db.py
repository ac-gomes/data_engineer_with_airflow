from airflow.providers.postgres.hooks.postgres import PostgresHook
from common.scripts.file_manager import write_csv_file


def postgres_to_local(postgres_conn_id, local_path, file_name, query_statement) -> None:

    hook = PostgresHook(postgres_conn_id=postgres_conn_id)

    try:
        with hook.get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(query_statement)
            write_csv_file(
                file_content=[i[0] for i in cursor.description],
                cursor=cursor,
                local_path=local_path,
                file_name=file_name
            )
            cursor.close()
    except Exception as Error:
        conn.rollback()
        print(Error)
