import requests
from typing import Dict, Any, List

from fetch.util import fetch_all_refs, fetch_page
from fetch.athlete import create_athletes
from models.team import Team

def create_team(team_data: Dict[str, Any], load_athletes: bool = False) -> Team:
    """Creates a Team object from Dictionary."""

    if load_athletes:
        athletes = create_athletes(
            fetch_all_refs(team_data.get("athletes", {}).get("$ref", ""))
        )
        
    else:
        athletes = []

    return Team(
        name = str(team_data['displayName']),
        id = int(team_data['id']),
        active_roster = [athlete for athlete in athletes if not athlete.is_practice_squad],
        practice_squad = [athlete for athlete in athletes if athlete.is_practice_squad],
        cap_room = 0,
        draft_picks = []
    )

def create_teams(team_urls: List[str], load_athletes: bool) -> List[Team]:
    """Creates a List of Team objects from a List of team urls."""

    if load_athletes:
        return [create_team(fetch_page(team_url), load_athletes=True) for team_url in team_urls]
    
    return [create_team(fetch_page(team_url)) for team_url in team_urls]