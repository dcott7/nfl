from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Athlete, Position, TeamHistory

def extract_team_history(session: Session, athlete_id: int, team_id: int, season: int) -> TeamHistory:
    return session.execute(
        select(TeamHistory).filter_by(athlete_id=athlete_id, team_id=team_id, season=season)
    ).scalars().first()
    

def extract_athlete_position(session: Session, position_name: str) -> Position:
    return session.execute(
        select(Position).filter_by(position_name=position_name)
    ).scalars().first()
    

def extract_athlete(session: Session, athlete_id: int) -> Athlete:
    return session.execute(
        select(Athlete).filter_by(id=athlete_id)
    ).scalars().first()