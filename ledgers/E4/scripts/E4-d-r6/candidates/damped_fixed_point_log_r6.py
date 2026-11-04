"""Candidate (verifier round 6, extra to the five alternatives): damped fixed-point iteration on log(informed fraction).

The map u <- min(u + eta * gap(exp(u)), 0) is a damped fixed-point iteration whose fixed point is the root of the gap in
log(lam). It is taken on the log scale because the root can be as small as the noise volume allows. Convergence check:
|du| <= 1e-13 (relative to max(1, |u|)). Standard library only.
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


def solve_model(noise_sd: float, info_cost: float) -> dict[str, float]:
    sd, cost = _check(noise_sd, info_cost)
    g0 = _gap(0.0, sd, cost)
    g1 = _gap(1.0, sd, cost)
    if g0 <= 0.0:
        return {"informed_fraction": 0.0, "price_informativeness": 0.0, "indifference_gap": g0}
    if g1 >= 0.0:
        return {"informed_fraction": 1.0, "price_informativeness": _pi(1.0, sd), "indifference_gap": g1}
    u = math.log(0.5)
    eta = 1.0
    for _ in range(20000):
        lam = math.exp(u)
        g = _gap(lam, sd, cost)
        u_new = min(u + eta * g, 0.0)
        if abs(u_new - u) <= 1e-13 * max(1.0, abs(u)):
            u = u_new
            break
        u = u_new
    lam = math.exp(u)
    return {"informed_fraction": lam, "price_informativeness": _pi(lam, sd), "indifference_gap": _gap(lam, sd, cost)}
