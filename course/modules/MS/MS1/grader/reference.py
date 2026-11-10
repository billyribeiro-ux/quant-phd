"""Reference implementation of the trade-level spread decomposition for MS1.

Implements the frozen interface:
    decompose_trades(prices: list[float], signs: list[int]) -> dict[str, float]
recovering the Roll spread, effective half-spread, order-processing cost,
adverse-selection cost, and adverse selection share.
"""

from __future__ import annotations

import math


def decompose_trades(prices: list[float], signs: list[int]) -> dict[str, float]:
    """Decompose transaction prices and trade signs into microstructure components.

    Parameters
    ----------
    prices : list[float]
        Sequential transaction prices (length >= 3).
    signs : list[int]
        Sequential trade directions, each in {-1, +1}.

    Returns
    -------
    dict[str, float]
        Dictionary with keys:
        - "roll_spread": Roll spread estimator 2*sqrt(-cov1), or NaN if cov1 >= 0.
        - "half_spread": Estimated effective half-spread H = b0.
        - "order_processing": Estimated order processing component c = -b1.
        - "adverse_selection": Estimated adverse selection component theta = b0 + b1.
        - "adverse_share": theta / H, or NaN if H == 0.
    """
    n = len(prices)
    if n < 3:
        raise ValueError("at least three trades are needed")
    if len(signs) != n:
        raise ValueError("prices and signs must have the same length")

    for s in signs:
        if s not in (-1, 1):
            raise ValueError("each sign must be -1 or +1")

    # Check whether all signs are identical
    if all(s == signs[0] for s in signs):
        raise ValueError("signs must vary: the regression is singular")

    # Compute price differences d_t = p_t - p_{t-1} for t = 2..n
    d = [prices[i] - prices[i - 1] for i in range(1, n)]
    mean_d = sum(d) / len(d)

    # Sample lag-1 autocovariance of price differences
    # cov1 = 1/(n-2) * sum_{t=3}^n (d_t - mean_d)*(d_{t-1} - mean_d)
    cov1 = sum((d[i] - mean_d) * (d[i - 1] - mean_d) for i in range(1, len(d))) / (len(d) - 1)
    roll_spread = 2.0 * math.sqrt(-cov1) if cov1 < 0.0 else float("nan")

    # Regress d_t on (q_t, q_{t-1}) without intercept for t = 2..n
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
    order_processing = -b1
    adverse_selection = b0 + b1

    adverse_share = adverse_selection / half_spread if half_spread != 0.0 else float("nan")

    return {
        "roll_spread": roll_spread,
        "half_spread": half_spread,
        "order_processing": order_processing,
        "adverse_selection": adverse_selection,
        "adverse_share": adverse_share,
    }
