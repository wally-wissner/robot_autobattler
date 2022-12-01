from dataclasses import dataclass
from typing import List

from scripts.backend.inventory import Inventory
from scripts.backend.unit import Unit
from scripts.backend.upgrades import UnitUpgrade
from scripts.utilities.enums import ECollectable


@dataclass
class Team(object):
    is_player: bool
    units: List[Unit]
    unit_upgrades: Inventory[UnitUpgrade]
    collectables: Inventory[ECollectable]
