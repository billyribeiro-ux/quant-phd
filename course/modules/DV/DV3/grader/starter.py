"""Starter code for DV3: Stochastic & Rough Volatility (rough_volatility.py).

Implement all required functions according to the specifications in project.html.
All functions must raise ValueError on degenerate or invalid inputs.
"""

from __future__ import annotations


def heston_call_price(
    spot: float,
    strike: float,
    maturity: float,
    rate: float,
    v0: float,
    kappa: float,
    theta: float,
    xi: float,
    rho: float,
) -> float:
    """European call price in the Heston model via Fourier inversion."""
    raise NotImplementedError("TODO: Implement heston_call_price with stable branch cut.")


def sabr_implied_volatility(
    forward: float,
    strike: float,
    maturity: float,
    alpha: float,
    beta: float,
    rho: float,
    nu: float,
) -> float:
    """Hagan et al. asymptotic formula for SABR implied volatility."""
    raise NotImplementedError("TODO: Implement sabr_implied_volatility.")


def bergomi_forward_variance(
    t: float,
    forward_curve: list[tuple[float, float]],
    omega: float,
    kappa: float,
    w_t: float,
) -> float:
    """Evaluate 1-factor Bergomi instantaneous forward variance xi_t(t)."""
    raise NotImplementedError("TODO: Implement bergomi_forward_variance.")


def compute_variogram(
    log_rv_series: list[float],
    lags: list[int],
    q: float = 2.0,
) -> dict[int, float]:
    """Compute empirical q-th order structure function m(q, Delta) = E[|X_{t+Delta} - X_t|^q]."""
    raise NotImplementedError("TODO: Implement compute_variogram.")


def estimate_hurst_exponent(
    log_rv_series: list[float],
    lags: list[int],
    q: float = 2.0,
) -> float:
    """Estimate Hurst exponent H via OLS regression of log m(q, Delta) vs log Delta."""
    raise NotImplementedError("TODO: Implement estimate_hurst_exponent.")


def estimate_hurst_noise_corrected(
    log_rv_series: list[float],
    lags: list[int],
    q: float = 2.0,
    min_lag: int = 4,
) -> tuple[float, float]:
    """Estimate noise-corrected Hurst exponent H and estimated noise variance sigma_eps^2."""
    raise NotImplementedError("TODO: Implement estimate_hurst_noise_corrected.")


def atmi_skew_term_structure(
    maturities: list[float],
    h: float,
    eta: float,
    rho: float,
) -> list[float]:
    """Theoretical leading-order rBergomi ATMI skew term structure."""
    raise NotImplementedError("TODO: Implement atmi_skew_term_structure.")
