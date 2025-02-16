from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Event

def extract_event(session: Session, event_id: int) -> Event:
    return session.execute(
        select(Event).filter_by(id=event_id)
    ).scalars().first()