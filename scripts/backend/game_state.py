from scripts.backend.event import Event
from scripts.backend.team import Team
from scripts.backend.unit import Unit
from scripts.backend.upgrades import Card, CardAbility, CardAbilityCondition, CardAbilityEffect
from scripts.utilities import enums
from scripts.utilities.game_math import clamp


class GameState(object):
    def __init__(self, version: str):
        self.version = version

        self.teams: list[Team] = []

        self.level: int = 1
        self.round: int = 1
        self.turn: int = 1

        event_history: list[Event] = []

    def units(self) -> set[Unit]:
        return {unit for team in self.teams for unit in team.units}

    def start_level(self):
        self.level += 1

    def start_round(self):
        self.round += 1

    def start_turn(self):
        self.turn += 1

    def evaluate_active_cards(self):
        # TODO
        pass

    def evaluate_card(self, actor: Unit, card: Card):
        for ability in card.abilities:
            self.evaluate_card_ability(actor, ability)

    def evaluate_card_ability(self, card_ability: CardAbility):
        # TODO
        pass

    # def evaluate_card_ability_condition(self, card_ability_condition: CardAbilityCondition):
    #
    #
    # def evaluate_card_ability_effect(self, card_ability_effect: CardAbilityEffect):
    #     if card_ability_effect.actor_category == enums.EActorCategory.ALLY


    def unit_stat_value(self, unit: Unit, stat: enums.EStat) -> float:
        # Initialize value to base value.
        value = unit.stats[stat].base_value
        # Split stat modifiers by operation.
        stat_modifiers = {operation: [] for operation in enums.EOperation}
        for stat_modifier in unit.stat_modifiers(stat):
            stat_modifiers[stat_modifier.operation].append(stat_modifier)
        # Apply appropriate operation from each stat modifier.
        for stat_modifier in stat_modifiers[enums.EOperation.PLUS]:
            value += stat_modifier.value
        for stat_modifier in stat_modifiers[enums.EOperation.TIMES]:
            value *= stat_modifier.value
        if stat_modifiers[enums.EOperation.ASSIGN]:
            value = max(stat_modifier.value for stat_modifier in stat_modifiers[enums.EOperation.ASSIGN])
        # Bound value between min value and max value.
        return clamp(value, unit.stats[stat].min_value, unit.stats[stat].max_value)
