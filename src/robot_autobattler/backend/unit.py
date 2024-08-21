import math

from backend.physics import DiscBody
from backend.unitstat import ConsumableStat, Stat, StatModifier
from backend.upgrades import Upgrade
from frontend.colors import ColorRGB
from utils.data_structures import Inventory, ShiftList
from utils.enums import EStat
from utils.identifiers import UUIDIdentifier


class Unit(DiscBody, UUIDIdentifier):
    def __init__(self, team, level: int):
        self.level = level

        self.alive = True
        self.upgrades: ShiftList[Upgrade] = ShiftList()
        self.status_effects = Inventory()
        self.stats = self._init_stats()

        DiscBody.__init__(self, team=team)
        UUIDIdentifier.__init__(self)

    def _init_stats(self) -> dict[EStat, Stat | ConsumableStat]:
        stats = {}
        for stat in EStat:
            stats[stat] = Stat(base_value=0)
        # Non-zero default stats.
        stats[EStat.MASS] = Stat(base_value=10)
        stats[EStat.SIZE] = Stat(base_value=10)
        # Consumable stats.
        stats[EStat.HP] = ConsumableStat(refill_on_encounter_start=True)
        stats[EStat.WINDUP] = ConsumableStat()
        return stats

    def stat_modifiers(self, stat: EStat) -> list[StatModifier]:
        stat_modifiers = []
        for upgrade in self.upgrades:
            for stat_modifier in upgrade.badge.stat_modifiers:
                if stat_modifier.stat == stat:
                    stat_modifiers.append(stat_modifier)
        return stat_modifiers

    def bp_used(self) -> int:
        return sum(upgrade.bp for upgrade in self.upgrades)

    def bp_available(self) -> int:
        return self.level - self.bp_used()

    def take_damage(self, damage: int) -> None:
        self.stats[EStat.HP] -= damage
        if self.stats[EStat.HP].current_value <= 0:
            self.die()

    def die(self) -> None:
        self.alive = False

    def level_up_cost(self) -> int:
        return int(math.sqrt(self.level))

    def add_upgrade(self, upgrade: Upgrade) -> None:
        self.upgrades.append(upgrade)

    def color(self) -> ColorRGB:
        return ColorRGB(*(int(hash(self.id) // 10 ** (3 * i) % 256) for i in range(3)))
