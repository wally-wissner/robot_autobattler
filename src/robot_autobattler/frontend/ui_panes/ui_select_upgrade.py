from typing import List

import pygame
from pygame_gui.elements import UIButton

from backend.unit import Upgrade
from frontend import colors
from frontend.application import application
from frontend.ui_upgrades import UIUpgrade
from utils.geometry import Rectangle
from utils.ui import anchored_blit


class UIPaneSelectUpgrade:
    """UI pane that allows the player to select an upgrade to add to their inventory."""

    def __init__(self, rectangle: Rectangle):
        self.rectangle: Rectangle = rectangle
        self.surface = pygame.Surface(size=self.rectangle.size())

        self.upgrades: List[Upgrade] = []

    def draw(self, surface: pygame.Surface):
        self.surface.fill(color=colors.POP_UP_PANE)

        surface.blit(source=self.surface, dest=self.rectangle.position())

        anchored_blit(
            target=application.display,
            source=self.surface,
            offset=(0, 0),
            x_anchor="center",
            y_anchor="center",
        )
