from typing import Dict, Any

from models.weather import Weather

def create_weather(weather_data: Dict[str, Any]) -> Weather:
    return Weather(
        display = str(weather_data['displayValue']),
        wind_speed = int(weather_data['windSpeed']),
        temperature = int(weather_data['temperature']),
        gust = int(weather_data['gust']),
        precipitation = int(weather_data['precipitation'])
    )