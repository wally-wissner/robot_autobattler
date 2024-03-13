import math
from shapely.geometry import Point, Polygon

from src.scripts.utilities.geometry import Vector2


class PhysicsBody(object):
    def __init__(
            self,
            shape: Polygon,
            mass: float = 0,
            position: Vector2 = Vector2(),
            velocity: Vector2 = Vector2(),
            acceleration: Vector2 = Vector2(),
            friction: float = 0,
            team=None,
    ):
        self.shape = shape
        self.mass = mass
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.acceleration = Vector2(acceleration)
        self.friction = friction
        self.team = team

        self.objects_touched: list[PhysicsBody] = []

    def update(self, dt):
        self.velocity = (self.acceleration - self.friction * self.velocity) * dt + self.velocity
        self.position = self.velocity * dt + self.position

        if not self.is_moving():
            self.velocity = Vector2()
            self.acceleration = Vector2()

    def is_moving(self):
        velocity_near_zero = math.isclose(self.velocity.magnitude(), 0, abs_tol=1e-8)
        acceleration_near_zero = math.isclose(self.acceleration.magnitude(), 0, abs_tol=1e-8)
        return not (velocity_near_zero and acceleration_near_zero)


class DiscBody(PhysicsBody):
    def __init__(self, radius: float = 0, *args, **kwargs):
        self._radius = radius
        super().__init__(shape=Point().buffer(distance=radius), *args, **kwargs)

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self.shape = Point().buffer(distance=value)
