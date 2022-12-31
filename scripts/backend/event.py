import dataclasses

import pandas as pd
from dataclasses import dataclass

from scripts.backend.cards import Card, SimpleCard
from scripts.utilities.enums import EEventType
from scripts.utilities.identifiers import uuid_identifier


@uuid_identifier
@dataclass
class Event(object):
    level: int
    round: int
    turn: int
    event_type: EEventType
    actor_id: str
    # card: Card
    damage_dealt: int


class EventHistory(object):
    def __init__(self):
        # self.df = pd.DataFrame()
        self.df = pd.DataFrame({
            "level": pd.Series(dtype=int),
            "round": pd.Series(dtype=int),
            "turn": pd.Series(dtype=int),
            "event_type": pd.Series(dtype=object),
            "actor_id": pd.Series(dtype=str),
            "damage_dealt": pd.Series(dtype=int),
        })
        # self.df = pd.DataFrame({key: value for key, value in Event.__dict__.items() if key != "id"})
        # self.df = pd.DataFrame(dataclasses.fields(Event))

    def append(self, event: Event):
        self.df = pd.concat([
            self.df,
            pd.DataFrame({key: value for key, value in event.__dict__.items() if key != "id"}, index=[event.id])
        ])

    def __repr__(self):
        return self.df.to_string()
