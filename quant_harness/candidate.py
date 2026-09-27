"""Serializable record for one proposed experiment candidate."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import math
import uuid


@dataclass
class Candidate:
    source: str
    score: float | None = None
    candidate_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    parent_id: str | None = None
    generation: int = 0
    metadata: dict = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def fingerprint(self) -> str:
        """Stable digest used for exact-source deduplication."""
        return hashlib.sha256(self.source.encode("utf-8")).hexdigest()

    @property
    def ranking_score(self) -> float:
        """Return a finite score, ranking unscored candidates last."""
        if self.score is None:
            return float("-inf")
        value = float(self.score)
        return value if math.isfinite(value) else float("-inf")

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "parent_id": self.parent_id,
            "generation": self.generation,
            "source": self.source,
            "score": self.score,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, value: dict) -> "Candidate":
        return cls(
            source=str(value["source"]),
            score=value.get("score"),
            candidate_id=str(value.get("candidate_id") or uuid.uuid4().hex[:12]),
            parent_id=value.get("parent_id"),
            generation=int(value.get("generation", 0)),
            metadata=dict(value.get("metadata") or {}),
            created_at=str(value.get("created_at") or datetime.now(timezone.utc).isoformat()),
        )
