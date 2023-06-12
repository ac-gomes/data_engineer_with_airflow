from os import getenv
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import create_engine


load_dotenv(find_dotenv())
SOURCE_POSTGRES_URL = getenv('SOURCE_POSTGRES_URL')


source_engine = create_engine(SOURCE_POSTGRES_URL, echo=True)
