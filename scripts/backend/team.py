import numpy as np
from collections import deque
from dataclasses import dataclass

from scripts.backend.cards import Card
from scripts.backend.inventory import Inventory
from scripts.backend.unit import Unit
from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.utilities.enums import ECollectable
from scripts.utilities.geometry import Vector2


@dataclass(eq=True, order=True)
class CardIndex:
    i_unit: int
    i_unit_upgrade: int


class Team(object):
    def __init__(self, is_player: bool):
        self.is_player: bool = is_player
        self.units: list[Unit] = []
        self.unit_upgrades: Inventory[UnitUpgrade, int] = Inventory()
        self.collectables: Inventory[ECollectable, int] = Inventory()

        self.library: deque[Card] = deque()
        self.hand: deque[Card] = deque()
        self.graveyard: deque[Card] = deque()

    def card_order(self) -> dict[Card, CardIndex]:
        return {
            unit_upgrade.card: CardIndex(i_unit, i_unit_upgrade)
            for i_unit, unit in enumerate(self.units)
            for i_unit_upgrade, unit_upgrade in enumerate(unit.unit_upgrades)
        }

    def card_actor(self, card: Card) -> Unit:
        return self.units[self.card_order()[card].i_unit]

    def build_library(self) -> None:
        library = deque(self.card_order())
        np.random.shuffle(library)
        self.library = library

    def refresh_library(self) -> None:
        self.library = self.library + self.graveyard
        np.random.shuffle(self.library)
        self.graveyard = deque()

    def draw_cards(self, n_cards) -> None:
        for _ in range(n_cards):
            try:
                if not self.library and self.graveyard:
                    self.refresh_library()
                card = self.library.popleft()
                self.hand.append(card)
            except IndexError:
                pass

    def build_hand(self, n_cards) -> None:
        self.draw_cards(n_cards)
        card_order = self.card_order()
        self.hand = sorted(self.hand, key=lambda card: card_order[card])
