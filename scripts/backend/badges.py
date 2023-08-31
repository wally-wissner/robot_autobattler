from dataclasses import dataclass

from scripts.backend.unit_upgrade_components import UnitUpgradeComponent
from scripts.backend.unitstat import StatModifier
from scripts.utilities import enums


@dataclass
class Badge(UnitUpgradeComponent):
    name: str
    rarity: enums.ERarity
    bp: int
    description_text: str
    stat_modifiers: set[StatModifier]

    def description(self):
        return self.description_text
