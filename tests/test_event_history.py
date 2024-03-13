import unittest
from src.utilities.enums import EEventType
from src.backend.event import Event, EventHistory


class TestEventHistory(unittest.TestCase):
    def setUp(self):
        self.e1 = Event(level=0, round=1, turn=6, event_type=EEventType.UNIT_ATTACKED, actor_id="34d3f2q", damage_dealt=10)
        self.e2 = Event(level=0, round=1, turn=6, event_type=EEventType.UNIT_ATTACKED, actor_id="64jl324", damage_dealt=2)

    def test_append(self):
        eh = EventHistory()
        eh.append(self.e1)
        eh.append(self.e2)
        self.assertTrue(eh.df.shape[0] == 2)
