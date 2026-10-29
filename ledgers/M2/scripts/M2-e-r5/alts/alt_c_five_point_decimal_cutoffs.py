"""Alternative C: five-point central stencil, Decimal half-even rounding, different but valid cutoffs and checks."""

from __future__ import annotations

import math
from collections.abc import Callable
from decimal import ROUND_HALF_EVEN, Decimal, localcontext
from typing import Any


def _check_step(h: float) -> float:
    if math.isnan(h) or h <= 0.0:
        raise ValueError("the step must be a positive number")
    return h


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    s = _check_step(h)
    if not isinstance(scheme, str) or scheme not in ("forward", "central"):
        raise ValueError("unknown scheme")
    if scheme == "forward":
        return (f(x + s) - f(x)) / s
    return (-f(x + 2 * s) + 8 * f(x + s) - 8 * f(x - s) + f(x - 2 * s)) / (12 * s)


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    class D:
        __slots__ = ("v", "d")

        def __init__(self, v: float, d: float) -> None:
            self.v, self.d = v, d

        @staticmethod
        def lift(o: Any) -> D:
            return o if isinstance(o, D) else D(float(o), 0.0)

        def __add__(self, o: Any) -> D:
            o = D.lift(o)
            return D(self.v + o.v, self.d + o.d)

        __radd__ = __add__

        def __sub__(self, o: Any) -> D:
            o = D.lift(o)
            return D(self.v - o.v, self.d - o.d)

        def __rsub__(self, o: Any) -> D:
            o = D.lift(o)
            return D(o.v - self.v, o.d - self.d)

        def __mul__(self, o: Any) -> D:
            o = D.lift(o)
            return D(self.v * o.v, self.d * o.v + self.v * o.d)

        __rmul__ = __mul__

    r = f(D(float(x), 1.0))
    return float(D.lift(r).d)


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    s = _check_step(h)
    p = [float(v) for v in x]
    n = len(p)
    out = [[0.0] * n for _ in range(n)]
    f0 = f(p)
    for i in range(n):
        for j in range(n):
            if i == j:
                pu, pd = list(p), list(p)
                pu[i] += s
                pd[i] -= s
                out[i][i] = (f(pu) - 2 * f0 + f(pd)) / (s * s)
            elif j > i:
                def g(a: float, b: float) -> float:
                    q = list(p)
                    q[i] += a
                    q[j] += b
                    return f(q)
                out[i][j] = (g(s, s) - g(s, -s) - g(-s, s) + g(-s, -s)) / (4 * s * s)
                out[j][i] = out[i][j]
    return out


def _cash(instance: dict[str, Any]) -> tuple[list[tuple[int, float]], float]:
    y = instance["yield_bps"]
    if y < -10_000:
        raise ValueError("yield must not be below -1")
    if y == -10_000:
        raise ValueError("yield must be above -1")
    face = instance["face_cents"]
    coupon = face * instance["coupon_bps"] / 10_000
    years = instance["maturity_years"]
    flows = [(t, coupon + (face if t == years else 0)) for t in range(1, years + 1)]
    return flows, y / 10_000


def bond_price_cents(instance: dict[str, Any]) -> int:
    flows, y = _cash(instance)
    v = 1 / (1 + y)
    p = sum(c * v**t for t, c in flows)
    with localcontext() as ctx:
        ctx.prec = 800
        return int(Decimal(p).quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    flows, y = _cash(instance)
    v = 1 / (1 + y)
    p = sum(c * v**t for t, c in flows)
    d1 = -sum(t * c * v ** (t + 1) for t, c in flows)
    d2 = sum(t * (t + 1) * c * v ** (t + 2) for t, c in flows)
    return {
        "dprice_dy": float(d1),
        "d2price_dy2": float(d2),
        "duration_analytic": float(-d1 / p),
        "convexity_analytic": float(d2 / p),
    }
