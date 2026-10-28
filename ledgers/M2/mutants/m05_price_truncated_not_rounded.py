"""The bond price is truncated toward zero instead of rounded half to even."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

_SCHEMES = ("forward", "central")


def _positive_step(h: float) -> float:
    """The step as a float, when it is above zero; anything else raises ValueError."""
    step = float(h)
    if not step > 0:
        raise ValueError("the step h must be above zero")
    return step


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    """A finite-difference estimate of f'(x): forward, (f(x+h) - f(x)) / h, or central, (f(x+h) - f(x-h)) / (2h)."""
    step = _positive_step(h)
    if scheme == "forward":
        return (f(x + step) - f(x)) / step
    if scheme == "central":
        return (f(x + step) - f(x - step)) / (2 * step)
    raise ValueError("scheme must be 'forward' or 'central'")


class _Dual:
    """A dual number value + dot * epsilon, with epsilon squared equal to zero: the forward-mode AD carrier."""

    __slots__ = ("dot", "value")

    def __init__(self, value: float, dot: float) -> None:
        self.value = value
        self.dot = dot

    def __add__(self, other: Any) -> _Dual:
        o = _lift(other)
        return _Dual(self.value + o.value, self.dot + o.dot)

    __radd__ = __add__

    def __sub__(self, other: Any) -> _Dual:
        o = _lift(other)
        return _Dual(self.value - o.value, self.dot - o.dot)

    def __rsub__(self, other: Any) -> _Dual:
        o = _lift(other)
        return _Dual(o.value - self.value, o.dot - self.dot)

    def __mul__(self, other: Any) -> _Dual:
        o = _lift(other)
        return _Dual(self.value * o.value, self.value * o.dot + self.dot * o.value)

    __rmul__ = __mul__


def _lift(x: Any) -> _Dual:
    """A dual number unchanged, or a real number as a dual number with zero derivative."""
    if isinstance(x, _Dual):
        return x
    return _Dual(float(x), 0.0)


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    """The derivative of f at x by forward-mode automatic differentiation: f is evaluated on a dual number."""
    result = _lift(f(_Dual(float(x), 1.0)))
    return float(result.dot)


def _moved(base: list[float], changes: dict[int, float]) -> list[float]:
    """A copy of the point base with the listed coordinates moved by the listed amounts."""
    point = list(base)
    for index, amount in changes.items():
        point[index] += amount
    return point


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    """The Hessian of f at x by central differences: diagonal second differences and mixed central differences."""
    step = _positive_step(h)
    base = [float(v) for v in x]
    n = len(base)
    hessian = [[0.0] * n for _ in range(n)]
    f0 = f(base)
    for i in range(n):
        up = f(_moved(base, {i: step}))
        down = f(_moved(base, {i: -step}))
        hessian[i][i] = (up - 2 * f0 + down) / (step * step)
        for j in range(i + 1, n):
            mixed = (
                f(_moved(base, {i: step, j: step}))
                - f(_moved(base, {i: step, j: -step}))
                - f(_moved(base, {i: -step, j: step}))
                + f(_moved(base, {i: -step, j: -step}))
            )
            hessian[i][j] = mixed / (4 * step * step)
            hessian[j][i] = hessian[i][j]
    return hessian


def _yield_rate(instance: dict[str, Any]) -> float:
    """The annual yield as a decimal, from its basis points; a yield at or below -1 raises ValueError."""
    yield_bps = instance["yield_bps"]
    if yield_bps <= -10_000:
        raise ValueError("the yield must be above -1 (-10000 basis points)")
    return float(yield_bps) / 10_000


def _cash_flows(instance: dict[str, Any]) -> tuple[list[tuple[int, float]], float]:
    """The (year, cash) pairs of the bond in cents, and the yield, after the yield check."""
    rate = _yield_rate(instance)
    face = float(instance["face_cents"])
    coupon = face * instance["coupon_bps"] / 10_000
    years = int(instance["maturity_years"])
    flows = [(t, coupon + (face if t == years else 0.0)) for t in range(1, years + 1)]
    return flows, rate


def bond_price_cents(instance: dict[str, Any]) -> int:
    """The bond price in integer cents, the unrounded price rounded half to even."""
    flows, rate = _cash_flows(instance)
    v = 1 / (1 + rate)
    price = sum(cash * v**t for t, cash in flows)
    return int(price)


def sensitivities(instance: dict[str, Any]) -> dict[str, float]:
    """The first and second derivatives of the unrounded price in the yield, and the two named ratios.

    dprice_dy is -sum t * cash_t * v^(t+1) in cents per unit of yield; d2price_dy2 is sum t(t+1) * cash_t * v^(t+2)
    in cents per squared unit of yield; duration_analytic is -dprice_dy / price in years and convexity_analytic is
    d2price_dy2 / price in years squared, both with the unrounded price.
    """
    flows, rate = _cash_flows(instance)
    v = 1 / (1 + rate)
    price = sum(cash * v**t for t, cash in flows)
    first = -sum(t * cash * v ** (t + 1) for t, cash in flows)
    second = sum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)
    return {
        "dprice_dy": first,
        "d2price_dy2": second,
        "duration_analytic": -first / price,
        "convexity_analytic": second / price,
    }
