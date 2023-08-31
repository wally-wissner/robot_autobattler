import arcade
import arcade.gui
from PIL import Image, ImageDraw
from typing import Callable

from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.frontend import colors
# from scripts.frontend.fonts import get_font
from scripts.utilities.enums import EFont, EScene, EStat
from scripts.utilities.geometry import Vector2


class UITextButton(arcade.gui.UIFlatButton):
    def __init__(self, on_click: Callable, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        super().__init__(*args, **kwargs)
        self._on_click = on_click

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self._on_click(*self.args, **self.kwargs)


class UITextureButton(arcade.gui.UITextureButton):
    def __init__(self, on_click: Callable, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        super().__init__(*args, **kwargs)
        self._on_click = on_click

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self._on_click(*self.args, **self.kwargs)


class UITextPane(arcade.gui.UITexturePane):
    def __init__(self, height: int, width: int, texture: arcade.Texture, text: str, font_size: float):
        label = arcade.gui.UILabel(text=text, width=width, height=height, font_size=font_size)
        super().__init__(tex=texture, text=text, child=label, size_hint=1, width=width, height=height)
