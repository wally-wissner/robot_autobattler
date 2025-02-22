import numpy as np

from backend.cards import Card, SimpleCard, CardAbility
from backend.event import EventHistory
from backend.physics import PhysicsBody
from backend.team import Team
from backend.unit import Unit
from backend.factories import generate_team, generate_upgrade
from utils import enums
from utils.game_math import clamp
from utils.geometry import Vector2


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


class Game:
    # pylint: disable=unused-argument

    def __init__(self, version: str, seed: int) -> None:
        self.version = version

        self.teams = self.generate_teams()
        self.event_history = EventHistory()

        self.projectiles: list[PhysicsBody] = []

    def generate_teams(self) -> list[Team]:
        teams: list[Team] = [
            generate_team(is_player=True, total_level=30, n_units=10, quality=0.75),
            generate_team(is_player=False, total_level=10, n_units=5, quality=0.75),
        ]
        for _ in range(5):
            teams[0].inventory.append(generate_upgrade())
        return teams

    def player_team(self) -> Team:
        return self.teams[0]

    def physics_bodies(self) -> list[PhysicsBody]:
        return self.units() + self.projectiles

    def units(self) -> list[Unit]:
        return [unit for team in self.teams for unit in team.units]

    def start_battle(self) -> None:
        self.place_units()
        for team in self.teams:
            for unit in team.units:
                unit.status_effects.clear()
                unit.size = self.stat_value(unit, enums.EStat.SIZE)
                unit.mass = self.stat_value(unit, enums.EStat.MASS)

    def place_units(self) -> None:
        deviation = 50
        # team_distance = 50
        for team in self.teams:
            for unit in team.units:
                # team_center = Vector2(.25, .5) if team.is_player else Vector2(.75, .5)
                team_center = (
                    Vector2(x=400, y=450) if team.is_player else Vector2(x=1200, y=450)
                )
                random_vector = np.random.randn(2)
                unit_relative_position = Vector2(x=random_vector[0], y=random_vector[1])
                unit.position = deviation * unit_relative_position + team_center

    def evaluate_active_cards(self) -> None:
        for team in self.teams:
            card = team.hand.pop()
            self.evaluate_card(actor=team.card_actor(card), card=card)
            team.graveyard.append(card)

    def evaluate_card(self, actor: Unit, card: Card) -> None:
        if isinstance(card, SimpleCard):
            for card_ability in card.abilities:
                self.evaluate_card_ability(actor, card_ability)
        else:
            raise NotImplementedError("Non-simple cards not implemented.")

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
                    value=damage_output - affected_unit.stats[enums.EStat.ARMOR],
                    min_value=affected_unit.stats[enums.EStat.MIN_DAMAGE_DEALT_TO],
                    max_value=affected_unit.stats[enums.EStat.MAX_DAMAGE_DEALT_TO],
                )
                affected_unit.take_damage(damage)

    def stat_value(self, unit: Unit, stat: enums.EStat) -> float:
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
            value = max(
                stat_modifier.value
                for stat_modifier in stat_modifiers[enums.EOperation.ASSIGN]
            )
        # Bound value between min value and max value.
        return clamp(
            value=value,
            min_value=unit.stats[stat].min_value,
            max_value=unit.stats[stat].max_value,
        )

    def update_physics(self, dt) -> None:
        for physics_body in self.physics_bodies():
            physics_body.update(dt)
