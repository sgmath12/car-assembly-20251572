import unittest

from car_assembly.car import Car
from car_assembly.models import BrakeSystem, CarSelection, CarType, Engine, SteeringSystem


class TestCar(unittest.TestCase):
    def test_valid_combination_is_valid(self):
        car = Car(
            CarSelection(
                car_type=CarType.SUV,
                engine=Engine.GM,
                brake=BrakeSystem.BOSCH,
                steering=SteeringSystem.BOSCH,
            )
        )
        self.assertTrue(car.is_valid())
        self.assertEqual(car.violations(), [])

    def test_invalid_combination_is_invalid(self):
        car = Car(
            CarSelection(
                car_type=CarType.SEDAN,
                engine=Engine.GM,
                brake=BrakeSystem.CONTINENTAL,
                steering=SteeringSystem.MOBIS,
            )
        )
        self.assertFalse(car.is_valid())
        self.assertEqual(len(car.violations()), 1)

    def test_default_selection_has_no_parts_and_is_valid(self):
        car = Car()
        self.assertTrue(car.is_valid())


if __name__ == "__main__":
    unittest.main()
