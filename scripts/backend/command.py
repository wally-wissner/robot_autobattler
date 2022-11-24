from scripts.backend.unit import Unit
from scripts.backend.unitstat import EStat
from scripts.backend.battleboard.topology.discrete_topology import Tile


class Command(object):
    def __init__(self, team):
        self.team = team

    def execute(self):
        raise NotImplemented()

    def fail(self):
        raise NotImplemented()

    def affordable(self) -> bool:
        raise NotImplemented()

    def acquired(self) -> bool:
        raise NotImplemented()

    def allowed(self) -> bool:
        return self.acquired() and self.affordable()

    def try_execute(self) -> bool:
        allowed = self.allowed()
        if allowed:
            self.execute()
        else:
            self.fail()
        return allowed


class CommandBattle(Command):
    def __init__(self, team, unit):
        super().__init__(team=team)
        self.unit = unit

    def affordable(self):
        return self.cost() <= self.unit.stats[EStat.AP]

    def cost(self):
        raise NotImplemented()


class CommandUpgrade(Command):
    def __init__(self, team, unit: Unit):
        super().__init__(team=team)
        self.unit = unit

    def affordable(self):
        return self.cost() <= self.team.currency

    def cost(self):
        raise NotImplemented()


class CommandEndTurn(Command):
    def __init__(self, team):
        super().__init__(team=team)

    def execute(self):
        self.team.end_turn()


class CommandAttack(CommandBattle):
    def __init__(self, team, attacker: Unit, target: Tile):
        super().__init__(team=team, unit=attacker)
        self.unit = attacker
        self.target = target

    def affordable(self):
        return True


class CommandMove(CommandBattle):
    def __init__(self, team, unit, target:Tile):
        super().__init__(team=team, unit=unit)
        self.unit = unit
        self.target = target

    def execute(self):
        self.unit.move_along_path(self.target)


class CommandCreateUnit(CommandUpgrade):
    # TODO
    pass

class CommandPromoteUnit(CommandUpgrade):
    # TODO
    pass


class CommandEquip(CommandUpgrade):
    def __init__(self, team, unit: Unit):
        super().__init__(team=team, unit=unit)
        self.unit = unit

    def affordable(self):
        return self.cost() <= self.team.currency


class CommandUnequip(CommandUpgrade):
    # TODO
    pass
