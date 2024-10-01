from abc import ABC, abstractmethod

# from typing import Self

from pygame import Surface

from frontend import colors
from utils.geometry import Rectangle


_x_anchors = {"left", "right", "center"}
_y_anchors = {"top", "bottom", "center"}


class UICompositeComponent(ABC):
    def __init__(self, size: tuple, *args, **kwargs):
        self.size = size
        self.surface: Surface = Surface(size=size)
        self.surface.set_colorkey(colors.TRANSPARENT)
        # self.children: list[Self] = []

    # def update(self) -> None:
    #     for child in self.children:
    #         child.draw(self.surface)

    @abstractmethod
    def render(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    # def draw(self, surface: Surface, dest: tuple = (0, 0)) -> None:
    #     surface.blit(source=self.surface, dest=dest)


def anchored_blit(
    target: Surface,
    source: Surface,
    x_anchor: str = "left",
    y_anchor: str = "top",
    offset: tuple = (0, 0),
):
    rect_target = Rectangle.from_rect(target.get_rect())
    rect_source = Rectangle.from_rect(source.get_rect())

    x_dest = {
        "left": 0,
        "right": rect_target.width() - rect_source.width(),
        "center": (rect_target.width() - rect_source.width()) / 2,
    }[x_anchor] + offset[0]

    y_dest = {
        "top": 0,
        "bottom": rect_target.height() - rect_source.height(),
        "center": (rect_target.height() - rect_source.height()) / 2,
    }[y_anchor] + offset[1]

    target.blit(source=source, dest=(x_dest, y_dest))
