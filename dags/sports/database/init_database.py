from sqlalchemy_utils import database_exists, create_database
from db_connection import source_engine


def create_source_database():
    """ Create source database"""
    try:
        if not database_exists(source_engine.url):
            create_database(source_engine.url)
        print(f'is database available? {database_exists(source_engine.url)}')

    except Exception as Error:
        f'Something went wrong: {Error}'


if __name__ == '__main__':
    create_source_database()
