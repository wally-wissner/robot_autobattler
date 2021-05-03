from typing import Iterable, Set, Union

from scripts.backend.battleboard.procedural_generation.procedural_generator import ProceduralGenerator
from scripts.backend.battleboard.battle_tile import BattleTile
from scripts.backend.battleboard.topology.discrete_topology import Tile, Tiling
from scripts.utilities.singleton import Singleton


@Singleton
class BattleBoard(object):
    def __init__(self, tiling: Tiling, generator: ProceduralGenerator):
        self.tiling = tiling
        self.generator = generator
        self.battle_tiles = None

    def place_units(self) -> None:
        # TODO
        pass

    def visible_tiles(self, tile: Tile, radius: int):
        return {
            t
            for t in self.tiling.disk(tile, radius)
            if
        }

    def generate(self, *args, **kwargs) -> None:
        self.generator.generate(*args, **kwargs)
        self.battle_tiles = {tile: BattleTile(position=tile, terrain=self.generator[tile]) for tile in self.tiling}

    def __getitem__(self, tiles: Union[Tile, Iterable[Tile]]) -> Union[BattleTile, Iterable[BattleTile]]:
        if isinstance(tiles, Tile):
            return self.battle_tiles[tiles]
        elif hasattr(tiles, "__iter__"):
            t = type(tiles)
            return t(self.battle_tiles[tile] for tile in tiles)
        else:
            raise TypeError("Argument `tiles` must be of type Tile or be an iterable of type Tile.")
