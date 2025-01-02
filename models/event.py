# http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/types/2/weeks/11/events?lang=en&region=us

from models.weather import Weather
from models.competition import Competition

class Event:
    def __init__(
        self, id: int, season: int, week: int, 
        season_type: int, name: str, weather: Weather,
        competition: Competition
    ) -> None:
        self.id = id
        self.name = name
        self.season = season
        self.week = week
        self.season_type = season_type
        self.weather = weather
        self.competition = competition

    def __str__(self) -> str:
        return (
            f"<Event(id={self.id}, name='{self.name}', season={self.season}, "
            f"week={self.week}, season_type={self.season_type}, "
            f"weather={self.weather.__repr__()}, competition={self.competition.__repr__()})>"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
