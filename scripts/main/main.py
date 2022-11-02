# import cx_Freeze
import pygame as pg
import pygame_gui as gui
import sys

import scripts.backend.scenes as scenes
from scripts.backend.settings import Settings
from scripts.utilities.singleton import Singleton


title = "Robot Autobattler"
version = "0.0.1"


@Singleton
class Game(object):
    def __init__(self):
        self.title = title
        self.version = version

        self.settings = Settings()
        self.settings.load()

        # self.load_data()

        # Pygame setup.
        pg.init()
        self.display = pg.display.set_mode(self.settings.resolution)
        pg.display.set_caption(self.title)
        self.manager = gui.UIManager(self.settings.resolution)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        # Game setup.
        self.active_scene = scenes.TestScene(self)
        self.delta_time = 0
        self.playing = True

    def run(self):
        self.display.fill((0, 0, 0))
        while self.playing:
            self.delta_time = self.clock.tick(self.settings.fps) / 1000
            self.handle_events(pg.event.get())
            self.update()
            self.draw()
        self.quit()

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.quit()

        self.active_scene.handle_events(events)

    def update(self):
        pg.display.update()
        self.manager.update(self.delta_time)

    def draw(self):
        self.active_scene.draw()
        self.manager.draw_ui(self.display)

    def relative_to_vector2(self, relative) -> pg.Vector2:
        width, height = self.settings.resolution
        return pg.Vector2(relative[0] * width, (1 - relative[1]) * height)

    def relative_to_rect(self, top_left, bottom_right) -> pg.Rect:
        vector2_top_left = self.relative_to_vector2(top_left)
        vector2_bottom_right = self.relative_to_vector2(bottom_right)
        width = vector2_bottom_right.x - vector2_top_left.x
        height = vector2_top_left.y - vector2_bottom_right.y
        return pg.Rect(
            vector2_top_left,
            (width, height)
        )

    def vector2_to_relative(self, pixel) -> pg.Vector2:
        width, height = self.settings.resolution
        return pg.Vector2(pixel.x / width, 1 - pixel.y / height)

    def quit(self):
        pg.quit()
        sys.exit()

    def load_data(self):
        # TODO
        raise NotImplemented()

    def save_data(self):
        # TODO
        raise NotImplemented()


if __name__ == "__main__":
    game = Game.instance()
    game.run()
