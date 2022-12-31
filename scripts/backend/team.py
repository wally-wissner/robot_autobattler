from dataclasses import dataclass, field

from scripts.backend.inventory import Inventory
from scripts.backend.unit import Unit
from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.utilities.enums import ECollectable


@dataclass
class Team(object):
    is_player: bool
    units: list[Unit] = field(default_factory=list)
    unit_upgrades: Inventory[UnitUpgrade] = field(default_factory=Inventory)
    collectables: Inventory[ECollectable] = field(default_factory=Inventory)
