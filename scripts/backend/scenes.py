import numpy as np
import pygame as pg
import pygame_gui as gui


class Scene(object):
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        raise NotImplemented()

    def draw(self):
        raise NotImplemented()


class MainMenuScene(Scene):
    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        button_new_game = gui.elements.UIButton(
            relative_rect=pg.Rect(
                self.game.relative_to_vector2((.45, .5)),
                self.game.relative_to_vector2((.55, .45)),
            ),
            text="New Game",
            manager=self.game.manager,
        )


class SettingsMenuScene(Scene):
    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass


class UpgradeScene(Scene):
    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass


class BattleScene(Scene):
    def handle_events(self, events):
        # todo
        pass

    def draw(self):
        # todo
        pass


class TestScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.circle_position = pg.Vector2(
            self.game.settings.resolution[0] / 2,
            self.game.settings.resolution[1] / 2,
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                key = event.key

                if key == pg.K_LEFT:
                    self.circle_position += [-1, 0]
                if key == pg.K_RIGHT:
                    self.circle_position += [1, 0]

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = event.pos
                print(pos)
                # if sprite.get_rect().collidepoint(x, y):
                #     print('clicked on image')

            if event.type == pg.MOUSEBUTTONUP:
                pos = event.pos


    def draw(self):
        self.circle_position += np.random.randn(2)
        pg.draw.circle(self.game.display, (255, 255, 255), self.circle_position, 4)
        pg.draw.circle(self.game.display, (0, 0, 255), self.circle_position, 3)

        # self.display.blit(bg, (0, 0))
        # pg.draw.rect()

        button_layout_rect = pg.Rect((0, 0), (100, 30))

        button = gui.elements.UIButton(
            relative_rect=button_layout_rect,
            text="Hello",
            manager=self.game.manager,
            # container=gui.elements.CON,
        )

        button_new_game = gui.elements.UIButton(
            relative_rect=self.game.relative_to_rect((.40, .5), (.60, .6)),
            text="New Game",
            manager=self.game.manager,
        )
