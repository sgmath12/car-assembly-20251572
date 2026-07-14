import unittest

from car_assembly.models import BrakeSystem, CarSelection, CarType, Engine, SteeringSystem
from car_assembly.rules import find_violations


class TestCompatibilityRules(unittest.TestCase):
    def test_fully_compatible_combination_has_no_violations(self):
        selection = CarSelection(
            car_type=CarType.SEDAN,
            engine=Engine.GM,
            brake=BrakeSystem.MANDO,
            steering=SteeringSystem.MOBIS,
        )
        self.assertEqual(find_violations(selection), [])

    def test_sedan_rejects_continental_brake(self):
        selection = CarSelection(car_type=CarType.SEDAN, brake=BrakeSystem.CONTINENTAL)
        names = [rule.name for rule in find_violations(selection)]
        self.assertIn("sedan_no_continental_brake", names)

    def test_suv_rejects_toyota_engine(self):
        selection = CarSelection(car_type=CarType.SUV, engine=Engine.TOYOTA)
        names = [rule.name for rule in find_violations(selection)]
        self.assertIn("suv_no_toyota_engine", names)

    def test_truck_rejects_wia_engine(self):
        selection = CarSelection(car_type=CarType.TRUCK, engine=Engine.WIA)
        names = [rule.name for rule in find_violations(selection)]
        self.assertIn("truck_no_wia_engine", names)

    def test_truck_rejects_mando_brake(self):
        selection = CarSelection(car_type=CarType.TRUCK, brake=BrakeSystem.MANDO)
        names = [rule.name for rule in find_violations(selection)]
        self.assertIn("truck_no_mando_brake", names)

    def test_bosch_brake_requires_bosch_steering(self):
        selection = CarSelection(brake=BrakeSystem.BOSCH, steering=SteeringSystem.MOBIS)
        names = [rule.name for rule in find_violations(selection)]
        self.assertIn("bosch_brake_requires_bosch_steering", names)

    def test_bosch_brake_with_bosch_steering_is_allowed(self):
        selection = CarSelection(brake=BrakeSystem.BOSCH, steering=SteeringSystem.BOSCH)
        names = [rule.name for rule in find_violations(selection)]
        self.assertNotIn("bosch_brake_requires_bosch_steering", names)

    def test_multiple_violations_are_all_reported(self):
        selection = CarSelection(
            car_type=CarType.TRUCK,
            engine=Engine.WIA,
            brake=BrakeSystem.MANDO,
        )
        names = {rule.name for rule in find_violations(selection)}
        self.assertEqual(names, {"truck_no_wia_engine", "truck_no_mando_brake"})


if __name__ == "__main__":
    unittest.main()
