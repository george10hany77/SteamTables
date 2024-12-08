from enum import Enum


class Phases(Enum):
    SUBCOOLED = 0
    SATMIXTURE = 1
    SUPERHEATED = 2
    NOTDETERMINED = 3
