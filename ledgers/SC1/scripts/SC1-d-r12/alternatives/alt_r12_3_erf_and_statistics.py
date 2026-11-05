"""Alternative 3: reflection_tail as 1 - erf (a different float route); discrete estimate with statistics.stdev on the indicators and a running-max loop."""
import math
import random
import statistics
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level must be positive")
    if t <= 0:
        raise ValueError("the time must be positive")
    return 1.0 - math.erf(a / math.sqrt(2.0 * t))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("the grid needs a step")
    n_paths = instance["n_paths"]
    if n_paths < 2:
        raise ValueError("two paths at least")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    indicators = []
    for _ in range(n_paths):
        pos = 0.0
        top = -math.inf
        for _ in range(n_steps):
            pos += rng.gauss(0.0, sd)
            top = max(top, pos)
        indicators.append(1.0 if top >= instance["a"] else 0.0)
    estimate = statistics.fmean(indicators)
    return estimate, statistics.stdev(indicators) / math.sqrt(n_paths)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("the fine grid needs a step")
    if n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("the coarse grid must divide the fine grid")
    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_fine)
    stride = n_fine // n_coarse
    fine = 0
    coarse = 0
    for _ in range(instance["n_paths"]):
        pos = 0.0
        fine_top = -math.inf
        coarse_top = -math.inf
        for k in range(1, n_fine + 1):
            pos += rng.gauss(0.0, sd)
            fine_top = max(fine_top, pos)
            if k % stride == 0:
                coarse_top = max(coarse_top, pos)
        fine += fine_top >= instance["a"]
        coarse += coarse_top >= instance["a"]
    return fine, coarse


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return sum(_ends(n, a)) + sum(_ends(n, a + 1))


def _ends(n: int, a: int) -> list[int]:
    out = []
    for j in range(n + 1):
        if 2 * j - n >= a:
            out.append(_choose(n, j))
    return out


def _choose(n: int, k: int) -> int:
    value = 1
    for i in range(1, k + 1):
        value = value * (n - k + i) // i
    return value


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return sum(_ends(n, a))
