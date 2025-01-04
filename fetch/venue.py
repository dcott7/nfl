from typing import Dict, Any

from python_models.venue import Venue

def create_venue(venue_data: Dict[str,Any]) -> Venue:
    venue = Venue(
        id = int(venue_data['id']),
        name = str(venue_data['fullName']),
        grass = bool(venue_data['grass']),
        indoor = bool(venue_data['indoor'])
    )
    
    venue.add_address(venue_data.get('address',{}))

    return venue