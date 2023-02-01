import math
import pygame
from shapely.geometry import Point, Polygon


class DiscObject(object):
    def __init__(
            self,
            radius: float,
            position: pygame.Vector2 = pygame.Vector2(),
            velocity: pygame.Vector2 = pygame.Vector2(),
            acceleration: pygame.Vector2 = pygame.Vector2(),
            resistance: float = 0,
    ):
        self._radius = radius
        self.shape: Polygon = Point().buffer(distance=radius)
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.resistance = resistance

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self.shape = Point().buffer(distance=value)

    def update(self, dt):
        self.velocity += (self.acceleration - self.resistance * self.velocity) * dt
        self.position += self.velocity * dt

        if math.isclose((self.velocity - pygame.Vector2()).magnitude(), 0, abs_tol=1e-8):
            self.velocity = pygame.Vector2()
