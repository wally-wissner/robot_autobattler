import dill
import pygame
import sys
from pygame_gui.ui_manager import UIManager

import scripts.frontend.scenes as scenes
from scripts.backend.game import Game
from scripts.backend.settings import SettingsManager
from scripts.frontend import colors
from scripts.utilities.singleton import Singleton
from scripts.utilities.structure import absolute_path
from utilities.enums import EScene


title = "Robot Autobattler"
version = "0.0.1"


@Singleton
class Application(object):
    def __init__(self):
        self.title = title
        self.version = version

        self.game_save_path = "../player_data/save.pickle"

        self.settings = SettingsManager()
        self.settings.load()

        # Pygame setup.
        pygame.init()
        self.display = pygame.display.set_mode(self.settings.resolution)
        pygame.display.set_caption(self.title)
        self.ui_manager = UIManager(self.settings.resolution)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)

        self.scenes = {
            EScene.MAIN_MENU: scenes.MainMenuScene(self),
            EScene.SETTINGS_MENU: scenes.SettingsMenuScene(self),
            "battle": scenes.BattleScene(self),
            EScene.UPGRADE: scenes.UpgradeScene(self),
        }

        # Game setup.
        self.game: Game | None = None
        self.active_scene = self.scenes[EScene.MAIN_MENU]
        self.delta_time = 0
        self.playing = True

    def run(self):
        self.display.fill(colors.blue)
        while self.playing:
            self.delta_time = self.clock.tick(self.settings.fps) / 1000
            self.handle_events(pygame.event.get())
            self.update()
            self.draw()
        self.quit()

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            self.ui_manager.process_events(event)
            if event.type == pygame.QUIT:
                self.quit()

        self.active_scene.handle_events(events)

    def update(self):
        pygame.display.update()
        self.ui_manager.update(self.delta_time)

    def draw(self):
        self.display.fill(color=colors.blue)
        self.active_scene.draw()
        self.ui_manager.draw_ui(self.display)

    def relative_to_vector2(self, relative: pygame.Vector2) -> pygame.Vector2:
        relative = pygame.Vector2(relative)
        resolution_width, resolution_height = self.settings.resolution
        return pygame.Vector2(relative.x * resolution_width, relative.y * resolution_height)

    def vector2_to_relative(self, pixel: pygame.Vector2) -> pygame.Vector2:
        pixel = pygame.Vector2(pixel)
        resolution_width, resolution_height = self.settings.resolution
        return pygame.Vector2(pixel.x / resolution_width, pixel.y / resolution_height)

    def relative_to_rect(self, top_left: pygame.Vector2, bottom_right: pygame.Vector2) -> pygame.Rect:
        vector2_top_left = self.relative_to_vector2(top_left)
        vector2_bottom_right = self.relative_to_vector2(bottom_right)
        return pygame.Rect(
            vector2_top_left,
            vector2_bottom_right - vector2_top_left
        )

    def quit(self):
        pygame.quit()
        sys.exit()

    def new_game(self, *args, **kwargs):
        self.game = Game(version=self.version, seed=0)
        self.game.start_encounter()

    def load_game(self):
        self.game = dill.load(self.game_save_path)

    def save_game(self):
        dill.dump(self.game, self.game_save_path)

    def change_scene(self, scene_type: EScene):
        self.active_scene.disable()
        # self.active_scene = self.scenes[scene_type]
        if scene_type == "battle":
            self.active_scene = scenes.BattleScene(self)


if __name__ == "__main__":
    game = Application.instance()
    game.run()
