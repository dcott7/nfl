import datetime

from fetch.util import fetch_all_refs
from fetch.team import create_teams
from fetch.event import create_events

"""
Global parameters.
"""
CURRENT_YEAR = datetime.datetime.now().year
START_YEAR = 2020

URL_BASE = 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl'
TEAMS_REF_PAGE = URL_BASE + '/teams'
EVENTS_REF_PAGE = URL_BASE + '/seasons/{YEAR}/types/{TYPE}/weeks/{WEEK}/events'

EVENT_YEARS = range(START_YEAR,CURRENT_YEAR+1)
EVENT_WEEKS = range(1,19)

"""
Required script parameters.
"""
LOAD_ATHLETES = True

EVENT_YEAR_START = START_YEAR
EVENT_YEAR_END = CURRENT_YEAR
EVENT_SEASON_TYPES = [1, 2, 3] # 1-pre, 2-reg, 3-post

"""
Load all of the NFL teams.
"""
TEAM_URLS = fetch_all_refs(TEAMS_REF_PAGE)
TEAMS = create_teams(TEAM_URLS, load_athletes=LOAD_ATHLETES)

"""
Load all of the NFL events.
"""
EVENTS=[]

EVENT_PAGES = [
    fetch_all_refs(EVENTS_REF_PAGE.format(YEAR=year,TYPE=season_type,WEEK=week))
    for year in EVENT_YEARS 
    for week in EVENT_WEEKS
    for season_type in EVENT_SEASON_TYPES
]

for event_page in EVENT_PAGES:
    EVENTS.extend(create_events(event_page))

for event in EVENTS:
    for competitor in event.competition.competitors:
        team = next((team for team in TEAMS if team.id == competitor.id), None)
        if team:
            team.add_event(event) # assign the event to a Team.