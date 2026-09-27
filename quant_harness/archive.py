"""Bounded candidate archive with exact-source deduplication."""

from __future__ import annotations

import random

from quant_harness.candidate import Candidate


class CandidateArchive:
    def __init__(self, capacity: int = 100, *, rng: random.Random | None = None):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._rng = rng or random.Random()
        self._candidates: dict[str, Candidate] = {}

    def __len__(self) -> int:
        return len(self._candidates)

    def insert(self, candidate: Candidate) -> bool:
        """Keep a candidate when it is new or improves its duplicate."""
        key = candidate.fingerprint
        existing = self._candidates.get(key)
        if existing is not None and candidate.ranking_score <= existing.ranking_score:
            return False

        self._candidates[key] = candidate
        if len(self._candidates) > self.capacity:
            worst_key = min(
                self._candidates,
                key=lambda fingerprint: self._candidates[fingerprint].ranking_score,
            )
            del self._candidates[worst_key]
        return key in self._candidates

    def top_k(self, count: int = 10) -> list[Candidate]:
        if count < 0:
            raise ValueError("count cannot be negative")
        return sorted(
            self._candidates.values(),
            key=lambda item: item.ranking_score,
            reverse=True,
        )[:count]

    def sample_parent(self) -> Candidate:
        """Choose uniformly from the retained candidates."""
        if not self._candidates:
            raise LookupError("cannot sample from an empty archive")
        return self._rng.choice(list(self._candidates.values()))

    def to_list(self) -> list[dict]:
        return [candidate.to_dict() for candidate in self.top_k(len(self))]

    @classmethod
    def from_list(
        cls, records: list[dict], capacity: int = 100, *, rng: random.Random | None = None
    ) -> "CandidateArchive":
        archive = cls(capacity=capacity, rng=rng)
        for record in records:
            archive.insert(Candidate.from_dict(record))
        return archive
