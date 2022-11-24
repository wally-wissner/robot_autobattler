from dataclasses import dataclass
from typing import List

from scripts.utilities.enums import (
    EActorCategory,
    ERarity,
    EResource,
    ETargetCategory,
    EUnitAction,
)


@dataclass
class Badge(object):
    name: str
    description: str
    rarity: ERarity
    stat_modifiers: list

    def __init__(self, name, description, stat_modifiers):
        self.stat_modifiers = stat_modifiers


@dataclass
class CardEffect(object):
    name: str
    actor: EActorCategory
    action: EUnitAction
    repetitions: int = 1
    magnitude: int | None = None
    dispersion: float | None = None
    element: E | None = None
    target: ETargetCategory | None = None
    resources_present_to_use: List[EResource]
    resources_consumed_to_use: List[EResource]

    def get_text(self):
        pass


@dataclass
class Card(object):
    rarity: ERarity

    def __init__(self):
        self.effects = []


@dataclass
class UnitUpgrade(object):
    def __init__(self, badge, card):
        self.badge = badge
        self.card = card


