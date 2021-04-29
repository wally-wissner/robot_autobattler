import pygame as pg
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Button(object):
    def __init__(self, polygon:Polygon, position, color, text):
        self.polygon = polygon
        self.position = position
        self.color = color
        self.text = text

    def draw(self):
        pg.draw.polygon(
            surface=,
            color=,
            points=,
            width=,
        )

    def mouse_over(self, point) -> bool:



    def mouse_down(self) -> bool:


    def mouse_up(self) -> bool:
