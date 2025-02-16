from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Team

def extract_team(session: Session, team_id: int) -> Team:
    return session.execute(
        select(Team).filter_by(id=team_id)
    ).scalars().first()