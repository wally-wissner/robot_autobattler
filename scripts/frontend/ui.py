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

