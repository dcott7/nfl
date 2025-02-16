from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models import Official, OfficialPosition
from db.extract.official import extract_official, extract_official_position


def create_official_position(
    session: Session, official_pos_data: Dict[str, Any]
) -> OfficialPosition:
    """
    Create or retrieve an OfficialPosition object.

    Args:
        session (Session): SQLAlchemy session.
        official_pos_data (Dict[str, Any]): Dictionary containing official position data.

    Returns:
        OfficialPosition: The persisted OfficialPosition object.
    """
    official_pos_id = int(official_pos_data["id"])
    
    existing_official_position = extract_official_position(official_pos_id)
    
    if existing_official_position:
        return existing_official_position

    position = OfficialPosition(
        id=official_pos_id,
        name=str(official_pos_data.get("name","Unknown")), 
    )
    return position


def create_position(session: Session, official_pos_id: int) -> OfficialPosition:
    """
    Helper function to create a new OfficialPosition object.

    Args:
        session (Session): SQLAlchemy session.
        official_pos_id (int): The ID of the official position.

    Returns:
        OfficialPosition: The newly created OfficialPosition object.
    """
    position = OfficialPosition(
        id=official_pos_id,
        name="Unnamed Position", 
    )

    session.add(position)
    session.commit()
    return position


def create_official(
    session: Session, official_data: Dict[str, Any], official_pos: OfficialPosition
) -> Official:
    """
    Helper function to create a new Official object if it does not already exist.

    Args:
        session (Session): SQLAlchemy session.
        official_data (Dict[str, Any]): Dictionary containing official data.
        official_pos (OfficialPosition): The official position associated with the official.

    Returns:
        Official: The existing or newly created Official object.
    """
    official_id = int(official_data["id"])

    existing_official = extract_official(session, official_id)
    
    if existing_official:
        return existing_official

    official = Official(
        id=official_id,
        first_name=str(official_data["firstName"]),
        last_name=str(official_data["lastName"]),
        order=int(official_data["order"]),
        officialposition_id=official_pos.id,
    )

    session.add(official)
    session.commit()
    return official



def create_officials(
    session: Session, officials_data: List[Dict[str, Any]]
) -> List[Official]:
    """
    Create and persist a list of Official objects.

    Args:
        session (Session): SQLAlchemy session.
        officials_data (List[Dict[str, Any]]): List of dictionaries containing official data.

    Returns:
        List[Official]: List of persisted Official objects.
    """
    officials = []
    for official_data in officials_data:
        official_position = create_official_position(session, official_data.get("position", {}))
        official = create_official(session, official_data, official_position)
        officials.append(official)

    return officials
