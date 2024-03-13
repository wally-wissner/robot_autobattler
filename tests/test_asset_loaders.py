import unittest

from src.scripts.backend.asset_loaders import badges, cards, simple_cards


class TestAssetLoaders(unittest.TestCase):
    def test_loaded(self):
        self.assertGreater(len(badges), 0)
        self.assertGreater(len(cards), 0)
        self.assertGreater(len(simple_cards), 0)
