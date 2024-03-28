# from frontend.application import application
from backend.unit import Unit, Upgrade
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
        self.rectangle: Rectangle = rectangle
        self.unit: Unit | None = None
        self.upgrade: Upgrade | None = None

    def set_upgrade(self, upgrade: Upgrade):
        self.upgrade = upgrade
        # UIUnitUpgrade(upgrade)
