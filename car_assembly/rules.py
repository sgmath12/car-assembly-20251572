"""Compatibility rules between car parts.

New rules can be added by appending a `CompatibilityRule` to `RULES`
without touching any validation logic.
"""

from dataclasses import dataclass
from typing import Callable, List

from .models import BrakeSystem, CarSelection, CarType, Engine, SteeringSystem


@dataclass(frozen=True)
class CompatibilityRule:
    name: str
    message: str
    is_violated: Callable[[CarSelection], bool]


RULES: List[CompatibilityRule] = [
    CompatibilityRule(
        name="sedan_no_continental_brake",
        message="Sedan에는 Continental 제동장치 사용 불가",
        is_violated=lambda s: s.car_type == CarType.SEDAN and s.brake == BrakeSystem.CONTINENTAL,
    ),
    CompatibilityRule(
        name="suv_no_toyota_engine",
        message="SUV에는 TOYOTA 엔진 사용 불가",
        is_violated=lambda s: s.car_type == CarType.SUV and s.engine == Engine.TOYOTA,
    ),
    CompatibilityRule(
        name="truck_no_wia_engine",
        message="Truck에는 WIA 엔진 사용 불가",
        is_violated=lambda s: s.car_type == CarType.TRUCK and s.engine == Engine.WIA,
    ),
    CompatibilityRule(
        name="truck_no_mando_brake",
        message="Truck에는 Mando 제동장치 사용 불가",
        is_violated=lambda s: s.car_type == CarType.TRUCK and s.brake == BrakeSystem.MANDO,
    ),
    CompatibilityRule(
        name="bosch_brake_requires_bosch_steering",
        message="Bosch 제동장치에는 Bosch 조향장치 이외 사용 불가",
        is_violated=lambda s: s.brake == BrakeSystem.BOSCH and s.steering != SteeringSystem.BOSCH,
    ),
]


def find_violations(selection: CarSelection) -> List[CompatibilityRule]:
    return [rule for rule in RULES if rule.is_violated(selection)]
