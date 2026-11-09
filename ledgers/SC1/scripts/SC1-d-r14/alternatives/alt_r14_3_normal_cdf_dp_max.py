"""Correct alternative 3 (round 14): normal CDF through erf for the tail, statistics.stdev for the error, and a
dynamic programme over (position, running maximum) for the maximum count, not the reflection identity."""

from __future__ import annotations

import math
import random
import statistics
from typing import Any


def _phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level must be positive")
    if t <= 0:
        raise ValueError("the time must be positive")
    return 2.0 * (1.0 - _phi(a / math.sqrt(t)))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("the grid needs one step or more")
    if instance["n_paths"] < 2:
        raise ValueError("two paths or more")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    flags = []
    for _ in range(instance["n_paths"]):
        pos = 0.0
        top = -math.inf
        for _ in range(n_steps):
            pos += rng.gauss(0.0, sd)
            top = max(top, pos)
        flags.append(1.0 if top >= instance["a"] else 0.0)
    return sum(flags) / len(flags), statistics.stdev(flags) / math.sqrt(len(flags))


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("the fine grid needs one step or more")
    if n_coarse < 1:
        raise ValueError("the coarse grid needs one step or more")
    if n_fine % n_coarse:
        raise ValueError("the coarse grid must divide the fine grid")
    stride = n_fine // n_coarse
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_fine)
    fine = coarse = 0
    for _ in range(instance["n_paths"]):
        pos = 0.0
        fine_top = coarse_top = -math.inf
        for k in range(1, n_fine + 1):
            pos += rng.gauss(0.0, sd)
            fine_top = max(fine_top, pos)
            if k % stride == 0:
                coarse_top = max(coarse_top, pos)
        fine += fine_top >= instance["a"]
        coarse += coarse_top >= instance["a"]
    return fine, coarse


def _max_count(n: int, a: int) -> int:
    # States: (position, running maximum) -> number of walks. Count walks whose maximum reaches a.
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, top), w in states.items():
            for step in (1, -1):
                key = (pos + step, max(top, pos + step))
                nxt[key] = nxt.get(key, 0) + w
        states = nxt
    return sum(w for (_, top), w in states.items() if top >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("the walk needs one step or more")
    if a < 1:
        raise ValueError("the level must be at least 1")
    return _max_count(n, a)


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("the walk needs one step or more")
    if a < 1:
        raise ValueError("the level must be at least 1")
    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)
