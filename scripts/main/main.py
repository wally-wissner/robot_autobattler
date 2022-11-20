import pygame as pg
import sys
from pygame_gui.ui_manager import UIManager

import scripts.backend.scenes as scenes
from scripts.backend.settings import Settings
from scripts.frontend import colors
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
        self.manager = UIManager(self.settings.resolution)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        # Game setup.
        self.active_scene = scenes.MainMenuScene(self)
        self.delta_time = 0
        self.playing = True

    def run(self):
        self.display.fill(colors.blue)
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

    def relative_to_vector2(self, relative: pg.Vector2) -> pg.Vector2:
        relative = pg.Vector2(relative)
        resolution_width, resolution_height = self.settings.resolution
        return pg.Vector2(relative.x * resolution_width, (1 - relative.y) * resolution_height)

    def relative_to_rect(self, bottom_left: pg.Vector2, top_right: pg.Vector2) -> pg.Rect:
        vector2_bottom_left = self.relative_to_vector2(bottom_left)
        vector2_top_right = self.relative_to_vector2(top_right)
        difference = vector2_top_right - vector2_bottom_left
        return pg.Rect(
            (vector2_bottom_left.x, vector2_bottom_left.y + difference.y),
            (difference.x, -difference.y)
        )

    def vector2_to_relative(self, pixel: pg.Vector2) -> pg.Vector2:
        pixel = pg.Vector2(pixel)
        resolution_width, resolution_height = self.settings.resolution
        return pg.Vector2(pixel.x / resolution_width, 1 - pixel.y / resolution_height)

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
