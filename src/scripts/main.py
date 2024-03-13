import arcade
import arcade.gui
import dill
import pyglet
from pyglet import resource

import src.scripts.frontend.scenes as scenes
from _version import __title__, __version__
from config import absolute_path
from src.scripts.backend.game import Game
from src.scripts.backend.settings import SettingsManager
from src.scripts.utilities.enums import EScene
from src.scripts.utilities.geometry import Vector2


class Application(object):
    def __init__(self) -> None:
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

        self.window = arcade.Window(*self.settings.resolution, title=self.title, resizable=True)
        self.window.on_draw = self.on_draw
        self.window.on_update = self.on_update

        # Scene setup.
        self._scene_map = {
            EScene.MAIN_MENU: scenes.MainMenuScene,
            EScene.SETTINGS: scenes.SettingsScene,
            EScene.BATTLE: scenes.BattleScene,
            EScene.UPGRADE: scenes.UpgradeScene,
        }
        self._active_scene: scenes.Scene | None = None
        self._scene_stack: list[EScene] = []
        self.change_scene(EScene.MAIN_MENU)

    def load_assets(self) -> None:
        self.default_font = "Courier New"

        # path = absolute_path("assets/fonts/JETBRAINS_MONO_REGULAR.ttf")
        # file_path = arcade.resources.resolve_resource_path(path)
        # pyglet.font.add_file(str(file_path))
        # pyglet.font.load("JETBRAINS_MONO_REGULAR")

        # self.default_font = str(absolute_path("assets/fonts/JETBRAINS_MONO_REGULAR.ttf"))
        # self.default_font = pyglet.font.load(absolute_path("assets/fonts/JETBRAINS_MONO_REGULAR.ttf"))

        # resource.add_font(absolute_path("assets/fonts/JETBRAINS_MONO_REGULAR.ttf"))
        # self.default_font = pyglet.font.load('JETBRAINS_MONO_REGULAR')

    def on_update(self, delta_time) -> None:
        self.delta_time = delta_time

    def on_draw(self) -> None:
        self.window.clear()
        self._active_scene.draw()
        # self.active_scene.ui_manager.draw()

    def run(self) -> None:
        arcade.run()

    def _transform(self, f, vec: Vector2 = None, x: float = None, y: float = None) -> Vector2 | float:
        if x and y:
            vec = Vector2(x, y, relative=True)
        if vec:
            vec = Vector2(*vec, relative=True)
            return Vector2(f(vec.x, self.window.width), f(vec.y, self.window.height), relative=False)
        elif x:
            return x * self.window.width
        elif y:
            return y * self.window.height
        else:
            raise ValueError("Must supply relative or x or y.")

    def rel2abs(self, relative: Vector2 = None, x: float = None, y: float = None) -> Vector2 | float:
        return self._transform(lambda a, b: a * b, relative, x, y)

    def abs2rel(self, pixel: Vector2 = None, x: float = None, y: float = None) -> Vector2 | float:
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
        self._scene_stack.append(scene)
        if self._active_scene:
            self._active_scene.disable()
        self._active_scene = self._scene_map[scene](self)
        self._active_scene.enable()

    def return_to_previous_scene(self, *args, **kwargs) -> None:
        try:
            self._scene_stack.pop()
            self.change_scene(self._scene_stack[-1])
        except IndexError:
            pass


if __name__ == "__main__":
    application = Application()
    application.run()
