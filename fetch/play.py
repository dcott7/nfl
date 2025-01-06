from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models import Play
from fetch.play_participant import create_participants

def create_play(session: Session, play_data: Dict[str, Any], drive_id) -> Play:
    """Creates and persists a Play object in the database.

    Params:
        session: SQLAlchemy session object.
        play_data: dictionary data for a single play from ESPN response.

    Returns:
        Persisted Play object.
    """

    # Check if the Play object already exists
    play_id = int(play_data['id'])
    existing_play = session.query(Play).filter_by(id=play_id).first()

    if existing_play:
        return existing_play

    # Parse data for the Play object
    start_data = play_data.get('start', {})
    end_data = play_data.get('end', {})
    play_type_data = play_data.get('type', {})

    # Create the Play object
    play = Play(
        id=play_id,
        sequence_number=int(play_data['sequenceNumber']),
        play_type=str(play_type_data.get('text', 'Unknown')),
        description=str(play_data['text']),
        away_score=int(play_data['awayScore']),
        home_score=int(play_data['homeScore']),
        quarter=int(play_data.get('period', {}).get('number', 0)),
        is_scoring_play=bool(play_data['scoringPlay']),
        score_value=int(play_data['scoreValue']),
        start_down=start_data.get('down'),
        end_down=end_data.get('down'),
        start_distance=start_data.get('distance'),
        end_distance=end_data.get('distance'),
        start_yardline=start_data.get('yardLine'),
        end_yardline=end_data.get('yardLine'),
        start_yards_to_endzone=start_data.get('yardsToEndzone'),
        end_yards_to_endzone=end_data.get('yardsToEndzone'),
        drive_id=drive_id
    )

    # Add relationships for PlayParticipants
    participants_data = play_data.get('participants', {})
    participants = create_participants(session, participants_data, play_id)
    play.participants.extend(participants)

    # Persist the Play object to the database
    session.add(play)
    session.commit()

    return play


def create_plays(session: Session, plays_data: Dict[str, Any], drive_id) -> List[Play]:
    """Creates and persists a list of Play objects in the database.

    Params:
        session: SQLAlchemy session object.
        plays_data: dictionary data containing a list of plays.

    Returns:
        List of persisted Play objects.
    """
    plays_list = plays_data.get('items', [])
    return [create_play(session, play_data, drive_id) for play_data in plays_list]
