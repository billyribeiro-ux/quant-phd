"""Alternative 3 (round 2): srw counts by dynamic programming over (position, running maximum) with exact integers; grid engine by reference-order gauss draws."""

from __future__ import annotations

import math
import random
from collections import defaultdict
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("level must be positive")
    if t <= 0:
        raise ValueError("time must be positive")
    return math.erfc(a / math.sqrt(2.0 * t))


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(instance["H"] / n_steps)
    out: list[list[float]] = []
    for _ in range(int(instance["n_paths"])):
        x = 0.0
        row: list[float] = []
        for _ in range(n_steps):
            x += rng.gauss(0.0, sd)
            row.append(x)
        out.append(row)
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    flags = [1.0 if max(row) >= instance["a"] else 0.0 for row in _paths(instance, n_steps)]
    n = len(flags)
    p = sum(flags) / n
    var = sum((f - p) ** 2 for f in flags) / (n - 1)
    return p, math.sqrt(var) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must be a positive divisor of n_fine")
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for row in _paths(instance, n_fine):
        fine += max(row) >= instance["a"]
        coarse += max(row[i] for i in range(stride - 1, n_fine, stride)) >= instance["a"]
    return fine, coarse


def _dp(n: int) -> dict[tuple[int, int], int]:
    states: dict[tuple[int, int], int] = defaultdict(int)
    states[(0, 0)] = 1
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = defaultdict(int)
        for (pos, top), count in states.items():
            for step in (1, -1):
                new = pos + step
                nxt[(new, max(top, new))] += count
        states = nxt
    return dict(states)


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return sum(c for (pos, _top), c in _dp(n).items() if pos >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return sum(c for (_pos, top), c in _dp(n).items() if top >= a)
