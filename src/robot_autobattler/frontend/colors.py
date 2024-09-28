from collections import namedtuple


ColorRGB = namedtuple(typename="ColorRGB", field_names="r g b")
ColorRGBA = namedtuple(typename="ColorRGBA", field_names="r g b a")


def with_alpha(color: ColorRGB, alpha: int) -> ColorRGBA:
    return ColorRGBA(color.r, color.g, color.b, alpha)


# Chromatic colors
_BLACK = ColorRGB(0, 0, 0)
_WHITE = ColorRGB(255, 255, 255)

_DARK_GRAY = ColorRGB(3, 24, 15)
_LIGHT_GRAY = ColorRGB(80, 80, 80)

_RED = ColorRGB(255, 0, 0)
_GREEN = ColorRGB(0, 255, 0)
_BLUE = ColorRGB(0, 0, 255)

_NEON_GREEN = ColorRGB(0, 243, 154)

_LIGHT_BROWN = ColorRGB(160, 82, 45)
_DARK_BROWN = ColorRGB(139, 69, 19)

_LIGHT_RED = ColorRGB(248, 131, 121)
_LIGHT_BLUE = ColorRGB(173, 216, 230)

_RETRO_RED = ColorRGB(100, 25, 25)
_RETRO_BLUE = ColorRGB(25, 25, 100)


# Utility colors
TRANSPARENT = ColorRGB(1, 1, 1)


# Semantic colors
BACKGROUND = _LIGHT_GRAY
TITLE = _NEON_GREEN

COMMON = ColorRGB(0, 0, 0)
UNCOMMON = ColorRGB(165, 169, 180)
RARE = ColorRGB(170, 146, 82)

BADGE = _LIGHT_RED
CARD = _LIGHT_BLUE
BORDER = _BLACK
UPGRADE_TEXT = _BLACK
OPACITY = _LIGHT_GRAY
POP_UP_PANE = _LIGHT_BROWN
