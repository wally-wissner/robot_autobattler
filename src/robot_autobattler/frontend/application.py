# *args and **kwargs needed for button interface compatibility.
# pylint: disable=unused-argument


import arcade
import arcade.gui
import dill

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

        self.window = arcade.Window(
            *self.settings.resolution, title=self.title, resizable=True
        )
        self.window.on_draw = self.on_draw
        self.window.on_update = self.on_update

        # Scene setup.
        self._scene_map: dict = {}
        self._active_scene = None
        self._active_scene_stack: list[EScene] = []

    def load_assets(self) -> None:
        self.default_font = "Courier New"

        # path = absolute_path("assets/fonts/JETBRAINS_MONO_REGULAR.ttf")
        # file_path = arcade.resources.resolve_resource_path(path)
        # pyglet.font.add_file(str(file_path))
        # pyglet.font.load("JETBRAINS_MONO_REGULAR")

        # self.default_font = str(absolute_path("assets/fonts/JETBRAINS_MONO_REGULAR.ttf"))
        # self.default_font = pyglet.font.load(
        #     absolute_path("assets/fonts/JETBRAINS_MONO_REGULAR.ttf")
        # )

        # resource.add_font(absolute_path("assets/fonts/JETBRAINS_MONO_REGULAR.ttf"))
        # self.default_font = pyglet.font.load('JETBRAINS_MONO_REGULAR')

    def on_update(self, delta_time) -> None:
        self.delta_time = delta_time

    def on_draw(self) -> None:
        self.window.clear()
        self._active_scene.draw()
        # self.active_scene.ui_manager.draw()

    def run(self) -> None:
        self.change_scene(EScene.MAIN_MENU)
        arcade.run()

    def _transform(
        self, f, vector: Vector2 = None, x: float = None, y: float = None
    ) -> Vector2 | float:
        if x and y:
            vector = Vector2(x=x, y=y)
        if vector:
            x, y = vector
            vector = Vector2(x=x, y=y)
            return Vector2(
                x=f(vector.x, self.window.width), y=f(vector.y, self.window.height)
            )
        if x:
            return x * self.window.width
        if y:
            return y * self.window.height
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
        arcade.exit()

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
