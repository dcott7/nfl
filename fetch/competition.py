from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models import Competition
from fetch.util import fetch_all_items
from fetch.venue import create_venue
from fetch.competitor import create_competitors
from fetch.drive import create_drives
from util import convert_to_datetime

def create_competition(session: Session, competition_data: Dict[str, Any], event_id: int) -> Competition:
    """Creates and persists a Competition object in the database.

    Params:
        session: SQLAlchemy session object.
        competition_data: dictionary data from ESPN response.

    Returns:
        Persisted Competition object.
    """

    competition_id = competition_data['id']

    existing_competition = session.query(Competition).filter_by(id=competition_id).first()
    
    if existing_competition:
        return existing_competition

    competitors_data = competition_data.get('competitors', [])
    drives_data = fetch_all_items(competition_data.get('drives', {})['$ref'])
    venue_data = competition_data.get('venue', {})

    venue = create_venue(session, venue_data)
    competitors = create_competitors(session, competitors_data, event_id, competition_id)
    drives = create_drives(session, drives_data, competition_id) if drives_data else None

    competition = Competition(
        id = int(competition_id),
        date = convert_to_datetime(competition_data['date']),
        venue_id = venue['id'],
        competitors = competitors,
        drives = drives,
        event_id = event_id
    )

    session.add(competition)
    session.commit()

    return competition
