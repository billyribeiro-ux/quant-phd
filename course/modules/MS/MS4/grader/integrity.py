"""Integrity and validation utilities for MS4 capacity models.

Validates input vectors, weights, price arrays, and structural invariants.
"""

from __future__ import annotations

import math


def validate_vectors(
    w_initial: list[float],
    w_target: list[float],
    adv: list[float],
    sigma: list[float],
    prices: list[float] | None = None,
) -> None:
    """Validate input dimensions and numeric ranges for portfolio assets."""
    n = len(w_initial)
    if n < 3:
        raise ValueError(f"portfolio must contain at least 3 assets; got {n}")
    if len(w_target) != n:
        raise ValueError(f"w_target length ({len(w_target)}) does not match w_initial length ({n})")
    if len(adv) != n:
        raise ValueError(f"adv length ({len(adv)}) does not match asset count ({n})")
    if len(sigma) != n:
        raise ValueError(f"sigma length ({len(sigma)}) does not match asset count ({n})")
    if prices is not None and len(prices) != n:
        raise ValueError(f"prices length ({len(prices)}) does not match asset count ({n})")

    sum_init = sum(w_initial)
    if not math.isclose(sum_init, 1.0, abs_tol=1e-5):
        raise ValueError(f"initial weights must sum to 1.0; got {sum_init:.6f}")
    sum_target = sum(w_target)
    if not math.isclose(sum_target, 1.0, abs_tol=1e-5):
        raise ValueError(f"target weights must sum to 1.0; got {sum_target:.6f}")

    for i in range(n):
        if adv[i] <= 0:
            raise ValueError(f"average daily volume must be positive; asset {i} has adv {adv[i]}")
        if sigma[i] <= 0:
            raise ValueError(f"volatility must be positive; asset {i} has sigma {sigma[i]}")
        if prices is not None and prices[i] <= 0:
            raise ValueError(f"asset price must be positive; asset {i} has price {prices[i]}")
        if w_initial[i] < -1e-6 or w_target[i] < -1e-6:
            raise ValueError(f"short positions not allowed in standard long-only sleeve; asset {i}")
