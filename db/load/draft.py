import random
from bs4 import BeautifulSoup
from typing import List
from collections import defaultdict

from db.models import DraftPick
from db.util import fetch_page

DRAFT_URL = 'https://www.spotrac.com/nfl/draft/_/year/{year}'
DRAFT_PICKS_CACHE = defaultdict(list)

TEAMS_ABV_LOOKUP = {
    '1': 'ATL', '2': 'BUF', '3': 'CHI',
    '4': 'CIN', '5': 'CLE', '6': 'DAL',
    '7': 'DEN', '8': 'DET', '9': 'GB',
    '10': 'TEN', '11': 'IND', '12': 'KC',
    '13': 'LV', '14': 'LAR', '15': 'MIA',
    '16': 'MIN', '17': 'NE', '18': 'NO',
    '19': 'NYG', '20': 'NYJ', '21': 'PHI',
    '22': 'ARI', '23': 'PIT', '24': 'LAC',
    '25': 'SF', '26': 'SEA', '27': 'TB',
    '28': 'WAS', '29': 'CAR', '30': 'JAX',
    '33': 'BAL', '34': 'HOU'
}

def fetch_draft_picks(year: int, proxies: List[str]) -> List[List[str]]:
    """
    Fetch draft picks for a specific year using a list of proxies.

    Args:
        year (int): The year of the draft to fetch.
        proxies (List[str]): List of proxies to use for the requests.

    Returns:
        List[List[str]]: Draft pick data where each row is a list of strings.
    """
    if year in DRAFT_PICKS_CACHE:
        return DRAFT_PICKS_CACHE[year]
    
    url = DRAFT_URL.format(year=year)

    proxy = random.choice(proxies) if proxies else None

    page_content = fetch_page(url, text=True, proxy=proxy)
    soup = BeautifulSoup(page_content, 'html.parser')

    tbody = soup.find("tbody")
    if not tbody:
        DRAFT_PICKS_CACHE[year] = []
        return []
    
    draft_data = [
        [cell.get_text(strip=True) for cell in row.find_all("td")]
        for row in tbody.find_all("tr")
    ]

    DRAFT_PICKS_CACHE[year] = draft_data
    return draft_data


def parse_draft_pick(row: List[str], year: int, team_id: int) -> DraftPick:
    """
    Parse a single row of draft data into a DraftPick object.

    Args:
        row (List[str]): A row of draft data.
        year (int): The year of the draft.
        team_id (int): The team ID.

    Returns:
        DraftPick: Parsed draft pick object.
    """
    return DraftPick(
        year=year,
        round=int(row[0]),
        pick_number=int(row[1]),
        team_id=team_id
    )


def get_team_draft_picks(year: int, team_id: int) -> List[DraftPick]:
    """
    Retrieve draft pick data for a team from the pre-fetched draft pick cache.

    Args:
        year (int): The year of the draft.
        team_id (int): The ID of the team.

    Returns:
        List[DraftPick]: A list of draft pick objects for the specified team.
    """
    team_abbreviation = TEAMS_ABV_LOOKUP.get(str(team_id), "").lower()
    if not team_abbreviation:
        return []

    draft_data = DRAFT_PICKS_CACHE.get(year, [])
    draft_picks = [
        parse_draft_pick(row, year, team_id)
        for row in draft_data
        if team_abbreviation in row[2].lower()
    ]
    
    return draft_picks
