import random
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.util import fetch_page
from db.models import Team
from db.extract.team import extract_team


def create_new_team(team_data: Dict[str, Any]) -> Team:
    """
    Creates a new Team object from the provided team data.

    Args:
        team_data (Dict[str, Any]): Data to create the new team.

    Returns:
        Team: The created Team object.
    """
    return Team(
        id=int(team_data['id']),
        name=str(team_data['displayName']),
        cap_room=0
    )


def get_or_create_team(session: Session, team_data: Dict[str, Any]) -> Team:
    """
    Fetch an existing team or create a new one.

    Args:
        session (Session): SQLAlchemy session object.
        team_data (Dict[str, Any]): Team data.

    Returns:
        Team: The existing or newly created Team object.
    """
    team = extract_team(session, int(team_data['id']))
    
    if team:
        return team

    return create_new_team(team_data)


def fetch_teams_data(team_urls: List[str], proxies: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch team data from a list of URLs using a list of proxies.

    Args:
        team_urls (List[str]): A list of team URLs to fetch data from.
        proxies (List[str]): List of proxies to use for requests.

    Returns:
        List[Dict[str, Any]]: A list of team data dictionaries.
    """
    team_data_list = []
    for team_url in team_urls:
        proxy = {"http": random.choice(proxies)} if proxies else None
        team_data = fetch_page(team_url, proxy=proxy)
        team_data_list.append(team_data)
    return team_data_list


def create_teams(session: Session, team_urls: List[str], proxies: List[str]) -> List[Team]:
    """
    Creates or fetches teams from the given list of URLs, using a list of proxies.

    Args:
        session (Session): SQLAlchemy session object.
        team_urls (List[str]): List of team URLs.
        proxies (List[str]): List of proxies to use for requests.

    Returns:
        List[Team]: List of Team objects.
    """
    team_data_list = fetch_teams_data(team_urls, proxies)

    teams = []
    for team_data in team_data_list:
        if team_data:
            team = get_or_create_team(session, team_data)
            teams.append(team)

    new_teams = [team for team in teams if not session.identity_map.get(team)]
    session.add_all(new_teams)
    session.commit()

    return teams
