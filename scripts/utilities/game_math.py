def clamp(x, min_value, max_value):
    assert min_value <= max_value, "min_value must be less than or equal to max_value."
    return sorted([x, min_value, max_value])[1]


def move_forward(items, index):
    if len(items) == 0:
        return ValueError("No items found.")
    if index != 0:
        items[index - 1], items[index] = items[index], items[index - 1]


def move_backward(items, index):
    if len(items) == 0:
        return ValueError("No items found.")
    if index != len(items - 1):
        items[index], items[index + 1] = items[index + 1], items[index]
