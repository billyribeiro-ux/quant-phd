"""Alternative 1: bisection with a relative bracket width of 1e-12, or at most 240 halvings.

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
    halvings = 0
    while hi - lo > 1e-12 * hi and halvings < 240:
        mid = 0.5 * (lo + hi)
        if _gap(mid, sd, cost) > 0.0:
            lo = mid
        else:
            hi = mid
        halvings += 1
    return _result(0.5 * (lo + hi), sd, cost)
