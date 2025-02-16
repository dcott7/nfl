from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Drive

def extract_drive(session: Session, drive_id: int) -> Drive:
    return session.execute(
        select(Drive).filter_by(id=drive_id)
    ).scalars().first()