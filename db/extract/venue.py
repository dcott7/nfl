from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Venue

def extract_venue(session: Session, venue_id: int) -> Venue:
    return session.execute(
        select(Venue).filter_by(id=venue_id)
    ).scalars().first()