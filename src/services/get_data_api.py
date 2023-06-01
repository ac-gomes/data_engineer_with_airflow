import requests
import json

from pydantic import BaseModel
from typing import Dict, Any

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
        self.default_sport = request_config.sport.get(
            "soccer_brazil_campeonato")
        self.default_request = request_config.request_type.get("sports")

    def data_request(self) -> ResponseData:

        try:
            if not self.request_type == self.default_request:
                response = self._get_scores(request_type=self.request_type)

                response_headers = dict(response.headers)
                json_string = json.dumps(response.json())
                response_data = json.loads(json_string)

                score_parser = Utils()
                data_score = score_parser.score_parser(response_data)

                return ResponseData(data=data_score, response_headers=response_headers)

            else:
                response = self._get_sport()

                response_headers = dict(response.headers)
                json_string = json.dumps(response.json())
                response_data = json.loads(json_string)

                sport_parser = Utils()
                data_sport = sport_parser.sport_parser(response_data)

                return ResponseData(data=data_sport, response_headers=response_headers)

        except Exception as Error:
            print(f"Something went wrong! Error: {Error}")

    def _get_scores(self, request_type):

        try:
            response = requests.get(
                f'{self._api_conn.API_URL}/{self.default_sport}/{request_type}',
                headers=self._request_config.headers,
                params=self._request_config.querystring.get(3)
            )

            return response

        except Exception as Error:
            print(f"Something went wrong! Error: {Error}")

    def _get_sport(self):

        try:
            response = requests.get(
                self._api_conn.API_URL,
                headers=self._request_config.headers,
                params=self._request_config.querystring.get(3)
            )

            return response

        except Exception as Error:
            print(f"Something went wrong! Error: {Error}")
