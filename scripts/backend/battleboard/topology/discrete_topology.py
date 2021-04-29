from typing import Iterable, Set, Union
from pygame.math import Vector2


class Tile(object):
    def __init__(self, coordinates):
        self.coordinates = tuple(i for i in coordinates)
        self.hashable = all(isinstance(i, int) for i in coordinates)

    def __repr__(self):
        return f"{self.__class__.__name__}{self.coordinates}"

    __str__ = __repr__

    def __eq__(self, other):
        return all(i == j for i, j in zip(self.coordinates, other.coordinates))

    def __hash__(self):
        return hash(str(self))


class Tiling(object):
    def __init__(self, tile_size: Union[float, int], *args, **kwargs):
        self.tile_size = tile_size
        self.tiles = None

    def __iter__(self):
        return (i for i in self.tiles)

    def generate(self, *args, **kwargs):
        raise NotImplemented()

    def distance(self, start: Tile, end: Tile) -> Union[int, float]:
        raise NotImplemented()

    def from_cartesian(self, point) -> Tile:
        raise NotImplemented()

    def to_cartesian(self, tile) -> Vector2:
        raise NotImplemented()

    def neighbors(self, tile) -> Set[Tile]:
        raise NotImplemented()

