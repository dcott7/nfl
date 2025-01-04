from typing import Dict, Any, List

from python_models.competitor import Competitor
from fetch.util import fetch_page

def create_competitor(competitor_data: Dict[str, Any]) -> Competitor:
    """Creates a Competitor.

    Params:
        competitor_data: dictionary data from ESPN response.

    Returns:
        Competitor object.
    """
    
    return Competitor(
        id = competitor_data['id'],
        is_home = True if competitor_data.get('homeAway','') == 'home' else False,
        is_winner = True if competitor_data.get('winner','') == 'true' else False,
        score = int(fetch_page(competitor_data.get('score',{})['$ref'])['value'])
    )

def create_competitors(competitors_data: List[Dict[str, Any]]) -> List[Competitor]:
    """Creates a List of Competitor."""
    return [create_competitor(competitor) for competitor in competitors_data]