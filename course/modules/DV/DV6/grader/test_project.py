"""Test suite for DV6: Exotics, Structured Products & Dealer Hedging.

Tests mathematical properties, no-arbitrage bounds, local volatility surfaces,
Monte Carlo Phoenix autocallable pricing, Greek sensitivities, and dealer hedging
profiles across deterministic pseudorandom seeds.
"""

from __future__ import annotations

import math
import os
from typing import Any

import pytest
from instance import make_instance
from reference import (
    analyze_dealer_hedging_profile,
    compute_autocallable_greeks,
    eval_local_vol,
    price_autocallable,
    simulate_hedging_pnl_impact,
)


@pytest.fixture(scope="module")
def instance() -> dict[str, Any]:
    """Load deterministic test instance from QF_SEED environment variable."""
    seed = int(os.environ.get("QF_SEED", "0"))
    return make_instance(seed=seed)


def test_local_vol_properties(instance: dict[str, Any]) -> None:
    """Test parametric local volatility surface properties and input validation."""
    spot = float(instance["spot"])
    strike = float(instance["strike"])
    base_vol = float(instance["base_vol"])
    skew = float(instance["skew"])
    curvature = float(instance["curvature"])

    # 1. Base evaluation at ATM
    vol_atm = eval_local_vol(spot, strike, 0.5, base_vol, skew, curvature)
    assert 0.01 <= vol_atm <= 1.0, f"Local vol at ATM out of reasonable bounds: {vol_atm}"

    # 2. Skew property: with positive skew parameter, downside volatility (S < K) exceeds upside volatility (S > K)
    vol_down = eval_local_vol(spot * 0.85, strike, 0.5, base_vol, skew, curvature)
    vol_up = eval_local_vol(spot * 1.15, strike, 0.5, base_vol, skew, curvature)
    if skew > 0.05:
        assert vol_down > vol_up, f"Downside local vol {vol_down} should exceed upside local vol {vol_up} with skew>0"

    # 3. Term structure decay: volatility should decay over time horizon
    vol_t1 = eval_local_vol(spot, strike, 0.25, base_vol, skew, curvature)
    vol_t2 = eval_local_vol(spot, strike, 2.0, base_vol, skew, curvature)
    assert vol_t1 > vol_t2, f"Expected term structure decay: vol(t=0.25)={vol_t1} vs vol(t=2.0)={vol_t2}"

    # 4. Input validation: verify exceptions on invalid arguments
    with pytest.raises(ValueError, match="strictly positive"):
        eval_local_vol(-10.0, strike, 0.5, base_vol, skew, curvature)
    with pytest.raises(ValueError, match="strictly positive"):
        eval_local_vol(spot, -50.0, 0.5, base_vol, skew, curvature)
    with pytest.raises(ValueError, match="non-negative"):
        eval_local_vol(spot, strike, -0.5, base_vol, skew, curvature)
    with pytest.raises(ValueError, match="strictly positive"):
        eval_local_vol(spot, strike, 0.5, -0.2, skew, curvature)


def test_autocallable_pricing_bounds_and_articulation(instance: dict[str, Any]) -> None:
    """Test autocallable pricing bounds, cash flow articulation, and probability sanity."""
    res = price_autocallable(instance, n_paths=2500, seed=42)

    notional = float(instance["notional"])
    coupon_rate = float(instance["coupon_rate"])
    n_obs = len(instance["observation_dates"])
    maturity = float(instance["observation_dates"][-1])

    # 1. Articulation: price = coupon_pv + redemption_pv
    price = float(res["price"])
    coupon_pv = float(res["coupon_pv"])
    redemption_pv = float(res["redemption_pv"])
    assert math.isclose(price, coupon_pv + redemption_pv, rel_tol=1e-6), (
        f"Price {price} does not articulate with coupon_pv {coupon_pv} + redemption_pv {redemption_pv}"
    )

    # 2. No-arbitrage upper and lower bounds
    # Maximum possible undiscounted payout is notional + n_obs * coupon
    max_possible = notional + float(n_obs) * coupon_rate * notional
    assert 0.0 < price <= max_possible, f"Note price {price} out of no-arbitrage bounds (0, {max_possible})"
    assert 0.0 <= coupon_pv <= float(n_obs) * coupon_rate * notional, f"Coupon PV out of bounds: {coupon_pv}"
    assert 0.0 < redemption_pv <= notional, f"Redemption PV out of bounds: {redemption_pv}"

    # 3. Probabilities and tenors
    autocall_probs: list[float] = res["autocall_probs"]
    assert len(autocall_probs) == n_obs, f"Expected {n_obs} autocall probabilities, got {len(autocall_probs)}"
    for p in autocall_probs:
        assert 0.0 <= p <= 1.0, f"Autocall probability out of bounds: {p}"
    assert sum(autocall_probs) <= 1.0001, f"Sum of autocall probabilities exceeds 1: {sum(autocall_probs)}"

    knock_in_prob = float(res["knock_in_prob"])
    assert 0.0 <= knock_in_prob <= 1.0, f"Knock-in probability out of bounds: {knock_in_prob}"

    expected_tenor = float(res["expected_tenor"])
    assert 0.0 < expected_tenor <= maturity + 1e-4, f"Expected tenor out of bounds: {expected_tenor}"

    # 4. Input validation
    with pytest.raises(ValueError):
        price_autocallable(dict(instance, spot=-100.0), n_paths=100)
    with pytest.raises(ValueError):
        price_autocallable(dict(instance, observation_dates=[]), n_paths=100)
    with pytest.raises(ValueError):
        price_autocallable(dict(instance, autocall_levels=[100.0]), n_paths=100)


