"""Acceptance suite for Module F4 Project: Crash-Risk Overlay.

Runs identically in Pyodide and locally:

    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pytest

try:
    import crash_overlay as proj
except ImportError:
    import reference as proj  # type: ignore[no-redef]

from instance import make_instance

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)


def test_make_instance_determinism_and_shapes() -> None:
    """Verify instance generation is deterministic, reproducible, and has valid schema."""
    inst1 = make_instance(SEED)
    inst2 = make_instance(SEED)
    assert inst1["seed"] == SEED
    assert inst1["n_months"] == 360
    assert inst1["n_stocks"] == 50
    assert inst1["in_sample_split"] == 180

    # Ensure reproducibility
    np.testing.assert_allclose(inst1["stock_returns"], inst2["stock_returns"])
    np.testing.assert_allclose(inst1["market_returns"], inst2["market_returns"])

    # Ensure different seed yields distinct returns
    inst_diff = make_instance(SEED + 888)
    assert not np.allclose(inst1["stock_returns"], inst_diff["stock_returns"])
    assert not np.allclose(inst1["market_returns"], inst_diff["market_returns"])

    # Verify no NaN or Inf values
    assert not np.isnan(inst1["stock_returns"]).any()
    assert not np.isnan(inst1["market_returns"]).any()
    assert np.isfinite(inst1["stock_returns"]).all()
    assert np.isfinite(inst1["market_returns"]).all()


def test_momentum_signals_and_weights_structure() -> None:
    """Validate momentum signal lookback, recent month skip, and dollar-neutral weights."""
    stock_returns = INST["stock_returns"]
    signals = proj.compute_momentum_signals(stock_returns, lookback=12, skip_recent=1)

    assert signals.shape == stock_returns.shape
    # Months 0..11 must have zero signals (insufficient lookback)
    np.testing.assert_allclose(signals[:12], 0.0)

    # For month 12, signal must equal sum of returns from month 0 to month 10 (skipping month 11)
    expected_m12 = np.sum(stock_returns[0:11], axis=0)
    np.testing.assert_allclose(signals[12], expected_m12, atol=1e-8)

    # Test WML weight construction
    weights = proj.construct_wml_weights(signals, n_long=10, n_short=10)
    assert weights.shape == stock_returns.shape

    # For t < 12, weights are 0
    np.testing.assert_allclose(weights[:12], 0.0)

    # For t >= 12, verify dollar neutrality and top/bottom decile allocation
    for t in range(12, INST["n_months"]):
        w = weights[t]
        long_sum = float(np.sum(w[w > 0]))
        short_sum = float(np.sum(w[w < 0]))
        net_sum = float(np.sum(w))

        assert np.isclose(long_sum, 1.0, atol=1e-6)
        assert np.isclose(short_sum, -1.0, atol=1e-6)
        assert np.isclose(net_sum, 0.0, atol=1e-6)

        # Count of active positions
        assert np.sum(w > 0) == 10
        assert np.sum(w < 0) == 10
        assert np.sum(w == 0) == INST["n_stocks"] - 20


def test_strictly_causal_volatility_estimation() -> None:
    """Verify trailing volatility estimator is strictly causal and non-negative."""
    market_returns = INST["market_returns"].copy()
    vol = proj.estimate_realized_volatility(market_returns, window=6, min_periods=3)

    assert len(vol) == len(market_returns)
    assert np.all(vol > 0.0)
    assert np.all(np.isfinite(vol))

    # Causality test: modifying return at month t must NOT change estimated vol at month t
    test_month = 50
    perturbed_returns = market_returns.copy()
    perturbed_returns[test_month] += 0.50  # large perturbation at month t

    vol_perturbed = proj.estimate_realized_volatility(perturbed_returns, window=6, min_periods=3)
    assert np.isclose(vol[test_month], vol_perturbed[test_month], atol=1e-10), (
        "Lookahead bias detected: vol[t] depends on return[t]"
    )
    # But month t+1 must reflect the shock
    assert not np.isclose(vol[test_month + 1], vol_perturbed[test_month + 1])


def test_panic_state_identification() -> None:
    """Verify panic state detection conforms to Daniel & Moskowitz (2016) conditions."""
    market_returns = INST["market_returns"]
    panic = proj.identify_panic_states(market_returns, lookback_months=24)

    assert len(panic) == len(market_returns)
    assert panic.dtype == bool

    # For any month where panic is True, trailing 2-year market return MUST be negative
    for t in range(24, len(market_returns)):
        if panic[t]:
            trailing_2yr = float(np.sum(market_returns[t - 24 : t]))
            assert trailing_2yr < 0.0, f"Panic active at month {t} despite positive 2-yr market return"

    # Confirm panic state activates during the simulated crisis episodes
    episodes = INST["panic_episodes"]
    for start, end in episodes:
        assert np.any(panic[start : end + 1]), f"Panic failed to activate during episode {start}..{end}"


def test_dynamic_overlay_weights_and_leverage_caps() -> None:
    """Verify exposure scaling logic, leverage caps, and panic overlay reduction."""
    stock_returns = INST["stock_returns"]
    market_returns = INST["market_returns"]
    signals = proj.compute_momentum_signals(stock_returns, lookback=12, skip_recent=1)
    base_weights = proj.construct_wml_weights(signals, n_long=10, n_short=10)

    raw_wml = np.sum(base_weights * stock_returns, axis=1)
    panic = proj.identify_panic_states(market_returns)

    max_lev = 2.0
    scalars = proj.compute_dynamic_overlay_weights(
        raw_wml, market_returns, panic, target_vol=0.15, max_leverage=max_lev
    )

    assert "static" in scalars and "vol_scaled" in scalars and "dynamic_dm" in scalars
    np.testing.assert_allclose(scalars["static"], 1.0)

    # Check leverage cap
    assert np.all(scalars["vol_scaled"] <= max_lev + 1e-6)
    assert np.all(scalars["dynamic_dm"] <= max_lev + 1e-6)
    assert np.all(scalars["vol_scaled"] > 0.0)
    assert np.all(scalars["dynamic_dm"] > 0.0)

    # In panic states, dynamic DM exposure must be strictly smaller than vol-scaled exposure
    panic_months = np.where(panic)[0]
    assert len(panic_months) > 0
    for t in panic_months:
        assert scalars["dynamic_dm"][t] < scalars["vol_scaled"][t] * 0.90

    # Inverse volatility verification: high-vol series must receive lower weight than low-vol series
    synthetic_low_vol = np.full(50, 0.01)
    synthetic_high_vol = np.tile([0.15, -0.15], 25)
    dummy_panic = np.zeros(50, dtype=bool)
    sc_low = proj.compute_dynamic_overlay_weights(
        synthetic_low_vol, np.zeros(50), dummy_panic, target_vol=0.15, max_leverage=max_lev
    )
    sc_high = proj.compute_dynamic_overlay_weights(
        synthetic_high_vol, np.zeros(50), dummy_panic, target_vol=0.15, max_leverage=max_lev
    )
    assert sc_low["vol_scaled"][-1] > sc_high["vol_scaled"][-1], (
        "Inverse volatility scaling violated: higher volatility did not reduce position scalar"
    )


def test_transaction_costs_and_turnover_mechanics() -> None:
    """Verify transaction costs reduce gross returns proportionally to turnover."""
    stock_returns = INST["stock_returns"]
    signals = proj.compute_momentum_signals(stock_returns)
    weights = proj.construct_wml_weights(signals)
    scalars = np.ones(len(stock_returns))

    bt_zero = proj.backtest_strategy(weights, stock_returns, scalars, cost_bps=0.0)
    bt_cost = proj.backtest_strategy(weights, stock_returns, scalars, cost_bps=20.0)

    np.testing.assert_allclose(bt_zero["gross_returns"], bt_cost["gross_returns"])
    np.testing.assert_allclose(bt_zero["net_returns"], bt_zero["gross_returns"])

    # Net returns with 20 bps cost must be strictly <= gross returns and total net < total gross
    assert np.all(bt_cost["net_returns"] <= bt_cost["gross_returns"] + 1e-12)
    assert float(np.sum(bt_cost["net_returns"])) < float(np.sum(bt_cost["gross_returns"])) - 0.01
    assert np.sum(bt_cost["costs"]) > 0.0

    # Turnover must be non-negative
    assert np.all(bt_cost["turnover"] >= 0.0)


def test_higher_order_moments_and_drawdown_metrics() -> None:
    """Verify statistical evaluation helper functions with analytical test inputs."""
    # Synthetic series with known properties:
    constant_rets = np.full(12, 0.01)
    perf_const = proj.evaluate_performance(constant_rets, rf=0.0)
    assert np.isclose(perf_const["ann_return"], 0.12, atol=1e-5)
    assert perf_const["max_drawdown"] == 0.0

    # Series with negative shock to test max drawdown
    # Wealth: 1.0 -> 1.10 -> 0.77 -> 0.88
    # Peak is 1.10, trough is 0.77 -> drawdown = (1.10 - 0.77)/1.10 = 0.30
    rets_dd = np.array([0.10, -0.30, 0.142857])
    perf_dd = proj.evaluate_performance(rets_dd, rf=0.0)
    assert np.isclose(perf_dd["max_drawdown"], 0.30, atol=1e-4)

    # Verify skewness: positively skewed distribution
    pos_skew_rets = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.20])
    perf_skew = proj.evaluate_performance(pos_skew_rets, rf=0.0)
    assert perf_skew["skewness"] > 0.0


def test_dynamic_momentum_crash_mitigation_invariants() -> None:
    """Verify dynamic overlay dampens crisis drawdown relative to unmanaged momentum."""
    results = proj.run_overlay_experiment(INST)

    # Check the simulated crisis episodes (months 80..104 in-sample, 250..274 out-of-sample)
    # Specifically during the rebound months (101..104 and 271..274), unmanaged static momentum crashes
    for r_start, r_end in [(101, 104), (271, 274)]:
        ret_stat = float(np.sum(results["backtests"]["static"]["gross_returns"][r_start : r_end + 1]))
        ret_vol = float(np.sum(results["backtests"]["vol_scaled"]["gross_returns"][r_start : r_end + 1]))
        ret_dm = float(np.sum(results["backtests"]["dynamic_dm"]["gross_returns"][r_start : r_end + 1]))

        # Static momentum must suffer a severe crash (>20% loss over rebound window)
        assert ret_stat < -0.20, f"Static momentum failed to crash during rebound {r_start}..{r_end}: {ret_stat:.2%}"

        # Dynamic DM must preserve capital and significantly outperform both static and vol-scaled
        assert ret_dm > ret_stat + 0.10, "Dynamic DM failed to protect capital relative to static"
        assert ret_dm > ret_vol, "Dynamic DM failed to protect capital relative to vol-scaled"
