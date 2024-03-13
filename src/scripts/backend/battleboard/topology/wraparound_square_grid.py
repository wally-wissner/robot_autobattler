from src.src.scripts.backend.battleboard import Tiling, Tile


class Square(Tile):
    def __init__(self, iterable):
        assert all(isinstance(i, int) for i in iterable)
        self.x, self.y = iterable

    def __add__(self, other):
        return Square([self.x + other.x, self.y + other.y])

    def __sub__(self, other):
        return Square([self.x - other.x, self.y - other.y])

    def __mul__(self, other):
        return Square([self.x * other, self.y * other])

    def __hash__(self):
        return hash(str(self))


class SquareTopology(Tiling):
    def __init__(self, width, height, square_size):
        self.width = width
        self.height = height
        self.square_size = square_size
        self.spaces = {Square((i, j)) for i in range(self.width) for j in range(self.height)}

    def __iter__(self):
        return (i for i in self.spaces)

    zero = Square((0, 0))
    up = Square((0, 1))
    down = Square((0, -1))
    left = Square((-1, 0))
    right = Square((1, 0))
    cardinal_directions = [up, down, left, right]
    intercardinal_directions = [up + left, up + right, down + left, down + right]

    metrics = {
        "L1": None,
        "L2": None,
    }

    def mirrors(self, space):
        return [
            space + x_direction * self.width + y_direction * self.height
            for x_direction in [self.left, self.zero, self.right]
            for y_direction in [self.down, self.zero, self.up]
        ]

    def neighbors(self, space, diagonal=False):
        return [self.modulo(space + direction) for direction in self.cardinal_directions]

    def distance(self, start, end, metric):
        distance = min(
            self.distance(start_mirror, end_mirror, metric)
            for start_mirror in self.mirrors(start)
            for end_mirror in self.mirrors(end)
        )
        return distance

    def modulo(self, space):
        return Square((space.x % self.width, space.y % self.height))

    def disk(self, space, radius, metric="L1"):

        assert metric in self.metrics, "Metric must be in "
        m = self.metrics[metric]
        return {other for other in self if self.distance(space, other, m) <= radius}

    def lerp(self, start, end, t):
        return (1 - t) * start + t * end

    def line(self, start, end):
        raise NotImplemented()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.width}, {self.height})"



if __name__ == "__main__":
    print(Square([0, 1]))
    print({Square([0, 1]), Square([0, 1]), Square([1, 1])})

    b = SquareTopology(height=5, width=6, square_size=1)
    print(b)
    print([i for i in b])
    print(b.neighbors(Square([1, 0])))
