from enum import Enum

class DevelopmentTrait(Enum):
    AGE_REGRESS: str = 'Start regressing with age.'
    NORMAL: str = 'Slow and steady improvement.'
    STAR: str = 'Decent rate of improvement.'
    SUPERSTAR: str = 'Fast rate of improvement.'
    GENERATIONAL: str = 'Extremely fast rate of improvement.'