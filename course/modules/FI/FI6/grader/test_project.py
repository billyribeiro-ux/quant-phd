"""Acceptance test suite for FI6 Swaption-Cube Engine autograded project.

Tests multi-curve cash-flow discounting, Black-76 and Bachelier normal models,
SABR asymptotic expansion properties and calibration, 2D parameter interpolation,
Breeden-Litzenberger risk-neutral density non-negativity, and off-grid pricing with Greeks.
"""

from __future__ import annotations

import math
import os
from typing import Any

import pytest
from instance import make_instance, unpack_market_grid
from swaption_cube import (
    MultiCurveDiscounting,
    SwaptionCubeEngine,
    bachelier_swaption,
    black76_swaption,
    calibrate_sabr_slice,
    sabr_black_vol,
)

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
MARKET_GRID: dict[str, Any] = unpack_market_grid(INST)


@pytest.fixture
def multi_curve() -> MultiCurveDiscounting:
    """Fixture providing initialized multi-curve framework."""
    return MultiCurveDiscounting(
        tenors=INST["tenors"],
        ois_zero_rates=INST["ois_zero_rates"],
        proj_zero_rates=INST["proj_zero_rates"],
    )


@pytest.fixture
def calibrated_engine(multi_curve: MultiCurveDiscounting) -> SwaptionCubeEngine:
    """Fixture providing calibrated SwaptionCubeEngine."""
    engine = SwaptionCubeEngine(
        curve=multi_curve,
        grid_expiries=INST["grid_expiries"],
        grid_tenors=INST["grid_tenors"],
        beta=0.5,
    )
    engine.calibrate_cube(MARKET_GRID)
    return engine


def test_multi_curve_discounting_invariants(multi_curve: MultiCurveDiscounting) -> None:
    """Check multi-curve discounting and forwarding properties."""
    # 1. Monotonic discount factors
    prev_df = 1.0
    for t in [0.5, 1.0, 2.0, 5.0, 10.0]:
        df = multi_curve.discount_factor(t)
        assert 0.0 < df < prev_df, f"Discount factors must strictly decrease with tenor: {df} >= {prev_df}"
        prev_df = df

    # 2. Positive forward basis spread: P_F(0, T) < P_D(0, T)
    for t in [1.0, 5.0, 10.0]:
        df_ois = multi_curve.discount_factor(t)
        df_proj = multi_curve.projection_factor(t)
        assert df_proj < df_ois, (
            f"Projection factor must be lower than OIS discount factor due to basis spread: {df_proj} >= {df_ois}"
        )

    # 3. Swap annuity formula: A(0) = sum(tau * P_D(0, T_k))
    annuity_5y = multi_curve.swap_annuity(texp=1.0, tenor=5.0, tau=0.5)
    expected_annuity = sum(0.5 * multi_curve.discount_factor(1.0 + 0.5 * k) for k in range(1, 11))
    assert math.isclose(annuity_5y, expected_annuity, rel_tol=1e-6), (
        f"Swap annuity {annuity_5y} must match sum of discount factors {expected_annuity}"
    )

    # 4. Forward swap rate consistency
    s_fwd = multi_curve.forward_swap_rate(texp=1.0, tenor=5.0, tau=0.5)
    assert 0.01 <= s_fwd <= 0.15, f"Forward swap rate {s_fwd} outside economic bounds [1%, 15%]"


