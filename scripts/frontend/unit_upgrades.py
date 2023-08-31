import arcade
import arcade.gui
from dataclasses import dataclass
from math import ceil
from PIL import Image, ImageDraw
from typing import Callable

from scripts.backend.badges import Badge
from scripts.backend.cards import Card
from scripts.backend.unit_upgrades import UnitUpgrade
from scripts.backend.unit_upgrade_components import UnitUpgradeComponent
from scripts.frontend import colors
from scripts.frontend.ui import UITextPane
# from scripts.frontend.fonts import get_font
from scripts.utilities.enums import EFont, EScene, EStat
from scripts.utilities.geometry import Vector2


@dataclass(eq=True, frozen=True)
class TextureParams:
    color: colors.ColorRGB
    width: int
    height: int


class UIUpgradeComponent(UITextPane):
    textures: dict[(TextureParams, arcade.Texture)] = {}

    def __init__(self, unit_upgrade_component: UnitUpgradeComponent, width: int, description: bool):
        self.unit_upgrade_component = unit_upgrade_component
        self.w = width
        self.h = width // 2
        self.description = description
        self.texture_params = TextureParams(self._get_color(), self.h, self.w)
        super().__init__(
            width=self.w,
            height=self.h,
            texture=self._get_texture(),
            text=self.unit_upgrade_component.name,
            font_size=self.w/10,
        )

    def _get_color(self) -> colors.ColorRGB:
        if isinstance(self.unit_upgrade_component, Badge):
            return colors.RETRO_BLUE
        elif isinstance(self.unit_upgrade_component, Card):
            return colors.RETRO_RED

    def _get_texture(self) -> arcade.Texture:
        if self.texture_params not in self.textures:
            self.textures[self.texture_params] = arcade.Texture(
                name=str(self.texture_params),
                image=Image.new(mode='RGB', size=(self.w, self.h), color=self._get_color()),
            )
        return self.textures[self.texture_params]


class UIUnitUpgrade(arcade.gui.UIPadding, arcade.gui.UIDraggableMixin):
    def __init__(self, unit_upgrade: UnitUpgrade, width: int, height: int, x: int, y: int, description: bool):
        padding = tuple(ceil(width / 100) for _ in range(4))
        self.unit_upgrade = unit_upgrade
        self.box = arcade.gui.UIBoxLayout(x=x, y=y, vertical=True, space_between=0)
        self.box.add(UIUpgradeComponent(unit_upgrade_component=unit_upgrade.badge, width=width, description=description))
        self.box.add(UIUpgradeComponent(unit_upgrade_component=unit_upgrade.card, width=width, description=description))
        super().__init__(child=self.box, bg_color=colors.RARE, width=width, height=height, padding=padding)
