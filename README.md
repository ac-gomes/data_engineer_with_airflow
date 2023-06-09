# data_engineer_with_airflow

## project structure
```sql
.
├── Dockerfile
├── LICENSE
├── README.md
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
│       ├── database
│       │   ├── __init__.py
│       │   ├── api_connection.py
│       │   ├── db_connection.py
│       │   ├── init_db.py
│       │   ├── landing_model.py
│       │   └── source_model.py
│       └── services
│           ├── __init__.py
│           ├── get_data_api.py
│           └── get_data_db.py
├── data
├── db.py
├── docker-compose.yaml
├── plugins
├── requirements.txt

```