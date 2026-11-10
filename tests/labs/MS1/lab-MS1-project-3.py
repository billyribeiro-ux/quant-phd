"""Lab MS1-project-3: Rung 3 verification check on the report parameter grid.

SIMULATED: generates trade series on the parameter grid (theta in {0.0, 0.1, 0.2},
c = 0.10, sigma = 0.05, n = 2000, seed 1).
Produces the reference output table required for the student report.
"""

from __future__ import annotations

import math
import random


def generate_trade_series(n: int, theta: float, c: float, sigma: float, seed: int) -> tuple[list[float], list[int]]:
    """Simulate trade-level data under repeated trade model."""
    rng = random.Random(seed)
    m = 100.0
    prices: list[float] = []
    signs: list[int] = []
    for _ in range(n):
        q = rng.choice([-1, 1])
        eta = rng.gauss(0.0, sigma)
        m += theta * q + eta
        prices.append(m + c * q)
        signs.append(q)
    return prices, signs


def run_decomposition(prices: list[float], signs: list[int]) -> tuple[float, float, float, float, float]:
    """Execute full decomposition and return roll spread, H, c, theta, and share."""
    n = len(prices)
    d = [prices[i] - prices[i - 1] for i in range(1, n)]
    mean_d = sum(d) / len(d)
    cov1 = sum((d[i] - mean_d) * (d[i - 1] - mean_d) for i in range(1, len(d))) / (len(d) - 1)
    roll = 2.0 * math.sqrt(-cov1) if cov1 < 0.0 else float("nan")

    q_curr = [float(signs[i]) for i in range(1, n)]
    q_lag = [float(signs[i - 1]) for i in range(1, n)]

    s00 = sum(x * x for x in q_curr)
    s11 = sum(x * x for x in q_lag)
    s01 = sum(x * y for x, y in zip(q_curr, q_lag, strict=False))
    det = s00 * s11 - s01 * s01

    y0 = sum(di * qi for di, qi in zip(d, q_curr, strict=False))
    y1 = sum(di * qi for di, qi in zip(d, q_lag, strict=False))

    b0 = (s11 * y0 - s01 * y1) / det
    b1 = (s00 * y1 - s01 * y0) / det

    half_spread = b0
    order_proc = -b1
    adv_sel = b0 + b1
    adv_share = adv_sel / half_spread if half_spread != 0.0 else float("nan")

    return roll, half_spread, order_proc, adv_sel, adv_share


def main() -> None:
    c_fixed = 0.10
    sigma_fixed = 0.05
    n_fixed = 2000
    seed_fixed = 1
    thetas = [0.0, 0.1, 0.2]

    print("Project Report Benchmark Grid (n=2000, c=0.10, sigma=0.05, seed=1):")
    print("theta |     c |     Roll |  Half-Sp | Order-Pr |  Adv-Sel | Adv-Share")
    for theta in thetas:
        prices, signs = generate_trade_series(n_fixed, theta, c_fixed, sigma_fixed, seed_fixed)
        roll, h, c_est, th_est, share = run_decomposition(prices, signs)
        print(f"{theta:5.2f} | {c_fixed:5.2f} | {roll:8.4f} | {h:8.4f} | {c_est:8.4f} | {th_est:8.4f} | {share:9.4f}")


main()
