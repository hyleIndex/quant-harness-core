"""Append-only JSON Lines event log."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping


class EventLog:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: Mapping) -> None:
        line = json.dumps(dict(event), ensure_ascii=False, default=str)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
            handle.flush()

    def __iter__(self):
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)
