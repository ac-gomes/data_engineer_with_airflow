# data_engineer_with_airflow

## project structure
```sql
dags
├── common
│   ├── config
│   │   ├── __init__.py
│   │   └── odds_api.py
│   └── scripts
│       ├── __init__.py
│       └── utils.py
└── sports
    ├── database
    │   ├── __init__.py
    │   ├── api_connection.py
    │   ├── db_connection.py
    │   ├── init_db.py
    │   ├── landing_model.py
    │   └── source_model.py
    └── services
        ├── __init__.py
        ├── get_data_api.py
        └── get_data_db.py

```