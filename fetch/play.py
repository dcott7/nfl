from typing import Dict, Any, List

from models.play import Play
from fetch.play_participant import create_participants

def create_play(play_data: Dict[str, Any]) -> Play:
    """Creates a Play.

    Params:
        play_data: dictionary data from ESPN response.

    Returns:
        Play object.
    """

    start_data = play_data.get('start',{})
    end_data = play_data.get('end',{})
    play_type_data = play_data.get('type', {})
    
    return Play(
        id = int(play_data['id']),
        sequence_number = int(play_data['sequenceNumber']),
        play_type = str(play_type_data.get('text', 'Unknown')),
        description = str(play_data['text']),
        away_score = int(play_data['awayScore']),
        home_score = int(play_data['homeScore']),
        quarter = int(play_data.get('period',{})['number']),
        is_scoring_play = bool(play_data['scoringPlay']),
        score_value = int(play_data['scoreValue']),
        participants = create_participants(play_data.get('participants',{})),
        start_down = start_data['down'],
        end_down = end_data['down'],
        start_distance = start_data['distance'],
        end_distance = end_data['distance'],
        start_yardline = start_data['yardLine'],
        end_yardline = end_data['yardLine'],
        start_yards_to_endzone = start_data['yardsToEndzone'],
        end_yards_to_endzone = end_data['yardsToEndzone']
    )

def create_plays(plays_data: List[Dict[str, Any]]) -> List[Play]:
    """Creates a List of Plays."""
    return [create_play(play_data) for play_data in plays_data.get('items',{})]