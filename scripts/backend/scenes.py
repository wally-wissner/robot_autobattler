import numpy as np
import pygame as pg
from pygame_gui.elements import UIButton, UIImage, UIPanel
from pygame_gui.elements.ui_window import UIWindow


class Scene(object):
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        raise NotImplemented()

    def draw(self):
        raise NotImplemented()


class MainMenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.buttons_container = UIPanel(
            relative_rect=self.game.relative_to_rect((.05, .05), (.95, .95)),
            starting_layer_height=0,
            manager=self.game.manager,
        )

        self.button_new_game = UIButton(
            relative_rect=self.game.relative_to_rect((.40, .65), (.60, .75)),
            text="Continue",
            manager=self.game.manager,
            # container=self.buttons_container,
        )

        self.button_new_game = UIButton(
            relative_rect=self.game.relative_to_rect((.40, .5), (.60, .6)),
            text="New Game",
            manager=self.game.manager,
            # container=self.buttons_container,
        )

        settings_icon = pg.image.load("../../assets/images/ui/settings-icon.png").convert_alpha()
        self.button_settings = UIImage(
            self.game.relative_to_rect((.95, .95), (.99, .99)),
            settings_icon,
            manager=self.game.manager,
            # container=self.buttons_container,
        )

    def handle_events(self, events):
        # for event in events:
        #     if event.ui_element == self.
        # todo
        pass

    def draw(self):
        # todo
        pass


class SettingsMenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass


class UpgradeScene(Scene):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass


class BattleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
    
    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass


class TestScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.circle_position = pg.Vector2(
            self.game.settings.resolution[0] / 2,
            self.game.settings.resolution[1] / 2,
        )

        self.button_layout_rect = pg.Rect((0, 0), (100, 30))

        self.button = UIButton(
            relative_rect=self.button_layout_rect,
            text="Hello",
            manager=self.game.manager,
            # container=gui.elements.CON,
        )

        self.button_new_game = UIButton(
            relative_rect=self.game.relative_to_rect((.40, .5), (.60, .6)),
            text="New Game",
            manager=self.game.manager,
        )

    def handle_events(self, events):
        for event in events:
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

    def draw(self):
        self.circle_position += np.random.randn(2)
        pg.draw.circle(self.game.display, (255, 255, 255), self.circle_position, 4)
        pg.draw.circle(self.game.display, (0, 0, 255), self.circle_position, 3)

        # self.display.blit(bg, (0, 0))
        # pg.draw.rect()

