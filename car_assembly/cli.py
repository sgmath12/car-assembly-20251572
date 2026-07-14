import sys
import time
from typing import Dict, Tuple

from .car import Car
from .models import BrakeSystem, CarSelection, CarType, Engine, SteeringSystem

CLEAR_SCREEN = "\033[H\033[2J"

STEP_CAR_TYPE = 0
STEP_ENGINE = 1
STEP_BRAKE = 2
STEP_STEERING = 3
STEP_RUN_TEST = 4

CAR_TYPE_LABELS: Dict[CarType, str] = {
    CarType.SEDAN: "Sedan",
    CarType.SUV: "SUV",
    CarType.TRUCK: "Truck",
}
BRAKE_SELECT_LABELS: Dict[BrakeSystem, str] = {
    BrakeSystem.MANDO: "MANDO",
    BrakeSystem.CONTINENTAL: "CONTINENTAL",
    BrakeSystem.BOSCH: "BOSCH",
}
BRAKE_DESCRIBE_LABELS: Dict[BrakeSystem, str] = {
    BrakeSystem.MANDO: "Mando",
    BrakeSystem.CONTINENTAL: "Continental",
    BrakeSystem.BOSCH: "Bosch",
}
STEERING_SELECT_LABELS: Dict[SteeringSystem, str] = {
    SteeringSystem.BOSCH: "BOSCH",
    SteeringSystem.MOBIS: "MOBIS",
}
STEERING_DESCRIBE_LABELS: Dict[SteeringSystem, str] = {
    SteeringSystem.BOSCH: "Bosch",
    SteeringSystem.MOBIS: "Mobis",
}

VALID_RANGES: Dict[int, Tuple[int, int, str]] = {
    STEP_CAR_TYPE: (1, 3, "차량 타입은 1 ~ 3 범위만 선택 가능"),
    STEP_ENGINE: (0, 4, "엔진은 1 ~ 4 범위만 선택 가능"),
    STEP_BRAKE: (0, 3, "제동장치는 1 ~ 3 범위만 선택 가능"),
    STEP_STEERING: (0, 2, "조향장치는 1 ~ 2 범위만 선택 가능"),
    STEP_RUN_TEST: (0, 2, "Run 또는 Test 중 하나를 선택 필요"),
}


def delay(ms: int) -> None:
    time.sleep(ms / 1000.0)


def clear() -> None:
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def show_menu(step: int) -> None:
    clear()
    if step == STEP_CAR_TYPE:
        print("        ______________")
        print("       /|            |")
        print("  ____/_|_____________|____")
        print(" |                      O  |")
        print(" '-(@)----------------(@)--'")
        print("===============================")
        print("어떤 차량 타입을 선택할까요?")
        print("1. Sedan")
        print("2. SUV")
        print("3. Truck")
    elif step == STEP_ENGINE:
        print("어떤 엔진을 탑재할까요?")
        print("0. 뒤로가기")
        print("1. GM")
        print("2. TOYOTA")
        print("3. WIA")
        print("4. 고장난 엔진")
    elif step == STEP_BRAKE:
        print("어떤 제동장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. MANDO")
        print("2. CONTINENTAL")
        print("3. BOSCH")
    elif step == STEP_STEERING:
        print("어떤 조향장치를 선택할까요?")
        print("0. 뒤로가기")
        print("1. BOSCH")
        print("2. MOBIS")
    elif step == STEP_RUN_TEST:
        print("멋진 차량이 완성되었습니다.")
        print("0. 처음 화면으로 돌아가기")
        print("1. RUN")
        print("2. Test")
    print("===============================")


def is_valid_range(step: int, ans: int) -> bool:
    lo, hi, message = VALID_RANGES[step]
    if ans < lo or ans > hi:
        print(f"ERROR :: {message}")
        return False
    return True


def select_car_type(selection: CarSelection, ans: int) -> None:
    selection.car_type = CarType(ans)
    label = CAR_TYPE_LABELS[selection.car_type]
    print(f"차량 타입으로 {label}을 선택하셨습니다.")


def select_engine(selection: CarSelection, ans: int) -> None:
    selection.engine = Engine(ans)
    if selection.engine == Engine.BROKEN:
        print("고장난 엔진을 선택하셨습니다.")
    else:
        print(f"{selection.engine.name} 엔진을 선택하셨습니다.")


def select_brake(selection: CarSelection, ans: int) -> None:
    selection.brake = BrakeSystem(ans)
    label = BRAKE_SELECT_LABELS[selection.brake]
    print(f"{label} 제동장치를 선택하셨습니다.")


def select_steering(selection: CarSelection, ans: int) -> None:
    selection.steering = SteeringSystem(ans)
    label = STEERING_SELECT_LABELS[selection.steering]
    print(f"{label} 조향장치를 선택하셨습니다.")


def describe_car(selection: CarSelection) -> list:
    lines = []
    if selection.car_type is not None:
        lines.append(f"Car Type : {CAR_TYPE_LABELS[selection.car_type]}")
    if selection.engine is not None:
        lines.append(f"Engine   : {selection.engine.name}")
    if selection.brake is not None:
        lines.append(f"Brake    : {BRAKE_DESCRIBE_LABELS[selection.brake]}")
    if selection.steering is not None:
        lines.append(f"Steering : {STEERING_DESCRIBE_LABELS[selection.steering]}")
    return lines


def run_produced_car(car: Car) -> None:
    if not car.is_valid():
        print("자동차가 동작되지 않습니다")
        return
    if car.selection.engine == Engine.BROKEN:
        print("엔진이 고장나있습니다.")
        print("자동차가 움직이지 않습니다.")
        return

    for line in describe_car(car.selection):
        print(line)
    print("자동차가 동작됩니다.")


def test_produced_car(car: Car) -> None:
    violations = car.violations()
    if violations:
        print(f"FAIL\n{violations[0].message}")
    else:
        print("PASS")


def main() -> None:
    step = STEP_CAR_TYPE
    selection = CarSelection()
    car = Car(selection)

    while True:
        show_menu(step)
        buf = input("INPUT > ").strip()

        if buf == "exit":
            print("바이바이")
            break

        try:
            ans = int(buf)
        except ValueError:
            print("ERROR :: 숫자만 입력 가능")
            delay(800)
            continue

        if not is_valid_range(step, ans):
            delay(800)
            continue

        if ans == 0:
            if step == STEP_RUN_TEST:
                step = STEP_CAR_TYPE
            elif step > STEP_CAR_TYPE:
                step -= 1
            continue

        if step == STEP_CAR_TYPE:
            select_car_type(selection, ans)
            delay(800)
            step = STEP_ENGINE
        elif step == STEP_ENGINE:
            select_engine(selection, ans)
            delay(800)
            step = STEP_BRAKE
        elif step == STEP_BRAKE:
            select_brake(selection, ans)
            delay(800)
            step = STEP_STEERING
        elif step == STEP_STEERING:
            select_steering(selection, ans)
            delay(800)
            step = STEP_RUN_TEST
        elif step == STEP_RUN_TEST:
            if ans == 1:
                run_produced_car(car)
                delay(2000)
            elif ans == 2:
                print("Test...")
                delay(1500)
                test_produced_car(car)
                delay(2000)


if __name__ == "__main__":
    main()
