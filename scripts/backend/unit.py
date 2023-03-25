import numpy as np

from scripts.backend.inventory import Inventory
from scripts.backend.physics import DiscBody
from scripts.backend.unitstat import Stat, ConsumableStat
from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.utilities.enums import EStat
from scripts.utilities.identifiers import uuid_identifier


@uuid_identifier
class Unit(DiscBody):
    def __init__(self, team, level):
        self.level = level
        self.alive = True

        self.unit_upgrades: list[UnitUpgrade] = []
        self.status_effects = Inventory()

        default_stats = {
            EStat.SIZE: Stat(base_value=10),
            EStat.MASS: Stat(base_value=10),
        }
        bonus_stats = {
            stat: Stat(base_value=0)
            for stat in [
                EStat.POWER,
                EStat.LASER_POWER,
                EStat.MISSILE_POWER,
                EStat.RAILGUN_POWER,
                EStat.ARMOR,
            ]
        }
        consumable_stats = {
            EStat.HP: ConsumableStat(refill_on_encounter_start=True),
            EStat.AP: ConsumableStat(refill_on_turn_start=True),
        }
        self.stats = default_stats | bonus_stats | consumable_stats

        super().__init__(team=team)

    def stat_modifiers(self, stat: EStat):
        stat_modifiers = []
        for unit_upgrade in self.unit_upgrades:
            for stat_modifier in unit_upgrade.badge.stat_modifiers:
                if stat_modifier.stat == stat:
                    stat_modifiers.append(stat_modifier)
        return stat_modifiers

    def bp_used(self):
        return sum(unit_upgrade.bp for unit_upgrade in self.unit_upgrades)

    def bp_available(self):
        return self.level - self.bp_used()

    def take_damage(self, damage):
        self.stats[EStat.HP] -= damage
        if self.stats[EStat.HP].current_value <= 0:
            self.die()

    def die(self):
        self.alive = False

    def level_up_cost(self):
        return int(np.sqrt(self.level))

    def add_unit_upgrade(self, unit_upgrade: UnitUpgrade):
        self.unit_upgrades.append(unit_upgrade)

    def color(self) -> tuple[int]:
        return tuple(int(hash(self.id) // 10 ** (3 * i) % 256) for i in range(3))
