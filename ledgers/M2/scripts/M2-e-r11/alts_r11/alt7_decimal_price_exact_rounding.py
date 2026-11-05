"""Alternative correct implementation (round 11): the price is priced in 60-digit Decimal and rounded half to even; derivatives in float."""

from __future__ import annotations

from collections.abc import Callable
from decimal import ROUND_HALF_EVEN, Decimal, localcontext
from typing import Any

_SCHEMES = frozenset({"forward", "central"})


def _step(h: float) -> float:
    if not h > 0:
        raise ValueError("step must be above zero")
    return float(h)


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    s = _step(h)
    if not (type(scheme) is str and scheme in _SCHEMES):
        raise ValueError("unknown scheme")
    if scheme == "forward":
        return (f(x + s) - f(x)) / s
    return (f(x + s) - f(x - s)) / (2 * s)


class _Dn:
    __slots__ = ("p", "q")

    def __init__(self, p: float, q: float) -> None:
        self.p, self.q = p, q

    def __add__(self, o: Any) -> _Dn:
        o = _lift(o)
        return _Dn(self.p + o.p, self.q + o.q)

    __radd__ = __add__

    def __sub__(self, o: Any) -> _Dn:
        o = _lift(o)
        return _Dn(self.p - o.p, self.q - o.q)

    def __rsub__(self, o: Any) -> _Dn:
        o = _lift(o)
        return _Dn(o.p - self.p, o.q - self.q)

    def __mul__(self, o: Any) -> _Dn:
        o = _lift(o)
        return _Dn(self.p * o.p, self.p * o.q + self.q * o.p)

    __rmul__ = __mul__


def _lift(v: Any) -> _Dn:
    return v if isinstance(v, _Dn) else _Dn(float(v), 0.0)


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    return float(_lift(f(_Dn(float(x), 1.0))).q)


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    s = _step(h)
    base = [float(v) for v in x]
    n = len(base)

    def at(shifts: dict[int, float]) -> float:
        p = list(base)
        for k, d in shifts.items():
            p[k] += d
        return f(p)

    f0 = at({})
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        out[i][i] = (at({i: s}) - 2 * f0 + at({i: -s})) / (s * s)
        for j in range(i + 1, n):
            m = (at({i: s, j: s}) - at({i: s, j: -s}) - at({i: -s, j: s}) + at({i: -s, j: -s})) / (4 * s * s)
            out[i][j] = out[j][i] = m
    return out


def _flows(instance: dict[str, Any]) -> tuple[Decimal, list[tuple[int, Decimal]]]:
    yb = instance["yield_bps"]
    if yb <= -10_000:
        raise ValueError("yield must be above -1")
    rate = Decimal(yb) / Decimal(10_000)
    face = Decimal(instance["face_cents"])
    coupon = face * Decimal(instance["coupon_bps"]) / Decimal(10_000)
    years = int(instance["maturity_years"])
    flows = [(t, coupon + (face if t == years else Decimal(0))) for t in range(1, years + 1)]
    return rate, flows


def bond_price_cents(instance: dict[str, Any]) -> int:
    rate, flows = _flows(instance)
    with localcontext() as ctx:
        ctx.prec = 400  # a yield just above -1 makes the price about 10**120 cents, so 60 digits are not enough
        v = 1 / (1 + rate)
        price = sum((c * v**t for t, c in flows), Decimal(0))
        return int(price.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    rate, flows = _flows(instance)
    with localcontext() as ctx:
        ctx.prec = 400  # a yield just above -1 makes the price about 10**120 cents, so 60 digits are not enough
        v = 1 / (1 + rate)
        price = sum((c * v**t for t, c in flows), Decimal(0))
        first = -sum((t * c * v ** (t + 1) for t, c in flows), Decimal(0))
        second = sum((t * (t + 1) * c * v ** (t + 2) for t, c in flows), Decimal(0))
        out = {
            "dprice_dy": float(first),
            "d2price_dy2": float(second),
            "duration_analytic": float(-first / price),
            "convexity_analytic": float(second / price),
        }
    return out
