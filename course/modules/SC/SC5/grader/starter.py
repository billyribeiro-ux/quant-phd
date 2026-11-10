"""Starter template for the SC5 project: Lévy model calibration engine, levy_calibration.py.

Implement each function according to the project specification in project.html.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def merton_characteristic_function(
    u: complex | np.ndarray,
    t: float,
    spot: float,
    r: float,
    sigma: float,
    lam: float,
    mu_j: float,
    sigma_j: float,
) -> complex | np.ndarray:
    """Evaluate the risk-neutral characteristic function E[exp(i*u*ln(S_t))] under Merton's jump-diffusion model."""
    raise NotImplementedError("Implement merton_characteristic_function")


def vg_characteristic_function(
    u: complex | np.ndarray,
    t: float,
    spot: float,
    r: float,
    sigma: float,
    nu: float,
    theta: float,
) -> complex | np.ndarray:
    """Evaluate the risk-neutral characteristic function E[exp(i*u*ln(S_t))] under the Variance Gamma model."""
    raise NotImplementedError("Implement vg_characteristic_function")


def price_european_option(
    spot: float,
    strike: float,
    tenor: float,
    r: float,
    model: str,
    params: dict[str, float],
    is_call: bool = True,
) -> float:
    """Price a European option using Fourier inversion under the specified Lévy model ('merton' or 'vg')."""
    raise NotImplementedError("Implement price_european_option")


def implied_volatility(
    price: float,
    spot: float,
    strike: float,
    tenor: float,
    r: float,
    is_call: bool = True,
) -> float:
    """Invert Black-Scholes formula to recover implied volatility from European option price."""
    raise NotImplementedError("Implement implied_volatility")


def calibrate_model(
    market_surface: list[dict[str, Any]],
    model: str,
    spot: float,
    r: float,
    initial_guess: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Calibrate model parameters ('merton' or 'vg') to market option surface via nonlinear least-squares."""
    raise NotImplementedError("Implement calibrate_model")
