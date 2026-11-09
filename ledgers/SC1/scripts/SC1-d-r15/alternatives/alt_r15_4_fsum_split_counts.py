"""Alternative r15-4 (verifier-written, correct): erfc closed form via the normal cdf identity written as 2(1 - Phi);
standard error from hits with math.fsum; grid maxima kept as a list of per-path maxima; nested counts from the
path maxima of each stride computed by index slicing over the stored fine path; walk counts by binomial sums."""

from __future__ import annotations

import math
import random
from typing import Any


def _phi(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("the level must be positive")
    if t <= 0:
        raise ValueError("the time must be positive")
    return 2.0 * (1.0 - _phi(a / math.sqrt(t)))


def _fine_paths(instance: dict[str, Any], n_steps: int) -> list[list[float]]:
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    paths: list[list[float]] = []
    for _ in range(int(instance["n_paths"])):
        acc = 0.0
        path = []
        for _ in range(n_steps):
            acc = acc + rng.gauss(0.0, sd)
            path.append(acc)
        paths.append(path)
    return paths


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if int(instance["n_paths"]) < 2:
        raise ValueError("n_paths must be at least 2")
    level = float(instance["a"])
    maxima = [max(p) for p in _fine_paths(instance, n_steps)]
    flags = [1.0 if m >= level else 0.0 for m in maxima]
    n = len(flags)
    mean = math.fsum(flags) / n
    se = math.sqrt(math.fsum((f - mean) ** 2 for f in flags) / (n - 1)) / math.sqrt(n)
    return mean, se


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine must be at least 1")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse must divide n_fine")
    stride = n_fine // n_coarse
    level = float(instance["a"])
    fine_count = 0
    coarse_count = 0
    for path in _fine_paths(instance, n_fine):
        sub = path[stride - 1 :: stride]
        if len(sub) != n_coarse:
            raise AssertionError("internal slicing error")
        fine_count += max(path) >= level
        coarse_count += max(sub) >= level
    return fine_count, coarse_count


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return sum(math.comb(n, k) for k in range(n + 1) if 2 * k >= n + a)


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n must be at least 1")
    if a < 1:
        raise ValueError("a must be at least 1")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
