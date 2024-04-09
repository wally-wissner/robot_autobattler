"""
Each of the application's scenes is its own class.
"""

# TODO: Ignore warnings until scenes are updated to pygame.
# pylint: disable=no-member


from abc import ABC, abstractmethod
from datetime import datetime

import arcade
import arcade.gui
import pygame
import pygame_gui

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
        self.ui_manager = application.ui_manager
        self.display_container = pygame_gui.core.UIContainer(
            pygame.Rect(
                0,
                0,
                application.settings_manager.width,
                application.settings_manager.height,
            ),
            manager=self.ui_manager,
        )
        self.buttons: dict[pygame_gui.elements.UIButton, tuple[callable, dict]] = {}

    @abstractmethod
    def draw(self) -> None:
        raise NotImplementedError()

    def enable(self) -> None:
        for button in self.buttons:
            button.visible = True

    def disable(self) -> None:
        for button in self.buttons:
            button.visible = False


class MainMenuScene(Scene):
    def __init__(self):
        super().__init__()

        button_width = 200
        button_height = 80
        button_vspace = 25

        self.background = pygame.Surface(application.settings_manager.resolution)

        n_buttons = 4

        buttons_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect(
                0,
                0,
                button_width,
                n_buttons * button_height + (n_buttons - 1) * button_vspace,
            ),
            anchors={"center": "center"},
            manager=self.ui_manager,
            container=self.display_container,
        )

        new_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (button_width, button_height)),
            text="New Game",
            manager=self.ui_manager,
            container=buttons_container,
            object_id="main_menu__new_game",
        )

        continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (0, button_height + button_vspace), (button_width, button_height)
            ),
            text="Continue",
            manager=self.ui_manager,
            container=buttons_container,
            object_id="main_menu__continue",
        )

        settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (0, 2 * (button_height + button_vspace)), (button_width, button_height)
            ),
            text="Settings",
            manager=self.ui_manager,
            container=buttons_container,
            object_id="main_menu__settings",
        )

        exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (0, 3 * (button_height + button_vspace)), (button_width, button_height)
            ),
            text="Exit",
            manager=self.ui_manager,
            container=buttons_container,
            object_id="main_menu__exit",
        )

        self.buttons = {
            new_game_button: (application.new_game, {}),
            continue_button: (application.continue_game, {}),
            settings_button: (application.change_scene, {"scene": EScene.SETTINGS}),
            exit_button: (application.quit, {}),
        }

    def draw(self):
        application.display.fill(color=colors.DARK_GRAY)
        title = application.title_font.render(
            # Flicker "cursor" every second.
            application.title + ("|" if datetime.now().second % 2 else " "),
            True,
            colors.NEON_GREEN,
        )
        application.display.blit(
            title,
            (application.settings_manager.width // 2 - title.get_width() // 2, 100),
        )


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

    def draw(self):
        self.ui_manager.draw()


scene_map = {
    EScene.MAIN_MENU: MainMenuScene,
    EScene.SETTINGS: SettingsScene,
    EScene.BATTLE: BattleScene,
    EScene.UPGRADE: UpgradeScene,
}