def test_bachelier_and_black76_pricing_and_parity(multi_curve: MultiCurveDiscounting) -> None:
    """Test Black-76 and Bachelier normal pricing, parity, and negative rate handling."""
    fwd = 0.0400
    strike = 0.0425
    annuity = multi_curve.swap_annuity(texp=1.0, tenor=5.0)
    texp = 1.0
    vol_black = 0.20
    vol_normal = fwd * vol_black  # 80 bps

    # 1. Black-76 Put-Call Parity
    p_black = black76_swaption(fwd, strike, annuity, texp, vol_black, is_payer=True)
    r_black = black76_swaption(fwd, strike, annuity, texp, vol_black, is_payer=False)
    expected_diff = annuity * (fwd - strike)
    assert math.isclose(p_black - r_black, expected_diff, rel_tol=1e-6, abs_tol=1e-8), (
        f"Black-76 put-call parity violated: {p_black - r_black} != {expected_diff}"
    )

    # 2. Bachelier Put-Call Parity
    p_bach = bachelier_swaption(fwd, strike, annuity, texp, vol_normal, is_payer=True)
    r_bach = bachelier_swaption(fwd, strike, annuity, texp, vol_normal, is_payer=False)
    assert math.isclose(p_bach - r_bach, expected_diff, rel_tol=1e-6, abs_tol=1e-8), (
        f"Bachelier put-call parity violated: {p_bach - r_bach} != {expected_diff}"
    )

    # 3. Negative rates scenario: Bachelier works seamlessly, Black-76 raises ValueError
    fwd_neg = -0.0030
    strike_neg = -0.0010
    with pytest.raises(ValueError):
        black76_swaption(fwd_neg, strike_neg, annuity, texp, vol_black, is_payer=True)

    p_bach_neg = bachelier_swaption(fwd_neg, strike_neg, annuity, texp, vol_normal, is_payer=True)
    r_bach_neg = bachelier_swaption(fwd_neg, strike_neg, annuity, texp, vol_normal, is_payer=False)
    assert p_bach_neg >= 0.0 and r_bach_neg >= 0.0, (
        "Bachelier swaption prices under negative rates must be non-negative"
    )
    assert math.isclose(p_bach_neg - r_bach_neg, annuity * (fwd_neg - strike_neg), rel_tol=1e-6, abs_tol=1e-8), (
        "Bachelier put-call parity must hold exactly under negative interest rates"
    )

    # 4. Expiry scaling: ATM Bachelier price must scale with sqrt(texp)
    p_bach_1y = bachelier_swaption(fwd, fwd, 1.0, 1.0, vol_normal, is_payer=True)
    p_bach_4y = bachelier_swaption(fwd, fwd, 1.0, 4.0, vol_normal, is_payer=True)
    assert math.isclose(p_bach_4y, 2.0 * p_bach_1y, rel_tol=1e-5), (
        f"ATM Bachelier price must scale with sqrt(texp): p(4y)={p_bach_4y} != 2 * p(1y)={2.0 * p_bach_1y}"
    )


def test_sabr_formula_properties() -> None:
    """Verify mathematical properties of the Hagan et al. (2002) SABR expansion."""
    fwd = 0.0380
    texp = 2.0
    alpha = 0.035
    beta = 0.5
    nu = 0.40

    # 1. Negative rho creates downward skew: sigma(K_low) > sigma(K_high)
    rho_neg = -0.30
    vol_low = sabr_black_vol(fwd, fwd - 0.0100, texp, alpha, beta, rho_neg, nu)
    vol_high = sabr_black_vol(fwd, fwd + 0.0100, texp, alpha, beta, rho_neg, nu)
    assert vol_low > vol_high, (
        f"Negative rho (-0.30) must generate downward sloping skew: vol_low={vol_low} <= vol_high={vol_high}"
    )

    # 2. Positive rho creates upward skew: sigma(K_low) < sigma(K_high)
    rho_pos = +0.30
    vol_low_pos = sabr_black_vol(fwd, fwd - 0.0100, texp, alpha, beta, rho_pos, nu)
    vol_high_pos = sabr_black_vol(fwd, fwd + 0.0100, texp, alpha, beta, rho_pos, nu)
    assert vol_low_pos < vol_high_pos, (
        f"Positive rho (+0.30) must generate upward sloping skew: vol_low={vol_low_pos} >= vol_high={vol_high_pos}"
    )

    # 3. ATM continuity: limit as strike -> fwd matches ATM evaluation
    vol_atm = sabr_black_vol(fwd, fwd, texp, alpha, beta, rho_neg, nu)
    vol_near = sabr_black_vol(fwd, fwd + 1e-7, texp, alpha, beta, rho_neg, nu)
    assert math.isclose(vol_atm, vol_near, rel_tol=1e-4), (
        f"SABR formula must be continuous at ATM: atm={vol_atm}, near={vol_near}"
    )


