import arcade
import arcade.gui
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw

from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.frontend import colors
from scripts.frontend import ui
# from scripts.frontend.fonts import get_font
from scripts.utilities.enums import EFont, EScene, EStat
from scripts.utilities.geometry import Vector2


class Scene(ABC):
    def __init__(self, application) -> None:
        self.application = application
        self.ui_manager = arcade.gui.UIManager()

    @abstractmethod
    def handle_events(self, events: list[arcade.gui.UIEvent]) -> None:
        raise NotImplemented()

    @abstractmethod
    def draw(self) -> None:
        raise NotImplemented()

    def enable(self) -> None:
        self.ui_manager.enable()

    def disable(self) -> None:
        self.ui_manager.disable()
        self.application.window.clear()


class MainMenuScene(Scene):
    def __init__(self, application):
        super().__init__(application)

        width = 200
        gap = 15

        # Set background color
        arcade.set_background_color(color=colors.DARK_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        button_new_game = ui.UIApplicationButton(self.application.new_game, text="New Game", width=width)
        self.v_box.add(button_new_game.with_space_around(bottom=gap))

        button_continue = ui.UIApplicationButton(self.application.load_game, text="Continue", width=width)
        self.v_box.add(button_continue.with_space_around(bottom=gap))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=width)
        self.v_box.add(settings_button.with_space_around(bottom=gap))

        quit_button = ui.UIApplicationButton(self.application.quit, text="Quit", width=width)
        self.v_box.add(quit_button)

        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box,
            )
        )

    def handle_events(self, events):
        pass
        # for event in events:
        #     if event.type == pygame_gui.UI_BUTTON_PRESSED:
        #         if event.ui_element == self.button_new_game:
        #             self.application.new_game()
        #             self.application.change_scene(EScene.BATTLE)
        #         if event.ui_element == self.button_continue:
        #             self.application.load_game()
        #             self.application.change_scene(EScene.BATTLE)

    def draw(self):
        # Title
        arcade.draw_text(
            text=self.application.title,
            start_x=self.application.rel2abs(x=.5),
            start_y=self.application.rel2abs(y=.8),
            color=colors.NEON_GREEN,
            font_name=self.application.default_font,
            font_size=48,
            # bold=True,
            anchor_x="center",
            anchor_y="baseline",
        )
        # Version
        arcade.draw_text(
            text=f"Version {self.application.version}",
            start_x=self.application.rel2abs(x=.95),
            start_y=self.application.rel2abs(y=.05),
            color=colors.NEON_GREEN,
            font_name=self.application.default_font,
            font_size=20,
            # bold=True,
            anchor_x="right",
            anchor_y="bottom",
        )
        self.ui_manager.draw()


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
        # self.camera = arcade.Camera(window=self.application.window)
        # self.camera.move(Vec2())
        # self.camera.update()
        # self.camera.use()

        for unit in self.application.game.units():
            for unit_upgrade in unit.unit_upgrades:
                uu = ui.UIUnitUpgrade(unit_upgrade=unit_upgrade)
        self.ui_manager.add(uu)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        self.application.game.update_physics(self.application.delta_time)
        for unit in self.application.game.units():
            arcade.draw_circle_filled(
                center_x=unit.position.x,
                center_y=unit.position.y,
                radius=self.application.game.stat_value(unit, EStat.SIZE),
                color=unit.color(),
            )
        self.ui_manager.draw()


class UpgradeScene(Scene):
    def __init__(self, application):
        super().__init__(application)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass
