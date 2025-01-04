from typing import List

from python_models.athlete import Athlete
from python_models.stat import Stat

class PlayParticipant:
    def __init__(
        self, athlete: Athlete, stats: List[Stat], 
        order: int, type: str
    ) -> None:
        self.athlete = athlete
        self.stats = stats
        self.order = order
        self.type = type