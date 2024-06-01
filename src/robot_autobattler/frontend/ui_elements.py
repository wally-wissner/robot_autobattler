import pygame

from backend.upgrades import Upgrade
from frontend.upgrades import UIUpgrade
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

        self.y_scroll = 0

    def item_visible(self, i: int) -> bool:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        for i, upgrade in enumerate(self.upgrades):
            ui_upgrade = UIUpgrade(upgrade=upgrade, size=self.ui_upgrade_size)
            ui_upgrade.draw(
                surface=self.surface, position=(0, i), display_description=True
            )
        surface.blit(source=self.surface, dest=(0, self.y_scroll), area=None)
