"""Alternative 4 (exact rational): the price and the sensitivities are sums of Fraction cash flows, rounded half to even."""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from reference_core import ad_derivative, fd_derivative, hessian_fd


def _bond(instance: dict[str, Any]) -> tuple[list[tuple[int, Fraction]], Fraction]:
    yield_bps = instance["yield_bps"]
    if yield_bps <= -10_000:
        raise ValueError("the yield must be above -1 (-10000 basis points)")
    face = instance["face_cents"]
    coupon = Fraction(face * instance["coupon_bps"], 10_000)
    years = instance["maturity_years"]
    flows = [(t, coupon + (face if t == years else 0)) for t in range(1, years + 1)]
    return flows, Fraction(1) / (1 + Fraction(yield_bps, 10_000))


def bond_price_cents(instance: dict[str, Any]) -> int:
    flows, v = _bond(instance)
    price = sum((cash * v**t for t, cash in flows), Fraction(0))
    return int(round(price))


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    flows, v = _bond(instance)
    price = sum((cash * v**t for t, cash in flows), Fraction(0))
    first = -sum((t * cash * v ** (t + 1) for t, cash in flows), Fraction(0))
    second = sum((t * (t + 1) * cash * v ** (t + 2) for t, cash in flows), Fraction(0))
    return {
        "dprice_dy": float(first),
        "d2price_dy2": float(second),
        "duration_analytic": float(-first / price),
        "convexity_analytic": float(second / price),
    }
