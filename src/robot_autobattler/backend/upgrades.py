from uuid import uuid4

from pydantic import BaseModel, Field

from backend.badges import Badge
from backend.cards import Card


class Upgrade(BaseModel):
    badge: Badge
    card: Card
    removable: bool = True
    id: str = Field(default_factory=lambda: uuid4().hex)

    @property
    def rarity(self):
        return max(self.badge.rarity, self.card.rarity)

    @property
    def bp(self):
        min_negative_bp = min(bp for bp in [0, self.badge.bp, self.card.bp] if bp <= 0)
        max_positive_bp = max(bp for bp in [0, self.badge.bp, self.card.bp] if bp >= 0)
        return max_positive_bp + min_negative_bp

    def __eq__(self, other):
        return self.id == other.id
