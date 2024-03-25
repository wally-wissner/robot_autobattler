"""
Math and algorithmic helper functions.
"""


def clamp(value, min_value, max_value):
    """
    Clamp a value between the min allowed value and the max allowed value.
    """
    assert min_value <= max_value, "min_value must be less than or equal to max_value."
    return sorted([value, min_value, max_value])[1]


def can_shift(items: list, index: int, shift=1) -> bool:
    """
    Check if the index can be shifted by the given amount within the list while still remaining
    within the list.
    """
    return (0 <= index < len(items)) and (0 <= index + shift < len(items))


def try_shift(items: list, index: int, shift=1) -> bool:
    """
    If item can be shifted within list by the given amount, shift it.
    """
    shiftable = can_shift(items, index, shift)
    if shiftable:
        item = items.pop(index)
        items.insert(index + shift, item)
    return shiftable
