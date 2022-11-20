import numpy as np
from functools import total_ordering

from scripts.utilities.enums import EStat
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
                if (stat_modifier.stat == self.estat) and (stat_modifier.type == "+"):
                    value += stat_modifier.value

        # Multiply all multiplicative values.
        for unit_upgrade in self.unit_upgrades:
            for stat_modifier in unit_upgrade.stat_modifiers:
                if (stat_modifier.stat == self.estat) and (stat_modifier.type == "*"):
                    value *= stat_modifier.value

        # Set based on set values.
        for unit_upgrade in self.unit_upgrades:
            value = max(
                stat_modifier.value
                for stat_modifier in unit_upgrade.stat_modifiers
                if (stat_modifier.stat == self.estat) and (stat_modifier.type == "=")
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
    def __init__(self, estat, unit_upgrades, turn_start_state=None, level_start_state=None, base_value=0, min_value=0, max_value=np.inf):
        assert turn_start_state in ["empty", "full", None]
        self.turn_start_state = turn_start_state

        assert level_start_state in ["empty", "full", None]
        self.level_start_state = level_start_state

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
        if self.turn_start_state == "empty":
            self.current_value = self.min_value
        if self.turn_start_state == "full":
            self.current_value = self.max_value

    def on_level_start(self):
        if self.level_start_state == "empty":
            self.current_value = self.min_value
        if self.level_start_state == "full":
            self.current_value = self.max_value


class StatModifier(object):
    def __init__(self, stat, quantity, operation):
        operations = ["+", "*", "="]
        if operation not in operations:
            raise ValueError(f"Modifier type must be in {operations}.")

        self.stat = stat
        self.quantity = quantity
        self.type = operation

    def __repr__(self):
        return f"StatModifier({self.stat} {self.type} {self.quantity})"


class UnitUpgrade(object):
    def __init__(self, name, rarity, description, stat_modifiers):
        self.name = name
        self.rarity = rarity
        self.description = description
        self.stat_modifiers = stat_modifiers

    def drop_rate(self):
        rates = {
            "common": .1,
            "uncommon": .05,
            "rare": .025,
            "mythic": .0125,
        }
        return rates[self.rarity]

    def draw(self):
        # TODO
        raise NotImplemented()
