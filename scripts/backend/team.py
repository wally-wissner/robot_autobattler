from dataclasses import dataclass
from typing import List

from scripts.backend.inventory import Inventory
from scripts.backend.unit import Unit
from scripts.backend.upgrades import UnitUpgrade


@dataclass
class Team(object):
    player: bool
    units: List[Unit]
    unit_upgrades: Inventory[UnitUpgrade]
    currency: int = 0
