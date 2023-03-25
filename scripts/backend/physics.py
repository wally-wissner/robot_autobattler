import math
import pygame
from shapely.geometry import Point, Polygon


class PhysicsBody(object):
    def __init__(
            self,
            shape: Polygon,
            mass: float = 0,
            position: pygame.Vector2 = pygame.Vector2(),
            velocity: pygame.Vector2 = pygame.Vector2(),
            acceleration: pygame.Vector2 = pygame.Vector2(),
            resistance: float = 0,
            team=None,
    ):
        self.shape = shape
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.resistance = resistance
        self.team = team

        self.objects_touched: list[PhysicsBody] = []

    def update(self, dt):
        self.velocity += (self.acceleration - self.resistance * self.velocity) * dt
        self.position += self.velocity * dt

        if math.isclose((self.velocity - pygame.Vector2()).magnitude(), 0, abs_tol=1e-8):
            self.velocity = pygame.Vector2()


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
