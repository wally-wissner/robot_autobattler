import numpy as np

from scripts.backend.cards import Card, SimpleCard, CardAbility, CardAbilityCondition, CardAbilityEffect
from scripts.backend.event import Event, EventHistory
from scripts.backend.team import Team
from scripts.backend.unit import Unit
from scripts.backend.factories import generate_team
from scripts.utilities import enums
from scripts.utilities.game_math import clamp


mapping_weapon_power = {
    enums.EWeapon.LASER: enums.EStat.LASER_POWER,
    enums.EWeapon.MISSILE: enums.EStat.MISSILE_POWER,
    enums.EWeapon.RAILGUN: enums.EStat.RAILGUN_POWER,
}

mapping_weapon_accuracy = {
    enums.EWeapon.LASER: enums.EStat.LASER_ACCURACY,
    enums.EWeapon.MISSILE: enums.EStat.MISSILE_ACCURACY,
    enums.EWeapon.RAILGUN: enums.EStat.RAILGUN_ACCURACY,
}


class Game(object):
    def __init__(self, version: str) -> None:
        self.version = version

        self.teams: list[Team] = [
            generate_team(is_player=True, total_level=30, n_units=10, quality=.75),
            generate_team(is_player=False, total_level=10, n_units=5, quality=.75)
        ]

        self.encounter: int = 1
        self.round: int = 1
        self.turn: int = 1

        event_history = EventHistory()

    def units(self) -> set[Unit]:
        return {unit for team in self.teams for unit in team.units}

    def start_encounter(self) -> None:
        self.encounter += 1

        for team in self.teams:
            for unit in team.units:
                unit.status_effects.clear()
                self.assign_initial_position(unit)

    def start_round(self) -> None:
        self.round += 1

    def start_turn(self) -> None:
        self.turn += 1

    def assign_initial_position(self, unit: Unit) -> None:
        deviation = 10
        team_distance = 50
        team_center = team_distance * np.array([-1 if unit.team.is_player else 1, 0])
        unit_relative_position = np.random.randn(2)
        unit.position = deviation * unit_relative_position + team_center

    def evaluate_active_cards(self) -> None:
        # TODO
        pass

    def evaluate_card(self, actor: Unit, card: SimpleCard) -> None:
        for card_ability in card.abilities:
            self.evaluate_card_ability(actor, card_ability)

    def evaluate_card_ability(self, actor: Unit, card_ability: CardAbility) -> None:
        # TODO
        pass

    # def evaluate_card_ability_condition(self, card_ability_condition: CardAbilityCondition):
    #
    #
    # def evaluate_card_ability_effect(self, card_ability_effect: CardAbilityEffect):
    #     if card_ability_effect.actor_category == enums.EActorCategory.ALLY

    def evaluate_attack(self, actor: Unit, target: Unit, weapon: enums.EWeapon) -> None:
        weapon_power = actor.stats[mapping_weapon_power[weapon]]
        damage_output = actor.stats[enums.EStat.POWER] + weapon_power
        affected_units = [target]
        for affected_unit in affected_units:
            if affected_unit.stats[enums.EStat.SHIELD_CHARGES].current_value > 0:
                affected_unit.stats[enums.EStat.SHIELD_CHARGES] -= 1
            else:
                damage = clamp(
                    damage_output - affected_unit.stats[enums.EStat.ARMOR],
                    min_value=affected_unit.stats[enums.EStat.MIN_DAMAGE_DEALT_TO],
                    max_value=affected_unit.stats[enums.EStat.MAX_DAMAGE_DEALT_TO],
                )
                affected_unit.take_damage(damage)

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
