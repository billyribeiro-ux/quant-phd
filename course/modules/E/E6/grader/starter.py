"""Starter template for the E6 New Keynesian model solver (nk_solver.py).

Implement is_determinate, solve_undetermined, and impulse_responses.
"""

from __future__ import annotations

from typing import Any


def is_determinate(params: dict[str, Any]) -> bool:
    """Check whether the New Keynesian model equilibrium is determinate.

    Parameters
    ----------
    params : dict
        Dictionary containing:
        - 'beta': discount factor in (0, 1)
        - 'sigma': intertemporal elasticity / CRRA risk aversion > 0
        - 'kappa': slope of NK Phillips curve > 0
        - 'phi_pi': Taylor rule inflation coefficient >= 0
        - 'phi_y': Taylor rule output gap coefficient >= 0
        - 'rho': shock persistence with |rho| < 1

    Returns
    -------
    bool
        True if the equilibrium is determinate, False otherwise.

    Raises
    ------
    ValueError
        If any parameter violates its admissible domain.
    """
    raise NotImplementedError


def solve_undetermined(params: dict[str, Any], shock: str = "demand") -> tuple[float, float]:
    """Solve for the undetermined coefficients (b, a) of the New Keynesian model.

    The model equilibrium takes the form:
        x_t = b * u_t
        pi_t = a * u_t

    Parameters
    ----------
    params : dict
        Structural parameters of the model.
    shock : str, default 'demand'
        Type of shock: 'demand' (natural real rate shock) or 'policy' (monetary policy shock).

    Returns
    -------
    tuple[float, float]
        (b, a), where b is the output gap coefficient and a is the inflation coefficient.

    Raises
    ------
    ValueError
        If inputs are invalid or if the model is indeterminate.
    """
    raise NotImplementedError


def impulse_responses(params: dict[str, Any], horizon: int) -> dict[str, list[float]]:
    """Compute impulse response functions to a unit demand shock and a unit policy shock.

    Parameters
    ----------
    params : dict
        Structural parameters of the model.
    horizon : int
        Number of forward periods (dates 0, 1, ..., horizon).

    Returns
    -------
    dict[str, list[float]]
        Dictionary with keys:
        - 'date': list of integers [0, 1, ..., horizon]
        - 'x_demand': output gap path under demand shock
        - 'pi_demand': inflation path under demand shock
        - 'i_demand': nominal interest rate path under demand shock
        - 'x_policy': output gap path under policy shock
        - 'pi_policy': inflation path under policy shock
        - 'i_policy': nominal interest rate path under policy shock

    Raises
    ------
    ValueError
        If inputs are invalid, horizon is negative/non-integer, or model is indeterminate.
    """
    raise NotImplementedError
