from typing import List, Dict, Any

from python_models.drive import Drive
from fetch.play import create_plays

def create_drive(drive_data: Dict[str, Any]) -> Drive:
    """Creates a Drive.

    Params:
        drive_data: dictionary data from ESPN response.

    Returns:
        Drive object.
    """

    start_data = drive_data.get('start',{})
    end_data = drive_data.get('end',{})

    return Drive(
        id = int(drive_data['id']),
        description = str(drive_data['description']),
        yards = int(drive_data['yards']),
        is_score = bool(drive_data['isScore']),
        num_offensive_plays = int(drive_data['offensivePlays']),
        start_quarter = int(start_data.get('period',{})['number']),
        start_time = int(start_data.get('clock',{})['value']),
        start_yardline = int(start_data['yardLine']),
        end_quarter = int(end_data.get('period',{})['number']),
        end_time = int(end_data.get('period',{})['number']),
        end_yardline = int(end_data.get('period',{})['number']),
        plays = create_plays(drive_data.get('plays',{}))
    )

def create_drives(drives_data: List[Dict[str, Any]]) -> List[Drive]:
    """Creates a List of Drive."""
    return [create_drive(drive_data) for drive_data in drives_data]