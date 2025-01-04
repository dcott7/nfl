import datetime
from typing import List

from python_models.team import Team
from python_models.drive import Drive

class Game:
    def __init__(self, away_team: Team, home_team: Team, date: datetime.datetime):
        self.away_team = away_team
        self.home_team = home_team
        self.date = date
        self.drives: List[Drive] = []
