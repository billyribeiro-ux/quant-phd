"""Alternative 5 (NumPy): the price and the sensitivities are NumPy vector sums over the cash-flow years."""

from __future__ import annotations

from typing import Any

import numpy as np

from reference_core import ad_derivative, fd_derivative, hessian_fd


def _vectors(instance: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, float]:
    yield_bps = instance["yield_bps"]
    if yield_bps <= -10_000:
        raise ValueError("the yield must be above -1 (-10000 basis points)")
    face = float(instance["face_cents"])
    years = int(instance["maturity_years"])
    t = np.arange(1, years + 1, dtype=np.float64)
    cash = np.full(years, face * instance["coupon_bps"] / 10_000, dtype=np.float64)
    cash[-1] += face
    return t, cash, float(yield_bps) / 10_000


def bond_price_cents(instance: dict[str, Any]) -> int:
    t, cash, rate = _vectors(instance)
    v = 1.0 / (1.0 + rate)
    price = float(np.sum(cash * v**t))
    return int(np.round(price))


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    t, cash, rate = _vectors(instance)
    v = 1.0 / (1.0 + rate)
    price = float(np.sum(cash * v**t))
    first = float(-np.sum(t * cash * v ** (t + 1)))
    second = float(np.sum(t * (t + 1) * cash * v ** (t + 2)))
    return {
        "dprice_dy": first,
        "d2price_dy2": second,
        "duration_analytic": -first / price,
        "convexity_analytic": second / price,
    }
