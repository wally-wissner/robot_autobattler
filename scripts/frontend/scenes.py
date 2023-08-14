import arcade
import arcade.gui
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw

from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.frontend import colors
# from scripts.frontend.fonts import get_font
from scripts.utilities.enums import EFont, EScene, EStat
from scripts.utilities.geometry import Vector2


class ApplicationButton(arcade.gui.UIFlatButton):
    def __init__(self, on_click, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        super().__init__(*args, **kwargs)
        self._on_click = on_click

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self._on_click(*self.args, **self.kwargs)


class TextBox(arcade.gui.UITexturePane):
    def __init__(self, height, width, texture, text, font_size):
        label = arcade.gui.UILabel(text=text, width=width, height=height, font_size=font_size)
        super().__init__(tex=texture, text=text, child=label, size_hint=1, width=width, height=height)
        # background = arcade.draw_rectangle_filled(width=width, height=height)
        # self.add(arcade.gui.)


class UIUnitUpgrade(arcade.gui.UIBorder, arcade.gui.UIDraggableMixin):
    height = 200
    width = 200

    texture_card = arcade.texture.Texture(
        name="bg_card",
        image=Image.new(mode='RGB', size=(width, height//2), color=colors.RETRO_RED),
    )
    texture_badge = arcade.texture.Texture(
        name="bg_badge",
        image=Image.new(mode='RGB', size=(width, height//2), color=colors.RETRO_BLUE),
    )

    def __init__(self, unit_upgrade: UnitUpgrade):
        self.unit_upgrade = unit_upgrade
        self.box = arcade.gui.UIBoxLayout(x=300, y=300, vertical=True, space_between=0)
        self.box.add(TextBox(
            width=self.width,
            height=self.height//2,
            texture=self.texture_card,
            text=self.unit_upgrade.card.description(),
            font_size=10,
        ))
        self.box.add(TextBox(
            width=self.width,
            height=self.height//2,
            texture=self.texture_badge,
            text=self.unit_upgrade.badge.description(),
            font_size=10,
        ))
        super().__init__(child=self.box, border_color=colors.RARE, border_width=3)


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
        button_new_game = ApplicationButton(self.application.new_game, text="New Game", width=width)
        self.v_box.add(button_new_game.with_space_around(bottom=gap))

        button_continue = ApplicationButton(self.application.load_game, text="Continue", width=width)
        self.v_box.add(button_continue.with_space_around(bottom=gap))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=width)
        self.v_box.add(settings_button.with_space_around(bottom=gap))

        quit_button = ApplicationButton(self.application.quit, text="Quit", width=width)
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
            start_x=.5 * self.application.window.width,
            start_y=.8 * self.application.window.height,
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
            start_x=.95 * self.application.window.width,
            start_y=.05 * self.application.window.height,
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
                uu = UIUnitUpgrade(unit_upgrade=unit_upgrade)
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
