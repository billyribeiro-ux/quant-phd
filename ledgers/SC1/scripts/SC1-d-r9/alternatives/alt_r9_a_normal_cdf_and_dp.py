"""Alternative correct engine (round 9, A): tail by the normal cdf, srw by a (position, maximum) recurrence."""

from __future__ import annotations

import math
import random
from statistics import NormalDist
from typing import Any

_PHI = NormalDist()


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return 2.0 * (1.0 - _PHI.cdf(a / math.sqrt(t)))


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    out = []
    for _ in range(instance["n_paths"]):
        draws = [rng.gauss(0.0, sd) for _ in range(n_steps)]
        out.append(list(__import__("itertools").accumulate(draws)))
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    level = instance["a"]
    hits = [1.0 if max(p) >= level else 0.0 for p in _paths(instance, n_steps)]
    n = len(hits)
    mean = sum(hits) / n
    var = (sum(h * h for h in hits) - n * mean * mean) / (n - 1)
    return mean, math.sqrt(max(var, 0.0)) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("n_coarse must divide n_fine")
    step = n_fine // n_coarse
    level = instance["a"]
    fine = coarse = 0
    for p in _paths(instance, n_fine):
        if max(p) >= level:
            fine += 1
        if any(p[i] >= level for i in range(step - 1, n_fine, step)):
            coarse += 1
    return fine, coarse


def _dp_counts(n: int, a: int) -> tuple[int, int]:
    """(#{max >= a}, #{S_n >= a}) by a recurrence on (position, running maximum), with exact integers."""
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, top), c in states.items():
            for step in (1, -1):
                q = pos + step
                key = (q, max(top, q))
                nxt[key] = nxt.get(key, 0) + c
        states = nxt
    max_hits = sum(c for (pos, top), c in states.items() if top >= a)
    end_hits = sum(c for (pos, top), c in states.items() if pos >= a)
    return max_hits, end_hits


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _dp_counts(n, a)[0]


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _dp_counts(n, a)[1]
