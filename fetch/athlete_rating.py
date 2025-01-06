import requests
from typing import List, Dict

from python_models.logger import Logger
from models import Rating

BASE_PLAYER_SEARCH_URL = 'https://drop-api.ea.com/rating/madden-nfl?locale=en&limit=100&search={player_name}'

def get_player_response(player_name: str):

    # Can't provide filter with a '.' in it (ex. A.J.). 
    # We will instead filter on the last_name, await 
    # the response and then filter the response by 
    # first_name
    first_name=''
    if '.' in player_name:
        first_name = player_name.split(' ')[0]
        last_name = player_name.split(' ')[1]
        player_name = last_name

    url = BASE_PLAYER_SEARCH_URL.format(player_name=player_name)
    response = requests.get(url)
    json_response = response.json()

    if not json_response.get("items"):
        Logger.warning(f'No madden data/ratings for "{player_name}" at: {url}')
        return
    
    if len(json_response.get("items")) > 1:
        if first_name: # if the case when '.' in the name, now we try to filter
            for player in json_response.get("items"):
                if player['firstName'] == first_name:
                    return {'items':[player]}
        else:
            Logger.warning(f'Multiple players found for "{player_name}" at {url}')
        return
    return json_response


def get_player_ratings(player_name: str) -> List[Rating]:
    player_data = get_player_response(player_name)
    
    if not player_data:
        return []
        
    player_stats = player_data["items"][0].get("stats", {})
    
    ratings = []
    for stat_name, stat_data in player_stats.items():
        rating_value = stat_data.get("value")
        
        rating_type = stat_name
        if rating_type:
            # Use keyword arguments to initialize Rating
            ratings.append(Rating(rating_type=rating_type, rating=rating_value))
        else:
            Logger.warning(f"{stat_name} is not a recognized RatingType.")
    
    return ratings