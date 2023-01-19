def clamp(value, min_value, max_value):
    assert min_value <= max_value, "min_value must be less than or equal to max_value."
    return sorted([value, min_value, max_value])[1]


def move_forward(items: list, index: int) -> None:
    if len(items) == 0:
        raise ValueError("No items found.")
    try:
        items[index - 1], items[index] = items[index], items[index - 1]
    except IndexError:
        pass


def move_backward(items: list, index: int) -> None:
    if len(items) == 0:
        raise ValueError("No items found.")
    try:
        items[index], items[index + 1] = items[index + 1], items[index]
    except IndexError:
        pass
