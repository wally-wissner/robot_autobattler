from dataclasses import dataclass
from typing import List, Set

from scripts.backend.unitstat import StatModifier
from scripts.utilities import enums


@dataclass
class Badge(object):
    name: str
    description: str
    rarity: enums.ERarity
    stat_modifiers: Set[StatModifier]


@dataclass
class CardAbilityCondition(object):
    variable: enums.EResource | enums.EVariable
    comparison: enums.EComparison
    threshold: enums.EVariable | bool | float | int
    consume_resource: bool
    actor: enums.EActorCategory | None = None
    target: enums.ETargetCategory | None = None


@dataclass
class CardAbilityEffect(object):
    actor_category: enums.EActorCategory
    actor_quantity: enums.EActorQuantity
    action: enums.EUnitAction
    target_category: enums.ETargetCategory | None = None
    target_quantity: enums.ETargetQuantity | None = None
    magnitude: int | None = None
    dispersion: float | None = None
    element: enums.EElement | None = None
    repetitions: int = 1


@dataclass
class CardAbility(object):
    conditions: List[CardAbilityCondition]
    effects: List[CardAbilityEffect]

    def get_text(self):
        # TODO
        pass


@dataclass
class Card(object):
    rarity: enums.ERarity
    abilities: List[CardAbility]


@dataclass
class UnitUpgrade(object):
    def __init__(self, badge, card):
        self.badge = badge
        self.card = card
