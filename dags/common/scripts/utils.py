from pydantic import BaseModel
from typing import Dict, Any


class SportsDict(BaseModel):
    key: str
    group: str
    title: str
    description: str
    active: str
    has_outrights: str


class SportsDictOut(BaseModel):
    __root__: Dict[str, Any]


class ScoresDict(BaseModel):
    id: str
    sport_key: str
    sport_title: str
    commence_time: str
    completed: str
    home_team: str
    away_team: str
    scores: Any
    last_update: str


class Utils():
    def __init__(self):
        self.data_dict = dict()

    def sport_parser(self, data):
        """Method to convert API sports from list to dict"""

        for count, item in enumerate(data):
            try:
                sport = SportsDict(
                    key=item.get('key'),
                    group=item.get('group'),
                    title=item.get('title'),
                    description=item.get('description'),
                    active=item.get('active'),
                    has_outrights=item.get('has_outrights')
                ).json(ensure_ascii=False)
                self.data_dict[int(count)] = sport

            except Exception as Error:
                print(f"Something went wrong! Error: {Error}")

        return self.data_dict

    def score_parser(self, data):
        """Method to convert API scores from list to dict"""

        try:
            for count, item in enumerate(data):
                score = ScoresDict(
                    id=item.get('id'),
                    sport_key=item.get('sport_key'),
                    sport_title=item.get('sport_title'),
                    commence_time=item.get('commence_time'),
                    completed=item.get('completed'),
                    home_team=item.get('home_team'),
                    away_team=item.get('away_team'),
                    scores=item.get('scores') if item.get(
                        'scores') is not None else 'null',
                    last_update=item.get('last_update') if item.get(
                        'scores') is not None else 'null'
                ).json(ensure_ascii=False)
                self.data_dict[int(count)] = score

        except Exception as Error:
            print(f"Something went wrong! Error: {Error}")

        return self.data_dict
