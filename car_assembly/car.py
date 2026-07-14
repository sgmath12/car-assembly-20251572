from dataclasses import dataclass, field
from typing import List

from .models import CarSelection
from .rules import CompatibilityRule, find_violations


@dataclass
class Car:
    selection: CarSelection = field(default_factory=CarSelection)

    def violations(self) -> List[CompatibilityRule]:
        return find_violations(self.selection)

    def is_valid(self) -> bool:
        return not self.violations()
