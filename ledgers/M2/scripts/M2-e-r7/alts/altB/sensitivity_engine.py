"""Alternative correct engine: Decimal bond maths at 400 digits, dual numbers as a tuple class, step-capped never."""

from __future__ import annotations

from collections.abc import Callable
from decimal import ROUND_HALF_EVEN, Context, Decimal
from typing import Any

CTX = Context(prec=400, rounding=ROUND_HALF_EVEN)


def _step(h: float) -> float:
    if not float(h) > 0:
        raise ValueError("the step must be above zero")
    return float(h)


def fd_derivative(f: Callable[[float], float], x: float, h: float, scheme: str) -> float:
    s = _step(h)
    if scheme == "forward":
        return (f(x + s) - f(x)) / s
    if scheme == "central":
        return (f(x + s) - f(x - s)) / (2.0 * s)
    raise ValueError("unknown scheme")


class _Dual:
    def __init__(self, a: float, b: float) -> None:
        self.a, self.b = a, b

    @staticmethod
    def lift(x: Any) -> _Dual:
        return x if isinstance(x, _Dual) else _Dual(float(x), 0.0)

    def __add__(self, o: Any) -> _Dual:
        o = _Dual.lift(o)
        return _Dual(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self) -> _Dual:
        return _Dual(-self.a, -self.b)

    def __sub__(self, o: Any) -> _Dual:
        return self + (-_Dual.lift(o))

    def __rsub__(self, o: Any) -> _Dual:
        return _Dual.lift(o) + (-self)

    def __mul__(self, o: Any) -> _Dual:
        o = _Dual.lift(o)
        return _Dual(self.a * o.a, self.a * o.b + self.b * o.a)

    __rmul__ = __mul__


def ad_derivative(f: Callable[[Any], Any], x: float) -> float:
    return float(_Dual.lift(f(_Dual(float(x), 1.0))).b)


def hessian_fd(f: Callable[[list[float]], float], x: list[float], h: float) -> list[list[float]]:
    s = _step(h)
    p = [float(v) for v in x]
    n = len(p)
    H = [[0.0] * n for _ in range(n)]

    def g(di: int, dj: int, si: float, sj: float) -> float:
        q = list(p)
        q[di] += si
        q[dj] += sj
        return f(q)

    for i in range(n):
        H[i][i] = (g(i, i, s, 0) - 2 * g(i, i, 0, 0) + g(i, i, -s, 0)) / (s * s)
        for j in range(i + 1, n):
            H[i][j] = H[j][i] = (g(i, j, s, s) - g(i, j, s, -s) - g(i, j, -s, s) + g(i, j, -s, -s)) / (4 * s * s)
    return H


def _parts(inst: dict[str, Any]) -> tuple[list[tuple[int, Decimal]], Decimal]:
    b = inst["yield_bps"]
    if b <= -10_000:
        raise ValueError("yield must be above -1")
    r = CTX.divide(Decimal(b), Decimal(10_000))
    face = Decimal(inst["face_cents"])
    coupon = CTX.divide(CTX.multiply(face, Decimal(inst["coupon_bps"])), Decimal(10_000))
    n = int(inst["maturity_years"])
    return [(t, coupon + (face if t == n else Decimal(0))) for t in range(1, n + 1)], r


def _v(r: Decimal, k: int) -> Decimal:
    base = CTX.divide(Decimal(1), CTX.add(Decimal(1), r))
    out = Decimal(1)
    for _ in range(k):
        out = CTX.multiply(out, base)
    return out


def bond_price_cents(inst: dict[str, Any]) -> int:
    flows, r = _parts(inst)
    total = sum((CTX.multiply(c, _v(r, t)) for t, c in flows), Decimal(0))
    return int(total.quantize(Decimal(1), rounding=ROUND_HALF_EVEN, context=CTX))


def sensitivities(inst: dict[str, Any]) -> dict[str, float]:
    flows, r = _parts(inst)
    price = sum((CTX.multiply(c, _v(r, t)) for t, c in flows), Decimal(0))
    first = -sum((CTX.multiply(CTX.multiply(Decimal(t), c), _v(r, t + 1)) for t, c in flows), Decimal(0))
    second = sum((CTX.multiply(CTX.multiply(Decimal(t * (t + 1)), c), _v(r, t + 2)) for t, c in flows), Decimal(0))
    return {
        "dprice_dy": float(first),
        "d2price_dy2": float(second),
        "duration_analytic": float(CTX.divide(-first, price)),
        "convexity_analytic": float(CTX.divide(second, price)),
    }
