class Singleton:
    _instance = None

    def __init__(self):
        pass

    def __call__(self):
        if not self._instance:
            self._instance = self
        return self._instance
