from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models import Drive
from fetch.play import create_plays
from fetch.util import fetch_page

def create_drive(session: Session, drive_data: Dict[str, Any], competition_id) -> Drive:
    """Creates and persists a Drive object in the database.

    Params:
        session: SQLAlchemy session object.
        drive_data: dictionary data from ESPN response.

    Returns:
        Persisted Drive object.
    """
    
    start_data = drive_data.get('start', {})
    end_data = drive_data.get('end', {})
    
    drive_id = drive_data['id']

    existing_drive = session.query(Drive).filter_by(id=drive_id).first()
    
    if existing_drive:
        return existing_drive

    drive = Drive(
        id = int(drive_data['id']),
        description = str(drive_data['description']),
        yards = int(drive_data['yards']),
        is_score = bool(drive_data['isScore']),
        num_offensive_plays = int(drive_data['offensivePlays']),
        start_quarter = int(start_data.get('period', {}).get('number', 0)),
        start_time = int(start_data.get('clock', {}).get('value', 0)),
        start_yardline = int(drive_data.get('yardLine', 0)),
        end_quarter = int(end_data.get('period', {}).get('number', 0)),
        end_time = int(end_data.get('clock', {}).get('value', 0)),
        end_yardline = int(end_data.get('yardLine', 0)),
        plays = create_plays(session, drive_data.get('plays', []), drive_id),
        competition_id = competition_id
    )

    session.add(drive)
    session.commit()

    return drive


def create_drives(session: Session, drives_data: List[Dict[str, Any]], competition_id) -> List[Drive]:
    """Creates and persists a List of Drive objects in the database.

    Params:
        session: SQLAlchemy session object.
        drives_data: List of dictionaries containing drive data.

    Returns:
        List of persisted Drive objects.
    """
    return [create_drive(session, drive_data, competition_id) for drive_data in drives_data]
