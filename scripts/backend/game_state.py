from dataclasses import dataclass
from typing import List

from scripts.backend.team import Team
from scripts.backend.unit import Unit
from scripts.utilities.enums import EOperation, EStat
from scripts.utilities.game_math import clamp


@dataclass
class GameState(object):
    version: str
    teams: List[Team]

    def unit_stat_value(self, unit: Unit, stat: EStat) -> float:
        # Initialize value to base value.
        value = unit.stats[stat].base_value
        # Split stat modifiers by operation.
        stat_modifiers = {operation: [] for operation in EOperation}
        for unit_upgrade in unit.unit_upgrades:
            for stat_modifier in unit_upgrade:
                if stat_modifier.stat == stat:
                    stat_modifiers[stat_modifier.operation].append(stat_modifier)
        # Apply appropriate operation from each stat modifier.
        for stat_modifier in stat_modifiers[EOperation.PLUS]:
            value += stat_modifier.value
        for stat_modifier in stat_modifiers[EOperation.TIMES]:
            value *= stat_modifier.value
        if stat_modifiers[EOperation.ASSIGN]:
            value = max(stat_modifier.value for stat_modifier in stat_modifiers[EOperation.ASSIGN])
        # Bound value between min value and max value.
        return clamp(value, unit.stats[stat].min_value, unit.stats[stat].max_value)
