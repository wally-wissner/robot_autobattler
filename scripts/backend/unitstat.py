import numpy as np
from dataclasses import dataclass

from scripts.utilities.enums import EOperation, EStat
from scripts.utilities.game_math import clamp


@dataclass
class Stat(object):
    base_value: int = 0
    min_value: int = 0
    max_value: int = np.inf


class ConsumableStat(Stat):
    def __init__(self, refill_on_turn_start=False, refill_on_encounter_start=False, base_value=0, min_value=0, max_value=np.inf):
        self.refill_on_turn_start = refill_on_turn_start
        self.refill_on_level_start = refill_on_encounter_start

        self.current_value = None

        super().__init__(base_value=base_value, min_value=min_value, max_value=max_value)

    def __add__(self, other: int) -> bool:
        needed_squeeze = self.current_value + other == clamp(self.current_value - other, self.min_value, self.max_value)
        self.current_value = clamp(self.current_value + other, self.min_value, self.max_value)
        return not needed_squeeze

    def __sub__(self, other: int) -> bool:
        needed_squeeze = self.current_value - other == clamp(self.current_value - other, self.min_value, self.max_value)
        self.current_value = clamp(self.current_value - other, self.min_value, self.max_value)
        return not needed_squeeze

    def on_turn_start(self):
        if self.refill_on_turn_start:
            self.current_value = self.max_value

    def on_level_start(self):
        if self.refill_on_level_start:
            self.current_value = self.max_value


@dataclass(eq=True, frozen=True)
class StatModifier(object):
    stat: EStat
    operation: EOperation
    value: int | float

    def __repr__(self):
        return f"StatModifier({self.stat.value} {self.operation.value} {self.value})"
