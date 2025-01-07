from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models import PlayParticipant
from fetch.stat import create_stats
from fetch.util import fetch_page
from fetch.athlete import create_athlete
from models import Athlete

def create_participant(session: Session, participant_data: Dict[str, Any], play_id) -> PlayParticipant:
    """Creates and persists a PlayParticipant object in the database.

    Params:
        session: SQLAlchemy session object.
        participant_data: dictionary data from ESPN response.

    Returns:
        Persisted PlayParticipant object.
    """
    
    athlete_url = participant_data.get('athlete', {}).get('$ref', '')
    athlete_id = athlete_url.split('/')[-1].replace('?lang=en&region=us','')
    
    athlete = session.query(Athlete).filter_by(id=athlete_id).first()
    if not athlete:
        athlete_data = fetch_page(athlete_url)
        athlete = create_athlete(session, athlete_data, None)

    order = int(participant_data['order'])

    existing_participant = session.query(PlayParticipant).filter_by(athlete_id=athlete_id, order=order).first()
    if existing_participant:
        return existing_participant

    participant = PlayParticipant(
        athlete=athlete,
        stats=[],
        order=order,
        type=str(participant_data['type']),
        play_id=play_id
    )

    session.add(participant)
    session.commit()

    stats = create_stats(session, participant_data.get('stats', []), participant.id)
    participant.stats = stats

    session.add(participant)
    session.commit()

    return participant


def create_participants(session: Session, participants_data: List[Dict[str, Any]], play_id) -> List[PlayParticipant]:
    """Creates and persists a list of PlayParticipant objects in the database.

    Params:
        session: SQLAlchemy session object.
        participants_data: List of dictionary data for multiple participants.

    Returns:
        List of persisted PlayParticipant objects.
    """
    return [create_participant(session, participant_data, play_id) for participant_data in participants_data]
