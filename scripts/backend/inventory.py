from collections import defaultdict
from functools import total_ordering


@total_ordering
class Inventory(defaultdict):
    def __init__(self):
        super().__init__(int)

    def add(self, item, quantity=1):
        self[item] += quantity

    def remove(self, item, quantity=1):
        if quantity > self[item]:
            raise ValueError("Cannot remove more items than exist in Inventory.")
        else:
            self[item] -= quantity
            if self[item] == 0:
                self.__delitem__(item)

    def __or__(self, other):
        for i in other:
            self[i] += other[i]

    def __le__(self, other):
        return all(self[i] <= other[i] for i in self)

    def __eq__(self, other):
        return self <= other <= self

    def __repr__(self):
        return f"Inventory({dict(self)})"


if __name__ == "__main__":
    a = Inventory()
    b = Inventory()

    a.add("Sword")
    a.add("Shield", 4)

    b.add("Sword", 2)
    b.add("Shield", 5)

    print(a)
    print(b)
    print(b >= a)

    a.remove("Sword")
    print(a)

    a.remove("Sword")
