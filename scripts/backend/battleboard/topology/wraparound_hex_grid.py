import numpy as np
from pygame.math import Vector2
from typing import Iterable, Set, Union

from scripts.backend.battleboard.topology.discrete_topology import Tiling, Tile
from scripts.backend.battleboard.topology.hex_tile import Hex


class TwistedTorusHexTiling(Tiling):
    def __init__(self, board_radius: int, tile_size: Union[float, int], flat_top: bool = True):
        super().__init__(tile_size=tile_size)

        self.board_radius = board_radius
        self.flat_top = flat_top

        self.tiles = Hex.zero().disk(radius=self.board_radius)
        self._mirror_centers = Hex((2 * self.board_radius + 1, -self.board_radius, -self.board_radius - 1)).rotations()

    def _mirrors(self, tile: Hex) -> Set[Hex]:
        return {tile + center for center in self._mirror_centers}

    def neighbors(self, tile: Hex) -> Set[Hex]:
        return {self.modulo(tile + direction) for direction in Hex.directions(include_zero=False)}

    def distance(self, start: Hex, end: Hex):
        distance = min(
            start_mirror.distance(end_mirror)
            for start_mirror in self._mirrors(start)
            for end_mirror in self._mirrors(end)
        )
        return distance

    def nearest_center(self, tile: Hex) -> Hex:
        return min([center for center in self._mirror_centers], key=lambda x: x.distance(tile))

    def modulo(self, tile: Hex) -> Hex:
        return tile - self.nearest_center(tile)

    def disk(self, tile: Hex, radius: int) -> Set[Hex]:
        return {self.modulo(hex) for hex in tile.disk(radius)}

    def lerp(self, start, end, t, modulo=True) -> Hex:
        hex = start * (1 - t) + end * t
        return self.modulo(hex) if modulo else hex

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
        return f"{self.__class__.__name__}(board_radius={self.board_radius})"

    def round(self, tile: Hex, modulo=True) -> Hex:
        rq = round(tile.q)
        rr = round(tile.r)
        rs = round(tile.s)

        x_diff = abs(rq - tile.q)
        y_diff = abs(rr - tile.r)
        z_diff = abs(rs - tile.s)

        if x_diff > y_diff and x_diff > z_diff:
            rq = -rr - rs
        elif y_diff > z_diff:
            rr = -rq - rs
        else:
            rs = -rq - rr

        hex = Hex((rq, rr, rs))

        return self.modulo(hex) if modulo else hex

    def from_cartesian(self, point: Vector2) -> Hex:
        if self.flat_top:
            transformation = np.array([[2/3, 0], [-1/3, np.sqrt(3)/3]])
        else:
            transformation = np.array([[np.sqrt(3)/3, -1/3], [0, 2/3]])

        point = np.array(point).reshape(-1)
        q, r = transformation @ point / self.tile_size

        hex = Hex((q, r, -q-r))

        return hex

    def to_cartesian(self, tile: Hex) -> Vector2:
        if self.flat_top:
            transformation = np.array([[3/2, 0], [np.sqrt(3)/2, np.sqrt(3)]])
        else:
            transformation = np.array([[np.sqrt(3), np.sqrt(3)/2], [0, 3/2]])

        qr = np.array([[tile.q], [tile.r]])
        point = Vector2((transformation @ qr * self.tile_size).reshape(-1).tolist())

        return point


if __name__ == "__main__":
    print(Hex((-2, 1, 1)))
    print(Hex((-2, 1, 1)) == Hex((-2, 1, 1)))
    print(Hex((-2., 1., 1.)) == Hex((-2., 1., 1.)))
    b = TwistedTorusHexTiling(board_radius=6, tile_size=1)
    print(b)
    print([i for i in b])
    print(b.neighbors(Hex((5, -2, -3))))
    print(b.from_cartesian(Vector2(2.5, 6)))
    print(b.to_cartesian(Hex((3, 4, -7))))
