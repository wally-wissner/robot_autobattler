from dataclasses import dataclass

from backend.upgrade_components import UpgradeComponent
from backend.unitstat import StatModifier
from utils import enums


@dataclass
class Badge(UpgradeComponent):
    name: str
    rarity: enums.ERarity
    bp: int
    description_text: str
    stat_modifiers: set[StatModifier]

    def description(self):
        return self.description_text
