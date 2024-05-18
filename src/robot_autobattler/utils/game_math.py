"""
Math and algorithmic helper functions.
"""


def clamp(value, min_value, max_value):
    """
    Clamp a value between the min allowed value and the max allowed value.
    """
    assert min_value <= max_value, "min_value must be less than or equal to max_value."
    return sorted([value, min_value, max_value])[1]
