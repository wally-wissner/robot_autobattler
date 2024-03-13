from itertools import count
from uuid import uuid4


class sequential_identifier(object):
    def __init__(self, cls):
        self.cls = cls
        self.cls.count = count()

    def __call__(self, *args, **kwargs):
        obj = self.cls(*args, **kwargs)
        obj.id = next(self.cls.count)
        return obj


class uuid_identifier(object):
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        obj = self.cls(*args, **kwargs)
        obj.id = uuid4()
        return obj
