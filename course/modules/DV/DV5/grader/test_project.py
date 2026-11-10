"""Test suite for DV5: Variance Risk Premium & Volatility Trading.

Tests property invariants, no-arbitrage bounds, mathematical articulation,
leverage and margin constraints, crash shock degradation, higher moments,
and input validation across deterministic pseudorandom seeds.
"""

from __future__ import annotations

import math
import os
from typing import Any

import pytest
from instance import make_instance
from reference import (
    compute_variance_swap_payoff,
    evaluate_strategy_metrics,
    replicate_vix_index,
    simulate_short_vol_strategy,
    stress_test_drawdowns,
)


@pytest.fixture(scope="module")
def instance() -> dict[str, Any]:
    seed = int(os.environ.get("QF_SEED", "0"))
    return make_instance(seed=seed)


def test_variance_swap_properties_and_bounds(instance: dict[str, Any]) -> None:
    """Test variance swap payoff articulation, vega notional scaling, and input validation."""
    realized_prices: list[float] = instance["realized_prices"]
    strike_var = float(instance["var_swap_strike"])
    vega_notional = float(instance["var_swap_vega_notional"])

    res = compute_variance_swap_payoff(realized_prices, strike_var, vega_notional)

    # 1. Non-negativity and mathematical definitions
    assert res["rv"] > 0.0, f"Realized variance must be positive: {res['rv']}"
    assert math.isclose(res["realized_vol"], math.sqrt(res["rv"]), rel_tol=1e-7), "Realized vol must equal sqrt(RV)"
    assert math.isclose(res["strike_vol"], math.sqrt(strike_var), rel_tol=1e-7), "Strike vol must equal sqrt(K_var)"

    # 2. Vega notional to variance notional scaling: N_var = N_vega / (2 * sqrt(K_var))
    expected_var_notional = vega_notional / (2.0 * math.sqrt(strike_var))
    assert math.isclose(res["var_notional"], expected_var_notional, rel_tol=1e-6), (
        f"Variance notional {res['var_notional']} does not match N_vega / (2 * K_vol) {expected_var_notional}"
    )

    # 3. Payoff articulation: PnL = N_var * (RV - K_var)
    expected_pnl = res["var_notional"] * (res["rv"] - strike_var)
    assert math.isclose(res["variance_pnl"], expected_pnl, rel_tol=1e-6), (
        f"Variance swap PnL {res['variance_pnl']} does not articulate with N_var * (RV - K_var)"
    )

    # 4. Error handling
    with pytest.raises(ValueError, match="At least 2 price observations"):
        compute_variance_swap_payoff([100.0], strike_var, vega_notional)
    with pytest.raises(ValueError, match="strictly positive"):
        compute_variance_swap_payoff([100.0, -90.0], strike_var, vega_notional)
    with pytest.raises(ValueError, match="strictly positive"):
        compute_variance_swap_payoff(realized_prices, -0.04, vega_notional)
    with pytest.raises(ValueError, match="strictly positive"):
        compute_variance_swap_payoff(realized_prices, strike_var, -1000.0)


def test_vix_replication_properties(instance: dict[str, Any]) -> None:
    """Test model-free implied volatility replication and strike sensitivity."""
    options = instance["options_chain"]
    forward = float(instance["forward"])
    rate = float(instance["rate"])
    maturity = float(instance["maturity"])

    vix = replicate_vix_index(options, forward, rate, maturity)

    # 1. Range sanity: VIX index should lie in realistic annualized percentage bounds [5.0, 90.0]
    assert 5.0 <= vix <= 90.0, f"Replicated VIX {vix} out of reasonable market bounds [5, 90]"

    # 2. Monotonicity: artificially doubling all option prices must increase replicated VIX
    scaled_options = [(k, is_call, bid * 1.5, ask * 1.5) for k, is_call, bid, ask in options]
    vix_scaled = replicate_vix_index(scaled_options, forward, rate, maturity)
    assert vix_scaled > vix, f"Higher option prices must increase VIX: {vix_scaled} vs {vix}"

    # 3. Strike weighting property: verify that replication fails gracefully on empty or degenerate input
    with pytest.raises(ValueError):
        replicate_vix_index([], forward, rate, maturity)
    with pytest.raises(ValueError):
        replicate_vix_index(options, -100.0, rate, maturity)
    with pytest.raises(ValueError):
        replicate_vix_index(options, forward, rate, -0.1)


