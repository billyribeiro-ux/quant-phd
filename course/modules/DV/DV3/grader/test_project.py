"""Test suite for DV3: Stochastic & Rough Volatility (rough_volatility.py).

Tests property invariants, mathematical bounds, monotonicity, no-arbitrage bounds,
variogram structure function scaling, noise-corrected Hurst estimation, and input validation
across deterministic pseudorandom seeds.
"""

from __future__ import annotations

import math
from typing import Any

import pytest
from instance import make_instance
from reference import (
    atmi_skew_term_structure,
    bergomi_forward_variance,
    compute_variogram,
    estimate_hurst_exponent,
    estimate_hurst_noise_corrected,
    heston_call_price,
    sabr_implied_volatility,
)


@pytest.fixture(scope="module")
def instance() -> dict[str, Any]:
    return make_instance(seed=0)


def test_heston_call_price_bounds_and_monotonicity(instance: dict[str, Any]) -> None:
    """Test no-arbitrage bounds and strike monotonicity for Heston call prices."""
    spot = float(instance["spot"])
    rate = float(instance["rate"])
    v0 = float(instance["heston_v0"])
    kappa = float(instance["heston_kappa"])
    theta = float(instance["heston_theta"])
    xi = float(instance["heston_xi"])
    rho = float(instance["heston_rho"])

    maturities = [0.10, 0.50, 1.00]
    strikes = [spot * factor for factor in [0.70, 0.85, 1.00, 1.15, 1.30]]

    for t in maturities:
        prices: list[float] = []
        for k in strikes:
            call = heston_call_price(spot, k, t, rate, v0, kappa, theta, xi, rho)
            intrinsic = max(0.0, spot - k * math.exp(-rate * t))
            # No-arbitrage lower and upper bounds
            assert call >= intrinsic - 1e-4, f"Call price {call} violates intrinsic bound {intrinsic}"
            assert call <= spot + 1e-4, f"Call price {call} exceeds spot price {spot}"
            prices.append(call)

        # Monotonicity in strike: call prices must strictly decrease with K
        for i in range(len(prices) - 1):
            assert prices[i] > prices[i + 1], (
                f"Call prices must decrease with strike: K={strikes[i]} vs K={strikes[i + 1]}"
            )


def test_heston_stable_trap_feller(instance: dict[str, Any]) -> None:
    """Test that Heston pricing produces finite, positive values across extreme maturities."""
    spot = float(instance["spot"])
    rate = float(instance["rate"])
    v0 = float(instance["heston_v0"])
    kappa = float(instance["heston_kappa"])
    theta = float(instance["heston_theta"])
    xi = float(instance["heston_xi"])
    rho = float(instance["heston_rho"])

    # Test short and long maturities to verify branch stability ('Little Heston Trap')
    for t in [0.02, 0.05, 0.50, 2.00, 5.00, 10.00]:
        call = heston_call_price(spot, spot, t, rate, v0, kappa, theta, xi, rho)
        assert math.isfinite(call), f"Non-finite call price for maturity T={t}"
        assert call > 0.0, f"Call price must be strictly positive for ATM at T={t}"

    # For T=10, verify accuracy against the stable branch formulation (kills unstable branch cut)
    call_long = heston_call_price(100.0, 100.0, 10.0, 0.03, 0.04, 2.0, 0.04, 0.5, -0.7)
    assert abs(call_long - 36.7742) < 1.0, f"Long maturity call {call_long} shows Little Heston Trap instability"


def test_sabr_implied_volatility_properties(instance: dict[str, Any]) -> None:
    """Test SABR formula properties: positivity, ATM limit, and negative skew."""
    spot = float(instance["spot"])
    alpha = float(instance["sabr_alpha"])
    beta = float(instance["sabr_beta"])
    rho = float(instance["sabr_rho"])
    nu = float(instance["sabr_nu"])

    t = 1.0
    k_atm = spot
    k_down = spot * 0.85
    k_up = spot * 1.15

    iv_atm = sabr_implied_volatility(spot, k_atm, t, alpha, beta, rho, nu)
    iv_down = sabr_implied_volatility(spot, k_down, t, alpha, beta, rho, nu)
    iv_up = sabr_implied_volatility(spot, k_up, t, alpha, beta, rho, nu)

    assert iv_atm > 0.0, f"ATM SABR implied vol must be positive, got {iv_atm}"
    assert iv_down > 0.0, f"Down strike SABR vol must be positive, got {iv_down}"
    assert iv_up > 0.0, f"Up strike SABR vol must be positive, got {iv_up}"

    # For negative rho < 0 and equity beta, IV(K_down) > IV(K_up)
    if rho < -0.1:
        assert iv_down > iv_up, (
            f"Negative correlation rho={rho} must generate downward skew: iv_down={iv_down} vs iv_up={iv_up}"
        )


def test_bergomi_forward_variance(instance: dict[str, Any]) -> None:
    """Test Bergomi forward variance dynamics: positivity, base curve match, and driver response."""
    fwd_curve: list[tuple[float, float]] = [(float(tenor), float(val)) for tenor, val in instance["forward_curve"]]
    omega = float(instance["bergomi_omega"])
    kappa = float(instance["bergomi_kappa"])

    # At t=0, driver w_t=0 must return initial curve value xi_0(0)
    v_init = bergomi_forward_variance(0.0, fwd_curve, omega, kappa, w_t=0.0)
    assert abs(v_init - fwd_curve[0][1]) < 1e-6, f"At t=0, v(0) must equal xi_0(0)={fwd_curve[0][1]}, got {v_init}"

    # Positivity under positive and negative driver realizations
    v_up = bergomi_forward_variance(0.50, fwd_curve, omega, kappa, w_t=1.0)
    v_down = bergomi_forward_variance(0.50, fwd_curve, omega, kappa, w_t=-1.0)
    assert v_up > 0.0, f"Bergomi forward variance must be positive: got {v_up}"
    assert v_down > 0.0, f"Bergomi forward variance must be positive: got {v_down}"
    assert v_up > v_down, f"Forward variance must monotonically increase with driver w_t: {v_up} vs {v_down}"


