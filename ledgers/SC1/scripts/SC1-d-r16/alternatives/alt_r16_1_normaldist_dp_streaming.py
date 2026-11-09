"""Verifier alternative r16-1: NormalDist tail, DP walk counts, streaming grid maxima, algebraic standard error."""

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


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    n = int(instance["n_paths"])
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    hits = 0
    for _ in range(n):
        position = 0.0
        best = -math.inf
        for _ in range(n_steps):
            position += rng.gauss(0.0, sd)
            if position > best:
                best = position
        if best >= level:
            hits += 1
    p = hits / n
    # Algebraic form of the sample sd over sqrt(N): sqrt(p(1-p)/(N-1)).
    return p, math.sqrt(p * (1.0 - p) / (n - 1))


def _walk_counts(n: int, a: int) -> tuple[int, int]:
    # DP over (position, running maximum): returns (#{max >= a}, #{S_n >= a}) as exact integers.
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, mx), c in states.items():
            for step in (1, -1):
                key = (pos + step, max(mx, pos + step))
                nxt[key] = nxt.get(key, 0) + c
        states = nxt
    max_hits = sum(c for (_, mx), c in states.items() if mx >= a)
    end_hits = sum(c for (pos, _), c in states.items() if pos >= a)
    return max_hits, end_hits


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    fine = coarse = 0
    for _ in range(int(instance["n_paths"])):
        position = 0.0
        best_fine = -math.inf
        best_coarse = -math.inf
        for k in range(1, n_fine + 1):
            position += rng.gauss(0.0, sd)
            best_fine = max(best_fine, position)
            if k % stride == 0:
                best_coarse = max(best_coarse, position)
        fine += best_fine >= level
        coarse += best_coarse >= level
    return fine, coarse


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
