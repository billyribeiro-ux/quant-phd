"""Mutant m01: Determinacy check ignores the output gap response in the Taylor principle.

Only checks phi_pi > 1.0, omitting (1 - beta) * phi_y / kappa.
"""

from __future__ import annotations

import math
from typing import Any


def _validate_params(params: dict[str, Any]) -> tuple[float, float, float, float, float, float]:
    for key in ("beta", "sigma", "kappa", "phi_pi", "phi_y", "rho"):
        if key not in params:
            raise ValueError(f"Missing required parameter: {key}")
    try:
        beta = float(params["beta"])
        sigma = float(params["sigma"])
        kappa = float(params["kappa"])
        phi_pi = float(params["phi_pi"])
        phi_y = float(params["phi_y"])
        rho = float(params["rho"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Parameters must be numeric: {exc}") from exc

    if math.isnan(beta) or beta <= 0.0 or beta >= 1.0:
        raise ValueError(f"beta must be strictly between 0 and 1, got {beta}")
    if math.isnan(sigma) or sigma <= 0.0:
        raise ValueError(f"sigma must be strictly positive, got {sigma}")
    if math.isnan(kappa) or kappa <= 0.0:
        raise ValueError(f"kappa must be strictly positive, got {kappa}")
    if math.isnan(rho) or abs(rho) >= 1.0:
        raise ValueError(f"|rho| must be strictly less than 1, got {rho}")
    if math.isnan(phi_pi) or phi_pi < 0.0:
        raise ValueError(f"phi_pi must be non-negative, got {phi_pi}")
    if math.isnan(phi_y) or phi_y < 0.0:
        raise ValueError(f"phi_y must be non-negative, got {phi_y}")
    return beta, sigma, kappa, phi_pi, phi_y, rho


def is_determinate(params: dict[str, Any]) -> bool:
    _validate_params(params)
    # Mutant bug: ignores output gap stabilization
    return bool(float(params["phi_pi"]) > 1.0)


def solve_undetermined(params: dict[str, Any], shock: str = "demand") -> tuple[float, float]:
    beta, sigma, kappa, phi_pi, phi_y, rho = _validate_params(params)
    if shock not in ("demand", "policy"):
        raise ValueError(f"Unknown shock type: {shock!r}")
    if not is_determinate(params):
        raise ValueError("Cannot solve undetermined coefficients: equilibrium is indeterminate.")
    delta = (1.0 - beta * rho) * (sigma * (1.0 - rho) + phi_y) + kappa * (phi_pi - rho)
    if shock == "demand":
        return float((1.0 - beta * rho) / delta), float(kappa / delta)
    return float(-(1.0 - beta * rho) / delta), float(-kappa / delta)


def impulse_responses(params: dict[str, Any], horizon: int) -> dict[str, list[float]]:
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 0:
        raise ValueError("Invalid horizon")
    _, _, _, phi_pi, phi_y, rho = _validate_params(params)
    if not is_determinate(params):
        raise ValueError("Cannot compute impulse responses: equilibrium is indeterminate.")
    b_d, a_d = solve_undetermined(params, "demand")
    b_v, a_v = solve_undetermined(params, "policy")
    dates = list(range(horizon + 1))
    xd, pid, id_path = [], [], []
    xv, piv, iv_path = [], [], []
    for t in dates:
        u_t = float(rho**t)
        xd.append(b_d * u_t)
        pid.append(a_d * u_t)
        id_path.append(phi_pi * (a_d * u_t) + phi_y * (b_d * u_t))
        xv.append(b_v * u_t)
        piv.append(a_v * u_t)
        iv_path.append(phi_pi * (a_v * u_t) + phi_y * (b_v * u_t) + u_t)
    return {
        "date": [float(d) for d in dates],
        "x_demand": xd,
        "pi_demand": pid,
        "i_demand": id_path,
        "x_policy": xv,
        "pi_policy": piv,
        "i_policy": iv_path,
    }
