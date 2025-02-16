from typing import Dict, Any, List
from sqlalchemy.orm import Session

from db.models import Stat
from db.extract.stat import extract_stat


def create_stat(session: Session, stat_data: Dict[str, Any], playparticipant_id: int) -> Stat:
    """
    Creates and persists a Stat object in the database.

    Args:
        session (Session): SQLAlchemy session object.
        stat_data (Dict[str, Any]): Dictionary data for a single stat from ESPN response.
        playparticipant_id (int): The ID of the play participant.

    Returns:
        Stat: The persisted Stat object.
    """
    stat_name = str(stat_data['name'])
    description = str(stat_data.get('description', ''))
    abbreviation = str(stat_data.get('abbreviation', ''))
    stat_value = float(stat_data['value'])

    existing_stat = extract_stat(
        session, stat_name, description, abbreviation, stat_value, playparticipant_id
    )
    if existing_stat:
        return existing_stat
    

    stat = Stat(
        name=stat_name,
        description=description,
        abbreviation=abbreviation,
        value=stat_value,
        playparticipant_id=playparticipant_id
    )

    session.add(stat)
    session.commit()

    return stat


def create_stats(session: Session, stats_data: List[Dict[str, Any]], playparticipant_id: int) -> List[Stat]:
    """
    Creates and persists multiple Stat objects in the database.

    Args:
        session (Session): SQLAlchemy session object.
        stats_data (List[Dict[str, Any]]): List of dictionary data for multiple stats from ESPN response.
        playparticipant_id (int): The ID of the play participant.

    Returns:
        List[Stat]: List of persisted Stat objects.
    """
    stats = []
    for stat_data in stats_data:
        stat = create_stat(session, stat_data, playparticipant_id)
        stats.append(stat)

    return stats