def test_short_vol_strategy_simulation(instance: dict[str, Any]) -> None:
    """Test short-volatility strategy simulation: NAV conservation, drawdowns, and stop-loss."""
    market_data = instance["market_data"]
    initial_capital = float(instance["initial_capital"])
    target_leverage = float(instance["target_leverage"])
    margin_requirement = float(instance["margin_requirement"])
    tc_bps = float(instance["transaction_cost_bps"])

    res = simulate_short_vol_strategy(
        market_data,
        initial_capital,
        target_leverage,
        margin_requirement,
        tc_bps,
        stop_loss_drawdown=0.40,
    )

    # 1. Output sequence lengths
    assert len(res["nav_series"]) == len(market_data) + 1, "NAV series must have length N + 1"
    assert len(res["returns"]) == len(market_data), "Returns series must have length N"
    assert len(res["drawdown_series"]) == len(market_data) + 1, "Drawdown series must have length N + 1"

    # 2. Initial state
    assert res["nav_series"][0] == initial_capital, "Starting NAV must equal initial capital"
    assert res["drawdown_series"][0] == 0.0, "Initial drawdown must be zero"

    # 3. Drawdown properties: 0 <= dd <= 1
    for dd in res["drawdown_series"]:
        assert 0.0 <= dd <= 1.0, f"Drawdown {dd} must lie in [0, 1]"
    assert math.isclose(res["max_drawdown"], max(res["drawdown_series"]), rel_tol=1e-7), (
        "Reported max drawdown must equal supremum of drawdown series"
    )

    # 4. Impact of transaction costs: higher costs must reduce terminal NAV
    res_high_tc = simulate_short_vol_strategy(
        market_data,
        initial_capital,
        target_leverage,
        margin_requirement,
        tc_bps * 5.0,
        stop_loss_drawdown=0.40,
    )
    assert res_high_tc["terminal_nav"] <= res["terminal_nav"] + 1e-4, (
        f"Higher transaction costs must reduce terminal NAV: {res_high_tc['terminal_nav']} vs {res['terminal_nav']}"
    )

    # 5. Invalid parameter validation
    with pytest.raises(ValueError):
        simulate_short_vol_strategy(market_data, -100.0, target_leverage, margin_requirement, tc_bps)
    with pytest.raises(ValueError):
        simulate_short_vol_strategy(market_data, initial_capital, -1.0, margin_requirement, tc_bps)
    with pytest.raises(ValueError):
        simulate_short_vol_strategy(market_data, initial_capital, target_leverage, -0.2, tc_bps)


def test_stress_test_drawdowns(instance: dict[str, Any]) -> None:
    """Test crash scenario stress tests across 2008 Lehman, 2018 Volmageddon, and 2020 Covid."""
    baseline_nav = float(instance["initial_capital"])
    target_leverage = float(instance["target_leverage"])
    margin_req = float(instance["margin_requirement"])
    shocks = instance["stress_shocks"]
    names = instance["stress_names"]

    for i in range(len(shocks)):
        spot_shock, vix_shock = shocks[i]
        name = names[i]

        res = stress_test_drawdowns(baseline_nav, spot_shock, vix_shock, target_leverage, margin_req)

        # 1. PnL Conservation: stressed_nav + loss_amount == baseline_nav
        diff_pnl = abs((res["stressed_nav"] + res["loss_amount"]) - baseline_nav)
        assert diff_pnl < 1e-4, f"Scenario {name}: PnL conservation violated"

        # 2. Loss fraction bounds [0, 1]
        assert 0.0 <= res["loss_fraction"] <= 1.0, (
            f"Scenario {name}: Loss fraction {res['loss_fraction']} out of [0, 1]"
        )

        # 3. Margin deficiency logic
        expected_deficiency = max(0.0, res["stressed_margin"] - res["stressed_nav"])
        assert math.isclose(res["margin_deficiency"], expected_deficiency, rel_tol=1e-6), (
            f"Scenario {name}: Margin deficiency mismatch"
        )

    # Shock monotonicity: larger VIX shock produces strictly larger loss amount
    res_mild = stress_test_drawdowns(baseline_nav, -0.05, 10.0, target_leverage, margin_req)
    res_severe = stress_test_drawdowns(baseline_nav, -0.05, 40.0, target_leverage, margin_req)
    assert res_severe["loss_amount"] > res_mild["loss_amount"], "Severe shock must yield larger loss than mild shock"


def test_evaluate_strategy_metrics() -> None:
    """Test performance statistics, Sharpe, Sortino, and higher moments (skewness, kurtosis, TRP)."""
    # Simulated short-vol daily returns: positive mean, negative skewness, heavy kurtosis
    # 20 calm days with small gains (+0.05%), 2 crash days with large losses (-3.5%, -4.0%)
    returns = [0.0005] * 20 + [-0.035, -0.040]

    metrics = evaluate_strategy_metrics(returns, rf_annual=0.02, periods_per_year=252.0)

    # 1. Basic metrics sanity
    assert "mean_return" in metrics
    assert "volatility" in metrics
    assert "sharpe_ratio" in metrics
    assert "sortino_ratio" in metrics
    assert "skewness" in metrics
    assert "excess_kurtosis" in metrics
    assert "tail_risk_penalty" in metrics

    # 2. Asymmetry & Tail Risk
    assert metrics["skewness"] < 0.0, f"Expected negative skewness, got {metrics['skewness']}"
    assert metrics["excess_kurtosis"] > 0.0, f"Expected positive excess kurtosis, got {metrics['excess_kurtosis']}"
    assert metrics["tail_risk_penalty"] > 0.0, (
        f"Expected positive tail risk penalty, got {metrics['tail_risk_penalty']}"
    )

    # 3. Degenerate input handling
    with pytest.raises(ValueError):
        evaluate_strategy_metrics([0.01, 0.02])  # less than 5 returns
    with pytest.raises(ValueError):
        evaluate_strategy_metrics([0.01] * 10)  # zero variance
