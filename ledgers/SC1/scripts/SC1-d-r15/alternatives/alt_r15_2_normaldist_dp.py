"""Alternative r15-2 (verifier-written, correct): tail from statistics.NormalDist; walks counted by dynamic programming
over (position, has-reached-a); grid paths built with itertools.accumulate over the seeded draws in the stated order."""

from __future__ import annotations

import itertools
import math
import random
import statistics
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level must be positive")
    if t <= 0:
        raise ValueError("the time must be positive")
    return 2.0 * (1.0 - statistics.NormalDist().cdf(a / math.sqrt(t)))


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    out = []
    for _ in range(int(instance["n_paths"])):
        steps = [rng.gauss(0.0, sd) for _ in range(n_steps)]
        out.append(list(itertools.accumulate(steps)))
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    indicators = [1.0 if max(path) >= level else 0.0 for path in _paths(instance, n_steps)]
    n = len(indicators)
    mean = math.fsum(indicators) / n
    sample_var = math.fsum((x - mean) ** 2 for x in indicators) / (n - 1)
    return mean, math.sqrt(sample_var / n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    stride = n_fine // n_coarse
    level = float(instance["a"])
    fine = 0
    coarse = 0
    for path in _paths(instance, n_fine):
        fine += max(path) >= level
        coarse += max(path[k] for k in range(stride - 1, n_fine, stride)) >= level
    return fine, coarse


def _walk_counts(n: int, a: int) -> tuple[int, int]:
    """Exact (max reaches a, final value at least a) counts by DP over (position, reached-flag)."""
    states: dict[tuple[int, bool], int] = {(0, False): 1}
    for _ in range(n):
        nxt: dict[tuple[int, bool], int] = {}
        for (pos, reached), count in states.items():
            for step in (1, -1):
                new_pos = pos + step
                key = (new_pos, reached or new_pos >= a)
                nxt[key] = nxt.get(key, 0) + count
        states = nxt
    max_hits = sum(c for (_, reached), c in states.items() if reached)
    end_hits = sum(c for (pos, _), c in states.items() if pos >= a)
    return max_hits, end_hits


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _walk_counts(n, a)[1]


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _walk_counts(n, a)[0]
