from pydantic import BaseModel
from typing import Dict, Any

import requests
import json

from database.api_connection import api_conn
from config.odds_api import request_config
from utils.utils import Utils


class ResponseData(BaseModel):
    data: Dict[str, Any]
    response_headers: Dict[str, Any]


class GetAPIData():
    """This class will retrive data from API """

    def __init__(self, request_type) -> None:
        self.request_type = request_type
        self._request_config = request_config
        self._api_conn = api_conn
        self.default = request_config.sport.get("soccer_brazil_campeonato")

    def data_request(self) -> ResponseData:
        try:
            if not self._request_config.sport.get(self.default):
                response = self._get_scores(request_type=self.request_type)
            else:
                response = self._get_sport(request_type=self.request_type)

            json_string = json.dumps(response.json())
            response_data = json.loads(json_string)

            response_parser = Utils(response_data)
            data = response_parser.sport_parser()

            response_headers = dict(response.headers)

            return ResponseData(data=data, response_headers=response_headers)

        except Exception as Error:
            print(f"Something went wrong! Error: {Error}")

    def _get_scores(self, request_type):

        try:
            response = requests.get(
                self._api_conn.API_URL,
                headers=self._request_config.headers,
                params=self._request_config.querystring.get(3)
            )

            return response

        except Exception as Error:
            print(f"Something went wrong! Error: {Error}")

    def _get_sport(self, request_type):

        try:
            response = requests.get(
                self._api_conn.API_URL,
                headers=self._request_config.headers,
                params=self._request_config.querystring.get(3)
            )

            return response

        except Exception as Error:
            print(f"Something went wrong! Error: {Error}")


# 'https://odds.p.rapidapi.com/v4/sports/upcoming/odds',

# 'https://odds.p.rapidapi.com/v4/sports/americanfootball_nfl/scores',


# Response Headers
# x-requests-remaining   The number of requests remaining until the quota resets
# x-requests-used   The number of requests used since the last quota reset
