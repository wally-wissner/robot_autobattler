import numpy as np
from typing import Iterable

from scripts.backend.asset_loaders import badges, cards, simple_cards
from scripts.backend.badges import Badge
from scripts.backend.cards import Card, SimpleCard
from scripts.backend.team import Team
from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.backend.unit import Unit
from scripts.utilities.enums import ERarity


class GenerationError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def random_rarity(min_rarity: ERarity = ERarity.COMMON, max_rarity: ERarity = ERarity.RARE) -> ERarity:
    defaults = {
        ERarity.COMMON: 11 / 15,
        ERarity.UNCOMMON: 3 / 15,
        ERarity.RARE: 1 / 15,
    }
    distribution = np.array([
        probability if min_rarity <= rarity <= max_rarity else 0
        for rarity, probability in defaults.items()
    ])
    distribution = distribution / distribution.sum()
    return np.random.choice(list(defaults.keys()), p=distribution)


def random_bp(min_bp: int = -np.inf, max_bp: int = np.inf) -> int:
    # TODO
    return 1


def generate_badge(
        rarity_range: Iterable[ERarity] = (ERarity.COMMON, ERarity.RARE),
        bp_range: Iterable[int] = (-np.inf, np.inf)
) -> Badge:
    rarity = random_rarity(*rarity_range)
    bp = random_bp(*bp_range)
    options = [
        badge
        for badge in badges
        if badge.rarity == rarity
        and badge.bp == bp
    ]
    badge = np.random.choice(options)
    return badge


def generate_card(
        rarity_range: Iterable[ERarity] = (ERarity.COMMON, ERarity.RARE),
        bp_range: Iterable[int] = (-np.inf, np.inf)
) -> SimpleCard:
    rarity = random_rarity(*rarity_range)
    bp = random_bp(*bp_range)
    options = [
        card
        for card in simple_cards
        if card.rarity == rarity
        and card.bp == bp
    ]
    card = np.random.choice(options)
    return card


def generate_unit_upgrade(
        rarity_range: Iterable[ERarity] = (ERarity.COMMON, ERarity.RARE),
        bp_range: Iterable[int] = (-np.inf, np.inf)
) -> UnitUpgrade:
    badge = generate_badge(rarity_range, bp_range)
    card = generate_card(rarity_range, bp_range)
    unit_upgrade = UnitUpgrade(badge, card)
    return unit_upgrade


def generate_unit(team: Team, level: int, quality: float) -> Unit:
    unit = Unit(team=team, level=level)
    return unit


def generate_team(is_player: bool = False, n_units: int = None, total_level: int = None, quality: int = None) -> Team:
    team = Team(is_player=is_player)
    for _ in range(n_units):
        unit = generate_unit(team=team, level=total_level//n_units, quality=quality)
        team.units.append(unit)
    return team
