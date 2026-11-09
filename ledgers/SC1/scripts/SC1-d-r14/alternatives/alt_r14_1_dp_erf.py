"""Correct alternative 1 (round 14): erf complement for the tail, dynamic programming for the walk counts."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return 1.0 - math.erf(a * (2.0 * t) ** -0.5)


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(instance["seed"])
    sd = (instance["H"] / n_steps) ** 0.5
    out = []
    for _ in range(instance["n_paths"]):
        pos = 0.0
        row = []
        for _ in range(n_steps):
            pos = pos + rng.gauss(0.0, sd)
            row.append(pos)
        out.append(row)
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("at least two paths")
    level = instance["a"]
    hits = 0
    rows = _paths(instance, n_steps)
    for row in rows:
        if max(row) >= level:
            hits += 1
    n = len(rows)
    p = hits / n
    se = math.sqrt(p * (1.0 - p) / (n - 1)) if n > 1 else 0.0
    return p, se


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("n_coarse must divide n_fine")
    stride = n_fine // n_coarse
    level = instance["a"]
    fine = coarse = 0
    for row in _paths(instance, n_fine):
        if max(row) >= level:
            fine += 1
        if max(row[stride - 1 :: stride]) >= level:
            coarse += 1
    return fine, coarse


def _walks_ge(n: int, a: int) -> int:
    # Count walks by DP over the endpoint: ways[k] is the number of walks at position 2k - n after the steps so far.
    ways = [1]
    for _ in range(n):
        nxt = [0] * (len(ways) + 1)
        for k, w in enumerate(ways):
            nxt[k] += w
            nxt[k + 1] += w
        ways = nxt
    return sum(w for k, w in enumerate(ways) if 2 * k - n >= a)


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _walks_ge(n, a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    # Walks whose maximum reaches a: the walks ending at a or above, plus those ending at a + 1 or above.
    return _walks_ge(n, a) + _walks_ge(n, a + 1)
