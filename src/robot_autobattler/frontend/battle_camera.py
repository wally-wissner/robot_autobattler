import pygame as pg

from backend.game import Game


class BattleCamera:
    def __init__(self, application, game: Game, center: pg.Vector2, zoom: float):
        self.display_surface = pg.display.get_surface()
        self.application = application
        self.game = game
        self.center = center
        self.zoom = zoom

    def draw(self):
        raise NotImplementedError()

    def update_bounds(self, padding: float) -> None:
        raise NotImplementedError()
