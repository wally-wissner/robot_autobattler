from dataclasses import dataclass

from scripts.backend.unitstat import StatModifier
from scripts.utilities import enums


@dataclass
class Badge(object):
    name: str
    description_text: str
    rarity: enums.ERarity
    bp: int
    stat_modifiers: set[StatModifier]

    def description(self):
        return self.description_text
