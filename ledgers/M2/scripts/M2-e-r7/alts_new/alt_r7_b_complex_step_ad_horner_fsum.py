"""Round 7 alternative B (verifier D7): complex-step ad_derivative, Horner-free fsum price, scheme type tests.

A different correct engine: ad_derivative is the imaginary part of f(x + i h) divided by h with h = 1e-30 (exact for
functions real on the real line, built from +, - and *); the price is an fsum over exact rational discount factors
(Fraction) rounded half-to-even by round(); the central and forward estimates are the reference formulas. Standard
library only.
"""
from __future__ import annotations

import math
from collections.abc import Callable
from fractions import Fraction
from typing import Any

_CS_STEP = 1e-30


def _positive_step(h: float) -> float:
    step = float(h)
    if not step > 0.0:
        raise ValueError("the step h must be above zero")
    return step


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    step = _positive_step(h)
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    if scheme == "central":
        return (f(x + step) - f(x - step)) / (2 * step)
    raise ValueError("scheme must be 'forward' or 'central'")


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    value = f(complex(float(x), _CS_STEP))
    return float(complex(value).imag / _CS_STEP)


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    step = _positive_step(h)
    base = [float(v) for v in x]
    n = len(base)
    hess = [[0.0] * n for _ in range(n)]

    def shifted(changes: dict[int, float]) -> list[float]:
        point = list(base)
        for k, amount in changes.items():
            point[k] += amount
        return point

    f0 = f(list(base))
    for i in range(n):
        plus, minus = f(shifted({i: step})), f(shifted({i: -step}))
        hess[i][i] = (plus - 2 * f0 + minus) / (step * step)
        for j in range(i + 1, n):
            mixed = (
                f(shifted({i: step, j: step}))
                - f(shifted({i: step, j: -step}))
                - f(shifted({i: -step, j: step}))
                + f(shifted({i: -step, j: -step}))
            )
            hess[i][j] = hess[j][i] = mixed / (4 * step * step)
    return hess


def _yield_fraction(instance: dict[str, Any]) -> Fraction:
    yield_bps = int(instance["yield_bps"])
    if yield_bps <= -10_000:
        raise ValueError("the yield must be above -1 (-10000 basis points)")
    return Fraction(yield_bps, 10_000)


def _cash(instance: dict[str, Any]) -> list[tuple[int, Fraction]]:
    face = Fraction(int(instance["face_cents"]))
    coupon = face * Fraction(int(instance["coupon_bps"]), 10_000)
    years = int(instance["maturity_years"])
    return [(t, coupon + (face if t == years else Fraction(0))) for t in range(1, years + 1)]


def bond_price_cents(instance: dict[str, Any]) -> int:
    rate = _yield_fraction(instance)
    v = 1 / (1 + rate)
    exact = sum((cash * v**t for t, cash in _cash(instance)), Fraction(0))
    return round(exact)


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    rate = _yield_fraction(instance)
    v = 1 / (1 + rate)
    flows = _cash(instance)
    price = sum((cash * v**t for t, cash in flows), Fraction(0))
    first = -sum((t * cash * v ** (t + 1) for t, cash in flows), Fraction(0))
    second = sum((t * (t + 1) * cash * v ** (t + 2) for t, cash in flows), Fraction(0))
    return {
        "dprice_dy": float(first),
        "d2price_dy2": float(second),
        "duration_analytic": float(-first / price),
        "convexity_analytic": float(second / price),
    }
