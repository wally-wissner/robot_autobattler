# import cx_Freeze
import json
import numpy as np
import pygame as pg
import sys

import scripts.backend.scenes as scenes
from scripts.utilities.singleton import Singleton


@Singleton
class Game(object):
    def __init__(self, title, gui=True):
        self.title = title
        self.gui = gui

        self.settings_file = "settings.json"
        self.settings = self.read_settings()

        self.delta_time = 0

        # test
        self.circle_position = pg.Vector2(self.settings["width"] / 2, self.settings["height"] / 2)

        # self.load_data()

        if self.gui:
            # Pygame setup.
            pg.init()
            self.display = pg.display.set_mode((self.settings["width"], self.settings["height"]))
            self.fps = self.settings["fps"]
            pg.display.set_caption(self.title)
            self.clock = pg.time.Clock()
            pg.key.set_repeat(500, 100)

        self.playing = True

        self.active_scene = scenes.MainMenuScene()

    def read_settings(self):
        with open(self.settings_file, 'r') as f:
            settings = json.load(f)
        return settings

    def save_settings(self, settings):
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

    def return_to_default_settings(self):
        settings = {
            "fps": 60,
            "width": 800,
            "height": 600,
        }
        self.save_settings(settings)

    def run(self):
        if self.gui:
            self.display.fill((0, 0, 0))
            while self.playing:
                self.delta_time = self.clock.tick(self.fps) / 1000
                self.handle_events()
                self.update()
                self.draw()


    def handle_events(self):
        for event in pg.event.get():
            self.active_scene.handle_event(event)

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

    def draw(self):

        self.circle_position += np.random.randn(2)
        pg.draw.circle(self.display, (0, 0, 255), self.circle_position, 25)
        # self.display.blit(bg, (0, 0))
        # pg.draw.rect()

        # self.state.draw()

    def relative_to_pygame(self, vec:pg.Vector2) -> pg.Vector2:
        return pg.Vector2()

    def pygame_to_relative(self, vec:pg.Vector2) -> pg.Vector2:
        width = self.settings["width"]
        height = self.settings["height"]
        return pg.Vector2(vec.x / width - .5, .5 - vec.y / height)

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
    g = Game(title="Robot RPG")
    g.run()
