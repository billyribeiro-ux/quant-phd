"""Lab MS1-project-1: Rung 1 worked example of trade-level spread decomposition.

SIMULATED: generates one sample of trade prices and signs (n=500, theta=0.10, c=0.15, sigma=0.05).
Solves the decomposition step by step, annotating why each mathematical step is taken:
price changes, lag-1 autocovariance, Roll spread, normal equations, components, and adverse share.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    # Step 1: Generate simulated instance
    # Why: Demonstrates the estimator on a controlled path with known true parameters.
    rng = random.Random(42)
    n = 500
    theta_true = 0.10
    c_true = 0.15
    sigma = 0.05
    m = 100.0

    prices: list[float] = []
    signs: list[int] = []
    for _ in range(n):
        q = rng.choice([-1, 1])
        eta = rng.gauss(0.0, sigma)
        m += theta_true * q + eta
        prices.append(m + c_true * q)
        signs.append(q)

    print(f"Step 1 | Generated {n} trades with true theta = {theta_true:.4f}, c = {c_true:.4f}")

    # Step 2: Calculate price changes d_t = p_t - p_{t-1}
    # Why: Stationarizes the price series; removes the random-walk level of fundamental value.
    d = [prices[i] - prices[i - 1] for i in range(1, n)]
    mean_d = sum(d) / len(d)
    print(f"Step 2 | Computed {len(d)} price changes. Mean price change: {mean_d:.6f}")

    # Step 3: Compute sample lag-1 autocovariance and Roll spread
    # Why: Negative autocovariance reflects bid-ask bounce; Roll's formula assumes theta = 0.
    cov1 = sum((d[i] - mean_d) * (d[i - 1] - mean_d) for i in range(1, len(d))) / (len(d) - 1)
    roll = 2.0 * math.sqrt(-cov1) if cov1 < 0.0 else float("nan")
    print(f"Step 3 | Lag-1 covariance: {cov1:.6f}, Roll spread estimate: {roll:.4f}")

    # Step 4: Assemble normal equations for regression without intercept
    # Why: In population, E[d_t | q_t, q_{t-1}] = (theta + c) q_t - c q_{t-1}.
    q_curr = [float(signs[i]) for i in range(1, n)]
    q_lag = [float(signs[i - 1]) for i in range(1, n)]

    s00 = sum(x * x for x in q_curr)
    s11 = sum(x * x for x in q_lag)
    s01 = sum(x * y for x, y in zip(q_curr, q_lag, strict=False))
    det = s00 * s11 - s01 * s01
    print(f"Step 4 | Design matrix determinant: {det:.1f} (non-singular)")

    y0 = sum(di * qi for di, qi in zip(d, q_curr, strict=False))
    y1 = sum(di * qi for di, qi in zip(d, q_lag, strict=False))

    b0 = (s11 * y0 - s01 * y1) / det
    b1 = (s00 * y1 - s01 * y0) / det
    print(f"Step 5 | OLS regression slopes: b_0 = {b0:.4f}, b_1 = {b1:.4f}")

    # Step 6: Recover structural spread components
    # Why: b_0 identifies total half-spread H; -b_1 identifies order processing c;
    # b_0 + b_1 identifies adverse selection theta.
    half_spread = b0
    order_processing = -b1
    adverse_selection = b0 + b1
    adverse_share = adverse_selection / half_spread if half_spread != 0.0 else float("nan")

    true_share = theta_true / (theta_true + c_true)
    print(f"Step 6 | Effective half-spread H:       {half_spread:.4f} (true: {theta_true + c_true:.4f})")
    print(f"       | Order-processing cost c:       {order_processing:.4f} (true: {c_true:.4f})")
    print(f"       | Adverse-selection cost theta:  {adverse_selection:.4f} (true: {theta_true:.4f})")
    print(f"       | Adverse selection share:       {adverse_share:.4f} (true: {true_share:.4f})")


main()
