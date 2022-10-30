# import cx_Freeze
import json
import pygame as pg
import pygame_gui as gui
import sys

import scripts.backend.scenes as scenes
from scripts.utilities.singleton import Singleton

title = "Robot Autobattler"
version = "0.0.1"

@Singleton
class Game(object):
    def __init__(self):
        self.title = title
        self.version = version

        self.settings_file = "settings.json"
        self.settings = self.load_settings()

        self.delta_time = 0

        # self.load_data()

        # Pygame setup.
        pg.init()
        self.display = pg.display.set_mode((self.settings["display_resolution"]["current"][0], self.settings["display_resolution"]["current"][1]))
        self.fps = self.settings["fps"]["current"]
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.playing = True

        self.active_scene = scenes.TestScene(self)

    def load_settings(self):
        with open(self.settings_file, 'r') as f:
            settings = json.load(f)
        return settings

    def save_settings(self, settings):
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

    def return_to_default_settings(self):
        settings = self.load_settings()
        for setting in settings:
            settings["current"] = settings["default"]
        self.save_settings(settings)

    def run(self):
        self.display.fill((0, 0, 0))
        while self.playing:
            self.delta_time = self.clock.tick(self.fps) / 1000
            self.handle_events()
            self.update()
            self.draw()

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

    def draw(self):
        self.active_scene.draw()

        # self.display.blit(bg, (0, 0))
        # pg.draw.rect()

        button_layout_rect = pg.Rect(30, 20, 100, 20)

        # manager = gui.UIManager((800, 600))
        # gui.elements.UIButton(
        #     relative_rect=button_layout_rect,
        #     text='Hello',
        #     manager=manager,
        #     container=self,
        # )

        # self.state.draw()

    def relative_to_pygame(self, vec: pg.Vector2) -> pg.Vector2:
        return pg.Vector2()

    def pygame_to_relative(self, vec: pg.Vector2) -> pg.Vector2:
        width, height = self.settings["display_resolution"]
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
    g = Game.instance()
    g.run()
