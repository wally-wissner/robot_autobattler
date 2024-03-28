import math
from typing import Iterable, Self

# import pygame as pg
from pyglet.math import Vec2


class Vector2(Vec2):
    def __init__(self, *args, relative=False) -> None:
        self.relative = relative
        if len(args) == 0:
            x, y = 0, 0
        elif len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        else:
            raise ValueError("Vector2 does not accept more than two arguments.")
        super().__init__(x, y)

    def as_tuple(self) -> tuple:
        return self.x, self.y

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __iter__(self):
        return iter(self.as_tuple())

    def __eq__(self, other: Self):
        other = Vector2(other)
        return self.x, self.y == other.x, other.y

    def __add__(self, other: Self):
        other = Vector2(other)
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self):
        other = Vector2(other)
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other: float):
        return self * other

    def __truediv__(self, other: float):
        return Vector2(self.x / other, self.y / other)

    def __round__(self, n: int = None):
        return Vector2(round(self.x, n), round(self.y, n))

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"


class Rectangle:
    # pylint: disable=too-many-instance-attributes

    def __init__(self, points: Iterable[Vector2]) -> None:
        self.x_min: float = min(point.x for point in points)
        self.x_max: float = max(point.x for point in points)
        self.y_min: float = min(point.y for point in points)
        self.y_max: float = max(point.y for point in points)

        self.bottom_left: Vector2 = Vector2(self.x_min, self.y_min)
        self.top_left: Vector2 = Vector2(self.x_min, self.y_max)
        self.bottom_right: Vector2 = Vector2(self.x_max, self.y_min)
        self.top_right: Vector2 = Vector2(self.x_max, self.y_max)

        self.width: float = self.x_max - self.x_min
        self.height: float = self.y_max - self.y_min

        self.center: Vector2 = Vector2(
            (self.x_min + self.x_max) / 2, (self.y_min + self.y_max) / 2
        )

    # def pad(self, aspect_ratio: float = None, fraction: float = 0) -> Self:
    #     if aspect_ratio:
    #
    #     return self

    # def to_pygame(self) -> tuple[pg.Vector2, tuple]:
    #     return pg.Vector2(self.x_min, self.y_max), (self.width, self.height)
