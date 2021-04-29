import pygame as pg


class Queue(object):
    def __init__(self, iterable=list()):
        self._queue = list(iterable)

    def pop(self):
        return self._queue.pop()

    def append(self, item):
        self._queue.append(item)

    def extend(self, iterable):
        self._queue.extend(iterable)

    def __getitem__(self, item):
        return self._queue[item]


class ScreenObject(object):
    def __init__(self, position=pg.math.Vector2()):
        self.position = position
        self.destination = position
        self.moving = False

    def move(self, destination, speed=None, duration=None):
        try:
            assert speed or duration
        except AssertionError:
            raise ValueError("Must specify speed of motion or time to execute motion.")

        self.moving = True
        while self.position

    def move_dt(self, dt):



    def at_destination(self, tolerance=1e-6):
        return abs(self.position - self.destination) < tolerance