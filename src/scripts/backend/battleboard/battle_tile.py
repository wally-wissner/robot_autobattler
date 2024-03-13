from enum import Enum

from src.scripts.frontend import colors
from src.src.scripts.backend.battleboard import BattleBoard
from src.src.scripts.backend.battleboard import Tile


class ETerrain(Enum):
    Ground = 0
    Wall = 1


debug_colors = {
    ETerrain.Ground: colors.LIGHT_BROWN,
    ETerrain.Wall: colors.DARK_BROWN,
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


if __name__ == "__main__":
    bt = BattleTile(position=Tile([0, 1]), terrain=ETerrain.Ground)
    print(bt)
