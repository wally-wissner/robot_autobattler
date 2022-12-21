import numpy as np

from scripts.backend.inventory import Inventory
from scripts.backend.battleboard.topology.discrete_topology import Tile
from scripts.backend.unitstat import Stat, ConsumableStat
from scripts.backend.upgrades import UnitUpgrade
from scripts.utilities.enums import EStat
from scripts.utilities.identifiers import uuid_identifier


@uuid_identifier
class Unit(object):
    def __init__(self, team):
        self.team = team

        self.level = 3
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

        # TODO: units that occupy more than one space
        # self.occupying = []

    def stat_modifiers(self, stat: EStat):
        stat_modifiers = []
        for unit_upgrade in self.unit_upgrades:
            for stat_modifier in unit_upgrade:
                if stat_modifier.stat == stat:
                    stat_modifiers.append(stat_modifier)
        return stat_modifiers

    def attack(self, target: Tile):
        # TODO
        pass

    # def defend(self, attacker, weapon):
    #     if self.stats[EStat.SHIELD_CHARGES].current_value > 0:
    #         self.stats[EStat.SHIELD_CHARGES] -= 1
    #     else:
    #         damage =
    #         # Attacks which land deal at least 1 damage.
    #         damage = max(damage, 1)
    #         self.take_damage(damage)

    def take_damage(self, damage):
        self.stats[EStat.HP] -= damage
        if self.stats[EStat.HP].current_value <= 0:
            self.die()

    def die(self):
        # TODO
        pass

    def change_active_weapon(self, weapon):
        # TODO
        pass

    def level_up_cost(self):
        return int(np.sqrt(self.level))

    def move_to_adjacent(self, tile: Tile):
        # TODO
        pass

    def move_along_path(self, tile: Tile):
        # TODO
        pass

    def drop_loot(self):
        # TODO
        pass

    @property
    def position(self) -> Tile:
        return self._position

    @position.setter
    def position(self, tile: Tile):
        self._position = tile

    def on_turn_end(self):
        for stat in self.stats:
            # TODO
            # self.stats[stat].
            pass

    def attach_unit_upgrade(self, unit_upgrade: UnitUpgrade):
        self.unit_upgrades.add(unit_upgrade, 1)

    def on_turn_start(self):
        for stat in self.stats:
            self.stats[stat].on_turn_start()

    def on_level_start(self):
        for stat in self.stats:
            self.stats[stat].on_level_start()
