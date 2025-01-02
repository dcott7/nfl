class Stat:
    def __init__(
        self, name: str, description: str, 
        abbreviation: str, value: float
    ) -> None:
        self.name = name
        self.description = description
        self.abbreviation = abbreviation
        self.value = value