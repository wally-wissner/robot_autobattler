import numpy as np

from scripts.backend.inventory import Inventory
from scripts.backend.battleboard.topology.discrete_topology import Tile
from scripts.backend.unitstat import Stat, ConsumableStat
from scripts.backend.upgrades import UnitUpgrade
from scripts.utilities.enums import EStat


class Unit(object):
    def __init__(self, team):
        self.team = team

        self.level = 3
        self.unit_upgrades = Inventory()
        self.status_effects = Inventory()
        self.stats = {
            # Simple stats
            stat: Stat(estat=stat, unit_upgrades=self.unit_upgrades)
            for stat in [
                EStat.SIZE,
                EStat.MASS,
                EStat.POWER,
                EStat.ARMOR,
            ]
        } | {
            # Consumable stats
            EStat.BP: ConsumableStat(estat=EStat.BP, unit_upgrades=self.unit_upgrades),
            EStat.HP: ConsumableStat(estat=EStat.HP, unit_upgrades=self.unit_upgrades, refill_on_level_start=True),
            EStat.AP: ConsumableStat(estat=EStat.AP, unit_upgrades=self.unit_upgrades, refill_on_turn_start=True),
        }

        self._position = None

        # TODO: units that occupy more than one space
        # self.occupying = []

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

    def draw(self):
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

