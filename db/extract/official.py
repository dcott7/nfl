from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Official, OfficialPosition

def extract_official_position(session: Session, official_pos_id: int) -> OfficialPosition:
    return session.execute(
        select(OfficialPosition).filter_by(id=official_pos_id)
    ).scalars().first()
    
    
def extract_official(session: Session, official_id: int) -> Official:
    return session.execute(
        select(Official).filter_by(id=official_id)
    ).scalars().first()