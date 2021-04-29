from enum import Enum

from scripts.frontend import colors
from scripts.backend.battleboard.battleboard import BattleBoard
from scripts.backend.battleboard.topology.discrete_topology import Tile


class ETerrain(Enum):
    Ground = 0
    Wall = 1


debug_colors = {
    ETerrain.Ground: colors.light_brown,
    ETerrain.Wall: colors.dark_brown,
}


class BattleTile(object):
    def __init__(self, position:Tile, terrain:ETerrain):
        self.position = position
        self.terrain = terrain
        self.units = []
        self.viewed_by = {}
        self.visible_by = {}

    def occupiable(self):
        return self.terrain == ETerrain.Ground

    def occupied(self):
        return len(BattleBoard.instance().units[self.position]) > 0

    def visible(self, team):
        return len({unit for unit in self.visible_by if unit.team == team}) > 0

    def __repr__(self):
        return f"BattleTile(position={self.position}, terrain={self.terrain})"


    def debug_color(self):
        return debug_colors[self.terrain]
