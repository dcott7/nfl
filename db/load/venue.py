from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, Any

from db.models import Venue
from db.extract.venue import extract_venue


def extract_address_data(address: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts and returns relevant address data.

    Args:
        address (Dict[str, Any]): The address data from the venue.

    Returns:
        Dict[str, Any]: The extracted city, state, and zip code.
    """
    return {
        "city": address.get("city", ""),
        "state": address.get("state", ""),
        "zip_code": address.get("zipCode", 0),
    }


def create_venue(session: Session, venue_data: Dict[str, Any]) -> Venue:
    """
    Fetches an existing venue or creates a new one synchronously from the given data.

    Args:
        session (Session): SQLAlchemy session object.
        venue_data (Dict[str, Any]): Data representing the venue.

    Returns:
        Venue: The persisted or fetched Venue object.
    """
    venue_id = int(venue_data['id'])

    venue = extract_venue(session, venue_id)
    if venue:
        return venue

    address_data = extract_address_data(venue_data.get('address', {}))

    venue = Venue(
        id=venue_id,
        name=str(venue_data['fullName']),
        grass=bool(venue_data.get('grass', False)),
        indoor=bool(venue_data.get('indoor', False)),
        city=address_data["city"],
        state=address_data["state"],
        zip_code=address_data["zip_code"],
    )

    session.add(venue)
    session.commit()

    return venue
