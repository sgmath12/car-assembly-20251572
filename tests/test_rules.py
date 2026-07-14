from car_assembly.models import BrakeSystem, CarSelection, CarType, Engine, SteeringSystem
from car_assembly.rules import find_violations


def test_fully_compatible_combination_has_no_violations():
    selection = CarSelection(
        car_type=CarType.SEDAN,
        engine=Engine.GM,
        brake=BrakeSystem.MANDO,
        steering=SteeringSystem.MOBIS,
    )
    assert find_violations(selection) == []


def test_sedan_rejects_continental_brake():
    selection = CarSelection(car_type=CarType.SEDAN, brake=BrakeSystem.CONTINENTAL)
    names = [rule.name for rule in find_violations(selection)]
    assert "sedan_no_continental_brake" in names


def test_suv_rejects_toyota_engine():
    selection = CarSelection(car_type=CarType.SUV, engine=Engine.TOYOTA)
    names = [rule.name for rule in find_violations(selection)]
    assert "suv_no_toyota_engine" in names


def test_truck_rejects_wia_engine():
    selection = CarSelection(car_type=CarType.TRUCK, engine=Engine.WIA)
    names = [rule.name for rule in find_violations(selection)]
    assert "truck_no_wia_engine" in names


def test_truck_rejects_mando_brake():
    selection = CarSelection(car_type=CarType.TRUCK, brake=BrakeSystem.MANDO)
    names = [rule.name for rule in find_violations(selection)]
    assert "truck_no_mando_brake" in names


def test_bosch_brake_requires_bosch_steering():
    selection = CarSelection(brake=BrakeSystem.BOSCH, steering=SteeringSystem.MOBIS)
    names = [rule.name for rule in find_violations(selection)]
    assert "bosch_brake_requires_bosch_steering" in names


def test_bosch_brake_with_bosch_steering_is_allowed():
    selection = CarSelection(brake=BrakeSystem.BOSCH, steering=SteeringSystem.BOSCH)
    names = [rule.name for rule in find_violations(selection)]
    assert "bosch_brake_requires_bosch_steering" not in names


def test_multiple_violations_are_all_reported():
    selection = CarSelection(
        car_type=CarType.TRUCK,
        engine=Engine.WIA,
        brake=BrakeSystem.MANDO,
    )
    names = {rule.name for rule in find_violations(selection)}
    assert names == {"truck_no_wia_engine", "truck_no_mando_brake"}
