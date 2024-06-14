from functools import cache

import pygame

from config import absolute_path
from utils.enums import EFont


@cache
def get_font(font: EFont, size: int):
    return pygame.font.Font(
        filename=absolute_path(f"assets/fonts/{font.value}.ttf"), size=size
    )


title_font = EFont.JETBRAINS_MONO_REGULAR
card_font = EFont.JETBRAINS_MONO_REGULAR
