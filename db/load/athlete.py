import random
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from db.util import fetch_page
from db.models import Athlete, Position, TeamHistory
from db.load.contract import get_athlete_contracts, TEAMS_LOOKUP
from db.load.athlete_rating import create_player_ratings
from util import get_id_from_url
from db.extract.athlete import extract_athlete, extract_athlete_position, extract_team_history

ATHLETE_CACHE = {}

def fetch_team_history(session: Session, athlete_id: int, proxies: List[str]) -> List[TeamHistory]:
    """
    Fetch and process an athlete's team history from the API using proxies.

    Args:
        session (Session): SQLAlchemy session object.
        athlete_id (int): ID of the athlete.
        proxies (List[str]): List of proxies to use for the requests.

    Returns:
        List[TeamHistory]: List of TeamHistory objects to persist in the database.
    """
    statistics_log_url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{athlete_id}/statisticslog"
    proxy = {"http": random.choice(proxies)} if proxies else None

    statistics_log = fetch_page(statistics_log_url, proxy=proxy)
    history_entries = []

    if not statistics_log:
        return history_entries

    for entry in statistics_log.get("entries", []):
        season_url = entry["season"]["$ref"]
        season_year = int(get_id_from_url(season_url))

        for stat in entry.get("statistics", []):
            if stat["type"] == "team" and "team" in stat:
                team_url = stat["team"]["$ref"]
                team_id = int(get_id_from_url(team_url))

                existing_history = extract_team_history(
                    session, athlete_id=athlete_id, team_id=team_id, season=season_year
                )

                if not existing_history:
                    history_entries.append(
                        TeamHistory(athlete_id=athlete_id, team_id=team_id, season=season_year)
                    )

    return history_entries


def fetch_or_create_position(session: Session, position_name: str) -> Position:
    """
    Fetch an existing position or create a new one.

    Args:
        session (Session): SQLAlchemy session object.
        position_name (str): Position abbreviation (e.g., QB, WR).

    Returns:
        Position: The fetched or newly created Position object.
    """
    position = extract_athlete_position(position_name)
    
    if not position:
        position = Position(position_name=position_name)
        session.add(position)
        session.commit()

    return position


def create_athlete(session: Session, athlete_data: Dict[str, Any], proxies: List[str]) -> Athlete:
    """
    Create and persist an Athlete object in the database with proxy support.

    Args:
        session (Session): SQLAlchemy session object.
        athlete_data (Dict[str, Any]): Raw data about the athlete from the API.
        proxies (List[str]): List of proxies to use for the requests.

    Returns:
        Athlete: The created Athlete object.
    """
    athlete_id = int(athlete_data.get("id", None))
    
    if athlete_id in ATHLETE_CACHE:
        return ATHLETE_CACHE[athlete_id]

    athlete_name = athlete_data["fullName"]
    first_name, *last_name = athlete_name.split(" ")
    last_name = " ".join(last_name)
    position_name = athlete_data.get("position", {}).get("abbreviation", "")
    team_id = get_id_from_url(athlete_data.get("team", {}).get("$ref", ""))
    team_id = int(team_id) if team_id else None
    position = fetch_or_create_position(session, position_name)

    athlete = Athlete(
        first_name=first_name,
        last_name=last_name,
        id=athlete_id,
        age=int(athlete_data.get("age", 0)),
        height=int(athlete_data.get("height", 0)),
        weight=int(athlete_data.get("weight", 0)),
        position_id=position.id,
        salary=float(athlete_data.get("salary", 0) or 0),
        is_practice_squad=athlete_data.get("status", {}).get("name", "") == "Practice Squad",
        team_id=team_id,
    )

    ratings = create_player_ratings(athlete_name)
    athlete.ratings.extend(ratings)

    history_entries = fetch_team_history(session, athlete_id, proxies)
    athlete.teamhistory.extend(history_entries)

    for team_history in history_entries:
        team_name = TEAMS_LOOKUP.get(str(team_history.team_id), "")
        contracts = get_athlete_contracts(athlete_name, team_name, team_history.season)
        athlete.contracts.extend(contracts)

    session.add(athlete)
    session.commit()

    ATHLETE_CACHE[athlete_id] = athlete
    return athlete


def create_athletes(session: Session, athlete_urls: List[str], proxies: List[str]) -> List[Athlete]:
    """
    Create multiple athletes and associate them with their teams, using proxy support.

    Args:
        session (Session): SQLAlchemy session object.
        athlete_urls (List[str]): List of URLs containing athlete data.
        proxies (List[str]): List of proxies to use for the requests.

    Returns:
        List[Athlete]: List of created Athlete objects.
    """
    athletes = []

    for athlete_url in athlete_urls:
        athlete_id = int(get_id_from_url(athlete_url))
        athlete = extract_athlete(id=athlete_id)

        if not athlete:
            proxy = {"http": random.choice(proxies)} if proxies else None
            athlete_data = fetch_page(athlete_url, proxy=proxy)
            if athlete_data:
                athlete = create_athlete(session, athlete_data, proxies)

        athletes.append(athlete)

    return athletes
