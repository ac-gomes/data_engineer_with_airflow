from pydantic import BaseModel


class SportsDict(BaseModel):
    key: str
    group: str
    title: str
    description: str
    active: str
    has_outrights: str


class Utils():
    def __init__(self, data):
        self.data = data
        self.data_dict = dict()

    def sport_parser(self):
        """Method to convert API response from list to dict"""

        for count, item in enumerate(self.data):
            try:
                sport = SportsDict(
                    key=item.get('key'),
                    group=item.get('group'),
                    title=item.get('title'),
                    description=item.get('description'),
                    active=item.get('active'),
                    has_outrights=item.get('has_outrights')
                )
                self.data_dict[count] = sport
            except Exception as Error:
                print(f"Something went wrong! Error: {Error}")

        return self.data_dict
