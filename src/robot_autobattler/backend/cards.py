from dataclasses import dataclass
from xml.etree import ElementTree

from frontend import colors
from utils import enums
from backend.upgrade_components import UpgradeComponent


@dataclass(frozen=True)
class Card(UpgradeComponent):
    name: str
    rarity: enums.ERarity
    bp: int
    windup: int

    def description(self):
        return self.name

    def color(self) -> colors.ColorRGB:
        return colors.CARD


@dataclass(frozen=True)
class AdvancedCard(Card):
    abilities: ElementTree

    def description(self) -> str:
        # TODO
        return self.name


@dataclass
class CardAbilityCondition:
    variable: enums.EResource | enums.EVariable
    comparison: enums.EComparison
    threshold: enums.EVariable | float
    consume_resource: bool

    def description(self) -> str:
        if self.consume_resource:
            text = f"CONSUME {self.threshold} {self.variable}"
        else:
            text = f"IF {self.variable} {self.comparison.value} {self.threshold}"
        return text


@dataclass
class CardAbilityEffect:
    actor_category: enums.EUnitCategory
    actor_quantity: enums.EUnitQuantity | int
    action: enums.EUnitAction
    value: float
    target_category: enums.EUnitCategory = None
    target_quantity: enums.EUnitQuantity | int = None
    dispersion: float = None
    weapon: enums.EWeapon = None
    repetitions: int = 1

    def get_text(self) -> str:
        if self.action == enums.EUnitAction.ATTACK:
            # TODO
            text = ""
        if self.action == enums.EUnitAction.PRODUCE:
            # TODO
            text = ""
        text = "lorem ipsum"
        return text


@dataclass
class CardAbility:
    conditions: list[CardAbilityCondition]
    success_effects: list[CardAbilityEffect]
    failure_effects: list[CardAbilityEffect]

    def get_text(self) -> str:
        condition_texts = [condition.description() for condition in self.conditions]
        effect_texts = [effect.get_text() for effect in self.success_effects]
        # TODO
        if self.conditions:
            text = (
                " and ".join(condition_texts) + ":" + "\n\t" + "\n\t".join(effect_texts)
            )
        else:
            text = "\n".join(effect_texts)
        return text


@dataclass(frozen=True)
class SimpleCard(Card):
    abilities: list[CardAbility]

    def get_text(self) -> str:
        return "\n".join(ability.get_text() for ability in self.abilities)
