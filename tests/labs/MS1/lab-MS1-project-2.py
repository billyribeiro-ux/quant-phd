"""Lab MS1-project-2: Rung 2 completion problem for trade decomposition.

SIMULATED: generates trade prices and signs for seed 7.
On the project page, the order processing recovery line is blanked:
order_processing = ___
The twin contains the complete solution.
"""

from __future__ import annotations

import random


def main() -> None:
    rng = random.Random(7)
    n = 400
    theta_true = 0.12
    c_true = 0.18
    sigma = 0.04
    m = 100.0

    prices: list[float] = []
    signs: list[int] = []
    for _ in range(n):
        q = rng.choice([-1, 1])
        eta = rng.gauss(0.0, sigma)
        m += theta_true * q + eta
        prices.append(m + c_true * q)
        signs.append(q)

    d = [prices[i] - prices[i - 1] for i in range(1, n)]
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
    order_processing = -b1
    adverse_selection = b0 + b1
    adverse_share = adverse_selection / half_spread if half_spread != 0.0 else float("nan")

    print(f"Regression slopes: b_0 = {b0:.4f}, b_1 = {b1:.4f}")
    print(f"Recovered order processing c: {order_processing:.4f} (true: {c_true:.4f})")
    print(f"Recovered adverse selection theta: {adverse_selection:.4f} (true: {theta_true:.4f})")
    print(f"Adverse share: {adverse_share:.4f}")


main()
