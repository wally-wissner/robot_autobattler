import numpy as np
import pygame
import pygame_gui
from abc import ABC, abstractmethod
from pygame_gui.elements import UIButton, UIImage, UIPanel
from pygame_gui.elements.ui_window import UIWindow

from scripts.utilities.enums import EStat, EScene


class Scene(ABC):
    def __init__(self, application) -> None:
        self.application = application
        self.ui_elements = set()

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        raise NotImplemented()

    @abstractmethod
    def draw(self) -> None:
        raise NotImplemented()

    def disable(self) -> None:
        for ui_element in self.ui_elements:
            ui_element.hide()


class MainMenuScene(Scene):
    def __init__(self, application):
        super().__init__(application)

        self.buttons_container = UIPanel(
            relative_rect=self.application.relative_to_rect((.05, .05), (.95, .95)),
            starting_layer_height=0,
            manager=self.application.ui_manager,
        )
        self.ui_elements.add(self.buttons_container)

        self.button_continue = UIButton(
            relative_rect=self.application.relative_to_rect((.40, .65), (.60, .75)),
            text="Continue",
            manager=self.application.ui_manager,
            # container=self.buttons_container,
        )
        self.ui_elements.add(self.button_continue)

        self.button_new_game = UIButton(
            relative_rect=self.application.relative_to_rect((.40, .5), (.60, .6)),
            text="New Game",
            manager=self.application.ui_manager,
            # container=self.buttons_container,
        )
        self.ui_elements.add(self.button_new_game)


        settings_icon = pygame.image.load("../assets/images/ui/settings-icon.png").convert_alpha()
        self.button_settings = UIImage(
            self.application.relative_to_rect((.95, .01), (.99, .05)),
            settings_icon,
            manager=self.application.ui_manager,
            # container=self.buttons_container,
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button_new_game:
                    self.application.new_game()
                    self.application.change_scene("battle")
                if event.ui_element == self.button_continue:
                    self.application.load_game()
                    self.application.change_scene("battle")

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


class BattleScene(Scene):
    def __init__(self, application):
        super().__init__(application)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        for unit in self.application.game.units():
            pygame.draw.circle(
                surface=self.application.display,
                color=unit.color(),
                center=unit.position + np.array(self.application.settings.resolution) / 2,
                radius=self.application.game.unit_stat_value(unit, EStat.SIZE),
            )


class UpgradeScene(Scene):
    def __init__(self, application):
        super().__init__(application)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass


class TestScene(Scene):
    def __init__(self, application):
        super().__init__(application)

        self.circle_position = pygame.Vector2(
            self.application.settings.resolution[0] / 2,
            self.application.settings.resolution[1] / 2,
        )

        self.button_layout_rect = pygame.Rect((0, 0), (100, 30))

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
            if event.operation == pygame.KEYDOWN:
                key = event.key

                if key == pygame.K_LEFT:
                    self.circle_position += [-1, 0]
                if key == pygame.K_RIGHT:
                    self.circle_position += [1, 0]

            if event.operation == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                print(pos)
                # if sprite.get_rect().collidepoint(x, y):
                #     print('clicked on image')

            if event.operation == pygame.MOUSEBUTTONUP:
                pos = event.pos

    def draw(self):
        self.circle_position += np.random.randn(2)
        pygame.draw.circle(self.application.display, (255, 255, 255), self.circle_position, 4)
        pygame.draw.circle(self.application.display, (0, 0, 255), self.circle_position, 3)

        # self.display.blit(bg, (0, 0))
        # pg.draw.rect()

