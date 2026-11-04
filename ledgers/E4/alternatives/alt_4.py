"""Alternative 4: secant steps on the gap, safeguarded by the sign-change bracket, with a relative stop.

Correct alternative implementation of the E4 solver (ruling 10). Standard library only.
"""

from __future__ import annotations

import math

A = 2.0
TAU_V = 1.0
TAU_E = 1.0


def _check(noise_sd: float, info_cost: float) -> tuple[float, float]:
    sd = float(noise_sd)
    cost = float(info_cost)
    if not (math.isfinite(sd) and sd > 0.0):
        raise ValueError("noise volume must be positive")
    if not (math.isfinite(cost) and cost >= 0.0):
        raise ValueError("information cost must be nonnegative")
    return sd, cost


def _tau_y(lam: float, sd: float) -> float:
    return lam * lam * TAU_E * TAU_E / (lam * lam * TAU_E + A * A * sd * sd)


def _gap(lam: float, sd: float, cost: float) -> float:
    if lam == 0.0:
        fu0 = math.pow(1.0 + A * A * sd * sd / TAU_V, -0.5)
        fi0 = math.pow(1.0 + TAU_E / TAU_V + (TAU_V + TAU_E) * A * A * sd * sd / (TAU_V * TAU_V), -0.5)
        return fu0 - math.exp(A * cost) * fi0
    ty = _tau_y(lam, sd)
    denom = lam * (TAU_V + TAU_E) + (1.0 - lam) * (TAU_V + ty)
    bs = (lam * TAU_E + (1.0 - lam) * ty) / denom
    bu = -A * bs / (lam * TAU_E)
    r = ty / (TAU_V + ty) - bs
    fu = math.pow(1.0 + r * r * (TAU_V + ty) * (1.0 / TAU_V + 1.0 / ty), -0.5)
    prec = TAU_V + TAU_E
    slope = TAU_E / prec - bs
    varg = slope * slope * (1.0 / TAU_V + 1.0 / TAU_E) + bu * bu * sd * sd
    fi = math.pow(1.0 + prec * varg, -0.5)
    return fu - math.exp(A * cost) * fi


def _pi(lam: float, sd: float) -> float:
    if lam == 0.0:
        return 0.0
    ty = _tau_y(lam, sd)
    return ty / (TAU_V + ty)


def _boundary(sd: float, cost: float) -> tuple[float, float, float] | None:
    g0 = _gap(0.0, sd, cost)
    g1 = _gap(1.0, sd, cost)
    if g0 <= 0.0:
        return 0.0, g0, _pi(0.0, sd)
    if g1 >= 0.0:
        return 1.0, g1, _pi(1.0, sd)
    return None


def _result(lam: float, sd: float, cost: float) -> dict[str, float]:
    return {
        "informed_fraction": lam,
        "price_informativeness": _pi(lam, sd),
        "indifference_gap": _gap(lam, sd, cost),
    }


def solve_model(noise_sd: float, info_cost: float) -> dict[str, float]:
    sd, cost = _check(noise_sd, info_cost)
    edge = _boundary(sd, cost)
    if edge is not None:
        lam, gap, pi = edge
        return {"informed_fraction": lam, "price_informativeness": pi, "indifference_gap": gap}
    lo, hi = 0.0, 1.0
    f_lo, f_hi = _gap(lo, sd, cost), _gap(hi, sd, cost)  # the gap is positive at lo and negative at hi
    x_prev, f_prev = lo, f_lo
    x, fx = hi, f_hi
    for _ in range(200):
        cand = x - fx * (x - x_prev) / (fx - f_prev) if fx != f_prev else 0.5 * (lo + hi)
        if not lo < cand < hi:
            cand = 0.5 * (lo + hi)
        f_cand = _gap(cand, sd, cost)
        if f_cand > 0.0:
            lo, f_lo = cand, f_cand
        else:
            hi, f_hi = cand, f_cand
        x_prev, f_prev = x, fx
        x, fx = cand, f_cand
        if abs(x - x_prev) <= 1e-13 * x:
            break
    return _result(x, sd, cost)
