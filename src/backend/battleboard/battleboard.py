from typing import Iterable

from src.backend.battleboard import ProceduralGenerator
from src.backend.battleboard import BattleTile
from src.backend.battleboard import Tile, Tiling
from src.backend.unit import Unit


class BattleBoard(object):
    def __init__(self, tiling: Tiling, generator: ProceduralGenerator):
        self.tiling = tiling
        self.generator = generator
        self._battle_tiles = None
        self._units = None

    def place_units(self) -> None:
        # TODO
        pass

    def visible_from(self, start: Tile, end: Tile) -> bool:
        # TODO
        pass

    def visible_tiles(self, tile: Tile, radius: int, method):
        assert method in ["disk", "line_of_sight", "directional"]

        if method == "disk":
            return self.tiling.disk(tile, radius)

        if method == "line_of_sight":
            return {other for other in self.tiling.disk(tile, radius) if self.visible_from(tile, other)}

        if method == "directional":
            # TODO
            raise NotImplemented()

        raise NotImplemented()

    def generate(self, *args, **kwargs) -> None:
        self.generator.generate(*args, **kwargs)
        self._battle_tiles = {tile: BattleTile(position=tile, terrain=self.generator[tile]) for tile in self.tiling}

    def units(self, tiles: Tile | Iterable[Tile]) -> Unit | Iterable[Unit]:
        if isinstance(tiles, Tile):
            return self._units[tiles]
        elif hasattr(tiles, "__iter__"):
            t = type(tiles)
            return t(self._units[tile] for tile in tiles)
        else:
            raise TypeError("Argument `tiles` must be of type Tile or be an iterable of type Tile.")

    def battle_tiles(self, tiles: Tile | Iterable[Tile]) -> BattleTile | Iterable[BattleTile]:
        if isinstance(tiles, Tile):
            return self._battle_tiles[tiles]
        elif hasattr(tiles, "__iter__"):
            t = type(tiles)
            return t(self._battle_tiles[tile] for tile in tiles)
        else:
            raise TypeError("Argument `tiles` must be of type Tile or be an iterable of type Tile.")
