from typing import List

from python_models.play import Play

class Drive:
    def __init__(
        self, id: int, description: str, yards: int,
        is_score: bool, num_offensive_plays: int, start_quarter: int,
        start_time: int, start_yardline: int, end_quarter: int, 
        end_time: int, end_yardline: int, plays: List[Play]
    ) -> None:
        self.id = id
        self.description = description
        self.yards = yards
        self.is_score = is_score
        self.num_offensive_plays = num_offensive_plays
        self.start_quarter = start_quarter
        self.start_time = start_time
        self.start_yardline = start_yardline
        self.end_quarter = end_quarter
        self.end_time = end_time
        self.end_yardline = end_yardline
        self.plays = plays

    def add_play(self, play: Play):
        self.plays.append(play)