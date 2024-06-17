# pylint: disable=unused-argument
# pylint: disable=unused-import
# pylint: disable=unused-variable

import pygame

from backend.unit import Unit, Upgrade
from frontend.application import application
from frontend import colors
from frontend.ui_elements import UpgradeScroller
from frontend.ui_upgrades import UIUpgrade
from utils.geometry import Rectangle


class InventoryPane:
    """UI pane that shows all the upgrades the player has the ability to equip."""

    def __init__(self, rectangle: Rectangle):
        self.rectangle: Rectangle = rectangle
        self.surface = pygame.Surface(size=self.rectangle.size())

        self.upgrade_scroller = UpgradeScroller(
            upgrades=application.game.player_team().upgrades,
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

        self.active_unit = application.game.player_team().units[0]

        self.upgrade_scroller = UpgradeScroller(
            upgrades=self.active_unit.upgrades,
            size=self.rectangle.size(),
        )

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
        ui_upgrade.draw(
            surface=self.surface,
            position=(0, 0),
            display_description=True,
        )
        surface.blit(source=self.surface, dest=self.rectangle.position())
