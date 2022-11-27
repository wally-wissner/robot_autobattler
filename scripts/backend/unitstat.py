import numpy as np
from dataclasses import dataclass
from functools import total_ordering

from scripts.utilities.enums import EOperation, EStat
from scripts.utilities.game_math import clamp


@total_ordering
class Stat(object):
    def __init__(self, estat: EStat, unit_upgrades, base_value=0, min_value=0, max_value=np.inf):
        self.estat = estat
        self.unit_upgrades = unit_upgrades
        self.base_value = base_value
        self.min_value = min_value
        self.max_value = max_value

    @property
    def value(self):
        value = self.base_value

        # Add all additive modifiers.
        for unit_upgrade in self.unit_upgrades:
            for stat_modifier in unit_upgrade.stat_modifiers:
                if (stat_modifier.stat == self.estat) and (stat_modifier.operation == EOperation.PLUS):
                    value += stat_modifier.value

        # Multiply all multiplicative values.
        for unit_upgrade in self.unit_upgrades:
            for stat_modifier in unit_upgrade.stat_modifiers:
                if (stat_modifier.stat == self.estat) and (stat_modifier.operation == EOperation.TIMES):
                    value *= stat_modifier.value

        # Set based on set values.
        for unit_upgrade in self.unit_upgrades:
            value = max(
                stat_modifier.value
                for stat_modifier in unit_upgrade.stat_modifiers
                if (stat_modifier.stat == self.estat) and (stat_modifier.operation == EOperation.ASSIGN)
            )

        # Bound value between min value and max value.
        return clamp(value, self.min_value, self.max_value)

    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return self.value == other

    def __lt__(self, other):
        try:
            return self.value < other.value
        except AttributeError:
            return self.value < other

    def on_turn_start(self):
        pass

    def on_level_start(self):
        pass


class ConsumableStat(Stat):
    def __init__(self, estat, unit_upgrades, refill_on_turn_start=False, refill_on_level_start=False, base_value=0, min_value=0, max_value=np.inf):
        self.refill_on_turn_start = refill_on_turn_start
        self.refill_on_level_start = refill_on_level_start

        self.current_value = None

        super().__init__(estat, unit_upgrades, base_value=base_value, min_value=min_value, max_value=max_value)

    def __add__(self, other: int) -> bool:
        needs_squeeze = self.current_value + other == clamp(self.current_value - other, self.min_value, self.max_value)
        self.current_value = clamp(self.current_value + other, self.min_value, self.max_value)
        return needs_squeeze

    def __sub__(self, other: int) -> bool:
        needs_squeeze = self.current_value - other == clamp(self.current_value - other, self.min_value, self.max_value)
        self.current_value = clamp(self.current_value - other, self.min_value, self.max_value)
        return needs_squeeze

    def on_turn_start(self):
        if self.refill_on_turn_start:
            self.current_value = self.max_value

    def on_level_start(self):
        if self.refill_on_level_start:
            self.current_value = self.max_value


@dataclass
class StatModifier(object):
    stat: EStat
    operation: EOperation
    value: int | float

    def __repr__(self):
        return f"StatModifier({self.stat} {self.operation} {self.value})"
