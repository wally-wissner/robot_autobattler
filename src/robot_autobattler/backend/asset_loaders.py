"""
Utility functions to load game asset files into their respective data structures.
"""

import json
from typing import Any
from xml.etree.ElementTree import fromstring

from backend.badges import Badge
from backend.cards import (
    AdvancedCard,
    SimpleCard,
    CardAbility,
    CardAbilityCondition,
    CardAbilityEffect,
)
from backend.unitstat import StatModifier
from utils import enums
from config import absolute_path


def _convert(value, enum_options) -> Any:
    if not isinstance(enum_options, list):
        enum_options = [enum_options]
    if isinstance(value, str):
        for option in enum_options:
            try:
                return option[value]
            except KeyError:
                pass
        raise ValueError("Could not parse type of value.")
    return value


def _load_badges() -> list[Badge]:
    with open(absolute_path("assets/item_data/badges.json"), encoding="utf-8") as f:
        json_badges = json.load(f)
        _badges = [
            Badge(
                name=json_badge["name"],
                description_text=json_badge["description"],
                rarity=enums.ERarity[json_badge["rarity"]],
                bp=json_badge["bp"],
                stat_modifiers=set(
                    StatModifier(
                        stat=enums.EStat[stat],
                        operation=enums.EOperation[operation],
                        value=value,
                    )
                    for stat, operation, value in json_badge["stat_modifiers"]
                ),
            )
            for json_badge in json_badges
        ]
    return _badges


def _load_cards() -> list[AdvancedCard]:
    with open(absolute_path("assets/item_data/cards.xml"), encoding="utf-8") as f:
        tree = fromstring(f.read())
        _cards = [
            AdvancedCard(
                name=element.get("name"),
                rarity=enums.ERarity[element.get("rarity")],
                bp=int(element.get("bp")),
                abilities=element,
                cooldown=float(element.get("cooldown")),
            )
            for element in tree
        ]
    return _cards


def _load_simple_cards() -> list[SimpleCard]:
    with open(
        absolute_path("assets/item_data/simple_cards.json"), encoding="utf-8"
    ) as f:
        json_cards = json.load(f)
        _cards = []
        for json_card in json_cards:
            abilities = []
            for json_ability in json_card["abilities"]:
                conditions = [
                    CardAbilityCondition(
                        variable=_convert(
                            condition["variable"], [enums.EResource, enums.EVariable]
                        ),
                        comparison=_convert(
                            condition["comparison"], [enums.EComparison]
                        ),
                        threshold=_convert(
                            condition["threshold"], [enums.EVariable, float]
                        ),
                        consume_resource=_convert(condition["consume_resource"], bool),
                    )
                    for condition in json_ability["conditions"]
                ]
                success_effects = [
                    CardAbilityEffect(
                        actor_category=_convert(
                            effect["actor_category"], enums.EUnitCategory
                        ),
                        actor_quantity=_convert(
                            effect["actor_quantity"], [enums.EUnitQuantity, int]
                        ),
                        action=_convert(effect["action"], enums.EUnitAction),
                        value=_convert(effect["value"], list),
                        target_category=_convert(
                            effect["actor_category"], enums.EUnitCategory
                        ),
                        target_quantity=_convert(
                            effect["target_quantity"], [enums.EUnitQuantity, int]
                        ),
                        dispersion=_convert(effect["dispersion"], float),
                        weapon=_convert(effect["weapon"], enums.EWeapon),
                        repetitions=_convert(effect["repetitions"], int),
                    )
                    for effect in json_ability["success_effects"]
                ]
                failure_effects = [
                    CardAbilityEffect(
                        actor_category=_convert(
                            effect["actor_category"], enums.EUnitCategory
                        ),
                        actor_quantity=_convert(
                            effect["actor_quantity"], [enums.EUnitQuantity, int]
                        ),
                        action=_convert(effect["action"], enums.EUnitAction),
                        value=_convert(effect["value"], list),
                        target_category=_convert(
                            effect["actor_category"], enums.EUnitCategory
                        ),
                        target_quantity=_convert(
                            effect["target_quantity"], [enums.EUnitQuantity, int]
                        ),
                        dispersion=_convert(effect["dispersion"], float),
                        weapon=_convert(effect["weapon"], enums.EWeapon),
                        repetitions=_convert(effect["repetitions"], int),
                    )
                    for effect in json_ability["failure_effects"]
                ]
                ability = CardAbility(
                    conditions=conditions,
                    success_effects=success_effects,
                    failure_effects=failure_effects,
                )
                abilities.append(ability)
            card = SimpleCard(
                name=json_card["name"],
                rarity=enums.ERarity[json_card["rarity"]],
                bp=json_card["bp"],
                abilities=abilities,
                cooldown=json_card["cooldown"],
            )
            _cards.append(card)
    return _cards


badges = _load_badges()
cards = _load_cards()
simple_cards = _load_simple_cards()
