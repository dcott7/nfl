import datetime
from typing import Dict, Any

from python_models.competition import Competition
from fetch.util import fetch_all_items
from fetch.competitor import create_competitors
from fetch.venue import create_venue
from util import convert_to_datetime
from fetch.drive import create_drives

def create_competition(competition_data: Dict[str, Any]) -> Competition:
    """Creates a Competition.

    Params:
        competition_data: dictionary data from ESPN response.

    Returns:
        Competition object.
    """

    competitors_data = competition_data.get('competitors',[])
    drives_data = fetch_all_items(competition_data.get('drives',{})['$ref'])

    return Competition(
        id = int(competition_data['id']),
        date = convert_to_datetime(competition_data['date']),
        venue = create_venue(competition_data.get('venue',{})),
        competitors = create_competitors(competitors_data),
        drives = create_drives(drives_data)
    )