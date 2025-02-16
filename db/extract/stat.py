from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Stat

def extract_stat(
    session: Session, stat_name: str, description: str, 
    abbreviation: str, stat_value: float, playparticipant_id: int
) -> Stat:
    return session.execute(
        select(Stat).filter_by(
            name=stat_name,
            description = description,
            abbreviation = abbreviation,
            value=stat_value, 
            playparticipant_id=playparticipant_id
        )
    ).scalars().first()