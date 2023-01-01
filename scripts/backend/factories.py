import numpy as np

from scripts.backend.asset_loaders import badges, cards, simple_cards
from scripts.backend.badges import Badge
from scripts.backend.cards import Card, SimpleCard
from scripts.backend.team import Team
from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.backend.unit import Unit
from scripts.utilities import enums


class GenerationError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def random_rarity():
    options = {
        enums.ERarity.COMMON: 11 / 15,
        enums.ERarity.UNCOMMON: 3 / 15,
        enums.ERarity.RARE: 1 / 15,
    }
    return np.random.choice(options.keys(), p=options.values())


def generate_badge(rarity: enums.ERarity = None, bp: int = None) -> Badge:
    rarity = rarity if rarity else random_rarity()
    options = [
        badge
        for badge in badges
        if badge.rarity == rarity
        and badge.bp == bp or bp is None
    ]
    badge = np.random.choice(options)
    return badge


def generate_card(rarity: enums.ERarity = None, bp: int = None) -> SimpleCard:
    rarity = rarity if rarity else random_rarity()
    options = [
        card
        for card in simple_cards
        if card.rarity == rarity
        and card.bp == bp or bp is None
    ]
    card = np.random.choice(options)
    return card


def generate_unit_upgrade(rarity: enums.ERarity = None, bp: int = None) -> UnitUpgrade:
    if rarity == enums.ERarity.COMMON:
        rarities = [enums.ERarity.COMMON, enums.ERarity.COMMON]

    rarities = np.random.shuffle(rarities)
    # badge =
    # card =
    # unit_upgrade = UnitUpgrade(badge, card)
    # return unit_upgrade
    pass


def generate_unit(team, level: int, quality: int) -> Unit:
    unit = Unit(team=team, level=level)
    return unit


def generate_team(is_player: bool = False, units: int = None, total_level: int = None) -> Team:
    team = Team(is_player=is_player)
    return team
