from typing import List

import pygame
from pygame_gui.elements import UIButton

from backend.unit import Upgrade
from backend.factories import generate_upgrade
from frontend import colors
from frontend.application import application
from frontend.ui_upgrades import UIUpgrade
from utils.enums import EUIDepth
from utils.geometry import Rectangle, Vector2
from utils.ui import UICompositeComponent, anchored_blit


class UIPaneSelectUpgrade(UICompositeComponent):
    """UI pane that allows the player to select an upgrade to add to their inventory."""

    def __init__(self, size: tuple[float, float]):
        super().__init__(size=size)

        self.upgrades: List[Upgrade] = []

    def generate_upgrades(self):
        self.upgrades = []
        for _ in range(3):
            self.upgrades.append(generate_upgrade())

    def render(self):
        self.surface.fill(color=colors.POP_UP_PANE)

        n = len(self.upgrades)
        for i, upgrade in enumerate(self.upgrades):
            ui_upgrade = UIUpgrade(
                upgrade=upgrade,
                size=(
                    0.1 * application.width(),
                    0.1 * application.height(),
                ),
                display_body=True,
            )
            ui_upgrade.render(display_description=True, highlighted=False)
            anchored_blit(
                target=self.surface,
                source=ui_upgrade.surface,
                x_anchor="center",
                y_anchor="center",
                # offset=(i/n * self.rectangle.width(), 0),  # TODO: correct spacing math
            )
