from dataclasses import dataclass

from scripts.backend.upgrades import Card
from scripts.utilities.enums import EEventType


@dataclass
class Event(object):
    level: int
    round: int
    turn: int
    event_type: EEventType
    actor_id: int
    card: Card
    damage_dealt: int
