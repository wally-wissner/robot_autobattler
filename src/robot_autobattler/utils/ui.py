from abc import ABC, abstractmethod
from typing import Self
from uuid import uuid4

import pygame
from pygame import Surface, mouse

from frontend import colors
from frontend.application import application
from utils.geometry import Rectangle, Vector2

_x_anchors = {"left", "right", "center"}
_y_anchors = {"top", "bottom", "center"}

_adjacency_directions = {"left", "right", "up", "down"}


def anchored_blit(
    target: Surface,
    source: Surface,
    x_anchor: str = "left",
    y_anchor: str = "top",
    offset: tuple = (0, 0),
) -> Vector2:
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

    dest = Vector2(x=x_dest, y=y_dest)
    target.blit(source=source, dest=tuple(dest))
    return dest


class UICompositeComponent(ABC):
    def __init__(self, size: tuple[float, float], *args, **kwargs):
        self.id = uuid4().hex

        self.size = size
        self.surface: Surface = Surface(size=size)
        self.surface.set_colorkey(colors.TRANSPARENT)

        self.parent: Self | None = None
        self.children: set[Self] = set()

        self.offset: Vector2 | None = None

        self._is_clicked_down = False

        self.adjacent_items = {
            "left": None,
            "right": None,
            "up": None,
            "down": None,
        }

    @abstractmethod
    def render(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def on_hovered(self, *args, **kwargs) -> None:
        pass

    def on_clicked(self, *args, **kwargs) -> None:
        pass

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        self.id = other.id

    def update(self) -> None:
        for child in self.children:
            child.update()
        self.render()

    def blit(
        self,
        target: Self,
        x_anchor: str = "left",
        y_anchor: str = "top",
        offset: tuple = (0, 0),
    ) -> None:
        self.parent = target
        self.parent.children[self] = anchored_blit(
            target=target.surface,
            source=self.surface,
            x_anchor=x_anchor,
            y_anchor=y_anchor,
            offset=offset,
        )

    def absolute_rect(self) -> Rectangle:
        composite_component = self
        offset = self.offset
        while composite_component.parent:
            composite_component = composite_component.parent
            offset += composite_component.offset
        return Rectangle.from_tuples(left_top=offset, width_height=self.size)

    def is_hovered(self) -> bool:
        # TODO: Only call this once per clock.
        return self.absolute_rect().to_pygame().collidepoint(*mouse.get_pos())

    def is_selected(self) -> bool:
        # Button is hovered over by mouse or is active by direction keys.
        # TODO
        pass

    def is_clicked(self) -> bool:
        for event in application.current_events:
            if event == pygame.MOUSEBUTTONDOWN:
                if self.is_hovered():
                    self._is_clicked_down = True
            if event == pygame.MOUSEBUTTONUP:
                if self._is_clicked_down:
                    self.on_clicked()
        # TODO: only if none are clicked up
        self._is_clicked_down = False

    def assign_adjacent(self, direction: str, item: Self) -> None:
        assert direction in _adjacency_directions
        self.adjacent_items[direction] = item

    def adjacent_item(self, direction: str) -> Self:
        assert direction in _adjacency_directions
        return self.adjacent_items[direction]
