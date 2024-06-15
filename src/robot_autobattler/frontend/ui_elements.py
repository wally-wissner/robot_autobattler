import pygame

from backend.upgrades import Upgrade
from frontend import colors
from frontend.ui_upgrades import UIUpgrade
from utils.data_structures import ShiftList


class UpgradeScroller:
    def __init__(
        self,
        upgrades: ShiftList[Upgrade],
        size: tuple[int, int],
        ui_upgrade_size: tuple[int, int],
    ) -> None:
        self.upgrades = upgrades
        self.size = size
        self.ui_upgrade_size = ui_upgrade_size

        self.surface = pygame.Surface(size=self.size)
        self.surface.set_colorkey(colors.TRANSPARENT)

        self.y_scroll = 0

    def item_visible(self, i: int) -> bool:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.surface.fill(color=colors.TRANSPARENT)

        for i, upgrade in enumerate(self.upgrades):
            ui_upgrade = UIUpgrade(
                upgrade=upgrade, size=self.ui_upgrade_size, display_body=True
            )
            ui_upgrade.draw(
                surface=self.surface,
                position=(0, i * self.ui_upgrade_size[1]),
                display_description=True,
            )
        surface.blit(source=self.surface, dest=(0, self.y_scroll), area=None)
