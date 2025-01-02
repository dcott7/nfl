from typing import Dict, Any, List

from models.stat import Stat

def create_stat(stat_data: Dict[str, Any]) -> Stat:
    """Creates a Stat player."""

    return Stat(
        name = str(stat_data['name']),
        description = str(stat_data['description']),
        abbreviation = str(stat_data['abbreviation']),
        value = float(stat_data['value'])
    )

def create_stats(stats_data: List[Dict[str, Any]]) -> List[Stat]:
    """Creates a multiple Stats for a player."""
    return [create_stat(stat_data) for stat_data in stats_data]