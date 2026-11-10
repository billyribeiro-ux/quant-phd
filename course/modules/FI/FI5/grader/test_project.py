"""Test suite for FI5 Inflation-Expectations Decomposition autograder.

Verifies breakeven yields, TIPS deflation floor protection, synthetic Treasury
replication, the Fleckenstein puzzle basis, and the tripartite decomposition identity.
"""

from __future__ import annotations

import os
from typing import Any, cast

import pytest
from instance import make_instance

# The browser autograder loads decomposition.py or reference.py
try:
    import decomposition as sol
except ImportError:
    import reference as sol


@pytest.fixture
def current_instance() -> dict[str, Any]:
    seed = int(os.environ.get("QF_SEED", "42"))
    inst = cast(dict[str, Any], make_instance(seed))
    return inst


def test_breakeven_yield_identity(current_instance: dict[str, Any]) -> None:
    """Breakeven yield must equal nominal yield minus real yield."""
    y_n = float(current_instance["nominal_yield"])
    y_r = float(current_instance["real_yield"])
    bei = sol.breakeven_yield(y_n, y_r)
    expected = y_n - y_r
    assert abs(bei - expected) < 1e-12, f"BEI must equal y_N - y_R; got {bei} vs expected {expected}"


def test_breakeven_zero_spread() -> None:
    """When nominal and real yields are equal, breakeven inflation must be zero."""
    bei = sol.breakeven_yield(0.040, 0.040)
    assert abs(bei) < 1e-12, "BEI must be zero when nominal and real yields are identical"


def test_breakeven_sign() -> None:
    """When nominal yield exceeds real yield, breakeven must be strictly positive."""
    bei = sol.breakeven_yield(0.045, 0.020)
    assert bei > 0.0, "BEI must be strictly positive when nominal yield exceeds real yield"


def test_tips_cash_flows_inflation(current_instance: dict[str, Any]) -> None:
    """Under inflation (ref_cpi > base_cpi), principal scales with index ratio with no floor benefit."""
    base_cpi = float(current_instance["base_cpi"])
    ref_cpi = base_cpi * 1.15
    coupon = float(current_instance["real_coupon_rate"])
    mat = int(current_instance["maturity_years"])
    face = float(current_instance["face_value"])

    res = sol.tips_cash_flows(base_cpi, ref_cpi, coupon, mat, face)
    assert abs(res["index_ratio"] - 1.15) < 1e-9
    assert abs(res["adjusted_principal"] - face * 1.15) < 1e-9
    assert abs(res["deflation_floor_benefit"] - 0.0) < 1e-9
    assert abs(res["adjusted_coupon"] - face * (coupon / 2.0) * 1.15) < 1e-9


def test_tips_cash_flows_deflation_floor(current_instance: dict[str, Any]) -> None:
    """Under deflation (ref_cpi < base_cpi), principal is protected at par (floor benefit > 0)."""
    base_cpi = float(current_instance["base_cpi"])
    ref_cpi = base_cpi * 0.90  # 10% deflation
    coupon = float(current_instance["real_coupon_rate"])
    mat = int(current_instance["maturity_years"])
    face = float(current_instance["face_value"])

    res = sol.tips_cash_flows(base_cpi, ref_cpi, coupon, mat, face)
    assert abs(res["index_ratio"] - 0.90) < 1e-9
    assert abs(res["adjusted_principal"] - face * 1.0) < 1e-9, "Deflation floor must protect full par"
    assert abs(res["deflation_floor_benefit"] - face * 0.10) < 1e-9, "Floor benefit must equal par shortfall"
    assert abs(res["adjusted_coupon"] - face * (coupon / 2.0) * 0.90) < 1e-9


def test_tips_cash_flows_validation() -> None:
    """Invalid parameters must raise ValueError."""
    with pytest.raises(ValueError):
        sol.tips_cash_flows(0.0, 250.0, 0.02, 5)
    with pytest.raises(ValueError):
        sol.tips_cash_flows(250.0, -10.0, 0.02, 5)
    with pytest.raises(ValueError):
        sol.tips_cash_flows(250.0, 250.0, 0.02, 0)
    with pytest.raises(ValueError):
        sol.tips_cash_flows(250.0, 250.0, -0.01, 5)


def test_synthetic_treasury_exact_compounding(current_instance: dict[str, Any]) -> None:
    """Synthetic yield must incorporate geometric Fisher compounding: (1 + y_R)(1 + s) - 1."""
    y_r = float(current_instance["real_yield"])
    s = float(current_instance["swap_rate"])

    synth_yield = sol.replicate_synthetic_treasury(y_r, s)
    expected = (1.0 + y_r) * (1.0 + s) - 1.0
    assert abs(synth_yield - expected) < 1e-12, (
        f"Synthetic yield must equal (1 + y_R)(1 + s) - 1; got {synth_yield} vs {expected}"
    )

    # Must strictly exceed linear sum when yields are positive
    assert synth_yield > (y_r + s), "Geometric compounding must exceed linear sum for positive rates"


def test_synthetic_treasury_monotonicity() -> None:
    """Synthetic yield must be strictly increasing in both real yield and swap rate."""
    base = sol.replicate_synthetic_treasury(0.020, 0.025)
    higher_r = sol.replicate_synthetic_treasury(0.025, 0.025)
    higher_s = sol.replicate_synthetic_treasury(0.020, 0.030)
    assert higher_r > base
    assert higher_s > base


