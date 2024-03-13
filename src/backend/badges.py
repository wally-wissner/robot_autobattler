from dataclasses import dataclass

from src.backend.upgrade_components import UpgradeComponent
from src.backend.unitstat import StatModifier
from src.utilities import enums


@dataclass
class Badge(UpgradeComponent):
    name: str
    rarity: enums.ERarity
    bp: int
    description_text: str
    stat_modifiers: set[StatModifier]

    def description(self):
        return self.description_text
