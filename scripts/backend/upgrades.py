from dataclasses import dataclass
from typing import List

from scripts.utilities.enums import (
    EActorCategory,
    EElement,
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


@dataclass
class CardEffect(object):
    name: str
    actor: EActorCategory
    condition:
    action_when: EUnitAction  # Action taken if condition is met
    action_else: EUnitAction  # Action taken if condition is not met
    repetitions: int
    resources_present_to_use: List[EResource]
    resources_consumed_to_use: List[EResource]
    magnitude: int | None = None
    dispersion: float | None = None
    element: EElement | None = None
    target: ETargetCategory | None = None

    """
    Allow for multiple cases?
    
    condition = quantity, comparison, threshold
    
    if possess/consume 3 energy:
        deal 5 laser damage
    else:
        deal 2 laser damage
    """


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
