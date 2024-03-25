import unittest

import numpy as np

from backend.factories import generate_team


class TestTeam(unittest.TestCase):
    def setUp(self):
        np.random.seed(0)
        self.team = generate_team(
            is_player=False, total_level=12, n_units=3, quality=0.75
        )

    def test_levels(self):
        for unit in self.team.units:
            self.assertGreater(unit.level, 0)

    def test_upgrades(self):
        for unit in self.team.units:
            self.assertGreater(len(unit.upgrades), 0)
