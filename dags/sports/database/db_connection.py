from os import getenv
from dotenv import load_dotenv, find_dotenv

from sqlalchemy import create_engine


load_dotenv(find_dotenv())
SOURCE_DATABASE_URL = getenv('SOURCE_DATABASE_URL')
LANDING_DATABASE_URL = getenv('LANDING_DATABASE_URL')

source_engine = create_engine(SOURCE_DATABASE_URL, echo=True)

landing_engine = create_engine(LANDING_DATABASE_URL, echo=True)
