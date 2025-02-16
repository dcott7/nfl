from typing import Dict, Any, Optional 
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models import Competition, CompetitionStatus, CompetitionStatusType
from db.util import fetch_all_items, fetch_page
from db.load.venue import create_venue
from db.load.competitor import create_competitors
from db.load.drive import create_drives
from db.load.official import create_officials
from util import convert_to_datetime
from db.extract.competition import (
    extract_competition, 
    extract_competition_status, 
    extract_competition_status_type
)


def create_competition_status(
    session: Session, competition_status_data: Dict[str, Any]
) -> CompetitionStatus:
    """
    Create or retrieve a CompetitionStatus object.

    Args:
        session (Session): SQLAlchemy session.
        competition_status_data (Dict[str, Any]): Dictionary containing competition status data.

    Returns:
        CompetitionStatus: The persisted CompetitionStatus object.
    """
    clock = competition_status_data.get("clock")
    display_clock = competition_status_data.get("displayClock")
    period = competition_status_data.get("period")
    
    status_type_data = competition_status_data.get("type", {})
    competition_status_type_id = int(status_type_data.get("id", 0))
    name = status_type_data.get("name", "")
    state = status_type_data.get("state", "")
    completed = status_type_data.get("completed", False)
    description = status_type_data.get("description", "")
    detail = status_type_data.get("detail", "")

    existing_competition_status = extract_competition_status(
        clock=clock,
        display_clock=display_clock,
        period=period,
        competition_status_type_id=competition_status_type_id
    )

    if existing_competition_status:
        return existing_competition_status

    competition_status_type = extract_competition_status_type(id=competition_status_type_id)

    if not competition_status_type:
        competition_status_type = CompetitionStatusType(
            id=competition_status_type_id,
            name=name,
            state=state,
            completed=completed,
            description=description,
            detail=detail
        )
        session.add(competition_status_type)
        session.flush()

    competition_status = CompetitionStatus(
        clock=clock,
        display_clock=display_clock,
        period=period,
        competition_status_type_id=competition_status_type.id
    )
    session.add(competition_status)
    session.flush()

    return competition_status


def fetch_related_data(competition_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fetch related data such as drives and officials synchronously.

    Args:
        competition_data (Dict[str, Any]): The raw competition data.

    Returns:
        Dict[str, Any]: A dictionary containing fetched related data.
    """
    drive_url = competition_data.get("drives", {}).get("$ref")
    officials_url = competition_data.get("officials", {}).get("$ref")
    status_url = competition_data.get("status",{}).get("$ref")

    return {
        "drives_data": fetch_all_items(drive_url) if drive_url else None,
        "officials_data": fetch_all_items(officials_url) if officials_url else None,
        "venue_data": competition_data.get("venue"),
        "competitors_data": competition_data.get("competitors", []),
        "status_data": fetch_page(status_url) if status_url else None
    }


def create_competition(
    session: Session, competition_data: Dict[str, Any], event_id: int
) -> Competition:
    """
    Creates and persists a Competition object in the database synchronously.

    Args:
        session (Session): SQLAlchemy session object.
        competition_data (Dict[str, Any]): Raw data about the competition.
        event_id (int): The associated event ID.

    Returns:
        Competition: The created or existing Competition object.
    """
    competition_id = int(competition_data["id"])

    existing_competition = extract_competition(session, competition_id)
    
    if existing_competition:
        return existing_competition

    related_data = fetch_related_data(competition_data)

    venue = (
        create_venue(session, related_data["venue_data"])
        if related_data["venue_data"]
        else None
    )
    competitors = create_competitors(
        session, related_data["competitors_data"], event_id, competition_id
    )
    drives = (
        create_drives(session, related_data["drives_data"], competition_id)
        if related_data["drives_data"]
        else []
    )
    referees = list(
        create_officials(session, related_data["officials_data"])
        if related_data["officials_data"]
        else []
    )
    competition_status = (
        create_competition_status(session, related_data['status_data'])
        if related_data['status_data']
        else None
    )
    
    unique_referees = list({ref.id: ref for ref in referees}.values())

    competition = Competition(
        id=competition_id,
        date=convert_to_datetime(competition_data["date"]),
        venue_id=venue.id if venue else None,
        competitors=competitors,
        drives=drives,
        event_id=event_id,
        referees=unique_referees,
        competition_status_id = competition_status.id if competition_status else None
    )

    session.add(competition)
    session.commit()

    return competition
