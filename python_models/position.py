from enum import Enum

class PositionEnum(Enum):
    # offense
    QB: str = 'qb'
    RB: str = 'rb'
    FB: str = 'fb'
    WR: str = 'wr'
    TE: str = 'te'
    OT: str = 'ot'
    G: str = 'g'
    C: str = 'c'

    # defense
    DT: str = 'dt'
    DE: str = 'de'
    LB: str = 'lb'
    CB: str = 'cb'
    S: str = 's'

    # special teams
    PK: str = 'k'
    P: str = 'p'
    LS: str = 'ls'

    UNKNOWN: str = 'UNKNOWN'