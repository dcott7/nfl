from typing import Dict, Any
from sqlalchemy.orm import Session
from models import Venue

def create_venue(session: Session, venue_data: Dict[str, Any]) -> Venue:
    """Creates and persists a Venue in the database.

    Params:
        session: SQLAlchemy session object.
        venue_data: dictionary data from ESPN response.

    Returns:
        Persisted Venue object.
    """
    # Check if the Venue already exists in the database
    venue_id = int(venue_data['id'])
    venue = session.query(Venue).filter_by(id=venue_id).first()
    
    if venue:
        return venue  # Return the existing venue if found

    # Create a new Venue object
    venue = Venue(
        id=venue_id,
        name=str(venue_data['fullName']),
        grass=bool(venue_data.get('grass', False)),
        indoor=bool(venue_data.get('indoor', False)),
        city=venue_data.get('address', {}).get('city', ""),
        state=venue_data.get('address', {}).get('state', ""),
        zip_code=venue_data.get('address', {}).get('zipCode', 0),
    )

    # Persist the new Venue to the database
    session.add(venue)
    session.commit()

    return venue
