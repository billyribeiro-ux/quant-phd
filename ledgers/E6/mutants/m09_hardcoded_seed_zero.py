"""Mutant m09: Hardcoded output for seed 0 returned on all inputs.

Ignores the actual parameters passed and returns static results computed for seed 0.
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
    # Mutant bug: always True (hardcoded seed 0 is determinate)
    return True


def solve_undetermined(params: dict[str, Any], shock: str = "demand") -> tuple[float, float]:
    _validate_params(params)
    # Mutant bug: hardcoded seed 0 coefficients
    if shock == "demand":
        return 0.394138417030721, 0.09638981750723037
    return -0.394138417030721, -0.09638981750723037


def impulse_responses(params: dict[str, Any], horizon: int) -> dict[str, list[float]]:
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 0:
        raise ValueError("Invalid horizon")
    _validate_params(params)
    b_d, a_d = 0.394138417030721, 0.09638981750723037
    b_v, a_v = -0.394138417030721, -0.09638981750723037
    phi_pi = 1.861
    phi_y = 0.338
    rho = -0.313
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
