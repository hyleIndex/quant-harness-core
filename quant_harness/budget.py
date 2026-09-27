"""Simple wall-clock and work-unit budget accounting."""

from __future__ import annotations

from dataclasses import dataclass, field
import time


@dataclass
class RunBudget:
    max_seconds: float = float("inf")
    max_work_units: int | None = None
    started_at: float = field(default_factory=time.monotonic)
    work_units: int = 0

    @property
    def elapsed_seconds(self) -> float:
        return max(0.0, time.monotonic() - self.started_at)

    def record(self, work_units: int = 1) -> None:
        if work_units < 0:
            raise ValueError("work_units cannot be negative")
        self.work_units += work_units

    def exhausted(self) -> tuple[bool, str]:
        if self.elapsed_seconds >= self.max_seconds:
            return True, "time limit reached"
        if self.max_work_units is not None and self.work_units >= self.max_work_units:
            return True, "work-unit limit reached"
        return False, ""
