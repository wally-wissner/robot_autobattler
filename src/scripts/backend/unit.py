import math

from src.scripts.backend.inventory import Inventory
from src.scripts.backend.physics import DiscBody
from src.scripts.backend.unitstat import Stat, ConsumableStat
from src.scripts.backend.upgrades import Upgrade
from src.scripts.frontend.colors import ColorRGB
from src.scripts.utilities.enums import EStat
from src.scripts.utilities.identifiers import uuid_identifier


@uuid_identifier
class Unit(DiscBody):
    def __init__(self, team, level):
        self.level = level

        self.alive = True
        self.upgrades: list[Upgrade] = []
        self.status_effects = Inventory()
        self.stats = self._init_stats()

        super().__init__(team=team)

    def _init_stats(self) -> dict[EStat, Stat]:
        stats = {}
        for stat in EStat:
            stats[stat] = Stat(base_value=0)
        # Non-zero default stats.
            stats[EStat.MASS] = Stat(base_value=10)
            stats[EStat.SIZE] = Stat(base_value=10)
        # Consumable stats.
            stats[EStat.HP] = ConsumableStat(refill_on_encounter_start=True)
            stats[EStat.AP] = ConsumableStat(refill_on_turn_start=True)
        return stats

    def stat_modifiers(self, stat: EStat):
        stat_modifiers = []
        for upgrade in self.upgrades:
            for stat_modifier in upgrade.badge.stat_modifiers:
                if stat_modifier.stat == stat:
                    stat_modifiers.append(stat_modifier)
        return stat_modifiers

    def bp_used(self):
        return sum(upgrade.bp for upgrade in self.upgrades)

    def bp_available(self):
        return self.level - self.bp_used()

    def take_damage(self, damage):
        self.stats[EStat.HP] -= damage
        if self.stats[EStat.HP].current_value <= 0:
            self.die()

    def die(self):
        self.alive = False

    def level_up_cost(self):
        return int(math.sqrt(self.level))

    def add_upgrade(self, upgrade: Upgrade):
        self.upgrades.append(upgrade)

    def color(self) -> ColorRGB:
        return ColorRGB(*(int(hash(self.id) // 10 ** (3 * i) % 256) for i in range(3)))
