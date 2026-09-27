"""UCB1 selector for allocating trials across named options."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass
class _Arm:
    trials: int = 0
    reward_sum: float = 0.0

    @property
    def mean_reward(self) -> float:
        return self.reward_sum / self.trials if self.trials else 0.0


class UCB1Selector:
    """Select options with UCB1; applications define the meaning of reward."""

    def __init__(self, options: list[str], exploration: float = math.sqrt(2), *,
                 rng: random.Random | None = None):
        if not options or len(set(options)) != len(options):
            raise ValueError("options must be a non-empty list of unique names")
        if exploration < 0 or not math.isfinite(exploration):
            raise ValueError("exploration must be a finite, non-negative number")
        self.exploration = exploration
        self._rng = rng or random.Random()
        self._arms = {name: _Arm() for name in options}

    def select(self) -> str:
        untried = [name for name, arm in self._arms.items() if arm.trials == 0]
        if untried:
            return self._rng.choice(untried)

        total_trials = sum(arm.trials for arm in self._arms.values())
        return max(
            self._arms,
            key=lambda name: self._arms[name].mean_reward
            + self.exploration * math.sqrt(math.log(total_trials) / self._arms[name].trials),
        )

    def update(self, option: str, reward: float) -> None:
        if option not in self._arms:
            raise KeyError(f"unknown option: {option}")
        reward = float(reward)
        if not math.isfinite(reward):
            raise ValueError("reward must be finite")
        arm = self._arms[option]
        arm.trials += 1
        arm.reward_sum += reward

    def snapshot(self) -> dict:
        return {
            "exploration": self.exploration,
            "options": {
                name: {"trials": arm.trials, "reward_sum": arm.reward_sum}
                for name, arm in self._arms.items()
            },
        }
