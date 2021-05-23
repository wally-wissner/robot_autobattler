from enum import auto, Enum


class AutoNameEnum(Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self


if __name__ == "__main__":
    class Test(AutoNameEnum):
        a = auto()
        b = auto()

    print(Test.a)
    print(Test.b)
    print(Test.a == Test.a)
    print(Test.a == Test.b)
    print(Test.__getattr__("a"))
    print(Test.__getattr__(name="b"))
