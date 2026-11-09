"""Round-17 alternative 3: reflection_tail by erfc with a * sqrt(0.5 / t); draws by list then accumulate; closed-form SE sqrt(p(1-p)/(N-1))/sqrt(N); thresholds by ceiling of (n + a) / 2."""
from __future__ import annotations

import itertools
import math
import random
from typing import Any


def reflection_tail(a: float, t: float) -> float:
    if a <= 0:
        raise ValueError("a")
    if t <= 0:
        raise ValueError("t")
    return math.erfc(a * math.sqrt(0.5 / t))


def discrete_max_exceedance(instance: dict[str, Any], n_steps: int) -> tuple[float, float]:
    if n_steps < 1:
        raise ValueError("n_steps")
    n = int(instance["n_paths"])
    if n < 2:
        raise ValueError("n_paths")
    level = float(instance["a"])
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_steps)
    hits = 0
    for _ in range(n):
        steps = [rng.gauss(0.0, sd) for _ in range(n_steps)]
        hits += max(itertools.accumulate(steps)) >= level
    p = hits / n
    return p, math.sqrt(p * (1.0 - p) / (n - 1))


def nested_grid_counts(instance: dict[str, Any], n_fine: int, n_coarse: int) -> tuple[int, int]:
    if n_fine < 1:
        raise ValueError("n_fine")
    if n_coarse < 1 or n_fine % n_coarse != 0:
        raise ValueError("n_coarse")
    level = float(instance["a"])
    stride = n_fine // n_coarse
    rng = random.Random(int(instance["seed"]))
    sd = math.sqrt(float(instance["H"]) / n_fine)
    fine = 0
    coarse = 0
    for _ in range(int(instance["n_paths"])):
        walk = list(itertools.accumulate(rng.gauss(0.0, sd) for _ in range(n_fine)))
        fine += max(walk) >= level
        coarse += max(walk[stride - 1 :: stride]) >= level
    return fine, coarse


def srw_terminal_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n")
    if a < 1:
        raise ValueError("a")
    k_min = (n + a + 1) // 2
    return sum(math.comb(n, k) for k in range(k_min, n + 1))


def srw_max_count(n: int, a: int) -> int:
    if n < 1:
        raise ValueError("n")
    if a < 1:
        raise ValueError("a")
    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)
