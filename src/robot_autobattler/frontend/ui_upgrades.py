"""
UI elements for upgrades.
"""

import pygame

from backend.upgrades import Upgrade
from backend.upgrade_components import UpgradeComponent
from frontend import colors
from frontend import fonts
from utils.enums import ERarity


rarity_colors = {
    ERarity.COMMON: colors.COMMON,
    ERarity.UNCOMMON: colors.UNCOMMON,
    ERarity.RARE: colors.RARE,
}


# Upgrade proportion constants.
TITLE_TEXT_SIZE = 0.05
BODY_TEXT_SIZE = 0.04
BORDER_RADIUS = 0.025
RARITY_BORDER_WIDTH = 0.015


class UIUpgradeComponent:
    def __init__(
        self,
        upgrade_component: UpgradeComponent,
        size: tuple[int, int],
        display_body: bool,
        round_top: bool,
        round_bottom: bool,
    ):
        self.upgrade_component = upgrade_component
        self.size = size
        self.display_body = display_body
        self.round_top = round_top
        self.round_bottom = round_bottom

        self.surface = pygame.Surface(self.size)
        self.surface.set_colorkey(colors.TRANSPARENT)

    def scale(self, frac: float) -> int:
        return int(frac * self.size[0])

    def draw(
        self,
        surface: pygame.Surface,
        position: tuple,
        display_description: bool,
    ):
        self.surface.fill(color=colors.TRANSPARENT)

        pygame.draw.rect(
            rect=((0, 0), self.size),
            surface=self.surface,
            color=self.upgrade_component.color(),
            border_top_left_radius=(
                int(BORDER_RADIUS * self.size[0]) if self.round_top else 0
            ),
            border_top_right_radius=(
                int(BORDER_RADIUS * self.size[0]) if self.round_top else 0
            ),
            border_bottom_left_radius=(
                int(BORDER_RADIUS * self.size[0]) if self.round_bottom else 0
            ),
            border_bottom_right_radius=(
                int(BORDER_RADIUS * self.size[0]) if self.round_bottom else 0
            ),
        )

        if display_description:
            component_title = fonts.get_font(
                font=fonts.card_font, size=self.scale(TITLE_TEXT_SIZE)
            ).render(
                text=self.upgrade_component.name,
                antialias=True,
                color=colors.BLACK,
            )
            component_body = fonts.get_font(
                font=fonts.card_font, size=self.scale(BODY_TEXT_SIZE)
            ).render(
                text=self.upgrade_component.description(),
                antialias=True,
                color=colors.BLACK,
            )
            self.surface.blit(source=component_title, dest=(15, 10))
            self.surface.blit(source=component_body, dest=(15, 50))

        else:
            component_title = fonts.get_font(
                font=fonts.card_font, size=self.scale(TITLE_TEXT_SIZE)
            ).render(
                text=self.upgrade_component.name,
                antialias=True,
                color=colors.BLACK,
            )
            self.surface.blit(source=component_title, dest=(15, 10))

        surface.blit(source=self.surface, dest=position)


class UIUpgrade:
    def __init__(self, upgrade: Upgrade, size: tuple, display_body: bool):
        self.upgrade = upgrade
        self.size = size
        self.display_body = display_body

        self.surface = pygame.Surface(self.size)
        self.surface.set_colorkey(colors.TRANSPARENT)

        self.badge_ui = UIUpgradeComponent(
            upgrade_component=upgrade.badge,
            size=(size[0], size[1] / 2),
            display_body=self.display_body,
            round_top=True,
            round_bottom=False,
        )
        self.card_ui = UIUpgradeComponent(
            upgrade_component=upgrade.card,
            size=(size[0], size[1] / 2),
            display_body=self.display_body,
            round_top=False,
            round_bottom=True,
        )

    def scale(self, frac: float) -> int:
        return int(frac * self.size[0])

    def draw(
        self,
        surface: pygame.Surface,
        position: tuple,
        display_description: bool,
    ):
        self.surface.fill(color=colors.TRANSPARENT)

        self.badge_ui.draw(
            surface=self.surface,
            position=(0, 0),
            display_description=display_description,
        )
        self.card_ui.draw(
            surface=self.surface,
            position=(0, self.size[1] / 2),
            display_description=display_description,
        )

        pygame.draw.rect(
            rect=((0, 0), self.size),
            surface=self.surface,
            width=self.scale(RARITY_BORDER_WIDTH),
            color=rarity_colors[self.upgrade.rarity],
            border_radius=self.scale(BORDER_RADIUS),
        )

        surface.blit(source=self.surface, dest=position)
