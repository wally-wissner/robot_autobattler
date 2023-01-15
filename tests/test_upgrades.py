import numpy as np
import unittest

from scripts.backend.factories import generate_badge, generate_card, generate_unit_upgrade
from scripts.utilities import enums


class TestUnitUpgrade(unittest.TestCase):
    def setUp(self):
        np.random.seed(0)
        self.rarity_badges = {
            rarity: generate_badge(rarity_range=(rarity, rarity))
            for rarity in enums.ERarity
        }

    def test_badge_rarity(self):
        for rarity in enums.ERarity:
            self.assertEqual(self.rarity_badges[rarity].rarity, rarity)
