"""
Each of the application's scenes is its own class.
"""

# pylint: disable=unused-import

from abc import ABC, abstractmethod
from datetime import datetime

import pygame
import pygame_gui

from backend.unit import Unit
from backend.upgrades import Upgrade
from frontend import colors
from frontend import fonts
from frontend import ui_panes
from frontend.application import application, game
from frontend.ui_upgrades import UIUpgrade
from frontend.ui_panes.ui_select_upgrade import UIPaneSelectUpgrade
from utils.enums import EScene, EStat
from utils.geometry import Rectangle, Vector2
from utils.ui import anchored_blit


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
                application.width(),
                application.height(),
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
        application.display.fill(color=colors.BACKGROUND)

        # Game title.
        title = fonts.get_font(fonts.title_font, 70).render(
            # Flicker "cursor" every second.
            text=application.title + ("|" if datetime.now().second % 2 else " "),
            antialias=True,
            color=colors.TITLE,
        )
        application.display.blit(
            title,
            (application.width() // 2 - title.get_width() // 2, 100),
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
        application.display.fill(color=colors.BACKGROUND)


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
            application.width(),
            0.075 * application.height(),
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

        self.select_upgrade_rect = Rectangle(
            x_min=0.25 * application.width(),
            x_max=0.75 * application.width(),
            y_min=0.25 * application.height(),
            y_max=0.75 * application.height(),
        )
        self.select_upgrade_pane = UIPaneSelectUpgrade(
            size=self.select_upgrade_rect.size()
        )

        self.buttons = {
            settings_button: (application.change_scene, {"scene": EScene.SETTINGS}),
        }

    def draw(self):
        application.display.fill(color=colors.BACKGROUND)

        game.update_physics(application.delta_time)

        for unit in game.units():
            pygame.draw.circle(
                surface=application.display,
                color=unit.color(),
                center=tuple(unit.position),
                radius=game.stat_value(unit, EStat.SIZE),
            )

        self.menu_bar_surface.fill(color=colors.BACKGROUND)

        self.select_upgrade_pane.render()
        anchored_blit(
            target=application.display,
            source=self.select_upgrade_pane.surface,
            x_anchor="center",
            y_anchor="center",
        )

        for unit in game.units():
            for upgrade in unit.upgrades:
                uu = UIUpgrade(
                    upgrade=upgrade,
                    size=tuple(Vector2(x=200, y=200)),
                    display_body=True,
                )
                uu.render(display_description=True, highlighted=True)
                anchored_blit(
                    target=application.display,
                    source=uu.surface,
                    x_anchor="left",
                    y_anchor="center",
                )
                break
            break
        application.display.blit(self.menu_bar_surface, (0, 0))


class UpgradeScene(Scene):
    def __init__(self):
        super().__init__()

        self.active_unit: Unit = None
        self.active_upgrade: Upgrade = None

        # self.team_pane = TeamPane(Rectangle(x_min=0, x_max=0.25, y_min=0, y_max=1))

        # self.unit_pane = UnitPane(Rectangle(x_min=0.25, x_max=0.75, y_min=0, y_max=0.5))

        self.inventory_pane = ui_panes.InventoryPane(
            rectangle=Rectangle(
                x_min=0,
                x_max=1 / 6,
                y_min=0,
                y_max=1,
            ).at_resolution(application.resolution())
        )

        self.active_unit_upgrades_pane = ui_panes.ActiveUnitUpgradesPane(
            rectangle=Rectangle(
                x_min=1 / 6,
                x_max=2 / 6,
                y_min=0,
                y_max=1,
            ).at_resolution(application.resolution())
        )

        self.set_active_unit(game.player_team().units[0])
        self.set_active_upgrade(
            game.player_team().inventory[0]
            if game.player_team().inventory
            else game.player_team().units[0].upgrade[0]
        )

        self.set_active_unit(game.player_team().units[0])
        self.set_active_upgrade(game.player_team().units[0].upgrades[0])

    def set_active_unit(self, unit: Unit) -> None:
        self.active_unit = unit
        self.active_unit_upgrades_pane.active_unit = unit

    def set_active_upgrade(self, upgrade: Upgrade) -> None:
        self.active_upgrade = upgrade
        self.active_unit_upgrades_pane.set_active_upgrade(upgrade)

    def draw(self):
        application.display.fill(color=colors.BACKGROUND)

        self.inventory_pane.draw(surface=application.display)
        self.active_unit_upgrades_pane.draw(surface=application.display)


scene_map = {
    EScene.MAIN_MENU: MainMenuScene,
    EScene.SETTINGS: SettingsScene,
    EScene.BATTLE: BattleScene,
    EScene.UPGRADE: UpgradeScene,
}
