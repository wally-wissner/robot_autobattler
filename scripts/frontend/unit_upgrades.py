import arcade
import arcade.gui
from dataclasses import dataclass
from PIL import Image, ImageDraw
from typing import Callable

from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.frontend import colors
from scripts.frontend.ui import UITextPane
# from scripts.frontend.fonts import get_font
from scripts.utilities.enums import EFont, EScene, EStat
from scripts.utilities.geometry import Vector2


class UIUnitUpgrade(arcade.gui.UIPadding, arcade.gui.UIDraggableMixin):
    def __init__(self, unit_upgrade: UnitUpgrade, height: int, width: int, x: int, y: int):
        self.unit_upgrade = unit_upgrade
        self.card_color = colors.RETRO_RED
        self.badge_color = colors.RETRO_BLUE
        self.texture_card = arcade.texture.Texture(
            name="bg_card",
            image=Image.new(mode='RGB', size=(width, height // 2), color=self.card_color),
        )
        self.texture_badge = arcade.texture.Texture(
            name="bg_badge",
            image=Image.new(mode='RGB', size=(width, height // 2), color=self.badge_color),
        )
        self.box = arcade.gui.UIBoxLayout(x=x, y=y, vertical=True, space_between=0)
        self.box.add(UITextPane(
            width=width,
            height=height//2,
            texture=self.texture_card,
            text=self.unit_upgrade.card.name,
            font_size=10,
        ))
        self.box.add(UITextPane(
            width=width,
            height=height//2,
            texture=self.texture_badge,
            text=self.unit_upgrade.badge.name,
            font_size=10,
        ))
        super().__init__(child=self.box, bg_color=colors.RARE, height=height, width=width, padding=(2, 2, 2, 2))
