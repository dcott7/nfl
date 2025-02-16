import random
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from collections import defaultdict

from db.util import fetch_page
from db.models import Contract

BASE_CONTRACT_URL = "https://www.spotrac.com/nfl/{team}/cap/{year}"
TEAM_YEAR_CONTRACT_CACHE = defaultdict(dict)

TEAMS_LOOKUP = {
    '1': 'Atlanta Falcons', '2': 'Buffalo Bills', '3': 'Chicago Bears',
    '4': 'Cincinnati Bengals', '5': 'Cleveland Browns', '6': 'Dallas Cowboys',
    '7': 'Denver Broncos', '8': 'Detroit Lions', '9': 'Green Bay Packers',
    '10': 'Tennessee Titans', '11': 'Indianapolis Colts', '12': 'Kansas City Chiefs',
    '13': 'Las Vegas Raiders', '14': 'Los Angeles Rams', '15': 'Miami Dolphins',
    '16': 'Minnesota Vikings', '17': 'New England Patriots', '18': 'New Orleans Saints',
    '19': 'New York Giants', '20': 'New York Jets', '21': 'Philadelphia Eagles',
    '22': 'Arizona Cardinals', '23': 'Pittsburgh Steelers', '24': 'Los Angeles Chargers',
    '25': 'San Francisco 49ers', '26': 'Seattle Seahawks', '27': 'Tampa Bay Buccaneers',
    '28': 'Washington Commanders', '29': 'Carolina Panthers', '30': 'Jacksonville Jaguars',
    '33': 'Baltimore Ravens', '34': 'Houston Texans'
}

def fetch_team_year_contracts(team_name: str, year: int, proxies: List[str] = []) -> List[Dict[str, Any]]:
    """
    Fetch contract data synchronously for an entire team for a specific year using a list of proxies.

    Args:
        team_name (str): The name of the team.
        year (int): The year to fetch the contracts for.
        proxies (List[str]): List of proxies to use for the requests.

    Returns:
        List[Dict[str, Any]]: The contract data.
    """
    team_name_normalized = "-".join(team_name.split())
    
    if year in TEAM_YEAR_CONTRACT_CACHE[team_name_normalized]:
        return TEAM_YEAR_CONTRACT_CACHE[team_name_normalized][year]
    
    url = BASE_CONTRACT_URL.format(team=team_name_normalized, year=year)

    proxy = random.choice(proxies) if proxies else None
    page_content = fetch_page(url, text=True, proxy=proxy)
    
    soup = BeautifulSoup(page_content, 'html.parser')
    tbody = soup.find("tbody")
    
    if not tbody:
        TEAM_YEAR_CONTRACT_CACHE[team_name_normalized][year] = []
        return []
    
    rows = tbody.find_all("tr")
    contract_data = [
        [cell.get_text(strip=True) for cell in row.find_all("td")]
        for row in rows
    ]

    TEAM_YEAR_CONTRACT_CACHE[team_name_normalized][year] = contract_data
    return contract_data


def parse_contract_row(row: List[str], team_name: str, year: int, player_name: str) -> Contract:
    """
    Parse a single contract row into a Contract object.

    Args:
        row (List[str]): The row data from the contract table.
        team_name (str): The team name.
        year (int): The year of the contract.
        player_name (str): The name of the player.

    Returns:
        Contract: Parsed contract object.
    """
    return Contract(
        team_name=team_name,
        year=year,
        apy_hit_pct=row[4],
        dead_cap=row[5],
        base_salary=row[6],
        signing_bonus=row[7],
        per_game_bonus=row[8],
        roster_bonus=row[9],
        option_bonus=row[10],
        workout_bonus=row[11],
        restructure_bonus=row[12],
        incentives=row[13],
    )


def get_athlete_contracts(team_name: str, year: int, player_name: str) -> List[Contract]:
    """
    Retrieve contract data for an athlete from the pre-fetched contract cache.

    Args:
        team_name (str): The name of the team.
        year (int): The year to fetch the contracts for.
        player_name (str): The name of the player to filter contracts.

    Returns:
        List[Contract]: List of Contract objects for the specified player.
    """
    team_name_normalized = "-".join(team_name.split())
    
    if year not in TEAM_YEAR_CONTRACT_CACHE[team_name_normalized]:
        return []

    contract_data = TEAM_YEAR_CONTRACT_CACHE[team_name_normalized][year]
    contracts = [
        parse_contract_row(row, team_name, year, player_name)
        for row in contract_data
        if player_name.lower() in row[0].lower()
    ]

    return contracts
