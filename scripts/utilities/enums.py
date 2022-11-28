from enum import Enum, auto


class AutoNameEnum(Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self


class ERarity(AutoNameEnum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()


class EStat(AutoNameEnum):
    SIZE = auto()
    MASS = auto()

    HP = auto()

    BP = auto()

    AP = auto()
    AP_SOT_ENDURANCE = auto()
    AP_ON_EOT = auto()

    MOVE_COST_AP = auto()

    KNOCKBACK = auto()
    KNOCKBACK_DAMAGE = auto()

    POWER = auto()
    POWER_ADDER = auto()
    POWER_MULTIPLIER = auto()

    LASER_DISPERSION_ANGLE = auto()
    LASER_ACCURACY = auto()
    LASER_ACCURACY_DROPOFF = auto()
    LASER_POWER = auto()
    LASER_COST_AP = auto()
    LASER_CHARGES = auto()
    LASER_PENETRATION = auto()
    LASER_SUBSEQUENT_COST_AP = auto()
    LASER_ACTION_DISCHARGE_ALL = auto()
    LASER_AOE = auto()

    MISSILE_DISPERSION_ANGLE = auto()
    MISSILE_ACCURACY = auto()
    MISSILE_ACCURACY_DROPOFF = auto()
    MISSILE_POWER = auto()
    MISSILE_COST_AP = auto()
    MISSILE_RANGE = auto()
    MISSILE_AOE = auto()

    RAILGUN_DISPERSION_ANGLE = auto()
    RAILGUN_ACCURACY = auto()
    RAILGUN_ACCURACY_DROPOFF = auto()
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

    USE_NEAREST_ALLY_TO_TILE = auto()

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
    MISSILE_LAUNCHER = auto()
    RAILGUN = auto()


class EUnitAction(AutoNameEnum):
    ATTACK = auto()
    CHARGE_LASERS = auto()
    CHARGE_SHIELDS = auto()
    DIE = auto()
    EXPLODE = auto()
    REPAIR = auto()
    PRODUCE = auto()


class EResource(AutoNameEnum):
    ENERGY = auto()
    PLASMA = auto()
    CAPACITOR = auto()
    MISSILE = auto()
    BOMB = auto()
    PATCH = auto()
    CYCLE = auto()
    CREDIT = auto()


class EDevice(AutoNameEnum):
    pass


class ECardEffectAction(AutoNameEnum):
    DEALS_DAMAGE = auto()
    DRAW = auto()


class EActorCategory(AutoNameEnum):
    UNIT = auto()
    ALLY = auto()
    ENEMY = auto()


class ETargetCategory(AutoNameEnum):
    UNIT = auto()
    ALLY = auto()
    ENEMY = auto()


class EActorProperty(AutoNameEnum):
    pass


class EActorQuantity(AutoNameEnum):
    INTEGER = auto()
    EACH = auto()


class ETargetProperty(AutoNameEnum):
    pass


class ETargetQuantity(AutoNameEnum):
    INTEGER = auto()
    EACH = auto()


class EElement(AutoNameEnum):
    pass


class EComparison(AutoNameEnum):
    EQ = "="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="


class EVariable(AutoNameEnum):
    TURN = auto()
