from scripts.backend.cards import Card
from scripts.backend.inventory import Inventory
from scripts.backend.unit import Unit
from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.utilities.enums import ECollectable


class Team(object):
    def __init__(self, is_player: bool):
        self.is_player: bool = is_player
        self.library: list[Card] = []
        self.queue: list[Card] = []
        self.graveyard: set[Card] = set()
        self.units: list[Unit] = []
        self.unit_upgrades = Inventory()
        self.collectables = Inventory()
