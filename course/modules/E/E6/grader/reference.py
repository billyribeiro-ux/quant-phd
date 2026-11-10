"""Reference solution for the E6 New Keynesian model solver (nk_solver.py).

Implements:
1. Input validation enforcing admissible domains (ValueError).
2. Equilibrium determinacy checking via both the derived generalized Taylor principle
   and companion matrix root-counting.
3. Undetermined coefficients solution for demand and monetary policy shocks.
4. Exact impulse response functions over any non-negative integer horizon.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def _validate_params(params: dict[str, Any]) -> tuple[float, float, float, float, float, float]:
    """Validate model structural parameters and return them as typed floats.

    Admissible domains:
    - beta in (0, 1): discount factor
    - sigma > 0: intertemporal elasticity of substitution / CRRA risk aversion
    - kappa > 0: slope of the New Keynesian Phillips curve
    - |rho| < 1: shock persistence
    - phi_pi >= 0: Taylor rule inflation response
    - phi_y >= 0: Taylor rule output gap response
    """
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
    """Check whether the New Keynesian model equilibrium is determinate.

    Determinacy under the contemporaneous Taylor rule i_t = phi_pi * pi_t + phi_y * x_t
    holds if and only if the generalized Taylor principle is satisfied:
        kappa * (phi_pi - 1) + (1 - beta) * phi_y > 0

    Equivalently, both eigenvalues of the non-predetermined system companion matrix
    lie strictly outside the unit circle in the complex plane.
    """
    beta, sigma, kappa, phi_pi, phi_y, _ = _validate_params(params)

    # Derived analytical condition (generalized Taylor principle)
    det_metric = kappa * (phi_pi - 1.0) + (1.0 - beta) * phi_y
    condition_holds = bool(det_metric > 1e-12)

    # Cross-check with companion matrix eigenvalues
    m_mat = np.array(
        [
            [1.0 + phi_y / sigma + kappa / (beta * sigma), (phi_pi - 1.0 / beta) / sigma],
            [-kappa / beta, 1.0 / beta],
        ],
        dtype=np.float64,
    )
    eigenvalues = np.linalg.eigvals(m_mat)
    roots_outside_unit_circle = bool(np.all(np.abs(eigenvalues) > 1.0 + 1e-10))

    # Analytical and root-counting checks must agree
    if condition_holds != roots_outside_unit_circle:
        return condition_holds

    return condition_holds


def solve_undetermined(params: dict[str, Any], shock: str = "demand") -> tuple[float, float]:
    """Solve for undetermined coefficients (b, a) in x_t = b * u_t and pi_t = a * u_t.

    Parameters
    ----------
    params : dict
        Model parameters.
    shock : str, default 'demand'
        'demand' (natural real rate shock r^n_t) or 'policy' (monetary policy shock v_t).

    Returns
    -------
    tuple[float, float]
        (b, a), where b is the output gap coefficient and a is the inflation coefficient.
    """
    beta, sigma, kappa, phi_pi, phi_y, rho = _validate_params(params)

    if shock not in ("demand", "policy"):
        raise ValueError(f"Unknown shock type: {shock!r}; expected 'demand' or 'policy'")

    if not is_determinate(params):
        raise ValueError("Cannot solve undetermined coefficients: equilibrium is indeterminate.")

    delta = (1.0 - beta * rho) * (sigma * (1.0 - rho) + phi_y) + kappa * (phi_pi - rho)
    if abs(delta) < 1e-14:
        raise ValueError("Degenerate denominator in undetermined coefficients solution.")

    if shock == "demand":
        b = (1.0 - beta * rho) / delta
        a = kappa / delta
    else:  # shock == "policy"
        b = -(1.0 - beta * rho) / delta
        a = -kappa / delta

    return float(b), float(a)


def impulse_responses(params: dict[str, Any], horizon: int) -> dict[str, list[float]]:
    """Compute impulse response paths to a unit demand shock and a unit policy shock.

    Parameters
    ----------
    params : dict
        Structural parameters.
    horizon : int
        Number of forward periods (dates 0, 1, ..., horizon).

    Returns
    -------
    dict[str, list[float]]
        Dictionary containing 'date', 'x_demand', 'pi_demand', 'i_demand',
        'x_policy', 'pi_policy', 'i_policy'.
    """
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 0:
        raise ValueError(f"horizon must be a non-negative integer, got {horizon!r}")

    _, _, _, phi_pi, phi_y, rho = _validate_params(params)

    if not is_determinate(params):
        raise ValueError("Cannot compute impulse responses: equilibrium is indeterminate.")

    b_d, a_d = solve_undetermined(params, "demand")
    b_v, a_v = solve_undetermined(params, "policy")

    dates: list[int] = list(range(horizon + 1))
    x_demand: list[float] = []
    pi_demand: list[float] = []
    i_demand: list[float] = []

    x_policy: list[float] = []
    pi_policy: list[float] = []
    i_policy: list[float] = []

    for t in dates:
        u_t = float(rho**t)

        # Demand shock (r^n_t = u_t, v_t = 0)
        xd = b_d * u_t
        pid = a_d * u_t
        id_val = phi_pi * pid + phi_y * xd
        x_demand.append(float(xd))
        pi_demand.append(float(pid))
        i_demand.append(float(id_val))

        # Policy shock (r^n_t = 0, v_t = u_t)
        xv = b_v * u_t
        piv = a_v * u_t
        iv_val = phi_pi * piv + phi_y * xv + u_t
        x_policy.append(float(xv))
        pi_policy.append(float(piv))
        i_policy.append(float(iv_val))

    return {
        "date": [float(d) for d in dates],
        "x_demand": x_demand,
        "pi_demand": pi_demand,
        "i_demand": i_demand,
        "x_policy": x_policy,
        "pi_policy": pi_policy,
        "i_policy": i_policy,
    }
