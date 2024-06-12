from abc import ABC, abstractmethod
from dataclasses import dataclass

from frontend.colors import ColorRGB
from utils import enums


@dataclass(frozen=True)
class UpgradeComponent(ABC):
    name: str
    rarity: enums.ERarity
    bp: int

    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def color(self) -> ColorRGB:
        raise NotImplementedError()
