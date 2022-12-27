import unittest

from scripts.backend.factories import *
from scripts.utilities import enums


class TestUnitUpgrade(unittest.TestCase):
    def setUp(self):
        self.rarity_badges = {
            rarity: generate_badge(rarity=rarity)
            for rarity in enums.ERarity
        }

    def test_rarity(self):
        self.assertTrue(len(self.rarity_badges) > 0)

        for rarity in enums.ERarity:
            self.assertTrue(self.rarity_badges[rarity].rarity == rarity)
