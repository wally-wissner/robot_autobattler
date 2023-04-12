import math


def clamp(value, min_value, max_value):
    assert min_value <= max_value, "min_value must be less than or equal to max_value."
    return sorted([value, min_value, max_value])[1]


def can_shift(items: list, index: int, shift=1) -> bool:
    return (0 <= index < len(items)) and (0 <= index + shift < len(items))


def shift_item(items: list, index: int, shift=1) -> None:
    if can_shift(items, index, shift):
        item = items.pop(index)
        items.insert(index + shift, item)


class Vector2:
    def __init__(self, *args, **kwargs):
        if not args and not kwargs:
            self.x, self.y = 0, 0
        if len(args) == 1:
            self.x, self.y = args[0]
        if len(args) == 2:
            self.x, self.y = args
        if kwargs:
            self.x, self.y = kwargs["x"], kwargs["y"]

    def as_tuple(self):
        return self.x, self.y

    def __iter__(self):
        return iter(self.as_tuple())

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
        return math.sqrt(self.x**2 + self.y**2)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"
