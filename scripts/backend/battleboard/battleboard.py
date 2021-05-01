from typing import Iterable, Set, Union

from scripts.backend.battleboard.procedural_generation.procedural_generator import ProceduralGenerator
from scripts.backend.battleboard.procedural_generation.cellular_automaton import CellularAutomaton
from scripts.backend.battleboard.battle_tile import BattleTile
from scripts.backend.battleboard.topology.discrete_topology import Tile, Tiling
from scripts.utilities.singleton import Singleton


@Singleton
class BattleBoard(object):
    def __init__(self):
        self.tiling = None

    def field_of_view(self, tile: Tile, radius: int) -> Set[Tile]:
        # return {tile for tile in }
        # TODO
        pass

    def place_units(self):
        # TODO
        pass


    def generate(self, generator: ProceduralGenerator):
        self.tiling = {tile: BattleTile(position=tile, terrain=generator[tile]) for tile in generator}

    def __getitem__(self, tiles: Union[Tile, Iterable[Tile]]) -> Union[BattleTile, Iterable[BattleTile]]:
        if isinstance(tiles, Tile):
            return self.battle_tiles[tiles]
        if hasattr(tiles, "__iter__"):
            t = type(tiles)
            return t(self.battle_tiles[tile] for tile in tiles)
        else:
            raise TypeError("tiles must be of type Tile or be an iterable of Tiles.")
