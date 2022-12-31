import json
from xml.etree.ElementTree import fromstring

from scripts.backend.badges import Badge
from scripts.backend.cards import Card, SimpleCard, CardAbility, CardAbilityCondition, CardAbilityEffect
from scripts.backend.unitstat import StatModifier
from scripts.utilities import enums
from scripts.utilities.structure import absolute_path


def load_badges() -> list[Badge]:
    with open(absolute_path("assets/item_data/badges.json")) as f:
        json_badges = json.load(f)
        badges = [
            Badge(
                name=json_badge["name"],
                description=json_badge["description"],
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
    return badges


def load_cards() -> list[Card]:
    with open(absolute_path("assets/item_data/cards.xml")) as f:
        tree = fromstring(f.read())
        cards = [
            SimpleCard(
                name=element.get("name"),
                rarity=enums.ERarity[element.get("rarity")],
                bp=int(element.get("bp")),
                abilities=element,
            )
            for element in tree
        ]
    return cards


def load_simple_cards() -> list[SimpleCard]:
    with open(absolute_path("assets/item_data/simple_cards.json")) as f:
        json_cards = json.load(f)
        cards = []
        for json_card in json_cards:
            abilities = []
            for json_ability in json_card["abilities"]:
                conditions = [
                    CardAbilityCondition(

                    )
                    for condition in json_ability["conditions"]
                ]
                effects = [
                    CardAbilityEffect(

                    )
                    for effect in json_ability["effects"]
                ]
                ability = CardAbility(
                    conditions=conditions,
                    effects=effects,
                )
                abilities.append(ability)
            card = SimpleCard(
                name=json_card["name"],
                rarity=enums.ERarity[json_card["rarity"]],
                bp=json_card["bp"],
                abilities=abilities,
            )
            cards.append(card)
    return cards


badges = load_badges()
cards = load_cards()
simple_cards = load_simple_cards()


if __name__ == "__main__":
    print(badges)
    print(cards)
    print(simple_cards)
