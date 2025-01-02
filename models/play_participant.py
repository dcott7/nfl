from typing import List

from models.athlete import Athlete
from models.stat import Stat

class PlayParticipant:
    def __init__(
        self, athlete: Athlete, stats: List[Stat], 
        order: int, type: str
    ) -> None:
        self.athlete = athlete
        self.stats = stats
        self.order = order
        self.type = type