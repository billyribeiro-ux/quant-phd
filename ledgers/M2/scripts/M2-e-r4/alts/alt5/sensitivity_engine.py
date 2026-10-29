"""Alternative 5: reverse-free dual numbers with a Horner-style price, round() half-even rounding, and a forward-only central quotient."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class Dual:
    def __init__(self, value: float, dot: float) -> None:
        self.value = value
        self.dot = dot

    @staticmethod
    def _lift(x: Any) -> Dual:
        return x if isinstance(x, Dual) else Dual(float(x), 0.0)

    def __add__(self, other: Any) -> Dual:
        o = self._lift(other)
        return Dual(self.value + o.value, self.dot + o.dot)

    def __radd__(self, other: Any) -> Dual:
        return self + other

    def __sub__(self, other: Any) -> Dual:
        o = self._lift(other)
        return Dual(self.value - o.value, self.dot - o.dot)

    def __rsub__(self, other: Any) -> Dual:
        o = self._lift(other)
        return Dual(o.value - self.value, o.dot - self.dot)

    def __mul__(self, other: Any) -> Dual:
        o = self._lift(other)
        return Dual(self.value * o.value, self.dot * o.value + self.value * o.dot)

    def __rmul__(self, other: Any) -> Dual:
        return self * other


def _check_step(h: float) -> None:
    if not h > 0:
        raise ValueError("step must be above zero")


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    _check_step(h)
    if scheme == "forward":
        return (f(x + h) - f(x)) / h
    if scheme == "central":
        return (f(x + h) - f(x - h)) / (2 * h)
    raise ValueError("scheme must be forward or central")


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    out = f(Dual(x, 1.0))
    if isinstance(out, Dual):
        return float(out.dot)
    return 0.0


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    _check_step(h)
    n = len(x)
    base = f(list(x))
    rows: list[list[float]] = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                up, dn = list(x), list(x)
                up[i] += h
                dn[i] -= h
                row.append(float((f(up) - 2 * base + f(dn)) / (h * h)))
            else:
                pp, pm, mp, mm = list(x), list(x), list(x), list(x)
                pp[i] += h; pp[j] += h
                pm[i] += h; pm[j] -= h
                mp[i] -= h; mp[j] += h
                mm[i] -= h; mm[j] -= h
                row.append(float((f(pp) - f(pm) - f(mp) + f(mm)) / (4 * h * h)))
        rows.append(row)
    return rows


def _flows(instance: dict[str, Any]) -> tuple[int, list[tuple[int, float]], float]:
    face = instance["face_cents"]
    coupon = face * instance["coupon_bps"] / 10_000
    years = instance["maturity_years"]
    y = instance["yield_bps"] / 10_000
    if y <= -1:
        raise ValueError("yield must be above -1")
    return face, [(t, coupon + (face if t == years else 0)) for t in range(1, years + 1)], y


def bond_price_cents(instance: dict[str, Any]) -> int:
    _, flows, y = _flows(instance)
    v = 1.0 / (1.0 + y)
    price = 0.0
    for t, c in flows:  # Horner in v over the years, then the sum of the flows
        price += c * v**t
    return int(round(price))  # round() on a float is half to even; no Decimal precision limit


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    _, flows, y = _flows(instance)
    v = 1.0 / (1.0 + y)
    price = sum(c * v**t for t, c in flows)
    d1 = -sum(t * c * v ** (t + 1) for t, c in flows)
    d2 = sum(t * (t + 1) * c * v ** (t + 2) for t, c in flows)
    return {
        "dprice_dy": float(d1),
        "d2price_dy2": float(d2),
        "duration_analytic": float(-d1 / price),
        "convexity_analytic": float(d2 / price),
    }
