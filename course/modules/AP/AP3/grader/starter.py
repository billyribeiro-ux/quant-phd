"""Starter template for AP3 project: Euler-Equation GMM & Hansen-Jagannathan Engine.

Implement each function below according to the specification.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def euler_residuals(
    params: tuple[float, float],
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
) -> np.ndarray:
    """Compute nonlinear consumption Euler equation pricing errors.

    u_{t+1, i}(beta, gamma) = beta * (c_{t+1} / c_t)^{-gamma} * R_{i, t+1} - 1.0
    """
    raise NotImplementedError("euler_residuals is not yet implemented")


def sample_moments(
    params: tuple[float, float],
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
    instruments: np.ndarray,
) -> np.ndarray:
    """Compute empirical moment conditions g_T(beta, gamma) = (1/T) sum_t (u_t (x) z_t)."""
    raise NotImplementedError("sample_moments is not yet implemented")


def spectral_covariance(residuals_kron: np.ndarray) -> np.ndarray:
    """Compute the zero-lag spectral covariance matrix S_T = (1/T) * H^T * H."""
    raise NotImplementedError("spectral_covariance is not yet implemented")


def gmm_objective(
    params: tuple[float, float],
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
    instruments: np.ndarray,
    weight_matrix: np.ndarray,
) -> float:
    """Compute the quadratic GMM criterion J_T(theta) = g_T(theta)^T * W * g_T(theta)."""
    raise NotImplementedError("gmm_objective is not yet implemented")


def gmm_gradient(
    params: tuple[float, float],
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
    instruments: np.ndarray,
    weight_matrix: np.ndarray,
) -> np.ndarray:
    """Compute the analytical gradient of the GMM objective: nabla J_T = 2 * G_T^T * W * g_T."""
    raise NotImplementedError("gmm_gradient is not yet implemented")


def estimate_gmm(
    c_growth: np.ndarray,
    gross_returns: np.ndarray,
    instruments: np.ndarray,
    initial_params: tuple[float, float] = (0.95, 2.0),
    two_step: bool = True,
) -> dict[str, Any]:
    """Perform two-step nonlinear GMM estimation of Hansen & Singleton (1982)."""
    raise NotImplementedError("estimate_gmm is not yet implemented")


def hansen_jagannathan_bound(
    gross_returns: np.ndarray,
    nu_grid: np.ndarray,
) -> np.ndarray:
    """Compute the Hansen-Jagannathan (1991) minimum SDF volatility frontier."""
    raise NotImplementedError("hansen_jagannathan_bound is not yet implemented")


def evaluate_consumption_sdf(
    beta: float,
    gamma: float,
    c_growth: np.ndarray,
) -> tuple[float, float]:
    """Compute the sample expectation and volatility of the power utility SDF M = beta * (c')^(-gamma)."""
    raise NotImplementedError("evaluate_consumption_sdf is not yet implemented")
