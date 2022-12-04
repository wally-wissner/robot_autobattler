from dataclasses import dataclass
from typing import List

from scripts.backend.team import Team


@dataclass
class GameState(object):
    version: str
    teams: List[Team]
