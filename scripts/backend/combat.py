from scripts.backend.unit import Unit
from scripts.utilities.singleton import Singleton


@Singleton
class CombatManager(object):
    def __init__(self):
        self.round = 0
        self.turn = 0

    def start_round(self):
        self.round += 1

    def start_turn(self):
        self.turn += 1

    def evaluate_active_cards(self):
        # TODO
        pass

    def evaluate_card(self, actor, card):
        for effect in card.effects:
            self.evaluate_card_effect(actor, effect)

    def evaluate_card_effect(self, actor, effect):
        # TODO
        pass
