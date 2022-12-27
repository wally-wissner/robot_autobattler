import json
import numpy as np

from scripts.backend.team import Team
from scripts.backend.upgrades import Badge, Card, UnitUpgrade
from scripts.backend.unit import Unit
from scripts.backend.unitstat import StatModifier
from scripts.utilities import enums
from scripts.utilities.structure import absolute_path


_rarity_distribution = {
    enums.ERarity.COMMON: 11/15,
    enums.ERarity.UNCOMMON: 3/15,
    enums.ERarity.RARE: 1/15,
}


def _load_badges() -> list[Badge]:
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


def _load_cards() -> list[Card]:
    # json.load(absolute_path("assets/item_data/cards.json"))
    pass


_badges = _load_badges()
# _cards = _load_cards()
print(_badges)


def generate_badge(rarity: enums.ERarity = None, bp: int = None) -> Badge:
    p = np.array([
        (_rarity_distribution[option.rarity])
        * (option.rarity == rarity or rarity is None)
        * (option.bp == bp or bp is None)
        for option in _badges
    ])
    p = p / p.sum()
    badge = np.random.choice(_badges, p=p)
    return badge


def generate_card(rarity: enums.ERarity = None, bp: int = None) -> Card:
    # card =
    # return card
    pass


def generate_unit_upgrade(rarity: enums.ERarity = None, bp: int = None) -> UnitUpgrade:
    # badge =
    # card =
    # unit_upgrade = UnitUpgrade(badge, card)
    # return unit_upgrade
    pass


def generate_unit(team, level: int) -> Unit:
    unit = Unit(team=team, level=level)
    return unit


def generate_team(is_player: bool = False, units: int = None, total_level: int = None) -> Team:
    team = Team(is_player=is_player)
    return team
