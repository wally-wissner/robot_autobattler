import unittest
from src.backend.inventory import Inventory


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.a = Inventory()
        self.b = Inventory()

        self.a.add("Sword")
        self.a.add("Shield", 4)

        self.b.add("Sword", 2)
        self.b.add("Shield", 5)

    def test_inequality(self):
        self.assertTrue(self.b >= self.a)

    def test_remove(self):
        self.a.remove("Sword")

        self.assertRaises(ValueError, Inventory.remove, self.a, "Sword")
