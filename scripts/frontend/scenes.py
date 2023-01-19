import numpy as np
import pygame as pg
from abc import ABC, abstractmethod
from pygame_gui.elements import UIButton, UIImage, UIPanel
from pygame_gui.elements.ui_window import UIWindow

from scripts.utilities.enums import EStat


class Scene(ABC):
    def __init__(self, application):
        self.application = application

    @abstractmethod
    def handle_events(self, events: list[pg.event.Event]):
        raise NotImplemented()

    @abstractmethod
    def draw(self):
        raise NotImplemented()


class MainMenuScene(Scene):
    def __init__(self, application):
        super().__init__(application)

        self.buttons_container = UIPanel(
            relative_rect=self.application.relative_to_rect((.05, .05), (.95, .95)),
            starting_layer_height=0,
            manager=self.application.ui_manager,
        )

        self.button_new_game = UIButton(
            relative_rect=self.application.relative_to_rect((.40, .65), (.60, .75)),
            text="Continue",
            manager=self.application.ui_manager,
            # container=self.buttons_container,
        )

        self.button_new_game = UIButton(
            relative_rect=self.application.relative_to_rect((.40, .5), (.60, .6)),
            text="New Game",
            manager=self.application.ui_manager,
            # container=self.buttons_container,
        )

        settings_icon = pg.image.load("../assets/images/ui/settings-icon.png").convert_alpha()
        self.button_settings = UIImage(
            self.application.relative_to_rect((.95, .95), (.99, .99)),
            settings_icon,
            manager=self.application.ui_manager,
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
    def __init__(self, application):
        super().__init__(application)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass


class UpgradeScene(Scene):
    def __init__(self, application):
        super().__init__(application)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass


class BattleScene(Scene):
    def __init__(self, application):
        super().__init__(application)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        for unit in self.application.game.units():
            pg.draw.circle(
                surface=self.application.display,
                color=unit.color(),
                center=unit.position + np.array(self.application.settings.resolution) / 2,
                radius=self.application.game.unit_stat_value(unit, EStat.SIZE),
            )


class TestScene(Scene):
    def __init__(self, application):
        super().__init__(application)

        self.circle_position = pg.Vector2(
            self.application.settings.resolution[0] / 2,
            self.application.settings.resolution[1] / 2,
        )

        self.button_layout_rect = pg.Rect((0, 0), (100, 30))

        self.button = UIButton(
            relative_rect=self.button_layout_rect,
            text="Hello",
            manager=self.application.ui_manager,
            # container=gui.elements.CON,
        )

        self.button_new_game = UIButton(
            relative_rect=self.application.relative_to_rect((.40, .5), (.60, .6)),
            text="New Game",
            manager=self.application.ui_manager,
        )

    def handle_events(self, events):
        for event in events:
            if event.operation == pg.KEYDOWN:
                key = event.key

                if key == pg.K_LEFT:
                    self.circle_position += [-1, 0]
                if key == pg.K_RIGHT:
                    self.circle_position += [1, 0]

            if event.operation == pg.MOUSEBUTTONDOWN:
                pos = event.pos
                print(pos)
                # if sprite.get_rect().collidepoint(x, y):
                #     print('clicked on image')

            if event.operation == pg.MOUSEBUTTONUP:
                pos = event.pos

    def draw(self):
        self.circle_position += np.random.randn(2)
        pg.draw.circle(self.application.display, (255, 255, 255), self.circle_position, 4)
        pg.draw.circle(self.application.display, (0, 0, 255), self.circle_position, 3)

        # self.display.blit(bg, (0, 0))
        # pg.draw.rect()

