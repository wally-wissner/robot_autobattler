import arcade
import arcade.gui
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw

from config import absolute_path
from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.frontend import colors
from scripts.frontend.ui import UITextButton, UITextureButton
from scripts.frontend.unit_upgrades import UIUnitUpgrade
# from scripts.frontend.fonts import get_font
from scripts.utilities.enums import EFont, EScene, EStat
from scripts.utilities.geometry import Rectangle, Vector2


class Scene(ABC):
    def __init__(self, app) -> None:
        self.app = app
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
        self.app.window.clear()


class MainMenuScene(Scene):
    def __init__(self, app):
        super().__init__(app)

        width = 200
        gap = 15

        # Set background color
        arcade.set_background_color(color=colors.DARK_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        button_new_game = UITextButton(self.app.new_game, text="New Game", width=width)
        self.v_box.add(button_new_game.with_space_around(bottom=gap))

        button_continue = UITextButton(self.app.load_game, text="Continue", width=width)
        self.v_box.add(button_continue.with_space_around(bottom=gap))

        settings_button = UITextButton(self.app.change_scene, scene=EScene.SETTINGS, text="Settings", width=width)
        self.v_box.add(settings_button.with_space_around(bottom=gap))

        exit_game_button = UITextButton(self.app.quit, text="Exit Game", width=width)
        self.v_box.add(exit_game_button)

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
            text=self.app.title,
            start_x=self.app.rel2abs(x=.5),
            start_y=self.app.rel2abs(y=.8),
            color=colors.NEON_GREEN,
            font_name=self.app.default_font,
            font_size=48,
            # bold=True,
            anchor_x="center",
            anchor_y="baseline",
        )
        # Version
        arcade.draw_text(
            text=f"Version {self.app.version}",
            start_x=self.app.rel2abs(x=.95),
            start_y=self.app.rel2abs(y=.05),
            color=colors.NEON_GREEN,
            font_name=self.app.default_font,
            font_size=20,
            # bold=True,
            anchor_x="right",
            anchor_y="bottom",
        )
        self.ui_manager.draw()


class SettingsScene(Scene):
    def __init__(self, app):
        super().__init__(app)

        width = 200
        gap = 15

        # Set background color
        arcade.set_background_color(color=colors.DARK_GRAY)

        # Create a vertical BoxGroup to align settings
        self.v_box = arcade.gui.UIBoxLayout(vertical=True)

        # Create a horizontal BoxGroup to align buttons
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        # Create the buttons
        back_button = UITextButton(self.app.return_to_previous_scene, text="Back", width=width)
        self.h_box.add(back_button.with_space_around(right=gap))
        main_menu_button = UITextButton(self.app.change_scene, scene=EScene.MAIN_MENU, text="Main Menu", width=width)
        self.h_box.add(main_menu_button.with_space_around(right=gap))
        exit_game_button = UITextButton(self.app.quit, text="Exit Game", width=width)
        self.h_box.add(exit_game_button)

        self.v_box.add(self.h_box)

        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box,
            )
        )

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        self.ui_manager.draw()


class BattleScene(Scene):
    def __init__(self, app):
        super().__init__(app)

        self.menu_rect = Rectangle([
            self.app.rel2abs(Vector2(0, .925)),
            self.app.rel2abs(Vector2(1, 1)),
        ])

        self.icon_height = .8 * self.menu_rect.height

        # self.camera = arcade.Camera(window=self.application.window)
        # self.camera.move(Vec2())
        # self.camera.update()
        # self.camera.use()

        for unit in self.app.game.units():
            for unit_upgrade in unit.unit_upgrades:
                uu = UIUnitUpgrade(unit_upgrade=unit_upgrade, x=300, y=300, width=200, height=200, description=False)
        self.ui_manager.add(uu)

        settings_button = UITextureButton(
            x=self.app.rel2abs(x=.975) - self.icon_height / 2,
            y=self.menu_rect.center.y - self.icon_height / 2,
            width=self.icon_height,
            height=self.icon_height,
            texture=arcade.load_texture(absolute_path("assets/images/ui/settings-icon.png")),
            on_click=self.app.change_scene,
            scene=EScene.SETTINGS,
        )
        self.ui_manager.add(settings_button)

        # anchored_settings_button = arcade.gui.UIAnchorWidget(
        #     child=settings_button,
        #     align_x=self.app.rel2abs(x=-.0125),
        #     align_y=-self.menu_rect.height / 2,
        #     # align_y=self.app.rel2abs(y=-self.menu_rect.height / 4),
        #     anchor_x='right',
        #     anchor_y='top',
        # )
        # self.ui_manager.add(anchored_settings_button)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        self.app.game.update_physics(self.app.delta_time)
        for unit in self.app.game.units():
            arcade.draw_circle_filled(
                center_x=unit.position.x,
                center_y=unit.position.y,
                radius=self.app.game.stat_value(unit, EStat.SIZE),
                color=unit.color(),
            )

        arcade.draw_rectangle_filled(
            center_x=self.menu_rect.center.x,
            center_y=self.menu_rect.center.y,
            width=self.menu_rect.width,
            height=self.menu_rect.height,
            color=colors.LIGHT_GRAY,
        )

        self.ui_manager.draw()


class UpgradeScene(Scene):
    def __init__(self, app):
        super().__init__(app)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        self.ui_manager.draw()

