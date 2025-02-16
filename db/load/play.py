from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models import Play
from db.load.play_participant import create_participants
from db.extract.play import extract_play


def create_play_object(play_data: Dict[str, Any], drive_id: int) -> Play:
    """
    Create a Play object from the given data.

    Args:
        play_data (Dict[str, Any]): Data for the play.
        drive_id (int): The ID of the drive this play belongs to.

    Returns:
        Play: The newly created Play object.
    """
    start_data = play_data.get('start', {})
    end_data = play_data.get('end', {})
    play_type_data = play_data.get('type', {})

    return Play(
        id=int(play_data['id']),
        sequence_number=int(play_data['sequenceNumber']),
        play_type=str(play_type_data.get('text', 'None')),
        description=str(play_data.get('text','None')),
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


def create_play(session: Session, play_data: Dict[str, Any], drive_id: int) -> Play:
    """
    Creates and persists a Play object in the database.

    Args:
        session (Session): SQLAlchemy session object.
        play_data (Dict[str, Any]): Dictionary data for a single play from ESPN response.
        drive_id (int): The ID of the drive this play belongs to.

    Returns:
        Play: The persisted Play object.
    """
    play_id = int(play_data['id'])

    existing_play = extract_play(session, play_id)
    
    if existing_play:
        return existing_play

    play = create_play_object(play_data, drive_id)

    participants_data = play_data.get('participants', {})
    
    if participants_data:
        create_participants(session, participants_data, play_id)

    session.add(play)
    session.commit()

    return play


def create_plays(session: Session, plays_data: Dict[str, Any], drive_id: int) -> List[Play]:
    """
    Creates and persists a list of Play objects in the database.

    Args:
        session (Session): SQLAlchemy session object.
        plays_data (Dict[str, Any]): Dictionary data containing a list of plays.
        drive_id (int): The ID of the drive these plays belong to.

    Returns:
        List[Play]: List of persisted Play objects.
    """
    plays_list = plays_data.get('items', [])
    plays = []

    for play_data in plays_list:
        play = create_play(session, play_data, drive_id)
        plays.append(play)

    return plays
