"""
Each of the application's scenes is its own class.
"""

from abc import ABC, abstractmethod
from datetime import datetime

import pygame
import pygame_gui

from backend.unit import Unit
from backend.upgrades import Upgrade
from frontend import colors
from frontend.application import application
from frontend.fonts import get_font
from frontend.ui_panes import InventoryPane, TeamPane, UnitPane, UpgradePane
from frontend.upgrades import UIUpgrade
from utils.enums import EFont, EScene, EStat
from utils.geometry import Rectangle, Vector2


class Scene(ABC):
    """
    Abstract base class for the application's scenes.
    """

    def __init__(self) -> None:
        self.ui_manager = application.ui_manager
        self.display_container = pygame_gui.core.UIContainer(
            relative_rect=pygame.Rect(
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

        # Game title.
        title = get_font(EFont.JETBRAINS_MONO_REGULAR, 70).render(
            # Flicker "cursor" every second.
            text=application.title + ("|" if datetime.now().second % 2 else " "),
            antialias=True,
            color=colors.NEON_GREEN,
        )
        application.display.blit(
            title,
            (application.settings_manager.width // 2 - title.get_width() // 2, 100),
        )


class SettingsScene(Scene):
    def __init__(self):
        super().__init__()

        button_width = 200
        button_height = 80
        button_vspace = 25

        n_buttons = 3

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

        back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (button_width, button_height)),
            text="Back",
            manager=self.ui_manager,
            container=buttons_container,
            object_id="settings__back",
        )

        main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (0, button_height + button_vspace), (button_width, button_height)
            ),
            text="Main Menu",
            manager=self.ui_manager,
            container=buttons_container,
            object_id="settings__main_menu",
        )

        exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (0, 2 * (button_height + button_vspace)), (button_width, button_height)
            ),
            text="Exit Game",
            manager=self.ui_manager,
            container=buttons_container,
            object_id="settings__exit",
        )

        self.buttons = {
            back_button: (application.return_to_previous_scene, {}),
            main_menu_button: (application.change_scene, {"scene": EScene.MAIN_MENU}),
            exit_button: (application.quit, {}),
        }

    def draw(self):
        application.display.fill(color=colors.DARK_GRAY)


class BattleScene(Scene):
    def __init__(self):
        super().__init__()

        # menu_bar_height = .075
        #
        # self.menu_bar_rect = Rectangle.from_points(
        #     [
        #         application.rel2abs(Vector2(x=0, y=1 - menu_bar_height)),
        #         application.rel2abs(Vector2(x=1, y=1)),
        #     ]
        # )
        #
        # self.icon_height = 0.8 * self.menu_bar_rect.height()
        #

        self.menu_bar_rect = pygame.Rect(
            0,
            0,
            application.settings_manager.width,
            0.075 * application.settings_manager.height,
        )

        self.menu_bar_surface = pygame.Surface(self.menu_bar_rect.size)

        self.menu_bar_container = pygame_gui.core.UIContainer(
            relative_rect=self.menu_bar_rect,
            anchors={"left": "left", "right": "right", "top": "top", "bottom": "top"},
            manager=self.ui_manager,
            container=self.display_container,
        )

        settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(-110, 0, 100, 50),
            text="Settings",
            manager=self.ui_manager,
            container=self.menu_bar_container,
            anchors={
                "right": "right",
                "centery": "centery",
            },
        )

        self.buttons = {
            settings_button: (application.change_scene, {"scene": EScene.SETTINGS}),
        }

    def draw(self):
        application.display.fill(color=colors.LIGHT_GRAY)

        application.game.update_physics(application.delta_time)

        for unit in application.game.units():
            pygame.draw.circle(
                surface=application.display,
                color=unit.color(),
                center=tuple(unit.position),
                radius=application.game.stat_value(unit, EStat.SIZE),
            )

        self.menu_bar_surface.fill(color=colors.DARK_GRAY)
        application.display.blit(self.menu_bar_surface, (0, 0))

        for unit in application.game.units():
            for upgrade in unit.upgrades:
                uu = UIUpgrade(upgrade=upgrade)
                uu.draw(
                    surface=application.display,
                    size=tuple(Vector2(x=200, y=200)),
                    position=tuple(Vector2(x=300, y=300)),
                    display_description=True,
                )
                break
            break


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
        pass


scene_map = {
    EScene.MAIN_MENU: MainMenuScene,
    EScene.SETTINGS: SettingsScene,
    EScene.BATTLE: BattleScene,
    EScene.UPGRADE: UpgradeScene,
}
