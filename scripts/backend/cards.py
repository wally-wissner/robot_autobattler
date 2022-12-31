from dataclasses import dataclass
from xml.etree import ElementTree

from scripts.utilities import enums


@dataclass
class Card(object):
    name: str
    rarity: enums.ERarity
    bp: int
    abilities: ElementTree

    def get_text(self) -> str:
        # TODO
        return ""


@dataclass
class CardAbilityCondition(object):
    variable: enums.EResource | enums.EVariable
    comparison: enums.EComparison
    threshold: enums.EVariable | bool | float | int
    consume_resource: bool

    def get_text(self) -> str:
        if self.consume_resource:
            return f"CONSUME {self.threshold} {self.variable}"
        else:
            return f"IF {self.variable} {self.comparison.value} {self.threshold}"


@dataclass
class CardAbilityEffect(object):
    actor_category: enums.EUnitCategory
    actor_quantity: enums.EUnitQuantity | int
    action: enums.EUnitAction
    values: list
    target_category: enums.EUnitCategory = None
    target_quantity: enums.EUnitQuantity | int = None
    dispersion: float = None
    element: enums.EElement = None
    repetitions: int = 1

    def get_text(self) -> str:
        if self.action == enums.EUnitAction.ATTACK:
            # TODO
            return ""
        if self.action == enums.EUnitAction.PRODUCE:
            # TODO
            return ""


@dataclass
class CardAbility(object):
    conditions: list[CardAbilityCondition]
    effects: list[CardAbilityEffect]

    def get_text(self) -> str:
        condition_texts = [condition.get_text() for condition in self.conditions]
        effect_texts = [effect.get_text() for effect in self.effects]
        if self.conditions:
            return " and ".join(condition_texts) + ":" + "\n\t" + "\n\t".join(effect_texts)
        else:
            return "\n".join(effect_texts)


@dataclass
class SimpleCard(object):
    name: str
    rarity: enums.ERarity
    bp: int
    abilities: list[CardAbility]

    def get_text(self) -> str:
        return "\n".join(ability.get_text() for ability in self.abilities)
