from typing import List

class Competitor:
    def __init__(
        self, id: int, is_home: bool, is_winner: bool, score: int
    ) -> None:
        self.id = id
        self.is_home = is_home
        self.is_winner = is_winner
        self.score = score
        self.team: 'Team' = None
        
    def set_team(self, teams: List['Team']) -> None:
        self.team = [team for team in teams if team.id == self.id][0]

    def __str__(self):
        return (
            f"<Competitor(id={self.id}, is_winner={self.is_winner}, is_home={self.is_home})>"
        )
    
    def __repr__(self):
        return self.__str__()