from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models import Drive
from db.load.play import create_plays
from db.extract.drive import extract_drive


def create_drive(
    session: Session, drive_data: Dict[str, Any], competition_id: int
) -> Drive:
    """
    Create and persist a Drive object in the database synchronously.

    Args:
        session (Session): SQLAlchemy session object.
        drive_data (Dict[str, Any]): Dictionary data representing the drive.
        competition_id (int): ID of the competition associated with the drive.

    Returns:
        Drive: The persisted Drive object.
    """
    drive_id = int(drive_data["id"])

    existing_drive = extract_drive(session, drive_id)
    if existing_drive:
        return existing_drive

    plays = create_plays(session, drive_data.get("plays", []), drive_id)

    start_data = drive_data.get("start", {})
    end_data = drive_data.get("end", {})

    drive = Drive(
        id=drive_id,
        description=drive_data.get("description", ""),
        yards=int(drive_data.get("yards", 0)),
        is_score=bool(drive_data.get("isScore", False)),
        num_offensive_plays=int(drive_data.get("offensivePlays", 0)),
        start_quarter=int(start_data.get("period", {}).get("number", 0)),
        start_time=int(start_data.get("clock", {}).get("value", 0)),
        start_yardline=int(start_data.get("yardLine", 0)),
        end_quarter=int(end_data.get("period", {}).get("number", 0)),
        end_time=int(end_data.get("clock", {}).get("value", 0)),
        end_yardline=int(end_data.get("yardLine", 0)),
        plays=plays,
        competition_id=competition_id,
    )

    session.add(drive)
    session.commit()
    
    return drive


def create_drives(
    session: Session, drives_data: List[Dict[str, Any]], competition_id: int
) -> List[Drive]:
    """
    Create and persist a list of Drive objects in the database synchronously.

    Args:
        session (Session): SQLAlchemy session object.
        drives_data (List[Dict[str, Any]]): List of dictionaries representing drives.
        competition_id (int): ID of the competition associated with the drives.

    Returns:
        List[Drive]: List of persisted Drive objects.
    """
    drives = []
    for drive_data in drives_data:
        if drive_data:
            drive = create_drive(session, drive_data, competition_id)
            drives.append(drive)
    return drives
