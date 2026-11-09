"""Verifier alternative r16-4: NormalDist tail, DP for both counts, index subsampling, sum of squares."""

from __future__ import annotations

import math
import random
from statistics import NormalDist
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return 2.0 * (1.0 - NormalDist().cdf(a / math.sqrt(t)))


def _draws(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    paths = []
    for _ in range(int(instance["n_paths"])):
        steps = [rng.gauss(0.0, sd) for _ in range(n_steps)]
        partial = []
        total = 0.0
        for s in steps:
            total += s
            partial.append(total)
        paths.append(partial)
    return paths


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    hits = [1.0 if max(p) >= level else 0.0 for p in _draws(instance, n_steps)]
    n = len(hits)
    p = sum(hits) / n
    sum_sq = sum(h * h for h in hits)
    variance = (sum_sq - n * p * p) / (n - 1)
    return p, math.sqrt(max(variance, 0.0)) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for path in _draws(instance, n_fine):
        fine += max(path) >= level
        subsample = [path[k] for k in range(stride - 1, n_fine, stride)]
        coarse += max(subsample) >= level
    return fine, coarse


def _dp_counts(n: int, a: int) -> tuple[int, int]:
    counts: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, top), c in counts.items():
            for step in (1, -1):
                new_pos = pos + step
                key = (new_pos, max(top, new_pos))
                nxt[key] = nxt.get(key, 0) + c
        counts = nxt
    maxima = sum(c for (_, top), c in counts.items() if top >= a)
    ends = sum(c for (pos, _), c in counts.items() if pos >= a)
    return maxima, ends


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _dp_counts(n, a)[1]


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _dp_counts(n, a)[0]