def test_puzzle_basis_zero_when_prices_equal() -> None:
    """When cash and synthetic prices are equal, puzzle basis must be zero."""
    res = sol.fleckenstein_puzzle_basis(100.0, 100.0, 5.0)
    assert abs(res["price_basis"]) < 1e-12
    assert abs(res["yield_basis_bps"]) < 1e-12


def test_puzzle_basis_positive_when_cash_expensive() -> None:
    """When cash nominal Treasury is overpriced relative to synthetic, basis must be positive."""
    cash_price = 102.50
    synth_price = 101.00
    mod_dur = 4.5
    res = sol.fleckenstein_puzzle_basis(cash_price, synth_price, mod_dur)
    assert res["price_basis"] == pytest.approx(1.50)
    expected_bps = (1.50 / (102.50 * 4.5)) * 10_000.0
    assert res["yield_basis_bps"] == pytest.approx(expected_bps)


def test_puzzle_basis_validation() -> None:
    """Invalid price or duration must raise ValueError."""
    with pytest.raises(ValueError):
        sol.fleckenstein_puzzle_basis(0.0, 100.0, 5.0)
    with pytest.raises(ValueError):
        sol.fleckenstein_puzzle_basis(100.0, 100.0, 0.0)


def test_decompose_breakeven_fundamental_identity(current_instance: dict[str, Any]) -> None:
    """Tripartite decomposition identity BEI == E[pi] + IRP - TLP must hold to machine precision."""
    y_n = float(current_instance["nominal_yield"])
    y_r = float(current_instance["real_yield"])
    exp_pi = float(current_instance["survey_inflation"])
    proxy = float(current_instance["tips_liquidity_proxy"])
    beta = float(current_instance["beta_liquidity"])

    res = sol.decompose_breakeven(y_n, y_r, exp_pi, proxy, beta)
    reconstructed_bei = res["expected_inflation"] + res["inflation_risk_premium"] - res["tips_liquidity_premium"]
    assert abs(res["bei"] - reconstructed_bei) < 1e-12, (
        f"Decomposition identity violated: BEI={res['bei']} vs E[pi]+IRP-TLP={reconstructed_bei}"
    )


def test_decompose_breakeven_irp_sensitivity(current_instance: dict[str, Any]) -> None:
    """An increase in nominal yield holding real yield and expectations fixed raises IRP one-for-one."""
    y_n = float(current_instance["nominal_yield"])
    y_r = float(current_instance["real_yield"])
    exp_pi = float(current_instance["survey_inflation"])
    proxy = float(current_instance["tips_liquidity_proxy"])
    beta = float(current_instance["beta_liquidity"])

    delta = 0.0050  # 50 bps increase
    res_base = sol.decompose_breakeven(y_n, y_r, exp_pi, proxy, beta)
    res_shock = sol.decompose_breakeven(y_n + delta, y_r, exp_pi, proxy, beta)

    assert abs(res_shock["bei"] - (res_base["bei"] + delta)) < 1e-12
    assert abs(res_shock["inflation_risk_premium"] - (res_base["inflation_risk_premium"] + delta)) < 1e-12


def test_decompose_breakeven_tlp_sensitivity(current_instance: dict[str, Any]) -> None:
    """Higher TIPS illiquidity proxy increases TLP and increases derived IRP."""
    y_n = float(current_instance["nominal_yield"])
    y_r = float(current_instance["real_yield"])
    exp_pi = float(current_instance["survey_inflation"])
    proxy = float(current_instance["tips_liquidity_proxy"])
    beta = float(current_instance["beta_liquidity"])

    res_base = sol.decompose_breakeven(y_n, y_r, exp_pi, proxy, beta)
    res_high_liq = sol.decompose_breakeven(y_n, y_r, exp_pi, proxy + 0.0020, beta)

    assert res_high_liq["tips_liquidity_premium"] > res_base["tips_liquidity_premium"]
    assert res_high_liq["inflation_risk_premium"] > res_base["inflation_risk_premium"]


def test_all_instance_calculations(current_instance: dict[str, Any]) -> None:
    """Run full calculations on current instance and verify all fields are finite numbers."""
    y_n = float(current_instance["nominal_yield"])
    y_r = float(current_instance["real_yield"])
    exp_pi = float(current_instance["survey_inflation"])
    proxy = float(current_instance["tips_liquidity_proxy"])
    beta = float(current_instance["beta_liquidity"])
    base_cpi = float(current_instance["base_cpi"])
    ref_cpi = float(current_instance["ref_cpi"])
    coupon = float(current_instance["real_coupon_rate"])
    mat = int(current_instance["maturity_years"])
    face = float(current_instance["face_value"])
    cash_price = float(current_instance["cash_nominal_price"])
    mod_dur = float(current_instance["mod_duration"])
    swap_rate = float(current_instance["swap_rate"])

    bei = sol.breakeven_yield(y_n, y_r)
    cfs = sol.tips_cash_flows(base_cpi, ref_cpi, coupon, mat, face)
    synth_yield = sol.replicate_synthetic_treasury(y_r, swap_rate)
    synth_price = cash_price * (1.0 - mod_dur * (synth_yield - y_n))
    puzzle = sol.fleckenstein_puzzle_basis(cash_price, synth_price, mod_dur)
    decomp = sol.decompose_breakeven(y_n, y_r, exp_pi, proxy, beta)

    assert bei > 0.0
    assert cfs["adjusted_principal"] >= face
    assert synth_yield > 0.0
    assert abs(puzzle["price_basis"]) >= 0.0
    assert decomp["bei"] == pytest.approx(
        decomp["expected_inflation"] + decomp["inflation_risk_premium"] - decomp["tips_liquidity_premium"]
    )
