from collections import defaultdict
from functools import total_ordering


@total_ordering
class Inventory(defaultdict):
    def __init__(self):
        super().__init__(int)

    def add(self, item, quantity: int = 1):
        """
        Add a quantity of an item to the inventory.
        """
        self[item] += quantity

    def remove(self, item, quantity: int = 1):
        if quantity > self[item]:
            raise ValueError("Cannot remove more items than exist in Inventory.")
        else:
            self[item] -= quantity
            if self[item] == 0:
                del self[item]

    def __or__(self, other):
        for i in other:
            self[i] += other[i]

    def __le__(self, other):
        return all(self[i] <= other[i] for i in self)

    def __eq__(self, other):
        return self <= other <= self

    def __repr__(self):
        return f"Inventory({dict(self)})"
