# data_engineer_with_airflow

## project structure
```sql
├── config
├── dags
│   ├── common
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   └── odds_api.py
│   │   └── scripts
│   │       ├── __init__.py
│   │       ├── file_manager.py
│   │       ├── load_to_aws.py
│   │       ├── load_to_azure.py
│   │       └── utils.py
│   └── sports
│       ├── dag_api_to_aws.py
│       ├── dag_api_to_azure.py
│       ├── dag_initialize_data_source.py
│       ├── dag_postgres_to_aws.py
│       ├── dag_postgres_to_azure.py
│       ├── database
│       │   ├── __init__.py
│       │   ├── api_connection.py
│       │   ├── db_connection.py
│       │   └── init_database.py
│       ├── includes
│       │   └── db_data.csv
│       └── services
│           ├── get_data_api.py
│           └── get_data_db.py
├── data
├── docker-compose.yaml
├── plugins
├── requirements.txt
├── Dockerfile
├── README.md
```