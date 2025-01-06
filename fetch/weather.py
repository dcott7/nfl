from typing import Dict, Any
from sqlalchemy.orm import Session
from models import Weather

def create_weather(session: Session, weather_data: Dict[str, Any]) -> Weather:
    """Creates and persists a Weather object in the database.

    Params:
        session: SQLAlchemy session object.
        weather_data: dictionary data from ESPN response.

    Returns:
        Persisted Weather object.
    """
    # Check if the Weather object already exists
    weather_display = str(weather_data['displayValue'])
    weather = session.query(Weather).filter_by(display=weather_display).first()
    
    if weather:
        return weather  # Return the existing Weather object if found

    # Create a new Weather object
    weather = Weather(
        display=weather_display,
        wind_speed=int(weather_data.get('windSpeed', 0)),
        temperature=int(weather_data.get('temperature', 0)),
        gust=int(weather_data.get('gust', 0)),
        precipitation=int(weather_data.get('precipitation', 0))
    )

    # Persist the new Weather object to the database
    session.add(weather)
    session.commit()

    return weather
