"""Alternative A: Richardson-extrapolated central quotient, complex-step AD, exact-Fraction price, NumPy-free."""

from __future__ import annotations

import math
from collections.abc import Callable
from fractions import Fraction
from typing import Any


def _step(h: float) -> float:
    if not (h > 0):
        raise ValueError("step must be above zero")
    return float(h)


def _central(f: Callable[[float], float], x: float, h: float) -> float:
    return (f(x + h) - f(x - h)) / (2 * h)


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    step = _step(h)
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    if scheme == "central":
        # Richardson: (4 D(h/2) - D(h)) / 3 cancels the h^2 term of the central quotient.
        return (4 * _central(f, x, step / 2) - _central(f, x, step)) / 3
    raise ValueError("scheme must be forward or central")


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    eps = 1e-20
    out = f(complex(x, eps))
    return float(complex(out).imag / eps)


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    step = _step(h)
    base = [float(v) for v in x]
    n = len(base)

    def at(changes: dict[int, float]) -> list[float]:
        p = list(base)
        for i, d in changes.items():
            p[i] += d
        return p

    def raw(s: float) -> list[list[float]]:
        H = [[0.0] * n for _ in range(n)]
        f0 = f(base)
        for i in range(n):
            H[i][i] = (f(at({i: s})) - 2 * f0 + f(at({i: -s}))) / (s * s)
            for j in range(i + 1, n):
                m = (
                    f(at({i: s, j: s}))
                    - f(at({i: s, j: -s}))
                    - f(at({i: -s, j: s}))
                    + f(at({i: -s, j: -s}))
                ) / (4 * s * s)
                H[i][j] = H[j][i] = m
        return H

    a, b = raw(step), raw(step / 2)
    return [[(4 * b[i][j] - a[i][j]) / 3 for j in range(n)] for i in range(n)]


def _price_fraction(instance: dict[str, Any]) -> Fraction:
    y = Fraction(instance["yield_bps"], 10_000)
    if y <= -1:
        raise ValueError("yield must be above -1")
    face = instance["face_cents"]
    coupon = Fraction(face * instance["coupon_bps"], 10_000)
    years = instance["maturity_years"]
    v = 1 / (1 + y)
    return sum(((coupon + (face if t == years else 0)) * v**t for t in range(1, years + 1)), Fraction(0))


def bond_price_cents(instance: dict[str, Any]) -> int:
    p = _price_fraction(instance)
    n = math.floor(p)
    r = p - n
    if r > Fraction(1, 2):
        return n + 1
    if r < Fraction(1, 2):
        return n
    return n if n % 2 == 0 else n + 1


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    y = Fraction(instance["yield_bps"], 10_000)
    if y <= -1:
        raise ValueError("yield must be above -1")
    face = instance["face_cents"]
    coupon = Fraction(face * instance["coupon_bps"], 10_000)
    years = instance["maturity_years"]
    v = 1 / (1 + y)
    flows = [(t, coupon + (face if t == years else 0)) for t in range(1, years + 1)]
    price = sum((c * v**t for t, c in flows), Fraction(0))
    first = -sum((t * c * v ** (t + 1) for t, c in flows), Fraction(0))
    second = sum((t * (t + 1) * c * v ** (t + 2) for t, c in flows), Fraction(0))
    return {
        "dprice_dy": float(first),
        "d2price_dy2": float(second),
        "duration_analytic": float(-first / price),
        "convexity_analytic": float(second / price),
    }
