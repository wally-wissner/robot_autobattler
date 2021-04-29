from scripts.utilities.autoname_enum import AutoNameEnum, auto


class EScene(AutoNameEnum):



class _Scene(object):
    def handle_event(self, input):
        raise NotImplemented()

    def draw(self):
        raise NotImplemented()


class MainMenuScene(_Scene):
    def handle_event(self, input):
        # todo
        pass

    def draw(self):


class BattleMapScene(_Scene):
    def handle_event(self, input):
        # todo
        pass

    def draw(self):


class AttackingScene(_Scene):
    def handle_event(self, input):
        # todo
        pass



class MovingScene(_Scene):
    def handle_event(self, input):
        #todo
        pass


class DialogueScene(_Scene):
    def handle_event(self, input):
        #todo
        pass
