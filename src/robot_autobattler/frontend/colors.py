from collections import namedtuple


ColorRGB = namedtuple("ColorRGB", "r g b")


BLACK = ColorRGB(0, 0, 0)
WHITE = ColorRGB(255, 255, 255)

DARK_GRAY = ColorRGB(40, 40, 40)
LIGHT_GRAY = ColorRGB(80, 80, 80)

RED = ColorRGB(255, 0, 0)
GREEN = ColorRGB(0, 255, 0)
BLUE = ColorRGB(0, 0, 255)

NEON_GREEN = ColorRGB(65, 255, 0)

LIGHT_BROWN = ColorRGB(160, 82, 45)
DARK_BROWN = ColorRGB(139, 69, 19)

RETRO_RED = ColorRGB(100, 25, 25)
RETRO_BLUE = ColorRGB(25, 25, 100)

COMMON = ColorRGB(0, 0, 0)
UNCOMMON = ColorRGB(170, 204, 232)
RARE = ColorRGB(170, 146, 82)
