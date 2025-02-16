import logging
import random
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from db.util import fetch_all_refs
from db.load.team import create_teams
from db.load.athlete import create_athletes
from db.load.event import create_events
from db.load.draft import fetch_draft_picks
from db.load.contract import fetch_team_year_contracts, TEAMS_LOOKUP
from db.models import Base

class DatabaseInitializer:
    def __init__(
        self,
        years: List[int],
        database_url: str,
        event_season_types: List[int] = [1, 2, 3],
        weeks: List[int] = list(range(1, 19)),
        echo: bool = False,
    ):
        self.years = years
        self.database_url = database_url
        self.event_season_types = event_season_types
        self.weeks = weeks
        self.echo = echo
        self.proxy_file = "./proxy_list.txt"
        self.proxies = self.load_proxies()
        self.engine = create_engine(self.database_url, echo=self.echo)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.ESPN_BASE_URL = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"

    def load_proxies(self) -> List[str]:
        """Load proxies from a file."""
        try:
            with open(self.proxy_file, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            logging.error(f"Proxy file {self.proxy_file} not found.")
            return []

    def get_random_proxy(self) -> str:
        """Get a random proxy from the loaded list."""
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def initialize_database(self) -> None:
        """Initialize the database by creating all tables."""
        with self.engine.begin() as conn:
            Base.metadata.create_all(conn)

    def initialize_teams(self, session) -> None:
        """Fetch and initialize NFL teams."""
        team_urls = fetch_all_refs(
            f"{self.ESPN_BASE_URL}/teams", limit=500, proxy=self.get_random_proxy()
        )
        create_teams(session, team_urls, self.proxies)

    def initialize_team_contracts(self) -> None:
        """Fetch and initialize NFL team contracts."""
        team_names = list(TEAMS_LOOKUP.values())
        for team_name in team_names:
            for year in self.years:
                fetch_team_year_contracts(team_name, year, self.proxies)

    def initialize_team_draftpicks(self) -> None:
        """Fetch and initialize NFL team draft picks."""
        for year in self.years:
            fetch_draft_picks(year, self.proxies)

    def initialize_athletes(self, session) -> None:
        """Fetch and initialize NFL athletes."""
        athlete_urls = fetch_all_refs(
            f"{self.ESPN_BASE_URL}/athletes", limit=500, proxy=self.get_random_proxy()
        )
        create_athletes(session, athlete_urls, self.proxies)
    
    def initialize_events(self, session) -> None:
        """Fetch and initialize NFL events with progress bar."""

        event_base_url = f"{self.ESPN_BASE_URL}/seasons/{{YEAR}}/types/{{TYPE}}/weeks/{{WEEK}}/events"

        total_iterations = sum(len(self.weeks) for _ in self.years for _ in self.event_season_types)
        
        with tqdm(total=total_iterations, desc="Fetching NFL Events") as pbar:
            for year in self.years:
                for season_type in self.event_season_types:
                    max_weeks = {
                        1: 4,   # Preseason
                        2: 18,  # Regular season
                        3: 5    # Postseason
                    }.get(season_type, 0)

                    valid_weeks = [week for week in self.weeks if week <= max_weeks]

                    for week in valid_weeks:
                        url = event_base_url.format(YEAR=year, TYPE=season_type, WEEK=week)
                        event_urls = fetch_all_refs(url, limit=18, proxy=self.get_random_proxy())
                        create_events(session, event_urls, self.proxies)
                        pbar.update(1)

    def run_initialization(self) -> None:
        """Run the full database initialization process."""
        self.initialize_database()

        with self.SessionLocal() as session:
            self.initialize_team_draftpicks()
            self.initialize_teams(session)
            self.initialize_team_contracts()
            self.initialize_athletes(session)
            self.initialize_events(session)
            session.commit()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="database_initializer.log"
    )

    years = list(range(2011, 2025))
    database_url = "sqlite:///sports.db"

    initializer = DatabaseInitializer(years, database_url)
    initializer.run_initialization()
