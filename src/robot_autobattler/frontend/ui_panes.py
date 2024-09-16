# pylint: disable=unused-argument
# pylint: disable=unused-import
# pylint: disable=unused-variable

import pygame

from backend.unit import Unit, Upgrade
from frontend.application import game
from frontend import colors
from frontend.ui_elements import UpgradeScroller
from frontend.ui_upgrades import UIUpgrade
from utils.geometry import Rectangle
from utils.ui import anchored_blit


class InventoryPane:
    """UI pane that shows all the upgrades the player has the ability to equip."""

    def __init__(self, rectangle: Rectangle):
        self.rectangle: Rectangle = rectangle
        self.surface = pygame.Surface(size=self.rectangle.size())

        self.upgrade_scroller = UpgradeScroller(
            upgrades=game.player_team().inventory,
            size=self.rectangle.size(),
        )

    def draw(self, surface: pygame.Surface):
        self.upgrade_scroller.draw(self.surface)
        surface.blit(source=self.surface, dest=self.rectangle.position())


class ActiveUnitUpgradesPane:
    """UI pane that shows all the upgrades equipped to the active unit."""

    def __init__(self, rectangle: Rectangle):
        self.rectangle: Rectangle = rectangle
        self.surface = pygame.Surface(size=self.rectangle.size())

        self.active_unit = game.player_team().units[0]
        self.active_upgrade: Upgrade | None = None

        self.upgrade_scroller = UpgradeScroller(
            upgrades=self.active_unit.upgrades,
            size=self.rectangle.size(),
        )

    def set_active_unit(self, unit: Unit) -> None:
        self.active_unit = unit

    def set_active_upgrade(self, upgrade: Upgrade | None) -> None:
        self.active_upgrade = upgrade
        self.upgrade_scroller.set_active_upgrade(upgrade)

    def draw(self, surface: pygame.Surface):
        self.upgrade_scroller.draw(self.surface)
        surface.blit(source=self.surface, dest=self.rectangle.position())


class TeamPane:
    """UI pane that shows all the units on the player's team."""

    def __init__(self, rectangle: Rectangle):
        self.rectangle: Rectangle = rectangle
        self.unit: Unit | None = None


class UnitPane:
    """UI pane that shows the upgrades attached to the currently selected unit."""

    def __init__(self, rectangle: Rectangle):
        self.rectangle: Rectangle = rectangle
        self.unit: Unit | None = None

    def set_unit(self, unit: Unit):
        self.unit = unit


class UpgradePane:
    """UI pane that shows the text of the currently selected upgrade."""

    def __init__(self, rectangle: Rectangle):
        self.rectangle = rectangle
        self.upgrade: Upgrade | None = None

        self.surface = pygame.Surface(self.rectangle.size())
        self.surface.set_colorkey(colors.TRANSPARENT)

    def set_upgrade(self, upgrade: Upgrade):
        self.upgrade = upgrade

    def draw(self, surface: pygame.Surface):
        self.surface.fill(color=colors.TRANSPARENT)
        ui_upgrade = UIUpgrade(
            upgrade=self.upgrade, size=self.rectangle.size(), display_body=True
        )
        ui_upgrade.render(display_description=True, highlighted=True)
        anchored_blit(
            target=self.surface,
            source=ui_upgrade.surface,
            x_anchor="left",
            y_anchor="top",
        )

        surface.blit(source=self.surface, dest=self.rectangle.position())
