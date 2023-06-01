
from pydantic import BaseModel
from database.api_connection import API_HOST, API_KEY


class RequestConfig(BaseModel):
    querystring: dict
    headers: dict
    params: dict
    all: dict
    sport: dict
    dateFormat: dict
    request_type: dict


request_config = RequestConfig(
    querystring={
        1: {"daysFrom": 1},
        2: {"daysFrom": 2},
        3: {"daysFrom": 3},
    },
    headers={
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    },
    params={
        "regions": 'us',
        "oddsFormat": 'decimal',
        "markets": 'h2h,spreads',
        "dateFormat": 'iso'
    },
    all={
        "all": 'true'
    },
    sport={
        "soccer_brazil_campeonato": "soccer_brazil_campeonato"
    },
    dateFormat={
        "iso": "iso",
        "unix": "unix"
    },
    request_type={
        "scores": "scores",
        "sports": "sports"
    }
)
