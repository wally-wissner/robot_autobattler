from uuid import uuid4


class SequentialIdentifier:
    count = 0

    def __init__(self):
        self.__class__.count += 1
        self.id = self.count


class UUIDIdentifier:
    def __init__(self):
        self.id = uuid4()
