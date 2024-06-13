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


class UIUpgradeComponent:
    vertical_proportions = (0.175, 0.025, 0.8)

    def __init__(
        self,
        upgrade_component: UpgradeComponent,
        size: tuple[int, int],
        border_radius: float,
        top_component: bool,
    ):
        self.upgrade_component = upgrade_component
        self.size = size
        self.border_radius = border_radius
        self.top_component = top_component

        self.surface = pygame.Surface(size=self.size)

    def title_font_size(self):
        return int(self.size[0] / 20)

    def body_font_size(self):
        return int(self.size[0] / 25)

    def draw(
        self,
        surface: pygame.Surface,
        position: tuple,
        display_description: bool,
    ):
        if self.top_component:
            pygame.draw.rect(
                rect=((0, 0), self.size),
                surface=self.surface,
                color=self.upgrade_component.color(),
                border_top_left_radius=int(self.border_radius * self.size[0]),
                border_top_right_radius=int(self.border_radius * self.size[0]),
            )
        else:
            pygame.draw.rect(
                rect=((0, 0), self.size),
                surface=self.surface,
                color=self.upgrade_component.color(),
                border_bottom_left_radius=int(self.border_radius * self.size[0]),
                border_bottom_right_radius=int(self.border_radius * self.size[0]),
            )

        if display_description:
            component_name = fonts.get_font(
                fonts.card_font, self.title_font_size()
            ).render(
                text=self.upgrade_component.name,
                antialias=True,
                color=colors.BLACK,
            )
            self.surface.blit(source=component_name, dest=(10, 10))

        surface.blit(source=self.surface, dest=position)


class UIUpgrade:
    border_width = 0.0125
    border_radius = 0.025

    def __init__(self, upgrade: Upgrade, size: tuple):
        self.upgrade = upgrade
        self.badge_ui = UIUpgradeComponent(
            upgrade_component=upgrade.badge,
            size=(size[0], size[1] / 2),
            border_radius=self.border_radius,
            top_component=True,
        )
        self.card_ui = UIUpgradeComponent(
            upgrade_component=upgrade.card,
            size=(size[0], size[1] / 2),
            border_radius=self.border_radius,
            top_component=False,
        )

        self.size = size
        self.surface = pygame.Surface(size=size)

    def draw(
        self,
        surface: pygame.Surface,
        position: tuple,
        display_description: bool,
    ):

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
            width=int(self.border_width * self.size[0]),
            color=rarity_colors[self.upgrade.rarity],
            border_radius=int(self.border_radius * self.size[0]),
        )

        surface.blit(source=self.surface, dest=position)
