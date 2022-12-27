import numpy as np

from pygame import Vector2
from scripts.backend.inventory import Inventory
from scripts.backend.unitstat import Stat, ConsumableStat
from scripts.backend.upgrades import UnitUpgrade
from scripts.utilities.enums import EStat
from scripts.utilities.identifiers import uuid_identifier


@uuid_identifier
class Unit(object):
    def __init__(self, team, level):
        self.team = team
        self.level = level
        self.alive = True

        self.unit_upgrades: list[UnitUpgrade] = []
        self.status_effects = Inventory()

        default_stats = {
            EStat.SIZE: Stat(estat=EStat.MASS, base_value=10),
            EStat.MASS: Stat(estat=EStat.MASS, base_value=10),
        }
        bonus_stats = {
            stat: Stat(estat=stat, base_value=0)
            for stat in [
                EStat.POWER,
                EStat.LASER_POWER,
                EStat.MISSILE_POWER,
                EStat.RAILGUN_POWER,
                EStat.ARMOR,
            ]
        }
        consumable_stats = {
            EStat.BP: ConsumableStat(estat=EStat.BP),
            EStat.HP: ConsumableStat(estat=EStat.HP, refill_on_level_start=True),
            EStat.AP: ConsumableStat(estat=EStat.AP, refill_on_turn_start=True),
        }
        self.stats = default_stats | bonus_stats | consumable_stats

        self._position = None

    def stat_modifiers(self, stat: EStat):
        stat_modifiers = []
        for unit_upgrade in self.unit_upgrades:
            for stat_modifier in unit_upgrade.badge.stat_modifiers:
                if stat_modifier.stat == stat:
                    stat_modifiers.append(stat_modifier)
        return stat_modifiers

    def take_damage(self, damage):
        self.stats[EStat.HP] -= damage
        if self.stats[EStat.HP].current_value <= 0:
            self.die()

    def die(self):
        self.alive = False

    def level_up_cost(self):
        return int(np.sqrt(self.level))

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, vector: Vector2):
        self._position = vector

    def add_unit_upgrade(self, unit_upgrade: UnitUpgrade):
        self.unit_upgrades.append(unit_upgrade)
