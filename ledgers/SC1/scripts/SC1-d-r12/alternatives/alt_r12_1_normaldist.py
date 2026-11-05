"""Alternative 1: reflection_tail through statistics.NormalDist, 2(1 - Phi(a / sqrt t)); the walk counts by DP over (position, running maximum)."""
import math
from statistics import NormalDist, stdev
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a must be positive")
    if t <= 0:
        raise ValueError("t must be positive")
    return 2.0 * (1.0 - NormalDist().cdf(a / math.sqrt(t)))


def _paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    import random

    rng = random.Random(instance["seed"])
    sd = math.sqrt(instance["H"] / n_steps)
    out = []
    for _ in range(instance["n_paths"]):
        pos, vals = 0.0, []
        for _ in range(n_steps):
            pos += rng.gauss(0.0, sd)
            vals.append(pos)
        out.append(vals)
    return out


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if instance["n_paths"] < 2:
        raise ValueError("need two paths")
    ind = [1.0 if max(v) >= instance["a"] else 0.0 for v in _paths(instance, n_steps)]
    n = len(ind)
    return sum(ind) / n, stdev(ind) / math.sqrt(n)


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1 or n_coarse < 1 or n_fine % n_coarse:
        raise ValueError("bad grids")
    step = n_fine // n_coarse
    fine = coarse = 0
    for v in _paths(instance, n_fine):
        fine += max(v) >= instance["a"]
        coarse += max(v[step - 1 :: step]) >= instance["a"]
    return fine, coarse


def _dp_counts(n: int, a: int) -> tuple[int, int]:
    """Walks that never reach a (DP over position) give the maximum count; the end counts come from the final distribution."""
    below: dict[int, int] = {0: 1}
    for _ in range(n):
        nxt: dict[int, int] = {}
        for pos, c in below.items():
            for step in (1, -1):
                q = pos + step
                if q < a:
                    nxt[q] = nxt.get(q, 0) + c
        below = nxt
    max_hits = 2**n - sum(below.values())
    dist: dict[int, int] = {0: 1}
    for _ in range(n):
        nxt = {}
        for pos, c in dist.items():
            for step in (1, -1):
                nxt[pos + step] = nxt.get(pos + step, 0) + c
        dist = nxt
    end_hits = sum(c for pos, c in dist.items() if pos >= a)
    return max_hits, end_hits


def srw_max_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return _dp_counts(n, a)[0]


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1 or a < 1:
        raise ValueError("n and a must be at least 1")
    return _dp_counts(n, a)[1]
