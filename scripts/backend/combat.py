from scripts.backend.unit import Unit
from scripts.utilities.singleton import Singleton


@Singleton
class CombatManager(object):
    def __init__(self):
        self.level = 1
        self.round = 1
        self.turn = 1

    def start_level(self):
        self.level += 1

    def start_round(self):
        self.round += 1

    def start_turn(self):
        self.turn += 1

    def evaluate_active_cards(self):
        # TODO
        pass

    def evaluate_card(self, actor, card):
        for effect in card.abilities:
            self.evaluate_card_effect(actor, effect)

    def evaluate_card_effect(self, actor, effect):
        # TODO
        pass
