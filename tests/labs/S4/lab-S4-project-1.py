"""Lab S4-project-1: Rung 1 worked example for Atlas A4 time-series toolkit.

SIMULATED: fully solved instance of GARCH(1,1) variance recursion, HAR design,
and QLIKE loss evaluation.
"""

from __future__ import annotations

import math
import random


def run_worked_example() -> None:
    rng = random.Random(42)
    # 1. GARCH(1,1) path
    omega, alpha, beta = 0.04, 0.10, 0.82
    h = omega / (1.0 - alpha - beta)
    returns: list[float] = []
    for _ in range(100):
        z = rng.gauss(0.0, 1.0)
        eps = math.sqrt(h) * z
        returns.append(eps)
        h = omega + alpha * (eps**2) + beta * h

    # GARCH variance recursion
    mean_r = sum(returns) / len(returns)
    h0 = sum((r - mean_r) ** 2 for r in returns) / len(returns)
    var_seq = [h0]
    for t in range(1, len(returns)):
        ht = omega + alpha * (returns[t - 1] ** 2) + beta * var_seq[-1]
        var_seq.append(ht)

    # 2. QLIKE calculation
    realized_val = 0.85
    forecast_val = var_seq[-1]
    ratio = realized_val / forecast_val
    qlike_val = ratio - math.log(ratio) - 1.0

    print("Rung 1 Worked Example Pipeline:")
    print(f"  Returns length: {len(returns)}")
    print(f"  Initial variance h_0: {h0:.4f}")
    print(f"  Terminal variance h_T: {var_seq[-1]:.4f}")
    print(f"  Realized target: {realized_val:.4f}")
    print(f"  QLIKE loss: {qlike_val:.4f}")


def main() -> None:
    run_worked_example()


main()
