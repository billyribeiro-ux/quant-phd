"""Alternative 2 (round 2): reflection_tail by Simpson quadrature of 2 P(B_t >= a) only, 4000 panels, no closed form; the grid engine is the reference's."""

from __future__ import annotations

import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("level must be positive")
    if t <= 0:
        raise ValueError("time must be positive")
    panels = 4000
    top = a + 12.0 * math.sqrt(t)
    h = (top - a) / panels
    total = 0.0
    for k in range(panels + 1):
        x = a + k * h
        w = 1 if k in (0, panels) else (4 if k % 2 else 2)
        total += w * math.exp(-x * x / (2.0 * t))
    return 2.0 * total * h / 3.0 / math.sqrt(2.0 * math.pi * t)


def _grid(instance: dict[str, Any], n_steps: int) -> list[float]:
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    maxima: list[float] = []
    for _ in range(instance["n_paths"]):
        s = 0.0
        m = -math.inf
        for _ in range(n_steps):
            s += rng.gauss(0.0, sd)
            m = max(m, s)
        maxima.append(m)
    return maxima


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("n_paths must be at least 2")
    ind = [1.0 if m >= instance["a"] else 0.0 for m in _grid(instance, n_steps)]
    n = len(ind)
    mean = sum(ind) / n
    s2 = sum((x - mean) ** 2 for x in ind) / (n - 1)
    return mean, math.sqrt(s2) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1 or n_coarse < 1:
        raise ValueError("grid sizes must be at least 1")
    if n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    stride = n_fine // n_coarse
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_fine)
    fine = coarse = 0
    for _ in range(instance["n_paths"]):
        s = 0.0
        fm = -math.inf
        cm = -math.inf
        for k in range(1, n_fine + 1):
            s += rng.gauss(0.0, sd)
            fm = max(fm, s)
            if k % stride == 0:
                cm = max(cm, s)
        fine += fm >= instance["a"]
        coarse += cm >= instance["a"]
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return sum(math.comb(n, k) for k in range(n + 1) if 2 * k - n >= a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
