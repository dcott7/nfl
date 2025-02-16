from typing import List, Dict, Optional
import logging

from db.models import Rating
from db.util import fetch_page

BASE_PLAYER_SEARCH_URL = 'https://drop-api.ea.com/rating/madden-nfl?locale=en&limit=100&search={player_name}'

def fetch_player_data(player_name: str) -> Optional[Dict]:
    """
    Fetch player data from the Madden API based on the given player name.

    Args:
        player_name (str): The name of the player to search for.

    Returns:
        Optional[Dict]: The JSON response containing player data, or None if no data is found.
    """
    first_name = ''
    if '.' in player_name:
        parts = player_name.split(' ')
        if len(parts) > 1:
            first_name, last_name = parts[0], parts[1]
            player_name = last_name

    url = BASE_PLAYER_SEARCH_URL.format(player_name=player_name)
    json_response = fetch_page(url)

    if not json_response.get("items"):
        logging.warning(f'No Madden data/ratings found for "{player_name}" at: {url}')
        return None

    items = json_response["items"]
    if len(items) > 1:
        if first_name:
            for player in items:
                if player.get('firstName') == first_name:
                    return {'items': [player]}
        logging.warning(f'Multiple players found for "{player_name}" at {url}')
        return None

    return json_response


def create_player_ratings(player_name: str) -> List[Rating]:
    """
    Create a list of Rating objects for the specified player.

    Args:
        player_name (str): The name of the player.

    Returns:
        List[Rating]: A list of Rating objects containing the player's stats and ratings.
    """
    player_data = fetch_player_data(player_name)
    if not player_data:
        return []

    player_stats = player_data["items"][0].get("stats", {})
    ratings = []

    for stat_name, stat_data in player_stats.items():
        rating_value = stat_data.get("value")
        if rating_value is not None:
            ratings.append(Rating(rating_type=stat_name, rating=rating_value))
        else:
            logging.warning(f'Invalid rating value for stat "{stat_name}".')

    return ratings
