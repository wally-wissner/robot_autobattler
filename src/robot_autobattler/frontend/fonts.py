import pygame
from functools import cache

from config import absolute_path
from utils.enums import EFont


@cache
def get_font(font: EFont, size: int):
    return pygame.font.Font(absolute_path(f"assets/fonts/{font.value}.ttf"), size)
