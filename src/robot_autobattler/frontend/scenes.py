"""
Each of the application's scenes is its own class.
"""

from abc import ABC, abstractmethod

import arcade
import arcade.gui

from config import absolute_path
from backend.unit import Unit
from backend.upgrades import Upgrade
from frontend import colors
from frontend.application import application
from frontend.ui_elements import UITextButton, UITextureButton
from frontend.ui_panes import InventoryPane, TeamPane, UnitPane, UpgradePane
from frontend.upgrades import UIUnitUpgrade
from utils.enums import EScene, EStat
from utils.geometry import Rectangle, Vector2


class Scene(ABC):
    """
    Abstract base class for the application's scenes.
    """

    def __init__(self) -> None:
        self.ui_manager = arcade.gui.UIManager()

    @abstractmethod
    def handle_events(self, events: list[arcade.gui.UIEvent]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError()

    def enable(self) -> None:
        self.ui_manager.enable()

    def disable(self) -> None:
        self.ui_manager.disable()
        application.window.clear()


class MainMenuScene(Scene):
    def __init__(self):
        super().__init__()

        width = 200
        gap = 15

        # Set background color
        arcade.set_background_color(color=colors.DARK_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        button_new_game = UITextButton(
            application.new_game, text="New Game", width=width
        )
        self.v_box.add(button_new_game.with_space_around(bottom=gap))

        button_continue = UITextButton(
            application.load_game, text="Continue", width=width
        )
        self.v_box.add(button_continue.with_space_around(bottom=gap))

        settings_button = UITextButton(
            application.change_scene,
            scene=EScene.SETTINGS,
            text="Settings",
            width=width,
        )
        self.v_box.add(settings_button.with_space_around(bottom=gap))

        exit_game_button = UITextButton(application.quit, text="Exit Game", width=width)
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
        #             application.new_game()
        #             application.change_scene(EScene.BATTLE)
        #         if event.ui_element == self.button_continue:
        #             application.load_game()
        #             application.change_scene(EScene.BATTLE)

    def draw(self):
        # Title
        arcade.draw_text(
            text=application.title,
            start_x=application.rel2abs(x=0.5),
            start_y=application.rel2abs(y=0.8),
            color=colors.NEON_GREEN,
            font_name=application.default_font,
            font_size=48,
            # bold=True,
            anchor_x="center",
            anchor_y="baseline",
        )
        # Version
        arcade.draw_text(
            text=f"Version {application.version}",
            start_x=application.rel2abs(x=0.95),
            start_y=application.rel2abs(y=0.05),
            color=colors.NEON_GREEN,
            font_name=application.default_font,
            font_size=20,
            # bold=True,
            anchor_x="right",
            anchor_y="bottom",
        )
        self.ui_manager.draw()


class SettingsScene(Scene):
    def __init__(self):
        super().__init__()

        width = 200
        gap = 15

        # Set background color
        arcade.set_background_color(color=colors.DARK_GRAY)

        # Create a vertical BoxGroup to align settings
        self.v_box = arcade.gui.UIBoxLayout(vertical=True)

        # Create a horizontal BoxGroup to align buttons
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        # Create the buttons
        back_button = UITextButton(
            application.return_to_previous_scene, text="Back", width=width
        )
        self.h_box.add(back_button.with_space_around(right=gap))
        main_menu_button = UITextButton(
            application.change_scene,
            scene=EScene.MAIN_MENU,
            text="Main Menu",
            width=width,
        )
        self.h_box.add(main_menu_button.with_space_around(right=gap))
        exit_game_button = UITextButton(application.quit, text="Exit Game", width=width)
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
    def __init__(self):
        super().__init__()

        self.menu_rect = Rectangle.from_points(
            [
                application.rel2abs(Vector2(x=0, y=0.925)),
                application.rel2abs(Vector2(x=1, y=1)),
            ]
        )

        self.icon_height = 0.8 * self.menu_rect.height()

        # self.camera = arcade.Camera(window=applicationlication.window)
        # self.camera.move(Vec2())
        # self.camera.update()
        # self.camera.use()

        for unit in application.game.units():
            for upgrade in unit.upgrades:
                uu = UIUnitUpgrade(
                    upgrade=upgrade,
                    x=300,
                    y=300,
                    width=200,
                    height=200,
                    description=False,
                )
        self.ui_manager.add(uu)

        settings_button = UITextureButton(
            x=application.rel2abs(x=0.975) - self.icon_height / 2,
            y=self.menu_rect.center().y - self.icon_height / 2,
            width=self.icon_height,
            height=self.icon_height,
            texture=arcade.load_texture(
                absolute_path("assets/images/ui/settings-icon.png")
            ),
            on_click=application.change_scene,
            scene=EScene.SETTINGS,
        )
        self.ui_manager.add(settings_button)

        # anchored_settings_button = arcade.gui.UIAnchorWidget(
        #     child=settings_button,
        #     align_x=application.rel2abs(x=-.0125),
        #     align_y=-self.menu_rect.height / 2,
        #     # align_y=application.rel2abs(y=-self.menu_rect.height / 4),
        #     anchor_x='right',
        #     anchor_y='top',
        # )
        # self.ui_manager.add(anchored_settings_button)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        application.game.update_physics(application.delta_time)
        for unit in application.game.units():
            arcade.draw_circle_filled(
                center_x=unit.position.x,
                center_y=unit.position.y,
                radius=application.game.stat_value(unit, EStat.SIZE),
                color=unit.color(),
            )

        arcade.draw_rectangle_filled(
            center_x=self.menu_rect.center().x,
            center_y=self.menu_rect.center().y,
            width=self.menu_rect.width(),
            height=self.menu_rect.height(),
            color=colors.LIGHT_GRAY,
        )

        self.ui_manager.draw()


class UpgradeScene(Scene):
    def __init__(self):
        super().__init__()
        self.active_unit: Unit | None = None
        self.active_upgrade: Upgrade | None = None

        self.team_pane = TeamPane(Rectangle(x_min=0, x_max=0.25, y_min=0, y_max=1))
        self.upgrade_pane = UpgradePane(
            Rectangle(x_min=0.25, x_max=0.75, y_min=0.5, y_max=1)
        )
        self.unit_pane = UnitPane(Rectangle(x_min=0.25, x_max=0.75, y_min=0, y_max=0.5))
        self.inventory_pane = InventoryPane(
            Rectangle(x_min=0.75, x_max=1, y_min=0, y_max=1)
        )

    def set_active_unit(self, unit: Unit) -> None:
        self.active_unit = unit
        # self.unit_pane.

    def set_active_upgrade(self, upgrade: Upgrade) -> None:
        self.active_upgrade = upgrade
        self.upgrade_pane.set_upgrade(upgrade)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        self.ui_manager.draw()


scene_map = {
    EScene.MAIN_MENU: MainMenuScene,
    EScene.SETTINGS: SettingsScene,
    EScene.BATTLE: BattleScene,
    EScene.UPGRADE: UpgradeScene,
}
