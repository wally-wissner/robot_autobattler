from scripts import Singleton


@Singleton
class Animator:
    def __init__(self):
        self.animate = True
        self.items_to_move = set()

    def animate_items(self):
        for item in self.items_to_move:
            if item.at_destination():
                self.items_to_move.pop(item)
