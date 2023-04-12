import arcade
import arcade.gui
import numpy as np
from abc import ABC, abstractmethod

from scripts.frontend.fonts import get_font
from scripts.utilities.enums import EFont, EScene, EStat


class QuitButton(arcade.gui.UIFlatButton):
    def __init__(self, application, *args, **kwargs) -> None:
        self.application = application
        super().__init__(*args, **kwargs)

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.application.quit()


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


class MainMenuScene(Scene):
    def __init__(self, application):
        super().__init__(application)

        # Set background color
        # arcade.set_background_color(arcade.color.BLACK_BEAN)
        arcade.set_background_color((40, 40, 40))

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        quit_button = QuitButton(self.application, text="Quit", width=200)
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
        arcade.draw_text(
            text=self.application.title,
            start_x=.5 * self.application.window.width,
            start_y=.8 * self.application.window.height,
            color=(65, 255, 0),
            font_name=self.application.default_font,
            font_size=48,
            # bold=True,
            anchor_x="center",
            anchor_y="baseline",
        )
        self.ui_manager.draw()
        # # todo
        # self.application.display.blit(
        #     get_font(EFont.JETBRAINS_MONO_REGULAR, 64).render(self.application.title, 0, (255, 240, 230)), (10, 10)
        # )


class SettingsMenuScene(Scene):
    def __init__(self, application):
        super().__init__(application)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass


# class BattleScene(Scene):
#     def __init__(self, application):
#         super().__init__(application)
#
#     def handle_events(self, events):
#         # todo
#         pass
#
#     def draw(self):
#         self.application.game.update_physics(self.application.delta_time)
#         for unit in self.application.game.units():
#             pygame.draw.circle(
#                 surface=self.application.display,
#                 color=unit.color(),
#                 center=unit.position + np.array(self.application.settings.resolution) / 2,
#                 radius=self.application.game.unit_stat_value(unit, EStat.SIZE),
#             )


class UpgradeScene(Scene):
    def __init__(self, application):
        super().__init__(application)

    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass
