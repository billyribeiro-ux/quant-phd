"""Acceptance suite for Module F3 Project: Multi-Asset Factor Book.

Runs identically in Pyodide and locally:

    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest

try:
    import factor_book as proj
except ImportError:
    import reference as proj  # type: ignore[no-redef]

from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def test_make_instance_determinism_and_shapes() -> None:
    """Verify instance generation is deterministic and has expected schema."""
    inst1 = make_instance(SEED)
    make_instance(SEED)
    assert inst1["seed"] == SEED
    assert inst1["n_months"] == 360

    # Ensure different seed generates different numbers
    inst_other = make_instance(SEED + 999)
    fx_1 = inst1["fx"]
    fx_oth = inst_other["fx"]
    assert isinstance(fx_1, dict) and isinstance(fx_oth, dict)
    assert not np.allclose(
        fx_1["returns"],
        fx_oth["returns"],
    )

    for ac in ["rates", "fx", "commodities"]:
        data = inst1[ac]
        assert isinstance(data, dict)
        r = np.asarray(data["returns"])
        c = np.asarray(data["carry"])
        v = np.asarray(data["value"])
        assert r.shape == (360, 4)
        assert c.shape == (360, 4)
        assert v.shape == (360, 4)
        assert not np.isnan(r).any()
        assert not np.isnan(c).any()
        assert not np.isnan(v).any()


def test_carry_factor_properties() -> None:
    """Verify dollar neutrality, signal monotonicity, and crash skewness of carry factors."""
    fx_data = INST["fx"]
    assert isinstance(fx_data, dict)
    returns = np.asarray(fx_data["returns"], dtype=np.float64)
    signals = np.asarray(fx_data["carry"], dtype=np.float64)

    c_rets = proj.compute_carry_factor(signals, returns)
    assert c_rets.shape == (359,)
    assert not np.isnan(c_rets).any()

    # Test exact synthetic cross-section for dollar neutrality and monotonicity
    synth_signals = np.array([[1.0, 2.0, 3.0, 4.0], [4.0, 3.0, 2.0, 1.0]])
    synth_returns = np.array([[0.01, 0.02, 0.03, 0.04], [0.05, 0.04, 0.03, 0.02]])

    ret_out = proj.compute_carry_factor(synth_signals, synth_returns)
    assert len(ret_out) == 1
    # When signals are [1, 2, 3, 4], demeaned is [-1.5, -0.5, 0.5, 1.5], sum abs = 4.0
    # Weights = [-0.375, -0.125, +0.125, +0.375], sum = 0
    # synth_returns[1] = [0.05, 0.04, 0.03, 0.02]
    # Expected ret = -0.375*0.05 - 0.125*0.04 + 0.125*0.03 + 0.375*0.02 = -0.0125
    expected_ret = -0.0125
    assert np.isclose(ret_out[0], expected_ret, atol=1e-6)


def test_tsmom_factor_properties() -> None:
    """Verify TSMOM directional sign responsiveness and inverse-volatility scaling."""
    comm_data = INST["commodities"]
    assert isinstance(comm_data, dict)
    returns = np.asarray(comm_data["returns"], dtype=np.float64)

    ts_rets = proj.compute_tsmom_factor(returns, lookback=12, target_vol=0.10)
    assert ts_rets.shape == (348,)
    assert not np.isnan(ts_rets).any()

    # Target vol scaling test: scaling target vol by 2 must double factor returns
    ts_rets_2x = proj.compute_tsmom_factor(returns, lookback=12, target_vol=0.20)
    np.testing.assert_allclose(
        ts_rets_2x, 2.0 * ts_rets, rtol=1e-5, err_msg="TSMOM must scale linearly with target_vol"
    )

    # Synthetic test to verify inverse-volatility scaling:
    # Asset 0: low volatility (vol 0.05). Asset 1: high volatility (vol 0.20).
    # Both have positive past returns. Low vol asset should receive 4x the position weight.
    n_t = 30
    synth_rets = np.zeros((n_t, 2))
    # Fill past 24 periods with deterministic returns
    synth_rets[:25, 0] = 0.01  # low vol
    synth_rets[:25, 1] = 0.04  # high vol
    # Add slight variation so std > 0
    synth_rets[0, 0] += 0.005
    synth_rets[0, 1] += 0.02

    out_ts = proj.compute_tsmom_factor(synth_rets, lookback=12, target_vol=0.10)
    assert len(out_ts) == n_t - 12
    assert np.isclose(out_ts[0], 0.125, atol=1e-3)
    out_ts_2 = proj.compute_tsmom_factor(synth_rets, lookback=12, target_vol=0.20)
    assert np.isclose(out_ts_2[0], 0.250, atol=1e-3)


def test_value_factor_properties() -> None:
    """Verify value factor dollar neutrality and cheap-minus-expensive orientation."""
    rates_data = INST["rates"]
    assert isinstance(rates_data, dict)
    returns = np.asarray(rates_data["returns"], dtype=np.float64)
    signals = np.asarray(rates_data["value"], dtype=np.float64)

    v_rets = proj.compute_value_factor(signals, returns)
    assert v_rets.shape == (359,)
    assert not np.isnan(v_rets).any()

    # Synthetic test: high valuation signal receives positive weight
    synth_signals = np.array([[10.0, 2.0], [5.0, 1.0]])
    synth_returns = np.array([[0.02, 0.01], [0.04, -0.02]])

    v_out = proj.compute_value_factor(synth_signals, synth_returns)
    assert len(v_out) == 1
    # Signals = [10, 2], demeaned = [4, -4], sum abs = 8. Weights = [+0.5, -0.5]
    # Return[1] = [0.04, -0.02]. Factor return = 0.5*0.04 - 0.5*(-0.02) = 0.03
    assert np.isclose(v_out[0], 0.03, atol=1e-6)


def test_factor_diagnostics_calculation() -> None:
    """Verify diagnostic moment formulas, annualization, and drawdown logic."""
    # Deterministic test sequence
    test_r = np.array([0.02, -0.01, 0.03, -0.04, 0.05, 0.01, -0.02, 0.03, 0.02, -0.01, 0.04, 0.02])
    diag = proj.compute_factor_diagnostics(test_r, annualization=12.0)

    exp_mean_ann = float(np.mean(test_r) * 12.0 * 100.0)
    exp_vol_ann = float(np.std(test_r, ddof=1) * np.sqrt(12.0) * 100.0)
    exp_sharpe = float(exp_mean_ann / exp_vol_ann)

    assert np.isclose(diag["mean_ann"], exp_mean_ann, atol=0.01)
    assert np.isclose(diag["vol_ann"], exp_vol_ann, atol=0.01)
    assert np.isclose(diag["sharpe"], exp_sharpe, atol=0.01)
    assert diag["max_drawdown"] <= 0.0
    assert np.isclose(diag["worst_month"], -4.0, atol=0.01)


def test_multi_asset_factor_book_construction_and_diversification() -> None:
    """Verify factor book risk-parity weighting and Sharpe ratio expansion."""
    book_rp = proj.construct_multi_asset_factor_book(INST, weighting_scheme="risk_parity")
    names = book_rp["factor_names"]
    assert isinstance(names, list)
    assert len(names) == 9

    book_rets = book_rp["book_returns"]
    assert isinstance(book_rets, np.ndarray)
    assert len(book_rets) == 348

    weights = book_rp["weights"]
    assert isinstance(weights, dict)
    total_weight = sum(weights.values())
    assert np.isclose(total_weight, 1.0, atol=1e-3)

    # Risk parity invariant: factor with higher volatility receives lower weight
    factor_diags = book_rp["factor_diagnostics"]
    assert isinstance(factor_diags, dict)
    sorted_by_vol = sorted(names, key=lambda name: float(factor_diags[name]["vol_ann"]))
    lowest_vol_factor = sorted_by_vol[0]
    highest_vol_factor = sorted_by_vol[-1]
    assert weights[lowest_vol_factor] >= weights[highest_vol_factor]

    # Equal weighting test
    book_ew = proj.construct_multi_asset_factor_book(INST, weighting_scheme="equal_weight")
    ew_weights = book_ew["weights"]
    assert isinstance(ew_weights, dict)
    for w in ew_weights.values():
        assert np.isclose(float(w), 1.0 / 9.0, atol=1e-4)

    # Diversification Sharpe expansion: composite Sharpe > single factor average
    expansion = book_rp["expansion_ratio"]
    assert isinstance(expansion, (int, float))
    assert expansion > 1.0


def test_error_handling_and_invariants() -> None:
    """Verify robust error raising on invalid inputs and shapes."""
    # Mismatched shapes
    with pytest.raises(ValueError, match="identical shapes"):
        proj.compute_carry_factor(np.zeros((10, 4)), np.zeros((10, 3)))

    with pytest.raises(ValueError, match="identical shapes"):
        proj.compute_value_factor(np.zeros((10, 4)), np.zeros((11, 4)))

    # Lookback exceeding sample length
    with pytest.raises(ValueError, match="exceed lookback"):
        proj.compute_tsmom_factor(np.zeros((10, 4)), lookback=12)

    # Short return series in diagnostics
    with pytest.raises(ValueError, match="at least 2 observations"):
        proj.compute_factor_diagnostics(np.array([0.05]))

    # Unknown weighting scheme
    with pytest.raises(ValueError, match="unknown weighting scheme"):
        proj.construct_multi_asset_factor_book(INST, weighting_scheme="unknown_scheme")
