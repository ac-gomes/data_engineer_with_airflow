from os import getenv
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
API_HOST = getenv('API_HOST')
SPORTS_END_POINT = getenv('SPORTS_END_POINT')
API_KEY = getenv('API_KEY')


class APIConn(BaseModel):
    API_HOST: str
    SPORTS_END_POINT: str
    API_KEY: str
    API_URL: str


api_conn = APIConn(
    API_HOST=API_HOST,
    SPORTS_END_POINT=SPORTS_END_POINT,
    API_KEY=API_KEY,
    API_URL=f'https://{API_HOST}/{SPORTS_END_POINT}'
)
