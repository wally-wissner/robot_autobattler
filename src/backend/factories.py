import numpy as np
from typing import Iterable

from src.backend.asset_loaders import badges, simple_cards
from src.backend.badges import Badge
from src.backend.cards import Card
from src.backend.team import Team
from src.backend.upgrades import Upgrade
from src.backend.unit import Unit
from src.utilities.enums import ERarity


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
) -> Card:
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


def generate_upgrade(
        rarity_range: Iterable[ERarity] = (ERarity.COMMON, ERarity.RARE),
        bp_range: Iterable[int] = (-np.inf, np.inf)
) -> Upgrade:
    badge = generate_badge(rarity_range, bp_range)
    card = generate_card(rarity_range, bp_range)
    upgrade = Upgrade(badge, card)
    return upgrade


def generate_unit(team: Team, level: int, quality: float) -> Unit:
    if not (0 <= quality <= 1):
        raise ValueError(f"Expected quality to be between 0 and 1. Received {quality}.")
    unit = Unit(team=team, level=level)
    while unit.bp_available() > 0:
        upgrade = generate_upgrade(bp_range=(-np.inf, unit.bp_available()))
        unit.add_upgrade(upgrade)
    return unit


def generate_team(is_player: bool, total_level: int, quality: float, n_units: int = None) -> Team:
    if not (0 <= quality <= 1):
        raise ValueError(f"Expected quality to be between 0 and 1. Received {quality}.")
    team = Team(is_player=is_player)
    for _ in range(n_units):
        unit = generate_unit(team=team, level=total_level//n_units, quality=quality)
        team.units.append(unit)
    return team