def test_sabr_slice_calibration() -> None:
    """Verify SABR slice calibration accuracy on market grid."""
    slice_data = MARKET_GRID["2.0x5.0"]
    fwd = slice_data["fwd"]
    strikes = slice_data["strikes"]
    vols = slice_data["vols"]

    alpha, rho, nu = calibrate_sabr_slice(fwd, 2.0, strikes, vols, beta=0.5)

    assert 0.005 < alpha < 0.20, f"Calibrated alpha {alpha} outside valid range"
    assert -0.95 < rho < 0.95, f"Calibrated rho {rho} outside valid range"
    assert 0.05 < nu < 1.5, f"Calibrated nu {nu} outside valid range"

    # Evaluate max fit error across strikes
    max_err = max(
        abs(sabr_black_vol(fwd, k, 2.0, alpha, 0.5, rho, nu) - v) for k, v in zip(strikes, vols, strict=False)
    )
    assert max_err < 0.015, f"SABR calibration max error {max_err} exceeds 150 bps vol threshold"


def test_cube_surface_interpolation(calibrated_engine: SwaptionCubeEngine) -> None:
    """Test 2D parameter interpolation across option expiry and swap tenor."""
    # Exact grid node interpolation must match calibrated parameters
    e_node, t_node = INST["grid_expiries"][1], INST["grid_tenors"][1]
    calib_params = calibrated_engine.calibrated_params[(e_node, t_node)]
    interp_params = calibrated_engine.interpolate_sabr_params(e_node, t_node)

    assert math.isclose(calib_params[0], interp_params[0], rel_tol=1e-5), (
        "Interpolated alpha at node must match calibrated"
    )
    assert math.isclose(calib_params[1], interp_params[1], rel_tol=1e-5), (
        "Interpolated rho at node must match calibrated"
    )
    assert math.isclose(calib_params[2], interp_params[2], rel_tol=1e-5), (
        "Interpolated nu at node must match calibrated"
    )

    # Off-grid interpolation point: 3.5Y x 6.5Y
    a_mid, r_mid, n_mid = calibrated_engine.interpolate_sabr_params(3.5, 6.5)
    assert 0.005 < a_mid < 0.20, f"Interpolated alpha {a_mid} outside reasonable bounds"
    assert -0.90 < r_mid < 0.90, f"Interpolated rho {r_mid} outside reasonable bounds"
    assert 0.05 < n_mid < 1.5, f"Interpolated nu {n_mid} outside reasonable bounds"


def test_breeden_litzenberger_arbitrage_validation(calibrated_engine: SwaptionCubeEngine) -> None:
    """Verify that the engine checks Breeden-Litzenberger risk-neutral density non-negativity."""
    texp = 2.0
    tenor = 5.0
    fwd = calibrated_engine.curve.forward_swap_rate(texp, tenor)
    strikes = [round(fwd + off, 4) for off in [-0.010, -0.005, 0.0, 0.005, 0.010]]

    arb_result = calibrated_engine.check_arbitrage(texp, tenor, strikes)
    assert "is_arbitrage_free" in arb_result, "Arbitrage result must contain 'is_arbitrage_free'"
    assert "min_density" in arb_result, "Arbitrage result must contain 'min_density'"
    assert arb_result["is_arbitrage_free"] is True, "Well-behaved market slice must be arbitrage-free"
    assert arb_result["min_density"] >= 0.0, f"Minimum density must be non-negative, got {arb_result['min_density']}"


def test_off_grid_pricing_and_greeks(calibrated_engine: SwaptionCubeEngine) -> None:
    """Test off-grid swaption pricing, implied volatility, DV01, and Vega."""
    n_targets = len(INST["off_grid_texp"])

    for i in range(n_targets):
        texp = float(INST["off_grid_texp"][i])
        tenor = float(INST["off_grid_tenor"][i])
        strike = float(INST["off_grid_strike"][i])
        is_payer = bool(INST["off_grid_is_payer"][i])

        result = calibrated_engine.price_swaption(texp, tenor, strike, is_payer=is_payer, model="bachelier")

        assert "price" in result and "implied_vol" in result and "dv01" in result and "vega" in result
        assert result["price"] >= 0.0, f"Swaption price {result['price']} must be non-negative"
        assert result["implied_vol"] > 0.0, f"Implied volatility {result['implied_vol']} must be positive"
        assert result["annuity"] > 0.0, f"Swap annuity {result['annuity']} must be positive"
        assert result["vega"] > 0.0, f"Vega {result['vega']} must be positive"

        # Payer DV01 must be positive; receiver DV01 must be negative
        if is_payer:
            assert result["dv01"] > 0.0, f"Payer swaption DV01 must be positive, got {result['dv01']}"
        else:
            assert result["dv01"] < 0.0, f"Receiver swaption DV01 must be negative, got {result['dv01']}"
