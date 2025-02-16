from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.models import Competitor
from db.util import fetch_page
from db.extract.competitor import extract_competitor


def fetch_score(session: Session, competitor_data: Dict[str, Any]) -> int:
    """
    Fetch the score of a competitor using the provided URL.

    Args:
        competitor_data (Dict[str, Any]): Competitor data containing the score URL.

    Returns:
        int: The score value, or 0 if not available.
    """
    score_url = competitor_data.get("score", {}).get("$ref")
    if score_url:
        score_data = fetch_page(score_url)
        return int(score_data["value"]) if score_data else 0
    return 0


def create_or_get_competitor(
    session: Session, competitor_data: Dict[str, Any], event_id: int, competition_id: int
) -> Competitor:
    """
    Fetch an existing Competitor or create a new one synchronously.

    Args:
        session (Session): SQLAlchemy session object.
        competitor_data (Dict[str, Any]): Data for the competitor.
        event_id (int): The associated event ID.
        competition_id (int): The associated competition ID.

    Returns:
        Competitor: The created or existing Competitor object.
    """
    is_home=competitor_data.get("homeAway", "").lower() == "home"
    is_winner=bool(competitor_data.get("winner", ""))
    score=score = fetch_score(session, competitor_data)
    team_id = int(competitor_data["id"])
    event_id=event_id
    competition_id=competition_id
    
    existing_competitor = extract_competitor(
        session, is_home, is_winner, score, team_id, event_id, competition_id
    )
    
    if existing_competitor:
        return existing_competitor

    competitor = Competitor(
        is_home=is_home,
        is_winner=is_winner,
        score=score,
        team_id=team_id,
        event_id=event_id,
        competition_id=competition_id
    )
    
    session.add(competitor)
    session.commit()

    return competitor


def create_competitors(
    session: Session, competitors_data: List[Dict[str, Any]], event_id: int, competition_id: int
) -> List[Competitor]:
    """
    Fetch or create multiple Competitor objects synchronously.

    Args:
        session (Session): SQLAlchemy session object.
        competitors_data (List[Dict[str, Any]]): List of dictionaries containing competitor data.
        event_id (int): The associated event ID.
        competition_id (int): The associated competition ID.

    Returns:
        List[Competitor]: A list of Competitor objects.
    """
    competitors = []
    for competitor_data in competitors_data:
        if competitor_data:
            if event_id != competition_id:
                raise ValueError(f"event_id ({event_id}) and competition_id ({competition_id}) do not match.")
            competitor = create_or_get_competitor(session, competitor_data, event_id, competition_id)
            competitors.append(competitor)
    return competitors
