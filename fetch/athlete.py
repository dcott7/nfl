import requests
from typing import Dict, Any, List

from python_models.athlete import Athlete
from python_models.position import PositionEnum
from fetch.util import fetch_page
from fetch.athlete_rating import get_player_ratings

# caching athletes that have been created so that 
# we do not make duplicates of the same athlete
ATHLETE_CACHE = {}

def create_athlete(athlete_data: Dict[str, Any]) -> Athlete:
    """Creates a Athlete.

    Params:
        athlete_data: dictionary data from ESPN response.

    Returns:
        Athlete object.
    """

    athlete_name = str(athlete_data['fullName'])

    position_abbreviation = athlete_data.get("position", {}).get("abbreviation", "")
    
    position_enum = PositionEnum[position_abbreviation]
    
    return Athlete(
        name = athlete_name,
        id = int(athlete_data['id']),
        age = int(athlete_data.get('age',0)),
        height = int(athlete_data['height']),
        weight = int(athlete_data['weight']),
        position = position_enum,
        salary = float(0),
        is_practice_squad = True if athlete_data.get('status',{}).get('name','') == 'Practice Squad' else False,
        ratings = get_player_ratings(athlete_name)
    )

def get_or_create_athlete(athlete_data: Dict[str, Any]) -> Athlete:
    """Creates or Retreives an Athlete.

    Params:
        athlete_data: dictionary data from ESPN response.

    Returns:
        Athlete object.
    """
    athlete_id = int(athlete_data['id'])

    if athlete_id in ATHLETE_CACHE:
        return ATHLETE_CACHE[athlete_id]
    
    new_athlete = create_athlete(athlete_data)
    ATHLETE_CACHE[athlete_id] = new_athlete
    
    return new_athlete

def create_athletes(athlete_urls: List[str]) -> List[Athlete]:
    """Create a List of Athlete."""

    return [get_or_create_athlete(fetch_page(athlete_url)) for athlete_url in athlete_urls]