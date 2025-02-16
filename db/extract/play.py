from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Play

def extract_play(session: Session, play_id: int) -> Play:
    return session.execute(
        select(Play).filter_by(id=play_id)
    ).scalars().first()