class Weather:
    def __init__(
        self, display: str, wind_speed: int, temperature: int, 
        gust: int, precipitation: int
    ) -> None:
        self.display = display
        self.wind_speed = wind_speed
        self.temperature = temperature
        self.gust = gust
        self.precipitation = precipitation

    def __str__(self) -> str:
        return (
            f"<Weather(display={self.display}, wind_speed={self.wind_speed}, "
            f"temperature={self.temperature}, gust={self.gust}, "
            f"precipitation={self.precipitation})>"
        )
    
    def __repr__(self) -> str:
        return self.__str__()