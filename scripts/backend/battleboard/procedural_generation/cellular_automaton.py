import numpy as np

from scripts.backend.battleboard.topology.discrete_topology import Tile, Tiling


class CellularAutomaton(object):
    def __init__(self, birth_limit:int, death_limit:int, iterations:int, seed=None):
        self.birth_limit = birth_limit
        self.death_limit = death_limit
        self.iterations = iterations
        self.seed = seed

        self.hexs = {}

    def iteration_rule(self):
        raise  NotImplemented()

    def validate(self):
        raise  NotImplemented()

    def iterate(self):
        raise  NotImplemented()

    def update_connected_components(self):
        raise  NotImplemented()

    def initialize(self):
        raise  NotImplemented()
