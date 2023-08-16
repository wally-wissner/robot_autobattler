import arcade
import arcade.gui
from PIL import Image, ImageDraw

from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.frontend import colors
# from scripts.frontend.fonts import get_font
from scripts.utilities.enums import EFont, EScene, EStat
from scripts.utilities.geometry import Vector2


class UIApplicationButton(arcade.gui.UIFlatButton):
    def __init__(self, on_click, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        super().__init__(*args, **kwargs)
        self._on_click = on_click

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self._on_click(*self.args, **self.kwargs)


class UITextBox(arcade.gui.UITexturePane):
    def __init__(self, height, width, texture, text, font_size):
        label = arcade.gui.UILabel(text=text, width=width, height=height, font_size=font_size)
        super().__init__(tex=texture, text=text, child=label, size_hint=1, width=width, height=height)
        # background = arcade.draw_rectangle_filled(width=width, height=height)
        # self.add(arcade.gui.)


class UIUnitUpgrade(arcade.gui.UIPadding, arcade.gui.UIDraggableMixin):
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
        self.box.add(UITextBox(
            width=self.width,
            height=self.height//2,
            texture=self.texture_card,
            text=self.unit_upgrade.card.description(),
            font_size=10,
        ))
        self.box.add(UITextBox(
            width=self.width,
            height=self.height//2,
            texture=self.texture_badge,
            text=self.unit_upgrade.badge.description(),
            font_size=10,
        ))
        super().__init__(child=self.box, bg_color=colors.RARE, padding=(2, 2, 2, 2))
