import requests
from typing import List, Dict, Optional
import logging

from db.models import Rating
from db.util import fetch_page

BASE_PLAYER_SEARCH_URL = 'https://247sports.com/season/{year}-football/RecruitRankings/?InstitutionGroup=HighSchool&PositionGroup={position}&State={state}'


