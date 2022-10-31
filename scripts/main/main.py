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
            self.handle_events()
            self.update()
            self.draw()
        self.quit()

    def handle_events(self):
        for event in pg.event.get():
            # self.active_scene.handle_event(event)

            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYDOWN:
                key = event.key

                if key == pg.K_LEFT:
                    self.circle_position += [-1, 0]
                if key == pg.K_RIGHT:
                    self.circle_position += [1, 0]

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = event.pos
                print(pos)
                # if sprite.get_rect().collidepoint(x, y):
                #     print('clicked on image')

            if event.type == pg.MOUSEBUTTONUP:
                pos = event.pos

    def update(self):
        pg.display.update()
        self.manager.update(self.delta_time)

    def draw(self):
        self.active_scene.draw()
        self.manager.draw_ui(self.display)

    def relative_to_pygame(self, relative) -> pg.Vector2:
        width, height = self.settings.resolution
        return pg.Vector2(relative[0] * width, (1 - relative[1]) * height)

    def pygame_to_relative(self, pixel) -> pg.Vector2:
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
