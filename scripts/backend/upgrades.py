from dataclasses import dataclass

from scripts.backend.unitstat import StatModifier
from scripts.utilities import enums
from scripts.utilities.identifiers import universal


@dataclass
class Badge(object):
    name: str
    description: str
    rarity: enums.ERarity
    stat_modifiers: set[StatModifier]
    bp: int


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
    conditions: list[CardAbilityCondition]
    effects: list[CardAbilityEffect]

    def get_text(self):
        # TODO
        pass


@dataclass
class Card(object):
    rarity: enums.ERarity
    abilities: list[CardAbility]
    bp: int


@dataclass
@universal
class UnitUpgrade(object):
    badge: Badge
    card: Card
    removable: bool = True

    @property
    def rarity(self):
        return max(self.badge.rarity, self.card.rarity)

    @property
    def bp(self):
        min_negative_bp = min(bp for bp in [0, self.badge.bp, self.card.bp] if bp <= 0)
        max_positive_bp = max(bp for bp in [0, self.badge.bp, self.card.bp] if bp >= 0)
        return max_positive_bp + min_negative_bp
