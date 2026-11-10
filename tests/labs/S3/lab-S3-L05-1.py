"""Lab S3-L05-1: Cointegration and error correction.

SIMULATED: generates a cointegrated pair from a common stochastic trend,
verifies variance stability of the spread across sub-blocks, and estimates
the error-correction speed of adjustment.
"""

from __future__ import annotations

import random


def main() -> None:
    rng = random.Random(42)
    n = 1000
    beta_true = 1.50
    phi_spread = 0.70

    # Common stochastic trend
    w = [0.0]
    for _ in range(n - 1):
        w.append(w[-1] + rng.gauss(0.0, 1.0))

    x = [w[t] + rng.gauss(0.0, 0.5) for t in range(n)]
    s = [0.0]
    for _ in range(1, n):
        s.append(phi_spread * s[-1] + rng.gauss(0.0, 0.8))

    y = [2.0 + beta_true * x[t] + s[t] for t in range(n)]
    spread = [y[t] - 2.0 - beta_true * x[t] for t in range(n)]

    # Sub-block variances (4 blocks of 250 observations)
    block_size = 250
    print("Sub-block Variance Comparison (4 blocks of 250):")
    print("Block | Var(x_t) [I(1)] | Var(spread_t) [I(0)]")
    print("-" * 46)
    for b in range(4):
        bx = x[b * block_size : (b + 1) * block_size]
        bs = spread[b * block_size : (b + 1) * block_size]
        mx = sum(bx) / block_size
        ms = sum(bs) / block_size
        vx = sum((v - mx) ** 2 for v in bx) / block_size
        vs = sum((v - ms) ** 2 for v in bs) / block_size
        print(f"  {b + 1}   |      {vx:6.2f}    |         {vs:.4f}")

    # Error-correction regression: Delta y_t = c + alpha_e * s_{t-1} + e_t
    dy = [y[t] - y[t - 1] for t in range(1, n)]
    s_lag = [spread[t - 1] for t in range(1, n)]
    m = n - 1
    mean_s = sum(s_lag) / m
    mean_dy = sum(dy) / m
    cov = sum((s_lag[i] - mean_s) * (dy[i] - mean_dy) for i in range(m))
    var_s = sum((s_lag[i] - mean_s) ** 2 for i in range(m))
    alpha_e = cov / var_s
    expected_alpha_e = -(1.0 - phi_spread)

    print("\nError-Correction Dynamics:")
    print(f"  Theoretical adjustment speed: {expected_alpha_e:+.4f} (-(1 - phi))")
    print(f"  Estimated adjustment speed:   {alpha_e:+.4f}")


main()
