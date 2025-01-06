import requests
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from models import Athlete, Position, TeamHistory
from fetch.util import fetch_page
from fetch.athlete_rating import get_player_ratings

# Caching athletes to reduce redundant database queries
ATHLETE_CACHE = {}

def get_athlete_history(session: Session, athlete_id: int) -> List[TeamHistory]:
    """
    Fetch and process an athlete's team history.

    Params:
        session: SQLAlchemy session object.
        athlete_id: ID of the athlete.

    Returns:
        List of TeamHistory objects to be persisted.
    """
    statistics_log_url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{athlete_id}/statisticslog"
    statistics_log = fetch_page(statistics_log_url)
    
    history_entries = []
    if "entries" in statistics_log:
        for entry in statistics_log["entries"]:
            season_url = entry["season"]["$ref"]
            season_year = int(season_url.split("/")[-1].replace('?lang=en&region=us',''))  # Extract year from URL

            for stat in entry.get("statistics", []):
                if stat["type"] == "team" and "team" in stat:
                    team_url = stat["team"]["$ref"]
                    team_id = int(team_url.split("/")[-1].replace('?lang=en&region=us',''))  # Extract team ID from URL

                    # Check if TeamHistory entry exists
                    existing_history = session.query(TeamHistory).filter_by(
                        athlete_id=athlete_id,
                        team_id=team_id,
                        season=season_year
                    ).first()
                    
                    if not existing_history:
                        # Create a new TeamHistory entry
                        team_history = TeamHistory(
                            athlete_id=athlete_id,
                            team_id=team_id,
                            season=season_year
                        )
                        history_entries.append(team_history)
    return history_entries

def create_athlete(session: Session, athlete_data: Dict[str, Any], team_id: int = None) -> Athlete:
    """Creates and persists an Athlete in the database.

    Params:
        session: SQLAlchemy session object.
        athlete_data: dictionary data from ESPN response.
        team_id: ID of the team to associate with the athlete.

    Returns:
        Persisted Athlete object.
    """

    athlete_id = int(athlete_data['id'])

    # Check cache first
    if athlete_id in ATHLETE_CACHE:
        return ATHLETE_CACHE[athlete_id]

    # Check database for existing Athlete
    athlete = session.query(Athlete).filter_by(id=athlete_id).first()
    if athlete:
        ATHLETE_CACHE[athlete_id] = athlete
        return athlete

    athlete_name = str(athlete_data['fullName'])
    position_abbreviation = athlete_data.get("position", {}).get("abbreviation", "")

    # Get or create the Position object
    position = session.query(Position).filter_by(position_name=position_abbreviation).first()
    if not position:
        position = Position(position_name=position_abbreviation)
        session.add(position)
        session.commit()

    # Create the Athlete object with the team_id
    athlete = Athlete(
        first_name=athlete_name.split(' ')[0],
        last_name=' '.join(athlete_name.split(' ')[1:]),
        id=athlete_id,
        age=int(athlete_data.get('age', 0)),
        height=int(athlete_data.get('height', 0)),
        weight=int(athlete_data.get('weight', 0)),
        position_id=position.id,  # Associate with Position
        salary=float(0),
        is_practice_squad=athlete_data.get('status', {}).get('name', '') == 'Practice Squad',
        team_id=team_id  # Ensure team_id is set here
    )

    # Add ratings (if available)
    ratings = get_player_ratings(athlete_name)
    for rating_data in ratings:
        athlete.ratings.append(rating_data)

    # Persist Athlete in the database
    session.add(athlete)
    session.commit()

    # Fetch and update Team History
    history_entries = get_athlete_history(session, athlete_id)
    session.add_all(history_entries)
    session.commit()

    # Cache and return the athlete
    ATHLETE_CACHE[athlete_id] = athlete
    return athlete


def create_athletes(session: Session, athlete_urls: List[str], team_id: int) -> List[Athlete]:
    """Create multiple athletes and associate them with a team.

    Params:
        session: SQLAlchemy session object.
        athlete_urls: List of URLs containing athlete data.
        team_id: ID of the team to associate with each athlete.

    Returns:
        List of Athlete objects.
    """
    athletes = []

    for athlete_url in athlete_urls:
        athlete_data = fetch_page(athlete_url)
        athlete = create_athlete(session, athlete_data, team_id)  # Pass team_id here

        athletes.append(athlete)  # Collect athletes

    session.commit()  # Commit once for all athletes
    return athletes