def test_compute_variogram_invariants(instance: dict[str, Any]) -> None:
    """Test variogram calculation: positivity, quadratic scaling on known series, and monotonic growth."""
    clean_series = [float(x) for x in instance["clean_log_rv"]]
    lags = [int(lag_val) for lag_val in instance["lags"]]

    # Deterministic test on synthetic linear series [0, 2, 4, 6] with increment Delta=2
    # m(q=2, 1) = |2|^2 = 4.0 (kills mutants that omit power q)
    test_lin = [0.0, 2.0, 4.0, 6.0]
    vario_lin = compute_variogram(test_lin, [1], q=2.0)
    assert abs(vario_lin[1] - 4.0) < 1e-6, f"Variogram must scale with power q=2: expected 4.0, got {vario_lin[1]}"

    vario = compute_variogram(clean_series, lags, q=2.0)
    assert len(vario) == len(lags), f"Variogram must return values for all requested lags ({len(lags)})"

    for lag in lags:
        assert vario[lag] > 0.0, f"Variogram value for lag {lag} must be strictly positive"

    # For a fractional process, variogram generally increases from lag 1 to lag 20
    assert vario[lags[-1]] > vario[lags[0]], f"Variogram must increase with lag: {vario[lags[0]]} to {vario[lags[-1]]}"


def test_estimate_hurst_exponent_bounds(instance: dict[str, Any]) -> None:
    """Test that estimated Hurst parameter falls within the rough volatility regime (0, 0.50)."""
    clean_series = [float(x) for x in instance["clean_log_rv"]]
    lags = [int(lag_val) for lag_val in instance["lags"]]
    true_h = float(instance["true_h"])

    h_est = estimate_hurst_exponent(clean_series, lags, q=2.0)
    assert 0.0 < h_est < 0.50, f"Estimated H must lie in the rough regime (0, 0.5), got {h_est}"
    # Verify reasonable proximity to true H on clean simulated series (within 0.15)
    assert abs(h_est - true_h) < 0.15, f"Estimated H={h_est} deviates too far from true H={true_h}"

    # Monofractal self-similarity: estimate with q=1 and q=2 must agree closely (kills slope/q omission)
    h_q1 = estimate_hurst_exponent(clean_series, lags, q=1.0)
    assert abs(h_q1 - h_est) < 0.05, f"Hurst estimate must be independent of q: q=1 ({h_q1}) vs q=2 ({h_est})"


def test_noise_corrected_hurst_estimation(instance: dict[str, Any]) -> None:
    """Test that noise-corrected estimator yields positive noise variance and valid H."""
    noisy_series = [float(x) for x in instance["noisy_log_rv"]]
    lags = [int(lag_val) for lag_val in instance["lags"]]

    h_naive = estimate_hurst_exponent(noisy_series, lags, q=2.0)
    h_hat, noise_var = estimate_hurst_noise_corrected(noisy_series, lags, q=2.0, min_lag=4)
    assert 0.0 < h_hat < 0.50, f"Noise-corrected H must lie in (0, 0.5), got {h_hat}"
    assert noise_var >= 0.0, f"Estimated noise variance must be non-negative, got {noise_var}"

    # Truncating noise-contaminated lags must shift the estimated H relative to naive OLS
    assert abs(h_hat - h_naive) > 0.005, (
        f"Noise correction excluding small lags must correct the naive slope: h_corr={h_hat} vs h_naive={h_naive}"
    )


def test_atmi_skew_power_law(instance: dict[str, Any]) -> None:
    """Test rBergomi ATMI skew term structure: negative sign, short-dated explosion."""
    maturities = [0.01, 0.05, 0.25, 1.00]
    h = 0.12
    eta = 1.90
    rho = -0.70

    skews = atmi_skew_term_structure(maturities, h, eta, rho)
    assert len(skews) == len(maturities)

    for sk in skews:
        assert sk < 0.0, f"ATMI skew must be negative for rho < 0, got {sk}"

    # Power law explosion: |skew(0.01)| > |skew(0.05)| > |skew(0.25)| > |skew(1.0)|
    for i in range(len(skews) - 1):
        assert abs(skews[i]) > abs(skews[i + 1]), (
            f"Short-dated skew must blow up as T -> 0: {skews[i]} vs {skews[i + 1]}"
        )


def test_input_validation() -> None:
    """Test input validation raising ValueError on invalid parameters."""
    with pytest.raises(ValueError):
        heston_call_price(-100.0, 100.0, 1.0, 0.03, 0.04, 2.0, 0.04, 0.3, -0.7)

    with pytest.raises(ValueError):
        heston_call_price(100.0, -100.0, 1.0, 0.03, 0.04, 2.0, 0.04, 0.3, -0.7)

    with pytest.raises(ValueError):
        heston_call_price(100.0, 100.0, 1.0, 0.03, 0.04, 2.0, 0.04, 0.3, -1.5)

    with pytest.raises(ValueError):
        sabr_implied_volatility(100.0, 100.0, 1.0, -0.5, 0.5, -0.3, 0.4)

    with pytest.raises(ValueError):
        sabr_implied_volatility(100.0, 100.0, 1.0, 0.5, 1.5, -0.3, 0.4)

    with pytest.raises(ValueError):
        compute_variogram([], [1, 2], q=2.0)

    with pytest.raises(ValueError):
        atmi_skew_term_structure([1.0], h=1.5, eta=1.9, rho=-0.7)
