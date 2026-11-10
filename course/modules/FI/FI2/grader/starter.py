"""Starter template for FI2: Affine term-structure model calibration.

Implement the required functions to satisfy the test suite.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def solve_riccati_ode(
    tau: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Solve the Duffie-Kan Riccati ODE system for a 3-factor Gaussian ATSM."""
    raise NotImplementedError("solve_riccati_ode not implemented")


def yield_loadings(
    tau: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute yield intercept a(tau) and factor loadings H(tau)."""
    raise NotImplementedError("yield_loadings not implemented")


def compute_unconditional_moments(
    c: np.ndarray,
    phi: np.ndarray,
    q_cov: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute unconditional mean and covariance of discrete VAR(1) state process."""
    raise NotImplementedError("compute_unconditional_moments not implemented")


def kalman_filter(
    yields: np.ndarray,
    tau: np.ndarray,
    delta0: float,
    kappa: np.ndarray,
    sigma: np.ndarray,
    c: np.ndarray,
    phi: np.ndarray,
    q_cov: np.ndarray,
    r_diag: np.ndarray,
) -> dict[str, Any]:
    """Run Kalman filter on zero-coupon yields to evaluate log-likelihood and filtered states."""
    raise NotImplementedError("kalman_filter not implemented")


def kalman_log_likelihood(
    params: np.ndarray,
    yields: np.ndarray,
    tau: np.ndarray,
    c: np.ndarray,
    phi: np.ndarray,
    q_cov: np.ndarray,
    r_diag: np.ndarray,
) -> float:
    """Evaluate Kalman log-likelihood for parameter vector."""
    raise NotImplementedError("kalman_log_likelihood not implemented")


def calibrate_mle(
    yields: np.ndarray,
    tau: np.ndarray,
    initial_params: np.ndarray | None = None,
) -> dict[str, Any]:
    """Calibrate 3-factor Gaussian ATSM parameters by Kalman-filter MLE."""
    raise NotImplementedError("calibrate_mle not implemented")
