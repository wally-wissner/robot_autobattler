from pygame import Surface

from utils.geometry import Rectangle


_x_anchors = {"left", "right", "center"}
_y_anchors = {"top", "bottom", "center"}


def anchored_blit(
    target: Surface,
    source: Surface,
    offset: tuple,
    x_anchor: str,
    y_anchor: str,
):
    rect_target = Rectangle.from_rect(target.get_rect())
    rect_source = Rectangle.from_rect(source.get_rect())

    x_dest = {
        "left": 0,
        "right": rect_source.x_max - rect_target.x_max,
        "center": (rect_source.x_max - rect_target.x_max) / 2,
    }[x_anchor] + offset[0]

    y_dest = {
        "top": 0,
        "bottom": rect_source.y_max - rect_target.y_max,
        "center": (rect_source.y_max - rect_target.y_max) / 2,
    }[y_anchor] + offset[1]

    target.blit(source=source, dest=(x_dest, y_dest))
