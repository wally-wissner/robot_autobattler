def clamp(value, min_value, max_value):
    assert min_value <= max_value, "min_value must be less than or equal to max_value."
    return sorted([value, min_value, max_value])[1]


def shift_item(items: list, index: int, shift=1) -> bool:
    can_shift = (0 <= index < len(items)) and (0 <= index + shift < len(items))
    if can_shift:
        item = items.pop(index)
        items.insert(index + shift, item)
    return can_shift
