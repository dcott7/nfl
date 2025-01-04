from typing import Dict, Any

class DraftPick:
    def __init__(self, round: int, pick: int):
        self.round = round
        self.pick = pick

    def to_dict(self) -> Dict[str, Any]:
        return {
            'round': self.round,
            'pick': self.pick
        }