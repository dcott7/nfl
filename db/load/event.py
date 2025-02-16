import random
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.util import fetch_page
from db.models import Event
from db.load.competition import create_competition
from util import get_id_from_url
from db.extract.event import extract_event

ATHLETE_CACHE = {}
IGNORE_EVENTS = {401220373}

def parse_season_data(event_data: Dict[str, Any]) -> Dict[str, int]:
    """
    Extract season-related data from the event dictionary.

    Args:
        event_data (Dict[str, Any]): The event data dictionary.

    Returns:
        Dict[str, int]: A dictionary with season, week, and season type IDs.
    """
    def extract_id(url: str, key: str) -> int:
        return int(url.split(f"{key}/")[1].split("?")[0])

    return {
        "season": extract_id(event_data["season"]["$ref"], "seasons"),
        "week": extract_id(event_data["week"]["$ref"], "weeks"),
        "season_type": extract_id(event_data["seasonType"]["$ref"], "types"),
    }


def create_event(session: Session, event_data: Dict[str, Any], proxies: List[str]) -> Optional[Event]:
    """
    Create and persist an Event object in the database.
    If the weather data cannot be fetched, it proceeds without weather data.

    Args:
        session (Session): SQLAlchemy session.
        event_data (Dict[str, Any]): The event data dictionary.
        proxies (List[str]): List of proxies to rotate for requests.

    Returns:
        Optional[Event]: The persisted Event object, or None if the event is ignored.
    """
    event_id = int(event_data.get("id", None))
    
    if not event_id or event_id in IGNORE_EVENTS:
        return None

    competition_data = event_data.get("competitions", [{}])[0]
    season_info = parse_season_data(event_data)

    competition = create_competition(session, competition_data, event_id) if competition_data else None

    event = Event(
        id=event_id,
        name=event_data.get("name", ""),
        season=season_info["season"],
        week=season_info["week"],
        season_type=season_info["season_type"],
        competition=competition,
    )

    session.add(event)
    session.commit()

    return event


def fetch_event_data(event_url: str, proxies: List[str]) -> Dict[str, Any]:
    """
    Fetch event data from a given URL with proxy support.

    Args:
        event_url (str): The URL of the event.
        proxies (List[str]): List of proxies to rotate through.

    Returns:
        Dict[str, Any]: The event data dictionary, or an empty dictionary if the request fails.
    """
    proxy = {"http": random.choice(proxies)} if proxies else None
    
    return fetch_page(event_url, proxy=proxy)


def create_events(session: Session, event_urls: List[str], proxies: List[str]) -> List[Optional[Event]]:
    """
    Create and persist a list of Event objects in the database.

    Args:
        session (Session): SQLAlchemy session.
        event_urls (List[str]): List of event URLs to fetch data from.
        proxies (List[str]): List of proxies to rotate through.

    Returns:
        List[Optional[Event]]: List of persisted Event objects.
    """
    events = []

    for event_url in event_urls:
        event_id = int(get_id_from_url(event_url))

        existing_event = extract_event(id=event_id)

        if existing_event:
            events.append(existing_event)
            continue

        event_data = fetch_event_data(event_url, proxies)
        if event_data:
            new_event = create_event(session, event_data, proxies)
            if new_event:
                events.append(new_event)

    return events
