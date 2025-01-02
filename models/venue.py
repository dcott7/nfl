from typing import Dict, Any

class Venue:
    def __init__(
        self, id: int, name: str, grass: bool, indoor: bool
    ) -> None:
        self.id = id
        self.name = name
        self.grass = grass
        self.indoor = indoor
        self.city: str = ''
        self.state: str = ''
        self.zip_code: int = 0

    def add_address(self, address_data: Dict[str, Any]) -> None:
        self.state = address_data.get('state','')
        self.zip_code = address_data.get('zip_code', None)
        self.city = address_data.get('city','')

    def __str__(self) -> str:
        return (
            f"<Venue(id={self.id}, name={self.name}, grass={self.grass}, "
            f"indoor={self.indoor}, city={self.city}, state={self.state}, "
            f"zip_code={self.zip_code})>"
        )
    
    def __repr__(self):
        return self.__str__()