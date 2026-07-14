import pytest

from car_assembly.cli import (
    STEP_BRAKE,
    STEP_CAR_TYPE,
    STEP_ENGINE,
    STEP_RUN_TEST,
    STEP_STEERING,
    describe_car,
    is_valid_range,
    select_brake,
    select_car_type,
    select_engine,
    select_steering,
)
from car_assembly.models import BrakeSystem, CarSelection, CarType, Engine, SteeringSystem


@pytest.mark.parametrize(
    "step, ans, expected",
    [
        (STEP_CAR_TYPE, 1, True),
        (STEP_CAR_TYPE, 3, True),
        (STEP_CAR_TYPE, 0, False),
        (STEP_CAR_TYPE, 4, False),
        (STEP_ENGINE, 0, True),
        (STEP_ENGINE, 4, True),
        (STEP_ENGINE, 5, False),
        (STEP_BRAKE, 3, True),
        (STEP_BRAKE, 4, False),
        (STEP_STEERING, 2, True),
        (STEP_STEERING, 3, False),
        (STEP_RUN_TEST, 0, True),
        (STEP_RUN_TEST, 3, False),
    ],
)
def test_is_valid_range(step, ans, expected):
    assert is_valid_range(step, ans) is expected


def test_select_car_type_sets_selection():
    selection = CarSelection()
    select_car_type(selection, 2)
    assert selection.car_type == CarType.SUV


def test_select_engine_sets_selection():
    selection = CarSelection()
    select_engine(selection, 4)
    assert selection.engine == Engine.BROKEN


def test_select_brake_sets_selection():
    selection = CarSelection()
    select_brake(selection, 3)
    assert selection.brake == BrakeSystem.BOSCH


def test_select_steering_sets_selection():
    selection = CarSelection()
    select_steering(selection, 1)
    assert selection.steering == SteeringSystem.BOSCH


def test_describe_full_selection():
    selection = CarSelection(
        car_type=CarType.SUV,
        engine=Engine.GM,
        brake=BrakeSystem.BOSCH,
        steering=SteeringSystem.BOSCH,
    )
    assert describe_car(selection) == [
        "Car Type : SUV",
        "Engine   : GM",
        "Brake    : Bosch",
        "Steering : Bosch",
    ]


def test_describe_empty_selection_has_no_lines():
    assert describe_car(CarSelection()) == []
