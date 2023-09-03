from dataclasses import dataclass

from scripts.backend.upgrade_components import UpgradeComponent
from scripts.backend.unitstat import StatModifier
from scripts.utilities import enums


@dataclass
class Badge(UpgradeComponent):
    name: str
    rarity: enums.ERarity
    bp: int
    description_text: str
    stat_modifiers: set[StatModifier]

    def description(self):
        return self.description_text
