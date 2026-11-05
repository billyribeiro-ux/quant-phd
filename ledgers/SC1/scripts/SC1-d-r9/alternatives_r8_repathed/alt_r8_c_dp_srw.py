"""Alternative C (round 8): srw counts by dynamic programming over (position, running maximum capped at a).

The normal-distribution tail and the grid functions are written out in this file, so it does not import the reference.
"""
from __future__ import annotations

import math
import random
import statistics
from typing import Any

_STD = statistics.NormalDist()


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return 2.0 * (1.0 - _STD.cdf(a / math.sqrt(t)))


def _grid_paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    paths = []
    for _ in range(int(instance["n_paths"])):
        position = 0.0
        values = []
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            values.append(position)
        paths.append(values)
    return paths


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    hits = [1.0 if max(v) >= level else 0.0 for v in _grid_paths(instance, n_steps)]
    p = statistics.fmean(hits)
    se = statistics.stdev(hits) / math.sqrt(len(hits))
    return p, se


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("n_coarse must be a positive divisor of n_fine")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    fine = coarse = 0
    for v in _grid_paths(instance, n_fine):
        fine += max(v) >= level
        coarse += max(v[i] for i in range(stride - 1, n_fine, stride)) >= level
    return fine, coarse


def _dp(n: int, a: int) -> tuple[int, int]:
    # state: (position, min(running max, a)) -> number of walks; returns (#{max >= a}, #{S_n >= a})
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, top), w in states.items():
            for step in (1, -1):
                p2 = pos + step
                t2 = min(max(top, p2), a)
                nxt[(p2, t2)] = nxt.get((p2, t2), 0) + w
        states = nxt
    max_hits = sum(w for (_, top), w in states.items() if top >= a)
    end_hits = sum(w for (pos, _), w in states.items() if pos >= a)
    return max_hits, end_hits


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return _dp(n, a)[0]


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return _dp(n, a)[1]
