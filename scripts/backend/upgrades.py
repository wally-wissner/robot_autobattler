from dataclasses import dataclass

from scripts.backend.badges import Badge
from scripts.backend.cards import Card
from scripts.utilities.identifiers import uuid_identifier


@uuid_identifier
@dataclass
class Upgrade(object):
    badge: Badge
    card: Card
    removable: bool = True

    @property
    def rarity(self):
        return max(self.badge.rarity, self.card.rarity)

    @property
    def bp(self):
        min_negative_bp = min(bp for bp in [0, self.badge.bp, self.card.bp] if bp <= 0)
        max_positive_bp = max(bp for bp in [0, self.badge.bp, self.card.bp] if bp >= 0)
        return max_positive_bp + min_negative_bp
