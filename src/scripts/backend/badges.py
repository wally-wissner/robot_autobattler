from dataclasses import dataclass

from src.scripts.backend.upgrade_components import UpgradeComponent
from src.scripts.backend.unitstat import StatModifier
from src.scripts.utilities import enums


@dataclass
class Badge(UpgradeComponent):
    name: str
    rarity: enums.ERarity
    bp: int
    description_text: str
    stat_modifiers: set[StatModifier]

    def description(self):
        return self.description_text
