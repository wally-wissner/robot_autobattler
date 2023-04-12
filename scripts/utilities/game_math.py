import math
from dataclasses import astuple, dataclass


def clamp(value, min_value, max_value):
    assert min_value <= max_value, "min_value must be less than or equal to max_value."
    return sorted([value, min_value, max_value])[1]


def can_shift(items: list, index: int, shift=1) -> bool:
    return (0 <= index < len(items)) and (0 <= index + shift < len(items))


def shift_item(items: list, index: int, shift=1) -> None:
    if can_shift(items, index, shift):
        item = items.pop(index)
        items.insert(index + shift, item)


@dataclass
class Vector2:
    x: float = 0
    y: float = 0

    def __iter__(self):
        return iter(astuple(self))

    def __eq__(self, other):
        return self.x, self.y == other.x, other.y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __round__(self, n=None):
        return Vector2(round(self.x, n), round(self.y, n))

    def magnitude(self):
        math.sqrt(self.x**2 + self.y**2)

