import pygame as pg
from typing import Iterable, Self


def rect_from_points(points: Iterable[pg.Vector2]) -> pg.rect:



class Rectangle(object):
    def __init__(self, points: Iterable[pg.Vector2]):
        self.x_min = min(point.x for point in points)
        self.x_max = max(point.x for point in points)
        self.y_min = min(point.x for point in points)
        self.y_max = max(point.x for point in points)

        self.bottom_left = pg.Vector2(self.x_min, self.y_min)
        self.top_left = pg.Vector2(self.x_min, self.y_max)
        self.bottom_right = pg.Vector2(self.x_max, self.y_min)
        self.top_right = pg.Vector2(self.x_max, self.y_max)

        self.width = self.x_max - self.x_min
        self.height = self.y_max - self.y_min

        self.center = pg.Vector2((self.x_min + self.x_max) / 2, (self.y_min + self.y_max) / 2)

    def pad(self, aspect_ratio: float = None, fraction: float = 0) -> Self:
        if aspect_ratio:

        return self

    def to_pygame(self) -> tuple[pg.Vector2, tuple]:
        return pg.Vector2(self.x_min, self.y_max), (self.width, self.height)
