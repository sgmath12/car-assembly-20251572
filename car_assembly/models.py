from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CarType(Enum):
    SEDAN = 1
    SUV = 2
    TRUCK = 3


class Engine(Enum):
    GM = 1
    TOYOTA = 2
    WIA = 3
    BROKEN = 4


class BrakeSystem(Enum):
    MANDO = 1
    CONTINENTAL = 2
    BOSCH = 3


class SteeringSystem(Enum):
    BOSCH = 1
    MOBIS = 2


@dataclass
class CarSelection:
    car_type: Optional[CarType] = None
    engine: Optional[Engine] = None
    brake: Optional[BrakeSystem] = None
    steering: Optional[SteeringSystem] = None
