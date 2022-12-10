import numpy as np
from pygame.math import Vector2

from scripts.backend.battleboard.topology.discrete_topology import Tiling, Tile
from scripts.backend.battleboard.topology.hex_tile import Hex


class FlatHexTiling(Tiling):
    def __init__(self, board_radius: int, tile_size: float | int, flat_top: bool):
        super().__init__(tile_size=tile_size)

        self.board_radius = board_radius
        self.flat_top = flat_top

        self.tiles = Hex.zero().disk(radius=self.board_radius)
        self._mirror_centers = Hex((2 * self.board_radius + 1, -self.board_radius, -self.board_radius - 1)).rotations()

    def neighbors(self, tile: Hex) -> set[Hex]:
        return {tile + direction for direction in Hex.directions(include_zero=False)}

    def distance(self, start: Hex, end: Hex):
        return start.distance(end)

    def disk(self, tile, radius) -> set[Hex]:
        return tile.disk(radius)

    def lerp(self, start, end, t) -> Hex:
        return start * (1 - t) + end * t


    # def line(self, start, end, modulo=True):
    #     start_center = self.nearest_center(start)
    #     end_center = self.nearest_center(end)
    #     start - start_center
    #     end - end_center
    #     # todo
    #
    #     distance = self.distance(start, )
    #
    #     [self.modulo(start + tile) for tile in line(self.nearest_center(end - start))]
    #
    #
    #     hexs = [self.round(self.lerp(start, end, 1.0/distance * i)) for i in range(distance+1)]
    #
    #     if modulo:
    #         hexs = [self.modulo(hex) for hex in hexs]
    #
    #     return hexs
    #
    #     """
    #     function cube_linedraw(a, b):
    #         var N = cube_distance(a, b)
    #         var results = []
    #         for each 0 ≤ i ≤ N:
    #             results.append(cube_round(cube_lerp(a, b, 1.0/N * i)))
    #         return results
    #     """
    #
    # def line_covering(self, start, end, modulo=True):
    #     # todo
    #     # https://www.shadertoy.com/view/XdSyzK
    #     # https://stackoverflow.com/questions/3233522/elegant-clean-special-case-straight-line-grid-traversal-algorithm
    #     # https://playtechs.blogspot.com/2007/03/raytracing-on-grid.html
    #     raise NotImplemented()

    def __repr__(self):
        return f"{self.__class__.__name__}(n_tiles={len(self.tiles)})"

    def from_cartesian(self, point: Vector2) -> Hex:
        if self.flat_top:
            transformation = np.array([[2/3, 0], [-1/3, np.sqrt(3)/3]])
        else:
            transformation = np.array([[np.sqrt(3)/3, -1/3], [0, 2/3]])

        point = np.array(point).reshape(-1)
        q, r = transformation @ point / self.tile_size

        return Hex((q, r, -q-r))

    def to_cartesian(self, tile) -> Vector2:
        return tile.to_cartesian(self.tile_size, self.flat_top)


if __name__ == "__main__":
    print(Hex((-2, 1, 1)))
    print(Hex((-2, 1, 1)) == Hex((-2, 1, 1)))
    print(Hex((-2., 1., 1.)) == Hex((-2., 1., 1.)))
    b = FlatHexTiling(board_radius=6, tile_size=1)
    print(b)
    print([i for i in b])
    print(b.neighbors(Hex((5, -2, -3))))
    print(b.from_cartesian(Vector2(2.5, 6)))
    print(b.to_cartesian(Hex((3, 4, -7))))
