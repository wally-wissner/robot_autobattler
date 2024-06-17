"""
UI elements for upgrades.
"""

from math import ceil

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
RARITY_BORDER_WIDTH = 0.020
BLACK_BORDER_WIDTH = 0.005
TITLE_Y_OFFSET = 0.025
BODY_Y_OFFSET = 0.100
X_OFFSET = 0.05


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

    def _scale(self, frac: float) -> int:
        return ceil(frac * self.size[0])

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
                self._scale(BORDER_RADIUS) if self.round_top else 0
            ),
            border_top_right_radius=(
                self._scale(BORDER_RADIUS) if self.round_top else 0
            ),
            border_bottom_left_radius=(
                self._scale(BORDER_RADIUS) if self.round_bottom else 0
            ),
            border_bottom_right_radius=(
                self._scale(BORDER_RADIUS) if self.round_bottom else 0
            ),
        )

        if display_description:
            component_title = fonts.get_font(
                font=fonts.card_font, size=self._scale(TITLE_TEXT_SIZE)
            ).render(
                text=self.upgrade_component.name,
                antialias=True,
                color=colors.BLACK,
            )
            component_body = fonts.get_font(
                font=fonts.card_font, size=self._scale(BODY_TEXT_SIZE)
            ).render(
                text=self.upgrade_component.description(),
                antialias=True,
                color=colors.BLACK,
            )
            self.surface.blit(
                source=component_title,
                dest=(self._scale(X_OFFSET), self._scale(TITLE_Y_OFFSET)),
            )
            self.surface.blit(
                source=component_body,
                dest=(self._scale(X_OFFSET), self._scale(BODY_Y_OFFSET)),
            )

        else:
            component_title = fonts.get_font(
                font=fonts.card_font, size=self._scale(TITLE_TEXT_SIZE)
            ).render(
                text=self.upgrade_component.name,
                antialias=True,
                color=colors.BLACK,
            )
            self.surface.blit(
                source=component_title,
                dest=(self._scale(X_OFFSET), self._scale(TITLE_Y_OFFSET)),
            )

        surface.blit(source=self.surface, dest=position)


class UIUpgrade:
    def __init__(self, upgrade: Upgrade, size: tuple, display_body: bool):
        self.upgrade = upgrade
        self.size = size
        self.display_body = display_body

        self.highlighted = False

        self.surface = pygame.Surface(self.size)
        self.surface.set_colorkey(colors.TRANSPARENT)

        self.highlight_surface = pygame.Surface(self.size)

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

    def _scale(self, frac: float) -> int:
        return ceil(frac * self.size[0])

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

        # Rarity border
        pygame.draw.rect(
            rect=((0, 0), self.size),
            surface=self.surface,
            width=self._scale(RARITY_BORDER_WIDTH),
            color=rarity_colors[self.upgrade.rarity],
            border_radius=self._scale(BORDER_RADIUS),
        )

        # Black border
        pygame.draw.rect(
            rect=((0, 0), self.size),
            surface=self.surface,
            width=self._scale(BLACK_BORDER_WIDTH),
            color=colors.BLACK,
            border_radius=self._scale(BORDER_RADIUS),
        )

        # # Non-highlighted opacity
        # if not self.highlighted:
        #     pygame.draw.rect(
        #         rect=((0, 0), self.size),
        #         surface=self.highlight_surface,
        #         color=colors.LIGHT_GRAY,
        #         border_radius=self._scale(BORDER_RADIUS),
        #     )
        #     self.highlight_surface.set_alpha(100)
        #     self.surface.blit(source=self.highlight_surface, dest=(0, 0))

        surface.blit(source=self.surface, dest=position)
