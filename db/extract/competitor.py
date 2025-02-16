from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Competitor

def extract_competitor(
    session: Session, is_home: bool, is_winner: bool, 
    score: int, team_id: int, event_id: int, competition_id: int
) -> Competitor:
    return session.execute(select(Competitor).filter_by(
        is_home=is_home, is_winner=is_winner, score=score, 
        team_id=team_id, event_id=event_id, competition_id=competition_id
    )).scalars().first()