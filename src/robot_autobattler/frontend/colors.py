from collections import namedtuple


ColorRGB = namedtuple("ColorRGB", "r g b")
ColorRGBA = namedtuple("ColorRGBA", "r g b a")


def with_alpha(color: ColorRGB, alpha: int) -> ColorRGBA:
    return ColorRGBA(color.r, color.g, color.b, alpha)


# Utility colors
TRANSPARENT = ColorRGB(1, 1, 1)

# Chromatic colors
BLACK = ColorRGB(0, 0, 0)
WHITE = ColorRGB(255, 255, 255)

DARK_GRAY = ColorRGB(3, 24, 15)
LIGHT_GRAY = ColorRGB(80, 80, 80)

RED = ColorRGB(255, 0, 0)
GREEN = ColorRGB(0, 255, 0)
BLUE = ColorRGB(0, 0, 255)

NEON_GREEN = ColorRGB(0, 243, 154)

LIGHT_BROWN = ColorRGB(160, 82, 45)
DARK_BROWN = ColorRGB(139, 69, 19)

LIGHT_RED = ColorRGB(248, 131, 121)
LIGHT_BLUE = ColorRGB(173, 216, 230)

RETRO_RED = ColorRGB(100, 25, 25)
RETRO_BLUE = ColorRGB(25, 25, 100)

# Semantic colors
COMMON = ColorRGB(0, 0, 0)
UNCOMMON = ColorRGB(165, 169, 180)
RARE = ColorRGB(170, 146, 82)

BADGE = LIGHT_RED
CARD = LIGHT_BLUE
UPGRADE_TEXT = BLACK
