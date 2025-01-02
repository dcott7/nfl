from typing import List, Dict, Any

from models.athlete import Athlete
from models.position import PositionEnum
from models.draft import DraftPick
from models.event import Event

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

    def add_player_active_roster(self, player: Athlete):
        self.active_roster.append(player)

    def add_player_practice_squad(self, player: Athlete):
        self.practice_squad.append(player)

    def get_players_by_pos_ranked(self, position: PositionEnum) -> List[Athlete]:
        players = [player for player in self.roster if player.position == position]
        return sorted(players, key=lambda player: player.get_overall(), reverse=True)
    
    def can_afford_cap(self, amount: float):
        can_afford = True if amount <= self.cap_room else False
        return can_afford
    
    def recalc_cap_room(self):
        self.cap_room = sum([player.salary for player in self.roster])
    
    def add_draft_pick(self, pick: DraftPick):
        self.draft_picks.append(pick)
    
    def adjust_cap_room(self, amount_change: float):
        self.cap_room += amount_change

    # def reset_wins(self):
    #     self.wins = 0

    # def reset_losses(self):
    #     self.losses = 0

    # def reset_ties(self):
    #     self.ties = 0

    # def reset_record(self):
    #     self.reset_wins()
    #     self.reset_losses()
    #     self.reset_ties()

    def to_dict(self) -> Dict[str,Any]:
        return {
            'name': self.name,
            'id': self.id,
            'roster': [athlete.to_dict() for athlete in self.roster],
            'cap_room': self.cap_room,
            'draft_picks': [pick.to_dict() for pick in self.draft_picks]
        }