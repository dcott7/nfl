from typing import Dict, Any, List

from python_models.play_participant import PlayParticipant
from fetch.stat import create_stats
from fetch.util import fetch_page
from fetch.athlete import get_or_create_athlete

def create_participant(participant_data: Dict[str, Any]) -> PlayParticipant:
    """Creates an PlayParticipant.

    Params:
        participant_data: dictionary data from ESPN response.

    Returns:
        EvenPlayParticipantt object.
    """
    
    athlete_data = fetch_page(participant_data.get('athlete',{})['$ref'])

    return PlayParticipant(
        athlete = get_or_create_athlete(athlete_data),
        stats = create_stats(participant_data.get('stats',{})),
        order = int(participant_data['order']),
        type = str(participant_data['type'])
    )

def create_participants(participants_data: List[Dict[str, Any]]) -> List[PlayParticipant]:
    """Creates a List of PlayParticipant."""
    return [create_participant(participant_data) for participant_data in participants_data]