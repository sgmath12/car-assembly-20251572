import unittest

from car_assembly.car import Car
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


class TestIsValidRange(unittest.TestCase):
    def test_car_type_step_accepts_1_to_3(self):
        self.assertTrue(is_valid_range(STEP_CAR_TYPE, 1))
        self.assertTrue(is_valid_range(STEP_CAR_TYPE, 3))
        self.assertFalse(is_valid_range(STEP_CAR_TYPE, 0))
        self.assertFalse(is_valid_range(STEP_CAR_TYPE, 4))

    def test_engine_step_accepts_0_to_4(self):
        self.assertTrue(is_valid_range(STEP_ENGINE, 0))
        self.assertTrue(is_valid_range(STEP_ENGINE, 4))
        self.assertFalse(is_valid_range(STEP_ENGINE, 5))

    def test_brake_step_accepts_0_to_3(self):
        self.assertTrue(is_valid_range(STEP_BRAKE, 3))
        self.assertFalse(is_valid_range(STEP_BRAKE, 4))

    def test_steering_step_accepts_0_to_2(self):
        self.assertTrue(is_valid_range(STEP_STEERING, 2))
        self.assertFalse(is_valid_range(STEP_STEERING, 3))

    def test_run_test_step_accepts_0_to_2(self):
        self.assertTrue(is_valid_range(STEP_RUN_TEST, 0))
        self.assertFalse(is_valid_range(STEP_RUN_TEST, 3))


class TestSelectFunctions(unittest.TestCase):
    def test_select_car_type_sets_selection(self):
        selection = CarSelection()
        select_car_type(selection, 2)
        self.assertEqual(selection.car_type, CarType.SUV)

    def test_select_engine_sets_selection(self):
        selection = CarSelection()
        select_engine(selection, 4)
        self.assertEqual(selection.engine, Engine.BROKEN)

    def test_select_brake_sets_selection(self):
        selection = CarSelection()
        select_brake(selection, 3)
        self.assertEqual(selection.brake, BrakeSystem.BOSCH)

    def test_select_steering_sets_selection(self):
        selection = CarSelection()
        select_steering(selection, 1)
        self.assertEqual(selection.steering, SteeringSystem.BOSCH)


class TestDescribeCar(unittest.TestCase):
    def test_describe_full_selection(self):
        selection = CarSelection(
            car_type=CarType.SUV,
            engine=Engine.GM,
            brake=BrakeSystem.BOSCH,
            steering=SteeringSystem.BOSCH,
        )
        lines = describe_car(selection)
        self.assertEqual(
            lines,
            [
                "Car Type : SUV",
                "Engine   : GM",
                "Brake    : Bosch",
                "Steering : Bosch",
            ],
        )

    def test_describe_empty_selection_has_no_lines(self):
        self.assertEqual(describe_car(CarSelection()), [])


if __name__ == "__main__":
    unittest.main()
