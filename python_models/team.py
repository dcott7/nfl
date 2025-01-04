from typing import List, Dict, Any

from python_models.athlete import Athlete
from python_models.position import PositionEnum
from python_models.draft import DraftPick
from python_models.event import Event

class Team:
    def __init__(
        self, name: str, id: int, active_roster: List[Athlete], 
        practice_squad: List[Athlete],
        cap_room: float, draft_picks: List[DraftPick]
    ) -> None:
        self.name = name
        self.id = id
        self.active_roster = active_roster
        self.practice_squad = practice_squad
        self.cap_room = cap_room
        self.draft_picks = draft_picks
        self.events: List[Event] = []
        
    def add_event(self, event: Event):
        self.events.append(event)