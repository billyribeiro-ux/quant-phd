"""Lab S4-project-2: Rung 2 completion problem for Atlas A4 time-series toolkit.

SIMULATED: completion twin containing the full solution to GARCH recursion
and QLIKE evaluation.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    rng = random.Random(101)
    omega, alpha, beta = 0.05, 0.12, 0.80
    n = 60

    h = omega / (1.0 - alpha - beta)
    returns: list[float] = []
    for _ in range(n):
        z = rng.gauss(0.0, 1.0)
        eps = math.sqrt(h) * z
        returns.append(eps)
        h = omega + alpha * (eps**2) + beta * h

    # Pre-calculated sample mean and h_0
    mean_r = sum(returns) / n
    h0 = sum((r - mean_r) ** 2 for r in returns) / n

    # Step 1: Complete the GARCH(1,1) variance step
    h_last = h0
    for t in range(1, n):
        h_last = omega + alpha * (returns[t - 1] ** 2) + beta * h_last

    # Step 2: Complete QLIKE loss formula
    realized_val = 0.90
    forecast_val = h_last
    ratio = realized_val / forecast_val
    qlike_val = ratio - math.log(ratio) - 1.0

    print("Rung 2 Completion Audit Check:")
    print(f"  Final GARCH conditional variance: {h_last:.4f}")
    print(f"  Evaluated QLIKE loss: {qlike_val:.4f}")
    print(f"  Loss non-negativity verified: {qlike_val >= 0.0}")


main()
