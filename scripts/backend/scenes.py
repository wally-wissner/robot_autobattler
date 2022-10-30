import numpy as np
import pygame as pg


class Scene(object):
    def __init__(self, game):
        self.game = game

    def handle_event(self, inputs):
        raise NotImplemented()

    def draw(self):
        raise NotImplemented()


class MainMenuScene(Scene):
    def handle_event(self, inputs):
        # todo
        pass

    def draw(self):
        # todo
        pass


class SettingsMenuScene(Scene):
    def handle_event(self, inputs):
        # todo
        pass

    def draw(self):
        # todo
        pass


class UpgradeScene(Scene):
    def handle_event(self, inputs):
        # todo
        pass

    def draw(self):
        # todo
        pass


class BattleScene(Scene):
    def handle_event(self, inputs):
        # todo
        pass

    def draw(self):
        # todo
        pass


class TestScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.circle_position = pg.Vector2(
            self.game.settings["display_resolution"]["current"][0] / 2,
            self.game.settings["display_resolution"]["current"][1] / 2,
        )

    def handle_event(self, inputs):
        # todo
        pass

    def draw(self):
        self.circle_position += np.random.randn(2)
        pg.draw.circle(self.game.display, (255, 255, 255), self.circle_position, 4)
        pg.draw.circle(self.game.display, (0, 0, 255), self.circle_position, 3)
