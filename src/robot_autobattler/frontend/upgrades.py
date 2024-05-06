"""
UI elements for upgrades.
"""

# pylint: disable=no-member
# pylint: disable=unused-import

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

    def draw(
        self,
        surface: pygame.Surface,
        size: tuple,
        position: tuple,
        display_description: bool,
    ):
        component_surface = pygame.Surface(size=size)
        component_surface.fill(color=self.upgrade_component.color())

        if display_description:
            title = get_font(EFont.JETBRAINS_MONO_REGULAR, 12).render(
                # Flicker "cursor" every second.
                text=self.upgrade_component.name,
                antialias=True,
                color=colors.BLACK,
            )
            component_surface.blit(source=title, dest=(10, 10))

        surface.blit(source=component_surface, dest=position)


class UIUpgrade:
    border_width = 0.025

    def __init__(self, upgrade: Upgrade):
        self.upgrade = upgrade
        self.badge_ui = UIUpgradeComponent(upgrade.badge)
        self.card_ui = UIUpgradeComponent(upgrade.card)

    def draw(
        self,
        surface: pygame.Surface,
        size: tuple,
        position: tuple,
        display_description: bool,
    ):
        upgrade_surface = pygame.Surface(size=size)

        self.badge_ui.draw(
            surface=upgrade_surface,
            size=(size[0], size[1] / 2),
            position=(0, 0),
            display_description=display_description,
        )
        self.card_ui.draw(
            surface=upgrade_surface,
            size=(size[0], size[1] / 2),
            position=(0, size[1] / 2),
            display_description=display_description,
        )

        surface.blit(source=upgrade_surface, dest=position)

        # pygame.draw.rect(
        #     surface=surface,
        #     # color=
        # )
