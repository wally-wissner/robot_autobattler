def clamp(x, min_value, max_value):
    assert min_value <= max_value, "min_value must be less than or equal to max_value."
    return sorted([x, min_value, max_value])[1]
