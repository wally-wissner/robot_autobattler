from abc import ABC, abstractmethod
from typing import Self
from uuid import uuid4

import pygame
from pygame import Surface

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

        # States
        self._is_clicked_down = False
        self._is_key_selected = False

        self.adjacent_items = {
            "left": None,
            "right": None,
            "up": None,
            "down": None,
        }

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        self.id = other.id

    @abstractmethod
    def render(self, *args, **kwargs) -> None:
        raise NotImplementedError()

    def on_selected(self, *args, **kwargs) -> None:
        pass

    def on_clicked(self, *args, **kwargs) -> None:
        pass

    def update(self, events) -> None:
        if self.is_clicked():
            self.on_clicked()
        if self.is_selected():
            self.on_selected()

        for child in self.children:
            child.update(events)

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

    def is_moused(self) -> bool:
        """
        Whether the UI item is currently moused over.
        """
        return self.absolute_rect().to_pygame().collidepoint(application.mouse_position)

    def is_selected(self) -> bool:
        """
        Whether the UI item is selected, either by mouse hover or key select.
        """
        return self.is_moused() or self._is_key_selected

    def is_clicked(self) -> bool:
        for event in application.current_events:
            if event == pygame.MOUSEBUTTONDOWN:
                if self.is_moused():
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
