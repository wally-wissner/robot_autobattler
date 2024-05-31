from numpy import cumsum

import pygame

from utils.data_structures import ShiftList


class VerticalScrollSurface:
    def __init__(self, items: ShiftList, size: tuple[int, int]) -> None:
        self.items = items
        self.size = size
        self.surface = pygame.Surface(size=self.size)
        self.y_offset = 0

        self._item_heights = {}

    def _set_item_heights(self):
        heights = cumsum([item.size[1] for item in self.items]) - self.items[0].size[1]
        self._item_heights = dict(zip(self.items, heights))

    def height(self) -> float:
        return sum(item.size[1] for item in self.items)

    def item_height(self, item) -> float:
        return self._item_heights[item]

    def item_visible(self, item) -> bool:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        for item in self.items:
            self.surface.blit(source=item, dest=(0, self.item_height(item)))
        surface.blit(source=self.surface, dest=(0, self.y_offset), area=None)
