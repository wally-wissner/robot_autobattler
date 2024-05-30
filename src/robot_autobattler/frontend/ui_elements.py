import pygame

from frontend.upgrades import UIUpgrade
from utils.data_structures import ShiftList


class VerticalScrollSurface:
    def __init__(self, items: ShiftList[UIUpgrade], size: tuple[int, int]):
        self.items = items
        self.size = size
        self.surface = pygame.Surface(size=self.size)
        self.x = 0

    def draw(self, surface: pygame.Surface):
        height = 0
        for item in self.items:
            self.surface.blit(source=item, dest=(0, height))
            height += item.size[1]
        surface.blit(source=self.surface, dest=(0, self.x), area=None)
