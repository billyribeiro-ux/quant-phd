"""Round-17 alternative 2: reflection_tail by statistics.NormalDist; srw counts by dynamic programming over (position, running max); statistics.variance SE; nested by index subsampling."""
from __future__ import annotations

import itertools
import math
import random
import statistics
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a")
    if t <= 0:
        raise ValueError("t")
    return 2.0 * (1.0 - statistics.NormalDist().cdf(a / math.sqrt(t)))


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    out = []
    for _ in range(int(instance["n_paths"])):
        out.append([rng.gauss(0.0, sd) for _ in range(n_steps)])
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths")
    level = float(instance["a"])
    indicators = []
    for steps in _paths(instance, n_steps):
        top = max(itertools.accumulate(steps))
        indicators.append(1.0 if top >= level else 0.0)
    count = len(indicators)
    return statistics.fmean(indicators), math.sqrt(statistics.variance(indicators) / count)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for steps in _paths(instance, n_fine):
        partial = []
        total = 0.0
        for s in steps:
            total += s
            partial.append(total)
        fine += max(partial) >= level
        idx = range(stride - 1, n_fine, stride)
        coarse += max(partial[i] for i in idx) >= level
    return fine, coarse


def _dp(n: int, a: int) -> tuple[int, int]:
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        new: dict[tuple[int, int], int] = {}
        for (pos, top), c in states.items():
            for step in (1, -1):
                p2 = pos + step
                key = (p2, max(top, p2))
                new[key] = new.get(key, 0) + c
        states = new
    max_hits = sum(c for (_, top), c in states.items() if top >= a)
    end_hits = sum(c for (pos, _), c in states.items() if pos >= a)
    return max_hits, end_hits


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n")
    if a < 1:
        raise ValueError("a")
    return _dp(n, a)[1]


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n")
    if a < 1:
        raise ValueError("a")
    return _dp(n, a)[0]
