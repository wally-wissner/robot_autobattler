"""
UI elements for upgrades.
"""

from dataclasses import dataclass
from math import ceil

import arcade
import arcade.gui
from PIL import Image

from backend.badges import Badge
from backend.cards import Card
from backend.upgrades import Upgrade
from backend.upgrade_components import UpgradeComponent
from frontend import colors

# from frontend.fonts import get_font


@dataclass(eq=True, frozen=True)
class TextureParams:
    color: colors.ColorRGB
    width: int
    height: int


class UIUpgradeComponent(arcade.gui.UITexturePane):
    textures: dict[(TextureParams, arcade.Texture)] = {}

    def __init__(
        self, upgrade_component: UpgradeComponent, width: int, description: bool
    ):
        self.upgrade_component = upgrade_component
        self.w = width
        self.h = width // 2
        self.description = description
        self.texture_params = TextureParams(self._get_color(), self.h, self.w)

        v_proportions = (0.175, 0.025, 0.8)
        if description:
            name_label = arcade.gui.UILabel(
                text=self.upgrade_component.name,
                width=self.w,
                height=v_proportions[0] * self.h,
                align="left",
                font_size=self.w / 20,
            )
            description_label = arcade.gui.UILabel(
                text=self.upgrade_component.description(),
                width=self.w,
                height=v_proportions[2] * self.h,
                align="left",
                font_size=self.w / 25,
            )
            body = arcade.gui.widgets.UIBoxLayout()
            body.add(name_label.with_space_around(bottom=v_proportions[1] * self.h))
            body.add(description_label)
        else:
            body = arcade.gui.UILabel(
                text=self.upgrade_component.name,
                width=self.w,
                height=self.h,
                align="center",
                font_size=self.w / 15,
            )

        super().__init__(
            tex=self._get_texture(),
            child=body,
            size_hint=1,
            width=self.w,
            height=self.h,
        )

    def _get_color(self) -> colors.ColorRGB:
        if isinstance(self.upgrade_component, Badge):
            color = colors.RETRO_BLUE
        if isinstance(self.upgrade_component, Card):
            color = colors.RETRO_RED
        return color

    def _get_texture(self) -> arcade.Texture:
        if self.texture_params not in self.textures:
            self.textures[self.texture_params] = arcade.Texture(
                name=str(self.texture_params),
                image=Image.new(
                    mode="RGB", size=(self.w, self.h), color=self._get_color()
                ),
            )
        return self.textures[self.texture_params]


class UIUnitUpgrade(arcade.gui.UIPadding, arcade.gui.UIDraggableMixin):
    def __init__(
        self,
        upgrade: Upgrade,
        width: int,
        height: int,
        x: int,
        y: int,
        description: bool,
    ):
        padding = tuple(ceil(width / 100) for _ in range(4))
        self.upgrade = upgrade
        self.box = arcade.gui.UIBoxLayout(x=x, y=y, vertical=True, space_between=0)
        self.box.add(
            UIUpgradeComponent(
                upgrade_component=upgrade.badge, width=width, description=description
            )
        )
        self.box.add(
            UIUpgradeComponent(
                upgrade_component=upgrade.card, width=width, description=description
            )
        )
        super().__init__(
            child=self.box,
            bg_color=colors.RARE,
            width=width,
            height=height,
            padding=padding,
        )
