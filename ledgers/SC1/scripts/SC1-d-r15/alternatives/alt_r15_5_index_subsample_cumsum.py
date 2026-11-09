"""Alternative r15-5 (verifier-written, correct): reflection tail by 1 - erf(x / sqrt 2) with the erf of the
standardised argument; grid maxima by cumulative sums over index lists; coarse grid by subsampling indices; standard
error from the binomial variance p(1 - p) / (N - 1) written directly; walk counts by a reflected dynamic programme over
the endpoint with the identity for the maximum."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level must be positive")
    if t <= 0:
        raise ValueError("the time must be positive")
    return 1.0 - math.erf((a / math.sqrt(t)) / math.sqrt(2.0))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    n_paths = int(instance["n_paths"])
    if n_paths < 2:
        raise ValueError("n_paths must be at least 2")
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    level = float(instance["a"])
    hits = 0
    for _ in range(n_paths):
        increments = [rng.gauss(0.0, sd) for _ in range(n_steps)]
        cumulative = [0.0] * n_steps
        running = 0.0
        for i, inc in enumerate(increments):
            running += inc
            cumulative[i] = running
        if max(cumulative) >= level:
            hits += 1
    p = hits / n_paths
    se = math.sqrt(p * (1.0 - p) / (n_paths - 1))
    return p, se


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    stride = n_fine // n_coarse
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    level = float(instance["a"])
    fine = 0
    coarse = 0
    coarse_indices = [i for i in range(n_fine) if (i + 1) % stride == 0]
    for _ in range(int(instance["n_paths"])):
        cumulative = []
        running = 0.0
        for _ in range(n_fine):
            running += rng.gauss(0.0, sd)
            cumulative.append(running)
        fine += 1 if max(cumulative) >= level else 0
        coarse += 1 if max(cumulative[i] for i in coarse_indices) >= level else 0
    return fine, coarse


def _reflected_counts(n: int, a: int) -> tuple[int, int]:
    """(number of walks with final value at least a, number of walks with maximum at least a) by DP on the endpoint."""
    end = {0: 1}
    for _ in range(n):
        nxt: dict[int, int] = {}
        for pos, c in end.items():
            nxt[pos + 1] = nxt.get(pos + 1, 0) + c
            nxt[pos - 1] = nxt.get(pos - 1, 0) + c
        end = nxt
    terminal = sum(c for pos, c in end.items() if pos >= a)
    above_a_plus_one = sum(c for pos, c in end.items() if pos >= a + 1)
    return terminal, terminal + above_a_plus_one


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _reflected_counts(n, a)[0]


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _reflected_counts(n, a)[1]
