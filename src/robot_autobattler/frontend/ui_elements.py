import pygame

# from pygame_gui.elements import UIVerticalScrollBar

from utils.geometry import Rectangle


class VerticalScrollSurface:
    def __init__(self, rectangle: Rectangle):
        self.surface = pygame.Surface(size=rectangle.size())

    def draw(self):
        pass
