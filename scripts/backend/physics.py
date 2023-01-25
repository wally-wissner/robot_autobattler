import pygame
from shapely.geometry import Polygon
from dataclasses import dataclass


tolerance = 1e-8


@dataclass
class RigidBody(object):
    shape: Polygon
    position: pygame.Vector2
    velocity: pygame.Vector2
    friction: float

    def update(self, dt):
        self.velocity += (-self.friction * self.velocity.normalize()) * dt
        self.position += self.velocity * dt


@dataclass
class KinematicBody(RigidBody):
    mass: float
