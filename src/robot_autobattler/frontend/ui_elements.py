import pygame

from backend.upgrades import Upgrade
from frontend import colors
from frontend.ui_upgrades import UIUpgrade
from utils.data_structures import ShiftList
from utils.ui import anchored_blit


class UpgradeScroller:
    def __init__(
        self,
        upgrades: ShiftList[Upgrade],
        size: tuple[int, int],
    ) -> None:
        self.upgrades = upgrades
        self.size = size
        self.ui_upgrade_size = (self.size[0], int(0.75 * self.size[0]))

        self.surface = pygame.Surface(size=self.size)
        self.surface.set_colorkey(colors.TRANSPARENT)

        self.y_scroll = 0

        self.active_index: int | None = 0

        self.active_upgrade: Upgrade | None = None

    def _is_active_upgrade(self, upgrade: Upgrade) -> bool:
        return self.active_upgrade is not None and self.active_upgrade is upgrade

    def set_active_upgrade(self, upgrade: Upgrade | None):
        self.active_upgrade = upgrade

    def item_visible(self, i: int) -> bool:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        self.surface.fill(color=colors.TRANSPARENT)

        for i, upgrade in enumerate(self.upgrades):
            ui_upgrade = UIUpgrade(
                upgrade=upgrade, size=self.ui_upgrade_size, display_body=True
            )
            ui_upgrade.render(
                display_description=True, highlighted=self.active_index == i
            )
            self.surface.blit(
                source=ui_upgrade.surface, dest=(0, i * self.ui_upgrade_size[1])
            )

        surface.blit(source=self.surface, dest=(0, self.y_scroll), area=None)
