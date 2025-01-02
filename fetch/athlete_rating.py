import requests
from typing import List, Dict

from models.logger import Logger
from models.rating import Rating
from models.rating import RatingType

BASE_PLAYER_SEARCH_URL = 'https://drop-api.ea.com/rating/madden-nfl?locale=en&limit=100&search={player_name}'

rating_key_map: Dict[str, RatingType] = {
    "overall": RatingType.OVERALL,
    "acceleration": RatingType.ACCELERATION,
    "agility": RatingType.AGILITY,
    "jumping": RatingType.JUMPING,
    "stamina": RatingType.STAMINA,
    "strength": RatingType.STRENGTH,
    "awareness": RatingType.AWARENESS,
    "bCVision": RatingType.BC_VISION,
    "blockShedding": RatingType.BLOCK_SHEDDING,
    "breakSack": RatingType.BREAK_SACK,
    "breakTackle": RatingType.BREAK_TACKLE,
    "carrying": RatingType.CARRYING,
    "catchInTraffic": RatingType.CATCH_IN_TRAFFIC,
    "catching": RatingType.CATCHING,
    "changeOfDirection": RatingType.CHANGE_OF_DIRECTION,
    "deepRouteRunning": RatingType.DEEP_ROUTE_RUNNING,
    "finesseMoves": RatingType.FINESSE_MOVES,
    "hitPower": RatingType.HIT_POWER,
    "impactBlocking": RatingType.IMPACT_BLOCKING,
    "injury": RatingType.INJURY,
    "jukeMove": RatingType.JUKE_MOVE,
    "kickAccuracy": RatingType.KICK_ACCURACY,
    "kickPower": RatingType.KICK_POWER,
    "kickReturn": RatingType.KICK_RETURN,
    "leadBlock": RatingType.LEAD_BLOCK,
    "manCoverage": RatingType.MAN_COVERAGE,
    "mediumRouteRunning": RatingType.MEDIUM_ROUTE_RUNNING,
    "passBlock": RatingType.PASS_BLOCK,
    "passBlockFinesse": RatingType.PASS_BLOCK_FINESSE,
    "passBlockPower": RatingType.PASS_BLOCK_POWER,
    "playAction": RatingType.PLAY_ACTION,
    "playRecognition": RatingType.PLAY_RECOGNITION,
    "powerMoves": RatingType.POWER_MOVES,
    "press": RatingType.PRESS,
    "pursuit": RatingType.PURSUIT,
    "release": RatingType.RELEASE,
    "runBlock": RatingType.RUN_BLOCK,
    "runBlockFinesse": RatingType.RUN_BLOCK_FINESSE,
    "runBlockPower": RatingType.RUN_BLOCK_POWER,
    "runningStyle": RatingType.RUNNING_STYLE,
    "shortRouteRunning": RatingType.SHORT_ROUTE_RUNNING,
    "spectacularCatch": RatingType.SPECTACULAR_CATCH,
    "speed": RatingType.SPEED,
    "spinMove": RatingType.SPIN_MOVE,
    "stiffArm": RatingType.STIFF_ARM,
    "tackle": RatingType.TACKLE,
    "throwAccuracyDeep": RatingType.THROW_ACCURACY_DEEP,
    "throwAccuracyMid": RatingType.THROW_ACCURACY_MID,
    "throwAccuracyShort": RatingType.THROW_ACCURACY_SHORT,
    "throwOnTheRun": RatingType.THROW_ON_THE_RUN,
    "throwPower": RatingType.THROW_POWER,
    "throwUnderPressure": RatingType.THROW_UNDER_PRESSURE,
    "toughness": RatingType.TOUGHNESS,
    "trucking": RatingType.TRUCKING,
    "zoneCoverage": RatingType.ZONE_COVERAGE
}

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
        
        rating_type = rating_key_map.get(stat_name)
        if rating_type:
            ratings.append(Rating(rating_type, rating_value))
        else:
            Logger.warning(f"{stat_name} is not a recognized RatingType.")
    
    return ratings