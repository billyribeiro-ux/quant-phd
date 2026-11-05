"""Alternative 2: reflection_tail by Simpson quadrature of 2 P(B_t >= a) on [a, a + 12 sqrt t]; walk counts by a dynamic programme over (position, running maximum); grid maxima from stored paths."""

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level a must be positive")
    if t <= 0:
        raise ValueError("the time t must be positive")
    top = a + 12.0 * math.sqrt(t)
    m = 4000
    h = (top - a) / m

    def dens(x: float) -> float:
        return math.exp(-(x * x) / (2.0 * t)) / math.sqrt(2.0 * math.pi * t)

    s = dens(a) + dens(top)
    for k in range(1, m):
        s += (4.0 if k % 2 else 2.0) * dens(a + k * h)
    return 2.0 * s * h / 3.0


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    paths = []
    for _ in range(instance["n_paths"]):
        pos = 0.0
        vals = []
        for _k in range(n_steps):
            pos += rng.gauss(0.0, sd)
            vals.append(pos)
        paths.append(vals)
    return paths


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    paths = _paths(instance, n_steps)
    ind = [1.0 if max(v) >= instance["a"] else 0.0 for v in paths]
    n = len(ind)
    mean = sum(ind) / n
    var = sum((x - mean) ** 2 for x in ind) / (n - 1)
    return mean, math.sqrt(var / n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must be at least 1 and divide n_fine")
    idx = list(range(n_fine // n_coarse - 1, n_fine, n_fine // n_coarse))
    fine = 0
    coarse = 0
    for v in _paths(instance, n_fine):
        fine += max(v) >= instance["a"]
        coarse += max(v[i] for i in idx) >= instance["a"]
    return fine, coarse


def _walk_dp(n: int, a: int) -> tuple[int, int]:
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, mx), c in states.items():
            for step in (1, -1):
                q = pos + step
                key = (q, max(mx, q))
                nxt[key] = nxt.get(key, 0) + c
        states = nxt
    by_max = sum(c for (pos, mx), c in states.items() if mx >= a)
    by_end = sum(c for (pos, mx), c in states.items() if pos >= a)
    return by_max, by_end


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _walk_dp(n, a)[1]


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return _walk_dp(n, a)[0]
