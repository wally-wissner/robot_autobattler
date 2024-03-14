import numpy as np
from pygame.math import Vector2

from src.backend.battleboard import Tile


class Hex(Tile):
    def __init__(self, coordinates):
        self.q, self.r, self.s = coordinates
        assert self.q + self.r + self.s == 0, "Invalid hex coordinates. q + r + s must equal zero."
        super().__init__(coordinates)

    def as_array(self):
        return np.array(self.coordinates)

    def __add__(self, other):
        return Hex(self.as_array() + other.as_array())

    def __sub__(self, other):
        return Hex(self.as_array() - other.as_array())

    def __mul__(self, other):
        return Hex(self.as_array() * other)

    def __lt__(self, other):
        return tuple(self.as_array()) < tuple(other.as_array())

    def distance(self, other):
        return abs(self.as_array() - other.as_array()).sum() / 2

    def direction(self, other):
        return (other - self) / self.distance(other)

    def cardinal_direction(self):
        distances = {direction: self.distance(direction) for direction in self.directions(include_zero=False)}
        print(distances)
        min_distance = min(distances.values())
        return tuple(sorted([distance for distance in distances if distances[distance] == min_distance]))

    def magnitude(self):
        return self.distance(self.zero())

    def disk(self, radius):
        return {
            self + Hex((q, r, -q-r))
            for q in range(-radius, radius + 1)
            for r in range(max(-radius, -q - radius), min(radius, -q + radius) + 1)
        }

    def round(self):
        rq = round(self.q)
        rr = round(self.r)
        rs = round(self.s)
        x_diff = abs(rq - self.q)
        y_diff = abs(rr - self.r)
        z_diff = abs(rs - self.s)
        if x_diff > y_diff and x_diff > z_diff:
            rq = -rr - rs
        elif y_diff > z_diff:
            rr = -rq - rs
        else:
            rs = -rq - rr
        return Hex((rq, rr, rs))

    def rotations(self):
        return {
            Hex((+self.q, +self.r, +self.s)),
            Hex((-self.q, -self.r, -self.s)),
            Hex((+self.r, +self.s, +self.q)),
            Hex((-self.r, -self.s, -self.q)),
            Hex((+self.s, +self.q, +self.r)),
            Hex((-self.s, -self.q, -self.r)),
        }

    @staticmethod
    def zero():
        return Hex((+0, +0, +0))

    @staticmethod
    def directions(include_zero):
        d = [
            Hex((+0, -1, +1)),
            Hex((+1, -1, +0)),
            Hex((+1, +0, -1)),
            Hex((+0, +1, -1)),
            Hex((-1, +1, +0)),
            Hex((-1, +0, +1)),
        ]
        if include_zero:
            return [Hex((+0, +0, +0))] + d
        else:
            return d

    def to_cartesian(self, tile_size, flat_top) -> Vector2:
        if flat_top:
            transformation = np.array([[3/2, 0], [np.sqrt(3)/2, np.sqrt(3)]])
        else:
            transformation = np.array([[np.sqrt(3), np.sqrt(3)/2], [0, 3/2]])
        qr = np.array([[self.q], [self.r]])
        point = Vector2((transformation @ qr * tile_size).reshape(-1).tolist())
        return point


if __name__ == "__main__":
    hex = Hex((2, 0, -2))
    print(hex)
    print(hex.cardinal_direction())
