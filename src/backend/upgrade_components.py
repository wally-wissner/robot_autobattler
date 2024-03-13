from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.utilities import enums


@dataclass
class UpgradeComponent(ABC):
    name: str
    rarity: enums.ERarity
    bp: int

    @abstractmethod
    def description(self):
        raise NotImplementedError()
