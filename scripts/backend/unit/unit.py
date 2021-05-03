import numpy as np

from scripts.backend.inventory import Inventory
from scripts.backend.battleboard.battleboard import BattleBoard
from scripts.backend.battleboard.topology.discrete_topology import Tile, Tiling
from scripts.backend.unit.unitstat import EStat, Stat, ConsumableStat, UnitUpgrade
from scripts.backend.unit.weapon import Laser, Missile, Railgun, BaseWeapon


class Unit(object):
    def __init__(self, team):
        self.team = team

        self.weapons =

        self.level = 3
        self.unit_upgrades = Inventory()
        self.staus_effects = Inventory()
        self.stats = {
            EStat.Attack: Stat(estat=EStat.Attack, unit_upgrades=self.unit_upgrades),
            EStat.Armor: Stat(estat=EStat.Armor, unit_upgrades=self.unit_upgrades),
            EStat.VisionDistance: Stat(estat=EStat.VisionRadius, unit_upgrades=self.unit_upgrades),
            EStat.AP: ConsumableStat(estat=EStat.AP, unit_upgrades=self.unit_upgrades, turn_start_state="full"),
            EStat.BP: ConsumableStat(estat=EStat.BP, unit_upgrades=self.unit_upgrades),
            EStat.HP: ConsumableStat(estat=EStat.HP, unit_upgrades=self.unit_upgrades, level_start_state="full"),
        }


        self._position = None

        # TODO: units that occupy more than one space
        # self.occupying = []


    def attack(self, target:Tile):
        # TODO


    def defend(self, attacker, weapon):
        if self.stats[EStat.Shields] > 0:
            self.stats[EStat.Shields] -= 1
        else:
            # Attacks deal at least 1 damage.
            damage = max(damage, 1)
            self.take_damage(damage)

    def take_damage(self, damage):
        self.stats[EStat.HP] -= damage
        if self.stats[EStat.HP] == 0:
            self.die()

    def die(self):
        # TODO

    def change_active_weapon(self, weapon):
        # TODO

    def level_up_cost(self):
        return int(np.sqrt(self.level))


    def move_to_adjacent(self, tile:Tile):
        # TODO

    def move_along_path(self, tile:Tile):
        # TODO

    def draw(self):
        # TODO

    def drop_loot(self):
        # TODO

    def visible_tiles(self):
        return BattleBoard.tiling.visible_tiles(self.position, self.stats[EStat.VisionRadius])

    @property
    def position(self) -> Tile:
        return self._position

    @position.setter
    def position(self, tile:Tile):
        self._position = tile

    def on_turn_end(self):
        for stat in self.stats:
            self.stats[stat].

    def attach_unit_upgrade(self, unit_upgrade: UnitUpgrade):
        self.unit_upgrades.add(unit_upgrade, 1)

    def on_turn_start(self):
        for stat in self.stats:
            self.stats[stat].on_turn_start()


    def on_level_start(self):
        for stat in self.stats:
            self.stats[stat].on_level_start()

