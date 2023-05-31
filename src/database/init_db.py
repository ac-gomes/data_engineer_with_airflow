from landing_model import LandingBase
from source_model import SourceBase
from db_connection import source_engine, landing_engine


def create_source_database():
    """ Delete and recreate tables from source """
    try:
        with source_engine.begin() as source_connection:
            SourceBase.metadata.drop_all(bind=source_connection)
            SourceBase.metadata.create_all(bind=source_connection)
            source_connection.execute("commit")
            source_connection.close()

    except Exception as Error:
        f'Something went wrong: {Error}'


def create_landing_database():
    """ Delete and recreate tables from landing """
    try:
        with landing_engine.begin() as landing_connection:
            LandingBase.metadata.drop_all(bind=landing_connection)
            LandingBase.metadata.create_all(bind=landing_connection)
            landing_connection.execute("commit")
            landing_connection.close()

    except Exception as Error:
        f'Something went wrong: {Error}'


if __name__ == '__main__':
    create_source_database()
    create_landing_database()
