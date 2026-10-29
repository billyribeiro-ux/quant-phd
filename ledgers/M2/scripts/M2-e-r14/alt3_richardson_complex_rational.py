"""Alternative correct engine: Richardson central estimate, complex-step AD, exact rational price (all permitted by the page)."""
from __future__ import annotations

import math
from collections.abc import Callable
from fractions import Fraction
from typing import Any

_SCHEMES = ("forward", "central")


def _positive_step(h: float) -> float:
    step = float(h)
    if not step > 0:
        raise ValueError("the step h must be above zero")
    return step


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    step = _positive_step(h)
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    if scheme == "central":
        def c(s: float) -> float:
            return (f(x + s) - f(x - s)) / (2 * s)
        return (4 * c(step / 2) - c(step)) / 3
    raise ValueError("scheme must be 'forward' or 'central'")


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    eps = 1e-20
    value = f(complex(float(x), eps))
    return float(complex(value).imag / eps)


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    step = _positive_step(h)
    base = [float(v) for v in x]
    n = len(base)

    def moved(changes: dict[int, float]) -> list[float]:
        p = list(base)
        for i, a in changes.items():
            p[i] += a
        return p

    hess = [[0.0] * n for _ in range(n)]
    f0 = f(base)
    for i in range(n):
        up = f(moved({i: step}))
        down = f(moved({i: -step}))
        hess[i][i] = (up - 2 * f0 + down) / (step * step)
        for j in range(i + 1, n):
            mixed = (f(moved({i: step, j: step})) - f(moved({i: step, j: -step}))
                     - f(moved({i: -step, j: step})) + f(moved({i: -step, j: -step})))
            hess[i][j] = mixed / (4 * step * step)
            hess[j][i] = hess[i][j]
    return hess


def _yield_rate(instance: dict[str, Any]) -> Fraction:
    yield_bps = instance["yield_bps"]
    if yield_bps <= -10_000:
        raise ValueError("the yield must be above -1 (-10000 basis points)")
    return Fraction(int(yield_bps), 10_000)


def _flows(instance: dict[str, Any]) -> tuple[list[tuple[int, Fraction]], Fraction]:
    rate = _yield_rate(instance)
    face = Fraction(int(instance["face_cents"]))
    coupon = face * Fraction(int(instance["coupon_bps"]), 10_000)
    years = int(instance["maturity_years"])
    return [(t, coupon + (face if t == years else 0)) for t in range(1, years + 1)], rate


def bond_price_cents(instance: dict[str, Any]) -> int:
    flows, rate = _flows(instance)
    v = 1 / (1 + rate)
    price = sum((cash * v**t for t, cash in flows), Fraction(0))
    return int(round(price))


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    flows, rate = _flows(instance)
    v = 1 / (1 + float(rate))
    price = sum(float(cash) * v**t for t, cash in flows)
    first = -sum(t * float(cash) * v ** (t + 1) for t, cash in flows)
    second = sum(t * (t + 1) * float(cash) * v ** (t + 2) for t, cash in flows)
    return {
        "dprice_dy": float(first),
        "d2price_dy2": float(second),
        "duration_analytic": float(-first / price),
        "convexity_analytic": float(second / price),
    }
