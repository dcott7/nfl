from typing import List

from models.play_participant import PlayParticipant

class Play:
    def __init__(
        self, id: int, sequence_number: int, play_type: str,
        description: str, away_score: int, home_score: int,
        quarter: int, is_scoring_play: bool,
        score_value: int, participants: List[PlayParticipant],
        start_down: int, end_down: int, start_distance: int, 
        end_distance: int, start_yardline: int, end_yardline: int, 
        start_yards_to_endzone: int, end_yards_to_endzone: int,
    ) -> None:
        self.id = id
        self.sequence_number = sequence_number
        self.play_type = play_type
        self.description = description
        self.away_score = away_score
        self.home_score = home_score
        self.quarter = quarter
        self.is_scoring_play = is_scoring_play
        self.score_value = score_value
        self.participants = participants
        self.start_down = start_down
        self.end_down = end_down
        self.start_distance = start_distance
        self.end_distance = end_distance
        self.start_yardline = start_yardline
        self.end_yardline = end_yardline
        self.start_yards_to_endzone = start_yards_to_endzone
        self.end_yards_to_endzone = end_yards_to_endzone
        
        