from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models import Event
from fetch.weather import create_weather
from fetch.competition import create_competition
from fetch.util import fetch_page

IGNORE_EVENTS = [401220373]

def create_event(session: Session, event_data: Dict[str, Any]) -> Event:
    """Creates and persists an Event object in the database.

    Params:
        session: SQLAlchemy session object.
        event_data: dictionary data from ESPN response.

    Returns:
        Persisted Event object.
    """
    
    event_id = int(event_data['id'])
    
    if event_id in IGNORE_EVENTS:
        return None
    
    weather_data = event_data.get('weather', {})
    competition_data = event_data.get('competitions', [{}])[0]  # Ensure there's at least one competition

    season_id = event_data['season']['$ref'].split("seasons/")[1].split("?")[0]
    week_id = event_data['week']['$ref'].split("weeks/")[1].split("?")[0]
    season_type_id = event_data['seasonType']['$ref'].split("types/")[1].split("?")[0]

    existing_event = session.query(Event).filter_by(id=event_data['id']).first()
    
    if existing_event:
        return existing_event

    weather = create_weather(session, weather_data) if weather_data else None
    competition = create_competition(session, competition_data, event_id) if competition_data else None
    weather_id = weather_data['id'] if weather_data['id'] else None
    
    print(weather)

    event = Event(
        id = event_id,
        name = str(event_data['name']),
        season = int(season_id),
        week = int(week_id),
        season_type = int(season_type_id),
        weather_id = weather_id,
        competition = competition
    )

    # Persist the Event object to the database
    session.add(event)
    session.commit()

    return event


def create_events(session: Session, event_urls: List[str]) -> List[Event]:
    """Creates and persists a List of Event objects in the database.

    Params:
        session: SQLAlchemy session object.
        event_urls: List of event URLs to fetch data from.

    Returns:
        List of persisted Event objects.
    """
    # Filter out None values for skipped events
    events = [create_event(session, fetch_page(event_url)) for event_url in event_urls]
    return [event for event in events if event is not None]
