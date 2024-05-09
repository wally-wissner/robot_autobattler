# pylint: disable=unused-argument
# pylint: disable=unused-variable

import pygame

# from frontend.application import application
from backend.unit import Unit, Upgrade
from frontend.upgrades import UIUpgrade
from utils.geometry import Rectangle


class InventoryPane:
    """UI pane that shows all the upgrades the player has the ability to equip."""

    def __init__(self, rectangle: Rectangle):
        self.rectangle: Rectangle = rectangle
        self.unit: Unit | None = None


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

    def set_upgrade(self, upgrade: Upgrade):
        self.upgrade = upgrade

    def draw(self, surface: pygame.Surface):
        ui_upgrade = UIUpgrade(upgrade=self.upgrade, size=self.rectangle.size())
        ui_upgrade.draw(
            surface=self.surface,
            position=(0, 0),
            display_description=True,
        )
        surface.blit(source=self.surface, dest=self.rectangle.position())
