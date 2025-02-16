from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Competition, CompetitionStatus, CompetitionStatusType

def extract_competition_status(
    session: Session, clock: str, display_clock:str, period: int, competition_status_type_id: int
) -> CompetitionStatus:
    
    return session.execute(
        select(CompetitionStatus).filter_by(
            clock=clock,
            display_clock=display_clock,
            period=period,
            competition_status_type_id=competition_status_type_id
        )
    ).scalars().first()


def extract_competition_status_type(
    session: Session, competition_status_type_id: int
) -> CompetitionStatusType:
    
    return session.execute(
        select(CompetitionStatusType).filter_by(id=competition_status_type_id)
    ).scalars().first()


def extract_competition(session: Session, competition_id: int) -> Competition:
    return session.execute(
        select(Competition).filter_by(id=competition_id)
    ).scalars().first()
    