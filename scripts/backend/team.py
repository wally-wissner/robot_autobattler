from scripts.backend.inventory import Inventory


class Team(object):
    def __init__(self, ai=None, currency=0):
        self.ai = ai
        self.player = ai is not None
        self.currency = currency
        self.units = {}
        self.inventory_upgrades = Inventory()

    def win(self):
        # TODO
        raise NotImplemented()

    def lose(self):
        # TODO
        raise NotImplemented()


    def end_turn(self):
        for unit in self.units:
            unit.on_turn_end()
