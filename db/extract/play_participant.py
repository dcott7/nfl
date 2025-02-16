from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import PlayParticipant

def extract_play_participant(session: Session, athlete_id: int, order: int) -> PlayParticipant:
    return session.execute(
        select(PlayParticipant).filter_by(athlete_id=athlete_id, order=order)
    ).scalars().first()