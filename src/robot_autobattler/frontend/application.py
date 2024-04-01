# *args and **kwargs needed for button interface compatibility.
# pylint: disable=no-member
# pylint: disable=unused-argument

import dill
import pygame

# import pygame_gui

from _version import __title__, __version__
from config import absolute_path
from backend.game import Game
from backend.settings import SettingsManager
from utils.enums import EScene
from utils.geometry import Vector2
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
        self.delta_time = 0

        self.default_font = None
        self.load_assets()

        self.settings = SettingsManager(application=self)
        self.settings.load()

        pygame.init()
        pygame.display.set_caption(self.title)
        self.display = pygame.display.set_mode(self.settings.resolution)

        # self.display.on_draw = self.on_draw
        # self.display.on_update = self.on_update

        # Scene setup.
        self._scene_map: dict = {}
        self._active_scene = None
        self._active_scene_stack: list[EScene] = []

    def load_assets(self) -> None:
        pygame.font.init()
        self.default_font = pygame.font.Font(
            absolute_path("assets/fonts/JETBRAINS_MONO_REGULAR.ttf")
        )
        # pygame.display.set_icon()

    def on_update(self, delta_time) -> None:
        self.delta_time = delta_time

    def on_draw(self) -> None:
        self.display.clear()
        self._active_scene.draw()
        # self.active_scene.ui_manager.draw()

    def run(self) -> None:
        # self.change_scene(EScene.BATTLE)
        done = False
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        white = (255, 255, 255)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            pygame.draw.rect(self.display, red, pygame.Rect(100, 30, 60, 60))
            pygame.draw.polygon(
                self.display,
                blue,
                ((25, 75), (76, 125), (275, 200), (350, 25), (60, 280)),
            )
            pygame.draw.circle(self.display, white, (180, 180), 60)
            pygame.draw.line(self.display, red, (10, 200), (300, 10), 4)
            pygame.draw.ellipse(self.display, green, (250, 200, 130, 80))

            text = self.default_font.render("Welcome to My Game", True, (255, 255, 255))
            self.display.blit(text, (500 // 2 - text.get_width() // 2, 20))
            pygame.display.update()

    def _transform(
        self, f, vector: Vector2 = None, x: float = None, y: float = None
    ) -> Vector2 | float:
        if x and y:
            vector = Vector2(x=x, y=y)
        if vector:
            x, y = vector
            vector = Vector2(x=x, y=y)
            return Vector2(
                x=f(vector.x, self.display.width), y=f(vector.y, self.display.height)
            )
        if x:
            return x * self.display.width
        if y:
            return y * self.display.height
        raise ValueError("Must supply relative or x or y.")

    def rel2abs(
        self, relative: Vector2 = None, x: float = None, y: float = None
    ) -> Vector2 | float:
        return self._transform(lambda a, b: a * b, relative, x, y)

    def abs2rel(
        self, pixel: Vector2 = None, x: float = None, y: float = None
    ) -> Vector2 | float:
        return self._transform(lambda a, b: a / b, pixel, x, y)

    # def relative_to_rect(self, top_left: Vector2, bottom_right: Vector2) -> pygame.Rect:
    #     vector2_top_left = self.relative_to_vector2(top_left)
    #     vector2_bottom_right = self.relative_to_vector2(bottom_right)
    #     return pygame.Rect(
    #         vector2_top_left,
    #         vector2_bottom_right - vector2_top_left
    #     )

    def quit(self, *args, **kwargs) -> None:
        pygame.quit()

    def new_game(self, *args, **kwargs) -> None:
        self.game = Game(version=self.version, seed=0)
        self.game.start_encounter()
        self.change_scene(scene=EScene.BATTLE)

    def load_game(self, *args, **kwargs) -> None:
        self.game = dill.load(self.game_save_path)

    def save_game(self, *args, **kwargs) -> None:
        dill.dump(self.game, self.game_save_path)

    def change_scene(self, scene: EScene, *args, **kwargs) -> None:
        self._active_scene_stack.append(scene)
        if self._active_scene:
            self._active_scene.disable()
        self._active_scene = self._scene_map[scene]()
        self._active_scene.enable()

    def return_to_previous_scene(self, *args, **kwargs) -> None:
        try:
            self._active_scene_stack.pop()
            self.change_scene(self._active_scene_stack[-1])
        except IndexError:
            pass

    def load_scene_map(self, scene_map):
        self._scene_map = scene_map


application = Application()
