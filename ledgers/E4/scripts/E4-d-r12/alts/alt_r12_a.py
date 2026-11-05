"""Alternative (round 12, verifier): no bisection. The closed-form root of Proposition 4 with the boundary rule, and the gap by the formulas of Proposition 3 at that root."""

from __future__ import annotations

import math

RISK_AVERSION = 2.0
TAU_V = 1.0
TAU_E = 1.0


def _check(noise_sd: float, info_cost: float) -> tuple[float, float]:
    sd, cost = float(noise_sd), float(info_cost)
    if not (math.isfinite(sd) and sd > 0.0):
        raise ValueError("noise volume must be positive")
    if not (math.isfinite(cost) and cost >= 0.0):
        raise ValueError("information cost must be nonnegative")
    return sd, cost


def _ty(lam: float, sd: float) -> float:
    return lam * lam * TAU_E * TAU_E / (lam * lam * TAU_E + RISK_AVERSION * RISK_AVERSION * sd * sd)


def _gap(lam: float, sd: float, cost: float) -> float:
    a = RISK_AVERSION
    if lam == 0.0:
        a2 = a * a * sd * sd
        return (1 + a2 / TAU_V) ** -0.5 - math.exp(a * cost) * (1 + TAU_E / TAU_V + (TAU_V + TAU_E) * a2 / TAU_V**2) ** -0.5
    ty = _ty(lam, sd)
    den = lam * (TAU_V + TAU_E) + (1 - lam) * (TAU_V + ty)
    bs = (lam * TAU_E + (1 - lam) * ty) / den
    bu = -a * bs / (lam * TAU_E)
    r = ty / (TAU_V + ty) - bs
    fu = (1 + r * r * (TAU_V + ty) * (1 / TAU_V + 1 / ty)) ** -0.5
    slope = TAU_E / (TAU_V + TAU_E) - bs
    vg = slope * slope * (1 / TAU_V + 1 / TAU_E) + bu * bu * sd * sd
    fi = (1 + (TAU_V + TAU_E) * vg) ** -0.5
    return fu - math.exp(a * cost) * fi


def solve_model(noise_sd: float, info_cost: float) -> dict[str, float]:
    sd, cost = _check(noise_sd, info_cost)
    tb = (TAU_V + TAU_E) * math.exp(-2.0 * RISK_AVERSION * cost) - TAU_V
    t1 = TAU_E * TAU_E / (TAU_E + RISK_AVERSION * RISK_AVERSION * sd * sd)
    if tb <= 0.0:
        lam = 0.0
    elif tb >= t1:
        lam = 1.0
    else:
        lam = RISK_AVERSION * sd * math.sqrt(tb / (TAU_E * (TAU_E - tb)))
    gap = _gap(lam, sd, cost)
    pi = 0.0 if lam == 0.0 else _ty(lam, sd) / (TAU_V + _ty(lam, sd))
    return {"informed_fraction": float(lam), "price_informativeness": float(pi), "indifference_gap": float(gap)}
