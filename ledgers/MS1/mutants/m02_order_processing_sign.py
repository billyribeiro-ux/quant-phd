"""Student error: forgets negative sign in order processing cost (sets c = b1 instead of -b1)."""

from __future__ import annotations

import math


def decompose_trades(prices: list[float], signs: list[int]) -> dict[str, float]:
    n = len(prices)
    if n < 3:
        raise ValueError("at least three trades are needed")
    if len(signs) != n:
        raise ValueError("prices and signs must have the same length")

    for s in signs:
        if s not in (-1, 1):
            raise ValueError("each sign must be -1 or +1")

    if all(s == signs[0] for s in signs):
        raise ValueError("signs must vary: the regression is singular")

    d = [prices[i] - prices[i - 1] for i in range(1, n)]
    mean_d = sum(d) / len(d)

    cov1 = sum((d[i] - mean_d) * (d[i - 1] - mean_d) for i in range(1, len(d))) / (len(d) - 1)
    roll_spread = 2.0 * math.sqrt(-cov1) if cov1 < 0.0 else float("nan")

    q_curr = [float(signs[i]) for i in range(1, n)]
    q_lag = [float(signs[i - 1]) for i in range(1, n)]

    s00 = sum(x * x for x in q_curr)
    s11 = sum(x * x for x in q_lag)
    s01 = sum(x * y for x, y in zip(q_curr, q_lag, strict=False))

    det = s00 * s11 - s01 * s01
    if det == 0.0:
        raise ValueError("signs must vary: the regression is singular")

    y0 = sum(di * qi for di, qi in zip(d, q_curr, strict=False))
    y1 = sum(di * qi for di, qi in zip(d, q_lag, strict=False))

    b0 = (s11 * y0 - s01 * y1) / det
    b1 = (s00 * y1 - s01 * y0) / det

    half_spread = b0
    order_processing = b1  # Bug: missing minus sign
    adverse_selection = b0 + b1

    adverse_share = adverse_selection / half_spread if half_spread != 0.0 else float("nan")

    return {
        "roll_spread": roll_spread,
        "half_spread": half_spread,
        "order_processing": order_processing,
        "adverse_selection": adverse_selection,
        "adverse_share": adverse_share,
    }
