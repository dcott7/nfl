from typing import Dict, Any, List

from fetch.util import fetch_page
from models.event import Event
from fetch.weather import create_weather
from fetch.competition import create_competition

def create_event(event_data: Dict[str, Any]) -> Event:
    """Creates an Event.

    Params:
        event_data: dictionary data from ESPN response.

    Returns:
        Event object.
    """

    weather_data = event_data.get('weather',{})
    competition_data = event_data.get('competitions',{})[0]

    return Event(
        id = int(event_data['id']),
        name = str(event_data['name']),
        season = int(event_data['season']['$ref'].split("seasons/")[1].split("?")[0]),
        week = int(event_data['week']['$ref'].split("weeks/")[1].split("?")[0]),
        season_type = int(event_data['seasonType']['$ref'].split("types/")[1].split("?")[0]),
        weather = create_weather(weather_data) if weather_data else None,
        competition = create_competition(competition_data) if competition_data else None
    )

def create_events(event_urls: List[str]) -> List[Event]:
    """Creates a List of Event."""
    return [create_event(fetch_page(event_url)) for event_url in event_urls]