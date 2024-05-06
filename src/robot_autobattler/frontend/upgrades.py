"""
UI elements for upgrades.
"""

import pygame

from backend.upgrades import Upgrade
from backend.upgrade_components import UpgradeComponent
from frontend import colors
from frontend.fonts import get_font
from utils.enums import EFont
from utils.geometry import Vector2


class UIUpgradeComponent:
    vertical_proportions = (0.175, 0.025, 0.8)

    def __init__(self, upgrade_component: UpgradeComponent):
        self.upgrade_component = upgrade_component

    def draw(self, surface: pygame.Surface, size: Vector2, display_description: bool):
        component_surface = pygame.Surface(size=size)

        pygame.draw.rect(
            surface=surface,
            color=self.upgrade_component.color(),
            rect=pygame.Rect(size, (0, 0)),
        )

        if display_description:
            pass


class UIUpgrade:
    border_width = 0.025

    def __init__(self, upgrade: Upgrade):
        self.upgrade = upgrade
        self.badge_ui = UIUpgradeComponent(upgrade.badge)
        self.card_ui = UIUpgradeComponent(upgrade.card)

    def draw(self, surface: pygame.Surface, size: Vector2, display_description: bool):
        upgrade_surface = pygame.Surface(size=size)

        self.badge_ui.draw(
            surface=upgrade_surface, display_description=display_description
        )
        self.card_ui.draw(
            surface=upgrade_surface, display_description=display_description
        )

        pygame.draw.rect(
            surface=surface,
            # color=
        )
