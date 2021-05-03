from typing import Iterable, List, Set

from scripts.backend.battleboard.battleboard import BattleBoard
from scripts.backend.battleboard.topology.discrete_topology import Tile
from scripts.backend.unit.unit import Unit
from scripts.backend.unit.unitstat import EStat


class BaseWeapon(object):
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit

    def targetable_area(self) -> Set[Tile]:
        raise NotImplemented()

    def area_of_effect(self, tile:Tile) -> Iterable[Tile]:
        raise NotImplemented()

    def affected_units(self, tile:Tile) -> Iterable[Unit]:
        raise NotImplemented()

    def damage(self) -> int:
        raise NotImplemented()

    def costAP(self) -> int:
        raise NotImplemented()

    def fire(self, tile:Tile) -> None:
        raise NotImplemented()

    def try_fire(self, tile:Tile) -> bool:
        return self.unit.stats[EStat.AP] >= self.costAP()


class Laser(BaseWeapon):
    def __init__(self, unit):
        super().__init__(name="Laser", unit=unit)

    def targetable_area(self):
        return self.unit.visible_tiles()

    def area_of_effect(self, tile:Tile):
        return {tile}

    def affected_units(self, tile:Tile):

    def damage(self) -> int:


class Railgun(BaseWeapon):
    def __init__(self, unit):
        super().__init__(name="Laser", unit=unit)

    def targetable_area(self):
        return self.unit.visible_tiles()

    def area_of_effect(self, tile:Tile):
        return {tile}

    def affected_units(self, tile:Tile):

    def damage(self) -> int:


class Missile(BaseWeapon):
    def __init__(self, unit):
        super().__init__(name="Laser", unit=unit)

    def targetable_area(self):
        return self.unit.visible_tiles()

    def area_of_effect(self, tile:Tile):
        return BattleBoard.tiling.disk(tile=tile, radius=self.unit.stats[EStat.MissileRange])

    def affected_units(self, tile:Tile):

    def damage(self) -> int:



class SelfDestruct(BaseWeapon):
    def __init__(self, unit):
        super().__init__(name="Self Destruct", unit=unit)

    def targetable_area(self):
        return self.unit.position

    def area_of_effect(self, tile: Tile):
        return BattleBoard.tiling.disk(tile=self.unit.position, radius=self.unit.stats[EStat.SelfDestructRadius])

    def affected_units(self, tile: Tile):

    def damage(self) -> int:
