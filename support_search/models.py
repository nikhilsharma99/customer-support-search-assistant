from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Conversation:
    """Represents one customer-support conversation."""

    id: int
    customer_name: str
    topic: str
    message: str
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def searchable_text(self) -> str:
        """Return the text used by the search algorithm."""
        return f"{self.topic} {self.message}"
