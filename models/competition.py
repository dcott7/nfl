import datetime
from typing import List

from models.venue import Venue
from models.competitor import Competitor
from models.drive import Drive

class Competition:
    def __init__(
        self, id: int, date: datetime.datetime, venue: Venue, 
        competitors: List[Competitor], drives: List[Drive]
    ) -> None:
        self.id = id
        self.date = date
        self.venue = venue
        self.competitors = competitors
        self.drives = drives

    def __str__(self):
        return (
            f"<Competition(id={self.id}, date={self.date}, venue={self.venue.__repr__()} "
            f"competitors={[competitor.__repr__() for competitor in self.competitors]})>"
        )
    
    def __repr__(self):
        return self.__str__()