def test_autocallable_monotonicity_and_knock_in(instance: dict[str, Any]) -> None:
    """Test spot monotonicity and knock-in barrier downside cliff."""
    spot = float(instance["spot"])

    # High spot (above initial spot, safe from barrier)
    params_high = dict(instance, spot=spot * 1.25)
    res_high = price_autocallable(params_high, n_paths=2000, seed=42)

    # Low spot (severely impaired, below knock-in barrier)
    knock_in_b = float(instance["knock_in_barrier"])
    params_low = dict(instance, spot=knock_in_b * 0.85)
    res_low = price_autocallable(params_low, n_paths=2000, seed=42)

    # 1. Monotonicity: higher spot produces strictly higher note price
    assert res_high["price"] > res_low["price"], (
        f"High spot price {res_high['price']} should strictly exceed low spot price {res_low['price']}"
    )

    # 2. Early redemption vs knock-in: high spot autocalls frequently, low spot knocks in
    assert res_high["autocall_probs"][0] > res_low["autocall_probs"][0], (
        "High spot should have much higher period-1 autocall probability"
    )
    assert res_low["knock_in_prob"] > res_high["knock_in_prob"], "Low spot should have much higher knock-in probability"
    assert res_low["knock_in_prob"] > 0.80, (
        f"Spot starting below barrier should knock in with high probability, got {res_low['knock_in_prob']}"
    )


def test_greeks_consistency(instance: dict[str, Any]) -> None:
    """Test Greek calculations and dealer exposure signs."""
    greeks = compute_autocallable_greeks(instance, n_paths=2500, seed=42)

    delta = greeks["delta"]
    gamma = greeks["gamma"]
    vega = greeks["vega"]

    # 1. Delta: the note holder is long equity downside, so delta is strictly positive
    assert delta > 0.0, f"Client note delta must be positive, got {delta}"

    # 2. Vega: for an autocallable note, high volatility increases barrier breach probability, typically reducing value
    # Even if near-zero, vega magnitude should be finite and realistic
    assert abs(vega) < float(instance["notional"]) * 10.0, f"Vega out of realistic bounds: {vega}"

    # 3. Finite differences sanity: gamma must be finite
    assert abs(gamma) < 1000.0, f"Gamma out of numerical stability bounds: {gamma}"


def test_dealer_hedging_profile_and_cliff_risk(instance: dict[str, Any]) -> None:
    """Test dealer gamma exposure profile and rebalancing flow impact."""
    spot_grid: list[float] = instance["spot_grid"]
    notional = float(instance["notional"])
    profile = analyze_dealer_hedging_profile(instance, spot_grid, n_paths=1500, seed=42)

    assert len(profile) == len(spot_grid), f"Expected {len(spot_grid)} grid entries, got {len(profile)}"

    # 1. Delta and Gamma conservation between client and dealer
    for r in profile:
        s = r["spot"]
        assert math.isclose(r["dealer_delta"], -r["delta"], rel_tol=1e-7), "Dealer delta must be -client delta"
        assert math.isclose(r["dealer_gamma"], -r["gamma"], rel_tol=1e-7), "Dealer gamma must be -client gamma"
        expected_dge = r["dealer_gamma"] * s * (notional / s)
        assert math.isclose(r["dealer_gamma_exposure"], expected_dge, rel_tol=1e-6), (
            f"Dealer GEX {r['dealer_gamma_exposure']} does not articulate with dealer_gamma * notional {expected_dge}"
        )

    # 2. Overall profile monotonicity: note price at top of grid must strictly exceed price at bottom by > 200 USD
    p_low = profile[0]["note_price"]
    p_high = profile[-1]["note_price"]
    assert p_high > p_low + 200.0, f"Expected higher note price at top of grid: {p_high} vs {p_low}"

    # 3. Test dealer hedging shock impact
    shock_res = simulate_hedging_pnl_impact(instance, spot_shock_pct=-0.05, rebalancing_friction_bps=5.0)
    assert shock_res["spot_shocked"] < shock_res["spot_initial"], "Spot shocked should be lower for -5% shock"
    assert shock_res["trading_volume_usd"] >= 0.0, "Trading volume must be non-negative"
    assert shock_res["rebalance_friction"] >= 0.0, "Rebalance friction must be non-negative"
