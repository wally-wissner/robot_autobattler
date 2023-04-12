import arcade
import arcade.gui
import dill
import pathlib
import pyglet

from config import ROOT_DIRECTORY
import scripts.frontend.scenes as scenes
from scripts.backend.game import Game
from scripts.backend.settings import SettingsManager
from scripts.frontend import colors
from scripts.utilities.enums import EScene
from scripts.utilities.game_math import Vector2


class Application(object):
    def __init__(self, title, version) -> None:
        self.title = title
        self.version = version

        self.game_save_path = pathlib.Path(ROOT_DIRECTORY, "player_data/save.pickle")
        print(self.game_save_path)

        self.load_assets()

        self.settings = SettingsManager()
        self.settings.load()

        self.window = arcade.Window(*self.settings.resolution, title=title, resizable=True)
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        self.window.on_draw = self.on_draw

        self.scenes = {
            EScene.MAIN_MENU: scenes.MainMenuScene(self),
            # EScene.SETTINGS_MENU: scenes.SettingsMenuScene(self),
            # EScene.BATTLE: scenes.BattleScene(self),
            # EScene.UPGRADE: scenes.UpgradeScene(self),
        }

        # Game setup.
        self.game: Game | None = None
        self.active_scene = self.scenes[EScene.MAIN_MENU]
        self.delta_time = 0
        self.playing = True

    def load_assets(self):
        pass
        # pyglet.font.add_file()

    def on_draw(self) -> None:
        self.window.clear()
        self.ui_manager.draw()

    def run(self) -> None:
        arcade.run()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    # def relative_to_vector2(self, relative: Vector2) -> Vector2:
    #     relative = Vector2(*relative)
    #     resolution_width, resolution_height = self.settings.resolution
    #     return Vector2(relative.x * resolution_width, relative.y * resolution_height)
    #
    # def vector2_to_relative(self, pixel: Vector2) -> Vector2:
    #     pixel = Vector2(*pixel)
    #     resolution_width, resolution_height = self.settings.resolution
    #     return Vector2(pixel.x / resolution_width, pixel.y / resolution_height)
    #
    # def relative_to_rect(self, top_left: Vector2, bottom_right: Vector2) -> pygame.Rect:
    #     vector2_top_left = self.relative_to_vector2(top_left)
    #     vector2_bottom_right = self.relative_to_vector2(bottom_right)
    #     return pygame.Rect(
    #         vector2_top_left,
    #         vector2_bottom_right - vector2_top_left
    #     )

    def quit(self) -> None:
        arcade.exit()

    def new_game(self, *args, **kwargs) -> None:
        self.game = Game(version=self.version, seed=0)
        self.game.start_encounter()

    def load_game(self) -> None:
        self.game = dill.load(self.game_save_path)

    def save_game(self) -> None:
        dill.dump(self.game, self.game_save_path)

    def change_scene(self, scene_type: EScene) -> None:
        self.active_scene.disable()
        self.active_scene = self.scenes[scene_type]


if __name__ == "__main__":
    game = Application(title="Robot Autobattler", version="0.0.1")
    game.run()
