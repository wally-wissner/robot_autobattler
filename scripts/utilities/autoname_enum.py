from enum import auto, Enum


class AutoNameEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


if __name__ == "__main__":
    class Test(AutoNameEnum):
        a = auto()
