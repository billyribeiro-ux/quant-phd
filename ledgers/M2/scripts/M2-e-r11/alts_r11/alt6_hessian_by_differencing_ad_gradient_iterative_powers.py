"""Alternative correct implementation (round 11): Hessian by the page formula with a shift helper; iterative discount powers, no AD."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

_SCHEMES = ("forward", "central")


def _need_positive(h: float) -> float:
    step = float(h)
    if step != step or step <= 0:
        raise ValueError("step must be a positive number")
    return step


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    step = _need_positive(h)
    if not isinstance(scheme, str) or scheme not in _SCHEMES:
        raise ValueError("scheme must be 'forward' or 'central'")
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    return (f(x + step) - f(x - step)) / (2.0 * step)


class _D:
    """Dual number a + b*eps, eps*eps = 0."""

    def __init__(self, a: float, b: float) -> None:
        self.a = a
        self.b = b

    def __add__(self, o: Any) -> _D:
        o = _as_d(o)
        return _D(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __sub__(self, o: Any) -> _D:
        o = _as_d(o)
        return _D(self.a - o.a, self.b - o.b)

    def __rsub__(self, o: Any) -> _D:
        o = _as_d(o)
        return _D(o.a - self.a, o.b - self.b)

    def __mul__(self, o: Any) -> _D:
        o = _as_d(o)
        return _D(self.a * o.a, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__


def _as_d(v: Any) -> _D:
    return v if isinstance(v, _D) else _D(float(v), 0.0)


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    out = _as_d(f(_D(float(x), 1.0)))
    return float(out.b)


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    """The page's formula: diagonal (f(+h) - 2 f(0) + f(-h)) / h^2 and mixed (four corners) / (4 h^2)."""
    step = _need_positive(h)
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
        out[i][i] = (at({i: step}) - 2.0 * f0 + at({i: -step})) / (step * step)
        for j in range(i + 1, n):
            mixed = (
                at({i: step, j: step}) - at({i: step, j: -step}) - at({i: -step, j: step}) + at({i: -step, j: -step})
            ) / (4.0 * step * step)
            out[i][j] = out[j][i] = mixed
    return out


def _cash(instance: dict[str, Any]) -> tuple[float, float, int, list[float]]:
    yield_bps = instance["yield_bps"]
    if yield_bps <= -10_000:
        raise ValueError("yield must be above -1")
    rate = float(yield_bps) / 10_000.0
    face = float(instance["face_cents"])
    coupon = face * float(instance["coupon_bps"]) / 10_000.0
    years = int(instance["maturity_years"])
    cash = [coupon] * years
    cash[-1] += face
    return rate, coupon, years, cash


def bond_price_cents(instance: dict[str, Any]) -> int:
    rate, _, years, cash = _cash(instance)
    v = 1.0 / (1.0 + rate)
    total = 0.0
    pw = 1.0
    for t in range(1, years + 1):
        pw *= v
        total += cash[t - 1] * pw
    return round(total)


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    rate, _, years, cash = _cash(instance)
    v = 1.0 / (1.0 + rate)
    price = 0.0
    first_sum = 0.0
    second_sum = 0.0
    pw = 1.0
    for t in range(1, years + 1):
        pw *= v  # v ** t, by repeated multiplication
        c = cash[t - 1]
        price += c * pw
        first_sum += t * c * (pw * v)  # t * C_t * v^(t+1)
        second_sum += t * (t + 1) * c * (pw * v * v)  # t(t+1) * C_t * v^(t+2)
    first = -first_sum
    return {
        "dprice_dy": first,
        "d2price_dy2": second_sum,
        "duration_analytic": -first / price,
        "convexity_analytic": second_sum / price,
    }
