import math
from typing import Iterable, Self

from pydantic import BaseModel
from pygame import Rect
from pyglet.math import Vec2


class Vector2(BaseModel):
    x: float = 0
    y: float = 0

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other: Self):
        return self.x, self.y == other.x, other.y

    def __add__(self, other: Self) -> Self:
        return Vector2(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return Vector2(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, other: float) -> Self:
        return Vector2(x=self.x * other, y=self.y * other)

    def __rmul__(self, other: float) -> Self:
        return self * other

    def __truediv__(self, other: float) -> Self:
        return Vector2(x=self.x / other, y=self.y / other)

    def __round__(self, n: int = None) -> Self:
        return Vector2(x=round(self.x, n), y=round(self.y, n))

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def at_resolution(self, resolution: tuple[int, int]) -> Self:
        return Vector2(x=self.x * resolution[0], y=self.y * resolution[1])

    def to_vec2(self):
        return Vec2(self.x, self.y)


class Rectangle(BaseModel):
    x_min: float = 0
    x_max: float = 0
    y_min: float = 0
    y_max: float = 0

    @classmethod
    def from_points(cls, points: Iterable[Vector2]) -> Self:
        return Rectangle(
            x_min=min(point.x for point in points),
            x_max=max(point.x for point in points),
            y_min=min(point.y for point in points),
            y_max=max(point.y for point in points),
        )

    @property
    def bottom_left(self) -> Vector2:
        return Vector2(x=self.x_min, y=self.y_min)

    @property
    def top_right(self) -> Vector2:
        return Vector2(x=self.x_max, y=self.y_max)

    def center(self) -> Vector2:
        return Vector2(x=(self.x_min + self.x_max) / 2, y=(self.y_min + self.y_max) / 2)

    def points(self) -> tuple[Vector2, Vector2]:
        return self.bottom_left, self.top_right

    def width(self) -> float:
        return self.x_max - self.x_min

    def height(self) -> float:
        return self.y_max - self.y_min

    def size(self) -> tuple[float, float]:
        return self.width(), self.height()

    def position(self) -> tuple[float, float]:
        return self.x_min, self.y_max

    def pad(self, x_padding: float = 0, y_padding: float = 0) -> Self:
        return Rectangle(
            x_min=self.x_min - x_padding,
            x_max=self.x_max + x_padding,
            y_min=self.y_min - y_padding,
            y_max=self.y_max + y_padding,
        )

    def __add__(self, other: Vector2) -> Self:
        return Rectangle.from_points((point + other for point in self.points()))

    def __sub__(self, other: Vector2) -> Self:
        return Rectangle.from_points((point - other for point in self.points()))

    def __mul__(self, other: float) -> Self:
        return Rectangle.from_points(
            ((point - self.center()) * other + self.center() for point in self.points())
        )

    def __rmul__(self, other: float) -> Self:
        return self * other

    def __truediv__(self, other: float) -> Self:
        return Rectangle.from_points(
            ((point - self.center()) / other + self.center() for point in self.points())
        )

    def at_resolution(self, resolution: tuple[int, int]) -> Self:
        return Rectangle.from_points(
            [point.at_resolution(resolution) for point in self.points()]
        )

    def to_pygame(self) -> Rect:
        return Rect(self.position(), self.size())
