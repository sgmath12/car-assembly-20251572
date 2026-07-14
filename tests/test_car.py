from car_assembly.car import Car
from car_assembly.models import BrakeSystem, CarSelection, CarType, Engine, SteeringSystem


def test_valid_combination_is_valid():
    car = Car(
        CarSelection(
            car_type=CarType.SUV,
            engine=Engine.GM,
            brake=BrakeSystem.BOSCH,
            steering=SteeringSystem.BOSCH,
        )
    )
    assert car.is_valid()
    assert car.violations() == []


def test_invalid_combination_is_invalid():
    car = Car(
        CarSelection(
            car_type=CarType.SEDAN,
            engine=Engine.GM,
            brake=BrakeSystem.CONTINENTAL,
            steering=SteeringSystem.MOBIS,
        )
    )
    assert not car.is_valid()
    assert len(car.violations()) == 1


def test_default_selection_has_no_parts_and_is_valid():
    car = Car()
    assert car.is_valid()
