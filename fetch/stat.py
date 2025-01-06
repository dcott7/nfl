from typing import Dict, Any, List
from sqlalchemy.orm import Session
from models import Stat

def create_stat(session: Session, stat_data: Dict[str, Any], playparticipant_id) -> Stat:
    """Creates and persists a Stat object in the database.

    Params:
        session: SQLAlchemy session object.
        stat_data: dictionary data for a single stat from ESPN response.

    Returns:
        Persisted Stat object.
    """

    stat_name = str(stat_data['name'])
    stat_value = float(stat_data['value'])
    
    stat = session.query(Stat).filter_by(name=stat_name, value=stat_value).first()
    
    if stat:
        return stat

    stat = Stat(
        name=stat_name,
        description=str(stat_data.get('description', '')),
        abbreviation=str(stat_data.get('abbreviation', '')),
        value=stat_value,
        playparticipant_id=playparticipant_id
    )

    session.add(stat)
    session.commit()

    return stat


def create_stats(session: Session, stats_data: List[Dict[str, Any]], playparticipant_id) -> List[Stat]:
    """Creates and persists multiple Stat objects in the database.

    Params:
        session: SQLAlchemy session object.
        stats_data: list of dictionary data for multiple stats from ESPN response.

    Returns:
        List of persisted Stat objects.
    """
    return [create_stat(session, stat_data, playparticipant_id) for stat_data in stats_data]
