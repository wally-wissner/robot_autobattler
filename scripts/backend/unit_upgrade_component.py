from abc import ABC, abstractmethod
from dataclasses import dataclass

from scripts.utilities import enums


@dataclass
class UnitUpgradeComponent(ABC):
    name: str
    rarity: enums.ERarity
    bp: int

    @abstractmethod
    def description(self):
        raise NotImplementedError()
