import math
from pyglet.math import Vec2
from typing import Self


def clamp(value, min_value, max_value):
    assert min_value <= max_value, "min_value must be less than or equal to max_value."
    return sorted([value, min_value, max_value])[1]


def can_shift(items: list, index: int, shift=1) -> bool:
    return (0 <= index < len(items)) and (0 <= index + shift < len(items))


def shift_item(items: list, index: int, shift=1) -> None:
    if can_shift(items, index, shift):
        item = items.pop(index)
        items.insert(index + shift, item)


class Vector2(Vec2):
    def __init__(self, *args, **kwargs):
        self.x, self.y = None, None
        if not args and not kwargs:
            x, y = 0, 0
        elif len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        else:
            x, y = kwargs["x"], kwargs["y"]
        super().__init__(x, y)

    def as_tuple(self) -> tuple:
        return self.x, self.y

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __iter__(self):
        return iter(self.as_tuple())

    def __eq__(self, other: Self):
        return self.x, self.y == other.x, other.y

    def __add__(self, other: Self):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self):
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
