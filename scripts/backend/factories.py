import numpy as np

from scripts.backend.asset_loaders import badges, cards, simple_cards
from scripts.backend.badges import Badge
from scripts.backend.cards import Card, SimpleCard
from scripts.backend.team import Team
from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.backend.unit import Unit
from scripts.utilities import enums


_rarity_distribution = {
    enums.ERarity.COMMON: 11/15,
    enums.ERarity.UNCOMMON: 3/15,
    enums.ERarity.RARE: 1/15,
}


class GenerationError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def generate_badge(rarity: enums.ERarity = None, bp: int = None) -> Badge:
    p = np.array([
        (_rarity_distribution[option.rarity])
        * (option.rarity == rarity or rarity is None)
        * (option.bp == bp or bp is None)
        for option in badges
    ])
    p = p / p.sum()
    badge = np.random.choice(badges, p=p)
    return badge


def generate_card(rarity: enums.ERarity = None, bp: int = None) -> SimpleCard:
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
