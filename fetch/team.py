import requests
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from fetch.util import fetch_all_refs, fetch_page
from fetch.athlete import create_athletes
from models import Team


def create_team(session: Session, team_data: Dict[str, Any], load_athletes: bool = False) -> Team:
    """Creates a Team database entry from a dictionary."""

    # Fetch athletes if required
    if load_athletes:
        athlete_data = fetch_all_refs(team_data.get("athletes", {}).get("$ref", ""))
        athletes = create_athletes(session, athlete_data, team_id=int(team_data['id']))
        for athlete in athletes:
            athlete.team_id = int(team_data['id'])  # Assign team_id to Athlete
            session.add(athlete)  # Add Athlete to the session
    else:
        athletes = []

    # Create Team object
    team = Team(
        id=int(team_data['id']),
        name=str(team_data['displayName']),
        cap_room=0
    )

    session.add(team)  # Add Team to the session
    session.commit()   # Commit to the database

    return team


def create_teams(session: Session, team_urls: List[str], load_athletes: bool) -> List[Team]:
    """Creates a list of Team database entries from a list of team URLs."""
    teams = []

    for team_url in team_urls:
        team_data = fetch_page(team_url)  # Fetch team data from API
        team = create_team(session, team_data, load_athletes=load_athletes)
        teams.append(team)

    return teams
