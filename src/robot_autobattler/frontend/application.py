# *args and **kwargs needed for button interface compatibility.
# pylint: disable=no-member
# pylint: disable=too-many-instance-attributes
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import sys

import dill
import pygame
import pygame_gui

from _version import __title__, __version__
from config import absolute_path
from backend.game import Game
from backend.settings import SettingsManager
from utils.enums import EScene
from utils.singleton import Singleton


class Application(Singleton):
    """
    Application that allows player to interact with the game's frontend interface.
    """

    def __init__(self) -> None:
        super().__init__()

        self.title = __title__
        self.version = __version__

        self.game_save_path = absolute_path("player_data/save.pickle")

        # Game setup.
        self.game = Game(version=self.version, seed=0)

        self.title_font = None
        self.load_assets()

        self.settings_manager = SettingsManager()
        self.settings_manager.load()

        # pygame setup
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        pygame.init()
        pygame.display.set_caption(self.title)
        self.display = pygame.display.set_mode(self.settings_manager.resolution)
        self.ui_manager = pygame_gui.UIManager(
            window_resolution=self.settings_manager.resolution,
            # theme_path=None,
        )

        # Scene setup.
        self._scene_map: dict = {}
        self.start_scene_type = EScene.MAIN_MENU
        self._active_scene = None
        self._active_scene_stack: list[EScene] = []

    def load_assets(self) -> None:
        pygame.font.init()
        # pygame.display.set_icon()

    def run(self) -> None:
        self.change_scene(self.start_scene_type)
        while True:
            self.delta_time = self.clock.tick(60) / 1000.0

            # Event handling.
            mouse_position = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    func, kwargs = self._active_scene.buttons[event.ui_element]
                    func(**kwargs)

                self.ui_manager.process_events(event)

            # Drawing.
            self.display.blit(pygame.Surface(self.settings_manager.resolution), (0, 0))
            self._active_scene.draw()

            self.ui_manager.update(self.delta_time)
            self.ui_manager.draw_ui(self.display)

            pygame.display.update()

    def quit(self, *args, **kwargs) -> None:
        pygame.quit()
        sys.exit()

    def new_game(self, *args, **kwargs) -> None:
        self.game = Game(version=self.version, seed=0)
        self.game.start_encounter()
        self.change_scene(scene=EScene.BATTLE)

    def continue_game(self, *args, **kwargs) -> None:
        # TODO
        pass

    def load_game(self, *args, **kwargs) -> None:
        self.game = dill.load(self.game_save_path)

    def save_game(self, *args, **kwargs) -> None:
        dill.dump(self.game, self.game_save_path)

    def change_scene(self, scene: EScene, *args, **kwargs) -> None:
        self._active_scene_stack.append(scene)
        if self._active_scene:
            self._active_scene.disable()
        self._active_scene = self._scene_map[scene]()

    def return_to_previous_scene(self, *args, **kwargs) -> None:
        try:
            self._active_scene_stack.pop()
            self.change_scene(self._active_scene_stack[-1])
        except IndexError:
            pass

    def load_scene_map(self, scene_map: dict) -> None:
        self._scene_map = scene_map

    def resolution(self) -> tuple[int, int]:
        return self.settings_manager.resolution


application = Application()
game = application.game
