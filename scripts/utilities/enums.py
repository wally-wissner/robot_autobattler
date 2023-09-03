from enum import Enum, IntEnum, auto


class AutoNameEnum(Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self


class EScene(AutoNameEnum):
    MAIN_MENU = auto()
    SETTINGS = auto()
    BATTLE = auto()
    UPGRADE = auto()
    REWARDS = auto()


class EUILayer(Enum):
    BATTLE_BACKGROUND = 0
    BATTLE_UNIT = 1
    BATTLE_WEAPON = 2


class ERarity(IntEnum):
    # np.random.choice does not preserve type of enums having value 0.
    COMMON = 1
    UNCOMMON = 2
    RARE = 3


class ECollectable(AutoNameEnum):
    SCRAP = auto()


class EStat(AutoNameEnum):
    # Consumable stats.
    HP = auto()
    AP = auto()

    # Non-zero default stats.
    SIZE = auto()
    MASS = auto()

    # Zero default stats.
    AP_SOT_ENDURANCE = auto()
    AP_ON_EOT = auto()

    MOVE_COST_AP = auto()

    KNOCKBACK = auto()
    KNOCKBACK_DAMAGE = auto()

    POWER = auto()
    POWER_ADDER = auto()
    POWER_MULTIPLIER = auto()

    MIN_DAMAGE_DEALT_BY = auto()
    MAX_DAMAGE_DEALT_BY = auto()
    MIN_DAMAGE_DEALT_TO = auto()
    MAX_DAMAGE_DEALT_TO = auto()

    ACCURACY = auto()

    LASER_ACCURACY = auto()
    LASER_POWER = auto()
    LASER_COST_AP = auto()
    LASER_CHARGES = auto()
    LASER_PENETRATION = auto()
    LASER_SUBSEQUENT_COST_AP = auto()
    LASER_ACTION_DISCHARGE_ALL = auto()
    LASER_AOE = auto()

    MISSILE_ACCURACY = auto()
    MISSILE_POWER = auto()
    MISSILE_COST_AP = auto()
    MISSILE_RANGE = auto()
    MISSILE_AOE = auto()

    RAILGUN_ACCURACY = auto()
    RAILGUN_POWER = auto()
    RAILGUN_COST_AP = auto()
    RAILGUN_RANGE = auto()
    RAILGUN_RICOCHET = auto()
    RAILGUN_FRAGMENTATION = auto()
    RAILGUN_PENETRATION_PROBABILITY = auto()
    RAILGUN_AOE = auto()

    ARMOR = auto()

    EVASION = auto()
    EVASION_FRIENDLY_FIRE = auto()

    SHIELD_CHARGES = auto()
    SMART_SHIELDS = auto()

    REPAIR = auto()

    SELFDESTRUCT_POWER = auto()
    SELFDESTRUCT_AOE_RADIUS = auto()

    USE_NEAREST_ALLY_TO_TARGET = auto()

    ON_DEATH_EXPLODE = auto()
    ON_DEATH_GAME_OVER = auto()

    REACT_ADDER = auto()
    REACT_MULTIPLIER = auto()

    REACT_ACCURACY = auto()
    REACT_DISCOUNT = auto()
    REACT_POWER = auto()
    REACT_ATTACKS = auto()


class EOperation(AutoNameEnum):
    PLUS = "+"
    TIMES = "*"
    ASSIGN = "="


class EWeapon(AutoNameEnum):
    LASER = auto()
    MISSILE = auto()
    RAILGUN = auto()


class EUnitAction(AutoNameEnum):
    MOVE = auto()
    ATTACK = auto()
    PRODUCE = auto()
    CHARGE_LASERS = auto()
    CHARGE_SHIELDS = auto()
    DIE = auto()
    EXPLODE = auto()
    REPAIR = auto()


class EResource(AutoNameEnum):
    ENERGY = auto()
    PLASMA = auto()
    CAPACITOR = auto()
    MISSILE = auto()
    BOMB = auto()
    PATCH = auto()
    CYCLE = auto()
    CREDIT = auto()


class EUnitCategory(AutoNameEnum):
    THIS = auto()
    UNIT = auto()
    ALLY = auto()
    ENEMY = auto()


class EUnitProperty(AutoNameEnum):
    MOST_DAMAGED = auto()
    LEAST_DAMAGED = auto()
    WEAK = auto()
    STRONG = auto()
    CLOSEST = auto()
    FARTHEST = auto()
    LAST_DAMAGED = auto()


class EUnitQuantity(AutoNameEnum):
    EACH = auto()


class EComparison(AutoNameEnum):
    EQ = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()


class EVariable(AutoNameEnum):
    TURN = auto()


class EEventType(AutoNameEnum):
    UPGRADE_ATTACHED = auto()
    UNIT_ATTACKED = auto()
    RESOURCE_PRODUCED = auto()


class EFont(AutoNameEnum):
    JETBRAINS_MONO_REGULAR = auto()
