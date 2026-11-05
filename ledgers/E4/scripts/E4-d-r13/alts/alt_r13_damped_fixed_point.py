"""Alternative (round 13, verifier): damped fixed-point iteration with Aitken acceleration on the informed fraction.

Plan section 5.5 item 4. The map is the sign rule of Proposition 3 solved for lam: tau_y(lam) = tau_bar. Standard library only.
"""

from __future__ import annotations

import math

A = 2.0
TAU_V = 1.0
TAU_E = 1.0
OMEGA = 0.5  # damping
MAX_ITER = 10_000


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


def _map(lam: float, tau_bar: float, sd: float) -> float:
    """T(lam) = sqrt(tau_bar (lam^2 tau_e + a^2 sd^2)) / tau_e: the fixed points of T solve tau_y(lam) = tau_bar."""
    return math.sqrt(tau_bar * (lam * lam * TAU_E + A * A * sd * sd)) / TAU_E


def solve_model(noise_sd: float, info_cost: float) -> dict[str, float]:
    sd, cost = _check(noise_sd, info_cost)
    g0, g1 = _gap(0.0, sd, cost), _gap(1.0, sd, cost)
    if g0 <= 0.0:
        return {"informed_fraction": 0.0, "price_informativeness": 0.0, "indifference_gap": g0}
    if g1 >= 0.0:
        return {"informed_fraction": 1.0, "price_informativeness": _pi(1.0, sd), "indifference_gap": g1}
    tau_bar = (TAU_V + TAU_E) * math.exp(-2.0 * A * cost) - TAU_V
    lam = 0.5
    history: list[float] = []
    for _ in range(MAX_ITER):
        damped = (1.0 - OMEGA) * lam + OMEGA * _map(lam, tau_bar, sd)
        history.append(damped)
        if len(history) >= 3:
            x0, x1, x2 = history[-3], history[-2], history[-1]
            denom = x2 - 2.0 * x1 + x0
            if denom != 0.0:
                accel = x2 - (x2 - x1) ** 2 / denom
                if 0.0 < accel < 1.0:
                    damped = accel
                    history[-1] = accel
        if abs(damped - lam) <= 1e-13 * damped:
            lam = damped
            break
        lam = damped
    gap = _gap(lam, sd, cost)
    return {"informed_fraction": lam, "price_informativeness": _pi(lam, sd), "indifference_gap": gap}
