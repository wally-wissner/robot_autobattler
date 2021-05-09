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

    def area_of_effect(self, target: Tile) -> Iterable[Tile]:
        raise NotImplemented()

    def affected_units(self, target: Tile) -> Iterable[Unit]:
        raise NotImplemented()

    def damage(self) -> int:
        raise NotImplemented()

    def costAP(self) -> int:
        raise NotImplemented()

    def fire(self, target: Tile) -> None:
        raise NotImplemented()

    def try_fire(self, target: Tile) -> bool:
        can_fire = (self.unit.stats[EStat.AP] >= self.costAP()) and (target in self.targetable_area())
        self.fire(target)
        return can_fire

class Laser(BaseWeapon):
    def __init__(self, unit):
        super().__init__(name="Laser", unit=unit)

    def targetable_area(self):
        return self.unit.visible_tiles()

    def area_of_effect(self, target:Tile):
        return {target}

    def affected_units(self, target:Tile):
        ordered_units =
        if self.unit.stats[EStat.LaserPenetration] > 0:
            return ordered_units
        else:
            return ordered_units[0]

    def damage(self) -> int:
        return self.unit.stats[EStat.BasePower] + self.unit.stats[EStat.LaserPower]


class Railgun(BaseWeapon):
    def __init__(self, unit):
        super().__init__(name="Railgun", unit=unit)

    def targetable_area(self):
        return self.unit.visible_tiles()

    def area_of_effect(self, target:Tile):
        return {target}

    def affected_units(self, target: Tile):
        return {target}

    def damage(self) -> int:
        return self.unit.stats[EStat.BasePower] + self.unit.stats[EStat.RailgunPower]


class Missile(BaseWeapon):
    def __init__(self, unit):
        super().__init__(name="Missile", unit=unit)

    def targetable_area(self):
        return self.unit.visible_tiles()

    def area_of_effect(self, target: Tile):
        return BattleBoard.instance().tiling.disk(tile=target, radius=self.unit.stats[EStat.MissileRange])

    def affected_units(self, target: Tile):
        return BattleBoard.instance().tiling.disk(tile=target, radius=self.unit.stats[EStat.MissileAOERadius])

    def damage(self) -> int:
        return self.unit.stats[EStat.BasePower] + self.unit.stats[EStat.MissilePower]



class SelfDestruct(BaseWeapon):
    def __init__(self, unit):
        super().__init__(name="Self-Destruct", unit=unit)

    def targetable_area(self):
        return self.unit.position

    def area_of_effect(self, target: Tile):
        return BattleBoard.instance().tiling.disk(tile=self.unit.position, radius=self.unit.stats[EStat.SelfDestructAEORadius])

    def affected_units(self, target: Tile):
        return BattleBoard.instance().tiling.disk(tile=target, radius=self.unit.stats[EStat.SelfDestructAEORadius])

    def damage(self) -> int:
        return self.unit.stats[EStat.BasePower] + self.unit.stats[EStat.SelfDestructPower]
