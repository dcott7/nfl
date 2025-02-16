from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models import PlayParticipant, Athlete
from db.load.stat import create_stats
from db.util import fetch_page
from db.load.athlete import create_athlete
from util import get_id_from_url
from db.extract.athlete import extract_athlete
from db.extract.play_participant import extract_play_participant
    
    
def get_or_create_athlete(session: Session, athlete_url: str) -> Athlete:
    """
    Retrieve an Athlete object, either by querying the database or fetching and creating it.

    Args:
        session (Session): SQLAlchemy session object.
        athlete_url (str): The URL to fetch the athlete's data from.

    Returns:
        Athlete: The retrieved or newly created Athlete object.
    """
    athlete_id = int(get_id_from_url(athlete_url))

    athlete = extract_athlete(session, athlete_id)
    
    if athlete:
        return athlete

    athlete_data = fetch_page(athlete_url)
    return create_athlete(session, athlete_data, None)


def create_participant(session: Session, participant_data: Dict[str, Any], play_id: int) -> PlayParticipant:
    """Creates and persists a PlayParticipant object in the database.

    Args:
        session (Session): SQLAlchemy session object.
        participant_data (Dict[str, Any]): Dictionary data from ESPN response.
        play_id (int): The ID of the play this participant is associated with.

    Returns:
        PlayParticipant: The persisted PlayParticipant object.
    """
    athlete_url = participant_data.get('athlete', {}).get('$ref', '')
    athlete = get_or_create_athlete(session, athlete_url)

    order = int(participant_data['order'])

    participant = extract_play_participant(session, athlete.id, order)

    if not participant:
        participant = PlayParticipant(
            athlete_id=athlete.id,
            stats=[],
            order=order,
            type=str(participant_data['type']),
            play_id=play_id
        )

        session.add(participant)
        session.commit()

    create_stats(session, participant_data.get('stats', []), participant.id)

    session.commit()
    return participant


def create_participants(session: Session, participants_data: List[Dict[str, Any]], play_id: int) -> List[PlayParticipant]:
    """Creates and persists a list of PlayParticipant objects in the database.

    Args:
        session (Session): SQLAlchemy session object.
        participants_data (List[Dict[str, Any]]): List of dictionaries containing participant data.
        play_id (int): The ID of the play these participants are associated with.

    Returns:
        List[PlayParticipant]: List of persisted PlayParticipant objects.
    """
    participants = []
    for participant_data in participants_data:
        participant = create_participant(session, participant_data, play_id)
        participants.append(participant)

    return participants
