"""Lab S3-project-2: Rung 2 completion problem for pairs-trading audit.

SIMULATED: completion twin containing the full solution to the half-life
and survival decision rules.
"""

from __future__ import annotations

import math
import random


def ols_1d(y: list[float], x: list[float]) -> tuple[float, float]:
    m = len(y)
    mx = sum(x) / m
    my = sum(y) / m
    cov = sum((x[i] - mx) * (y[i] - my) for i in range(m))
    var_x = sum((x[i] - mx) ** 2 for i in range(m))
    beta = cov / var_x
    alpha = my - beta * mx
    return alpha, beta


def compute_half_life(spread: list[float]) -> float:
    """Estimate AR(1) spread persistence and compute half-life."""
    y = spread[1:]
    x = spread[:-1]
    _, phi = ols_1d(y, x)
    if phi <= 0.0:
        raise ValueError("phi <= 0")
    if phi >= 1.0:
        return math.inf
    return math.log(2.0) / (-math.log(phi))


def audit_survives(eg_stat: float, eg_critical: float, half_life_val: float) -> bool:
    """Return True iff eg_stat is below critical value and half-life is finite."""
    return bool(eg_stat < eg_critical and math.isfinite(half_life_val))


def main() -> None:
    rng = random.Random(101)
    n = 450
    split = 270
    eg_crit_5pct = -3.3395

    # Simulated candidate pair
    rw = [0.0]
    for _ in range(n - 1):
        rw.append(rw[-1] + rng.gauss(0.0, 1.0))
    x = [80.0 + rw[t] for t in range(n)]
    s = [0.0]
    for _ in range(n - 1):
        s.append(0.80 * s[-1] + rng.gauss(0.0, 0.6))
    y = [1.5 + 0.95 * x[t] + s[t] for t in range(n)]

    # Pre-calculated formation values
    alpha, beta = ols_1d(y[:split], x[:split])
    trading_spread = [y[t] - alpha - beta * x[t] for t in range(split, n)]
    eg_stat = -3.5214

    # Completed steps
    hl = compute_half_life(trading_spread)
    survives = audit_survives(eg_stat, eg_crit_5pct, hl)

    print("Rung 2 Completion Audit Check:")
    print(f"  Formation EG stat: {eg_stat:.4f} (critical: {eg_crit_5pct:.4f})")
    print(f"  Trading window spread half-life: {hl:.4f} days")
    print(f"  Candidate survives audit: {survives}")


main()
