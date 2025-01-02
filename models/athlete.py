from typing import List

from models.position import PositionEnum
from models.development import DevelopmentTrait
from models.rating import Rating, RatingType

class Athlete:
    def __init__(
        self, name: str, id: int, age: int, height: int, weight: int,
        position: PositionEnum, salary: float, ratings: List[Rating],
        is_practice_squad: bool
        # development_trait: DevelopmentTrait
    ) -> None:
        self.name = name
        self.id = id 
        self.age = age
        self.height = height
        self.weight = weight
        self.position = position
        self.salary = salary
        self.is_active = True
        self.ratings = ratings
        self.is_practice_squad = is_practice_squad
        # self.development_trait = development_trait

    def change_salary(self, new_salary: float):
        self.salary = new_salary

    def make_active(self):
        self.is_active = True

    def make_inactive(self):
        self.is_active = False

    def get_overall(self):
        return [rating.rating for rating in self.ratings if rating.rating_type == RatingType.OVERALL][0]

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'position': self.position.name,
            'salary': self.salary,
            'is_active': self.is_active
        }