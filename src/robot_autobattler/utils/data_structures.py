from collections import defaultdict
from functools import total_ordering


@total_ordering
class Inventory(defaultdict):
    def __init__(self) -> None:
        super().__init__(int)

    def add(self, item, quantity: int = 1) -> None:
        """
        Add a quantity of an item to the inventory.
        """
        self[item] += quantity

    def remove(self, item, quantity: int = 1) -> None:
        if quantity > self[item]:
            raise ValueError("Cannot remove more self.list than exist in Inventory.")
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


class ShiftList(list):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def can_shift(self, index: int, shift=1) -> bool:
        """
        Check if the index can be shifted by the given amount within the list while still remaining
        within the list.
        """
        return (0 <= index < len(self)) and (0 <= index + shift < len(self))

    def try_shift(self, index: int, shift=1) -> bool:
        """
        If item can be shifted within list by the given amount, shift it.
        """
        shiftable = self.can_shift(index, shift)
        if shiftable:
            item = self.pop(index)
            self.insert(index + shift, item)
        return shiftable
