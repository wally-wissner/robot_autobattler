import numpy as np
import pygame


def draw_regular_polygon(surface, color, vertex_count, radius, position):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(
        surface,
        color,
        [
            (x + r * np.cos(2 * np.pi * i / n), y + r * np.sin(2 * np.pi * i / n))
            for i in range(n)
        ],
    )
