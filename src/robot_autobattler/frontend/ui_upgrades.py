"""
UI elements for upgrades.
"""

from math import ceil

import pygame

from backend.upgrades import Card, Upgrade
from backend.upgrade_components import UpgradeComponent
from frontend import colors
from frontend import fonts
from utils.enums import ERarity
from utils.ui import anchored_blit, UICompositeComponent


rarity_colors = {
    ERarity.COMMON: colors.COMMON,
    ERarity.UNCOMMON: colors.UNCOMMON,
    ERarity.RARE: colors.RARE,
}


OPACITY = 100

# Upgrade proportion constants.
TITLE_TEXT_SIZE = 0.05
BODY_TEXT_SIZE = 0.04
BORDER_RADIUS = 0.025
RARITY_BORDER_WIDTH = 0.020
BLACK_BORDER_WIDTH = 0.005
TITLE_Y_OFFSET = 0.025
BODY_Y_OFFSET = 0.100
X_OFFSET = 0.05
COST_X_OFFSET = 0.8


class UIUpgradeComponent(UICompositeComponent):
    def __init__(
        self,
        upgrade_component: UpgradeComponent,
        size: tuple[float, float],
        display_body: bool,
        round_top: bool,
        round_bottom: bool,
    ):
        super().__init__(size=size)

        self.upgrade_component = upgrade_component
        self.display_body = display_body
        self.round_top = round_top
        self.round_bottom = round_bottom

        self.surface.set_colorkey(colors.TRANSPARENT)

        self.highlight_surface = pygame.Surface(self.size)

        self.component_title = fonts.get_font(
            font=fonts.card_font, size=self._scale(TITLE_TEXT_SIZE)
        ).render(
            text=self.upgrade_component.name,
            antialias=True,
            color=colors.UPGRADE_TEXT,
        )

        self.component_cost_text = fonts.get_font(
            font=fonts.card_font, size=self._scale(TITLE_TEXT_SIZE)
        ).render(
            text=str(
                f"{self.upgrade_component.windup} WU"
                if isinstance(self.upgrade_component, Card)
                else f"{self.upgrade_component.bp} BP"
            ),
            antialias=True,
            color=colors.UPGRADE_TEXT,
        )

        self.component_body = fonts.get_font(
            font=fonts.card_font, size=self._scale(BODY_TEXT_SIZE)
        ).render(
            text=self.upgrade_component.description(),
            antialias=True,
            color=colors.UPGRADE_TEXT,
        )

    def _scale(self, frac: float) -> int:
        return ceil(frac * self.size[0])

    def render(self, display_description: bool, highlighted: bool):
        self.surface.fill(color=colors.TRANSPARENT)

        radius_kwargs = {
            "border_top_left_radius": (
                self._scale(BORDER_RADIUS) if self.round_top else 0
            ),
            "border_top_right_radius": (
                self._scale(BORDER_RADIUS) if self.round_top else 0
            ),
            "border_bottom_left_radius": (
                self._scale(BORDER_RADIUS) if self.round_bottom else 0
            ),
            "border_bottom_right_radius": (
                self._scale(BORDER_RADIUS) if self.round_bottom else 0
            ),
        }

        pygame.draw.rect(
            rect=((0, 0), self.size),
            surface=self.surface,
            color=self.upgrade_component.color(),
            **radius_kwargs,
        )

        # Non-highlighted opacity
        if not highlighted:
            pygame.draw.rect(
                rect=((0, 0), self.size),
                surface=self.highlight_surface,
                color=colors.OPACITY,
                **radius_kwargs,
            )
            self.highlight_surface.set_alpha(OPACITY)
            self.surface.blit(source=self.highlight_surface, dest=(0, 0))

        if display_description:
            self.surface.blit(
                source=self.component_title,
                dest=(self._scale(X_OFFSET), self._scale(TITLE_Y_OFFSET)),
            )
            self.surface.blit(
                source=self.component_cost_text,
                dest=(self._scale(COST_X_OFFSET), self._scale(TITLE_Y_OFFSET)),
            )
            self.surface.blit(
                source=self.component_body,
                dest=(self._scale(X_OFFSET), self._scale(BODY_Y_OFFSET)),
            )

        else:
            self.surface.blit(
                source=self.component_title,
                dest=(self._scale(X_OFFSET), self._scale(TITLE_Y_OFFSET)),
            )
            self.surface.blit(
                source=self.component_cost_text,
                dest=(self._scale(COST_X_OFFSET), self._scale(TITLE_Y_OFFSET)),
            )


class UIUpgrade(UICompositeComponent):
    def __init__(self, upgrade: Upgrade, size: tuple[float, float], display_body: bool):
        super().__init__(size=size)

        self.upgrade = upgrade
        self.display_body = display_body

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

    def _scale(self, frac: float) -> int:
        return ceil(frac * self.size[0])

    def render(self, display_description: bool, highlighted: bool):
        self.surface.fill(color=colors.TRANSPARENT)

        self.badge_ui.render(
            display_description=display_description, highlighted=highlighted
        )
        print("badge ui:")
        anchored_blit(
            target=self.surface,
            source=self.badge_ui.surface,
            x_anchor="center",
            y_anchor="top",
        )

        self.card_ui.render(
            display_description=display_description, highlighted=highlighted
        )
        print("card ui:")
        anchored_blit(
            target=self.surface,
            source=self.card_ui.surface,
            x_anchor="center",
            y_anchor="bottom",
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
            color=colors.BORDER,
            border_radius=self._scale(BORDER_RADIUS),
        )
