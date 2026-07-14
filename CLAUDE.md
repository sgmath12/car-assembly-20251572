
### 차량 제조 순서

1) 자동차타입을선택한다.
세단, SUV(에스-유-브이), 트럭
2) 자동차에들어갈부품을선택한다.
엔진, 제동장치, 조향장치
3) 완성된차량을테스트한다.
선택한부품이자동차타입에사용가능한지검사

### 제조순서 1) 자동차 타입 선택

차량의종류를선택한다.
총세가지타입을제작할수있으며,
향후에타입이더추가될수있다.

### 제조순서 2) 자동차 조립

엔진, 제동장치, 조향장치를각각선택한다

### 제조순서 3) 완성 가능조합 확인

#### 제한조건1

+ 제동장치에Bosch 제품을사용했다면, 조향장치도Bosch 제품을사용해야한다. (타사제품과호환되지않는다.)

#### 제한조건2

+ Continental은 Sedan용 제동장치를만들지않는다. (-> 세단에 Continental 제품 사용 불가)
+ 도요타는SUV용엔진을만들지않는다.
+ WIA는Truck용엔진을만들지않는다.
+ Mando는Truck용제동장치(brake System)을만들지않는다.

### To do (반영 완료)

+ ~~절차지향식코드로, 유지보수가어려운구조~~ -> `car_assembly` 패키지로 분리, 전역변수/global 제거
+ ~~안전하지않은문법들이사용~~ -> bare `except:` 제거, `except ValueError:`로 명시
+ ~~확장성이고려되지않음~~ -> 제약조건을 데이터(RULES 리스트)로 표현, 신규 제약 추가 시 규칙 로직 수정 불필요
+ ~~유닛테스트가없음~~ -> pytest 기반 테스트 30개 추가

### 리팩토링 구조

절차지향 스크립트(`assemble.py` 하나)를 아래처럼 역할별로 분리했습니다.

```text
assemble.py            # 진입점 (car_assembly.cli.main() 호출만 함)
car_assembly/
  models.py             # 도메인 모델: CarType/Engine/BrakeSystem/SteeringSystem Enum, CarSelection dataclass
  rules.py              # 호환성 제약조건을 CompatibilityRule 목록(RULES)으로 표현
  car.py                # Car: CarSelection을 감싸서 violations()/is_valid() 제공
  cli.py                # 메뉴 출력, 입력 검증, 화면 문구 등 UI 로직 (도메인 로직과 분리)
tests/
  test_rules.py         # 제한조건1, 제한조건2 각각 검증
  test_car.py           # Car.is_valid()/violations() 검증
  test_cli.py           # 입력 범위 검증, 선택 함수, 화면 출력 문자열 검증
```

#### 동작 방식

1. `cli.main()`이 상태 없는 `CarSelection` 객체 하나를 만들어 단계(step)를 따라 값을 채웁니다. (기존처럼 전역 `q0~q3` 대신 이 객체 하나로 상태를 들고 다님)
2. 각 단계 선택 시 `select_car_type/engine/brake/steering()`이 `CarSelection` 필드를 채우고 안내 문구를 출력합니다.
3. RUN/Test 단계에서 `Car(selection).violations()`를 호출하면 `rules.RULES` 리스트를 순회하며 위반된 규칙들을 반환합니다.
    + 기존 제한조건1, 2가 각각 하나의 `CompatibilityRule` 항목(이름 + 실패 메시지 + 판정 함수)으로 등록되어 있습니다.
    + 새 제약조건을 추가하려면 `car_assembly/rules.py`의 `RULES` 리스트에 항목만 추가하면 되고, `is_valid_check`/`test_produced_car` 같은 곳을 따로 고칠 필요가 없습니다(기존엔 같은 조건을 두 함수에 중복 작성해야 했음).
4. `RUN`은 위반이 있으면 실패 메시지를, 없으면 부품 구성을 출력합니다. 단, "고장난 엔진(4번)"은 호환성 규칙이 아니라 별개의 결함으로 취급해 `run_produced_car`에서만 체크합니다(원본 동작 유지 — `Test` 메뉴는 고장난 엔진을 잡아내지 않는 원본의 동작도 그대로 보존했습니다).
5. `Test`는 `Car.violations()`의 첫 번째 위반 메시지를 출력하거나, 위반이 없으면 `PASS`를 출력합니다.

#### 실행/테스트 방법

```bash
python assemble.py          # 대화형 CLI 실행
python -m pytest -q         # 단위 테스트 30개 실행
```

#### 저장소

+ git init 후 `origin` = `https://github.com/sgmath12/car-assembly-20251572.git` 로 연결, `main` 브랜치에 커밋/푸시함.

### 참고

+ git address : <https://github.com/sgmath12/car-assembly-20251572>
