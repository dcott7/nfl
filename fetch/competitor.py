from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models import Competitor
from fetch.util import fetch_page

def create_competitor(session: Session, competitor_data: Dict[str, Any], event_id: int, competition_id: int) -> Competitor:
    """Creates and persists a Competitor object in the database.

    Params:
        session: SQLAlchemy session object.
        competitor_data: dictionary data from ESPN response.

    Returns:
        Persisted Competitor object.
    """
    
    # Check if the competitor already exists to avoid duplication
    existing_competitor = session.query(Competitor).filter_by(id=competitor_data['id']).first()
    
    if existing_competitor:
        return existing_competitor

    # Fetch the score
    score_data = fetch_page(competitor_data.get('score', {}).get('$ref', ''))
    score_value = int(score_data['value']) if score_data else 0

    # Create the Competitor object
    competitor = Competitor(
        id = competitor_data['id'],
        is_home = True if competitor_data.get('homeAway', '') == 'home' else False,
        is_winner = True if competitor_data.get('winner', '') == 'true' else False,
        score = score_value,
        team_id = competitor_data['id'], # this is always the same as the competitior_id
        event_id = event_id,
        competition_id = competition_id
    )

    # Persist the Competitor object to the database
    session.add(competitor)
    session.commit()

    return competitor

def create_competitors(session: Session, competitors_data: List[Dict[str, Any]], event_id: int, competition_id: int) -> List[Competitor]:
    """Creates and persists a List of Competitor objects in the database.

    Params:
        session: SQLAlchemy session object.
        competitors_data: List of dictionaries containing competitor data.

    Returns:
        List of persisted Competitor objects.
    """
    return [create_competitor(session, competitor, event_id, competition_id) for competitor in competitors_data]
