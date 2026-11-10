"""Acceptance test suite for MS4 Factor Strategy Capacity Study (capacity.py).

Dual-mode: runs identically in the browser (Pyodide) and locally:
    QF_SEED=<seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Evaluates trade calculation, square-root market impact scaling, capacity limits,
alpha degradation curves, cost mitigation hysteresis, and input validation.
"""

from __future__ import annotations

import importlib
import math
import os
from typing import Any

import pytest
from instance import make_instance

sol: Any
try:
    sol = importlib.import_module("capacity")
except ImportError:
    sol = importlib.import_module("reference")

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST: dict[str, Any] = make_instance(SEED)
INST2: dict[str, Any] = make_instance(SEED + 9973)


def expect(condition: bool, hint: str) -> None:
    """Fail with a descriptive hint if condition is not satisfied."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(hint, pytrace=False)


def test_instance_determinism_and_uniqueness() -> None:
    """Verify instance generation is deterministic and distinct across seeds."""
    i1 = make_instance(42)
    i2 = make_instance(42)
    i3 = make_instance(43)

    expect(i1["w_initial"] == i2["w_initial"], "make_instance is non-deterministic for identical seed")
    expect(i1["w_initial"] != i3["w_initial"], "make_instance produced identical vectors for distinct seeds")
    p_list = i1["prices"]
    assert isinstance(p_list, list)
    expect(len(p_list) == 50, "asset universe size must be 50")


def test_trade_lists_articulation() -> None:
    """Verify trade dollar conservation, share calculations, and turnover definition."""
    w_init = list(INST["w_initial"])
    w_tgt = list(INST["w_target"])
    aum = float(INST["aum_test"])
    prices = list(INST["prices"])

    res = sol.compute_trade_lists(w_init, w_tgt, aum, prices)

    for k in ("dollar_trades", "share_trades", "turnover_dollars", "turnover_fraction"):
        expect(k in res, f"compute_trade_lists missing key '{k}'")

    d_trades = res["dollar_trades"]
    s_trades = res["share_trades"]
    n = len(w_init)
    expect(len(d_trades) == n, "dollar_trades length must match asset count")
    expect(len(s_trades) == n, "share_trades length must match asset count")

    for i in range(n):
        expected_dollar = aum * (w_tgt[i] - w_init[i])
        expect(math.isclose(d_trades[i], expected_dollar, abs_tol=1e-2), f"dollar trade mismatch at index {i}")
        expect(math.isclose(s_trades[i] * prices[i], d_trades[i], abs_tol=1e-2), f"share*price != dollar at {i}")

    one_way_sum = 0.5 * sum(abs(d) for d in d_trades)
    expect(math.isclose(res["turnover_dollars"], one_way_sum, abs_tol=1e-2), "turnover_dollars != half sum |trades|")
    expect(math.isclose(res["turnover_fraction"], one_way_sum / aum, abs_tol=1e-4), "turnover_fraction != turnover/aum")


def test_square_root_impact_scaling() -> None:
    """Verify market impact cost scales as Q^{1.5} per the square-root law."""
    adv = list(INST["adv"])
    sigma = list(INST["sigma"])
    d_trades_base = [100_000.0] * len(adv)
    d_trades_double = [200_000.0] * len(adv)

    res_base = sol.estimate_impact_costs(d_trades_base, adv, sigma, prefactor_y=0.5)
    res_double = sol.estimate_impact_costs(d_trades_double, adv, sigma, prefactor_y=0.5)

    c_base = res_base["total_cost_dollars"]
    c_double = res_double["total_cost_dollars"]

    # Under square-root impact, doubling dollar trade scales cost by 2^{1.5} = 2 * sqrt(2) ≈ 2.828427
    ratio = c_double / c_base
    expected_ratio = 2.0**1.5
    expect(
        math.isclose(ratio, expected_ratio, rel_tol=1e-3),
        f"impact cost scaling ratio was {ratio:.4f}, expected {expected_ratio:.4f} (2^1.5). Linear impact detected.",
    )


def test_capacity_limits_closed_forms() -> None:
    """Verify analytical break-even and profit-maximizing capacity relationships."""
    w_init = list(INST["w_initial"])
    w_tgt = list(INST["w_target"])
    adv = list(INST["adv"])
    sigma = list(INST["sigma"])
    alpha = float(INST["gross_alpha"])

    limits = sol.find_capacity_limits(w_init, w_tgt, adv, sigma, alpha, prefactor_y=0.5)

    for k in ("breakeven_aum", "optimal_aum", "max_dollar_alpha", "net_alpha_at_optimal", "friction_kappa"):
        expect(k in limits, f"find_capacity_limits missing key '{k}'")

    a_star = limits["breakeven_aum"]
    a_opt = limits["optimal_aum"]
    kappa = limits["friction_kappa"]
    max_d_alpha = limits["max_dollar_alpha"]
    net_alpha_opt = limits["net_alpha_at_optimal"]

    # Analytical theorem: A_opt / A* = 4/9 exactly
    ratio = a_opt / a_star
    expect(
        math.isclose(ratio, 4.0 / 9.0, rel_tol=1e-4),
        f"A_opt / A* ratio was {ratio:.5f}, expected 4/9 (0.44444). Incorrect optimality formula.",
    )

    # Net alpha at optimal AUM: exactly alpha_0 / 3
    expect(
        math.isclose(net_alpha_opt, alpha / 3.0, rel_tol=1e-4),
        f"net_alpha_at_optimal was {net_alpha_opt:.5f}, expected alpha/3 = {alpha / 3.0:.5f}",
    )

    # Max dollar alpha: A_opt * (alpha/3)
    expected_max_d = a_opt * (alpha / 3.0)
    expect(
        math.isclose(max_d_alpha, expected_max_d, rel_tol=1e-3),
        f"max_dollar_alpha was {max_d_alpha:.2f}, expected {expected_max_d:.2f}",
    )

    # Break-even check: at A*, net alpha = alpha_0 - kappa * sqrt(A*) = 0
    net_alpha_star = alpha - kappa * math.sqrt(a_star)
    expect(math.isclose(net_alpha_star, 0.0, abs_tol=1e-4), "at breakeven_aum, net alpha does not equal 0.0")


def test_adv_scaling_invariance() -> None:
    """Verify that doubling market ADV scales strategy capacity by exactly 2.0."""
    w_init = list(INST["w_initial"])
    w_tgt = list(INST["w_target"])
    adv_base = list(INST["adv"])
    adv_double = [2.0 * a for a in adv_base]
    sigma = list(INST["sigma"])
    alpha = float(INST["gross_alpha"])

    lim_base = sol.find_capacity_limits(w_init, w_tgt, adv_base, sigma, alpha)
    lim_double = sol.find_capacity_limits(w_init, w_tgt, adv_double, sigma, alpha)

    # Under square-root impact, kappa proportional to 1/sqrt(ADV).
    # Capacity A* = (alpha / kappa)^2 proportional to ADV.
    # Doubling ADV should double A*!
    ratio = lim_double["breakeven_aum"] / lim_base["breakeven_aum"]
    expect(
        math.isclose(ratio, 2.0, rel_tol=1e-3),
        f"capacity did not double when ADV doubled; ratio was {ratio:.4f}. Check ADV exponent in impact law.",
    )


def test_capacity_simulation_monotonicity_and_extrema() -> None:
    """Verify simulated net alpha monotonically decays and dollar alpha peaks at A_opt."""
    w_init = list(INST["w_initial"])
    w_tgt = list(INST["w_target"])
    adv = list(INST["adv"])
    sigma = list(INST["sigma"])
    alpha = float(INST["gross_alpha"])

    limits = sol.find_capacity_limits(w_init, w_tgt, adv, sigma, alpha)
    a_star = limits["breakeven_aum"]
    a_opt = limits["optimal_aum"]

    grid = [0.1 * a_opt, 0.5 * a_opt, a_opt, 0.8 * a_star, a_star, 1.2 * a_star]
    sim = sol.simulate_capacity_curve(grid, w_init, w_tgt, adv, sigma, alpha)

    net_alphas = sim["net_alpha"]
    dollar_alphas = sim["dollar_alpha"]
    cost_bps = sim["cost_bps"]

    # Net alpha must strictly decrease
    for i in range(len(net_alphas) - 1):
        expect(net_alphas[i] > net_alphas[i + 1], f"net_alpha not strictly decreasing at grid step {i}")
        expect(cost_bps[i] < cost_bps[i + 1], f"cost_bps not strictly increasing at grid step {i}")

    # Net alpha at A* should be approximately 0
    idx_star = grid.index(a_star)
    expect(math.isclose(net_alphas[idx_star], 0.0, abs_tol=1e-4), "simulated net alpha at A* must equal 0")

    # Net alpha before A* is positive, after A* is negative
    expect(net_alphas[idx_star - 1] > 0.0, "net alpha before A* must be positive")
    expect(net_alphas[idx_star + 1] < 0.0, "net alpha beyond A* must be negative. Check sign of trading cost.")

    # Dollar alpha peaks at a_opt
    idx_opt = grid.index(a_opt)
    expect(dollar_alphas[idx_opt] > dollar_alphas[idx_opt - 1], "dollar alpha did not increase approaching A_opt")
    expect(dollar_alphas[idx_opt] > dollar_alphas[idx_opt + 1], "dollar alpha did not decrease past A_opt")


def test_buffer_mitigation_turnover_reduction() -> None:
    """Verify that buy-hold buffer zones with hysteresis strictly reduce turnover."""
    ranks = list(INST["ranks"])
    n = len(ranks)
    current_w = [0.0] * n
    # Start with holdings in top 15 ranks
    held_indices = [i for i in range(n) if ranks[i] <= 15]
    for idx in held_indices:
        current_w[idx] = 1.0 / 15.0

    # Perturb ranks slightly (simulate drift)
    drifted_ranks = list(ranks)
    # Move rank 14 to rank 18 (inside buffer 15..22, but outside pure top 15)
    idx_14 = ranks.index(14.0)
    idx_18 = ranks.index(18.0)
    drifted_ranks[idx_14] = 18.0
    drifted_ranks[idx_18] = 14.0

    # Without buffer: buffer_ratio = 1.0 -> will trade out asset 14
    w_no_buffer = sol.mitigate_costs(drifted_ranks, current_w, target_n_assets=15, buffer_ratio=1.0)
    # With buffer: buffer_ratio = 1.5 -> hold threshold is floor(15 * 1.5) = 22 -> asset 14 (rank 18) stays held!
    w_with_buffer = sol.mitigate_costs(drifted_ranks, current_w, target_n_assets=15, buffer_ratio=1.5)

    expect(len(w_no_buffer) == n, "weights length mismatch")
    expect(len(w_with_buffer) == n, "weights length mismatch")
    expect(math.isclose(sum(w_no_buffer), 1.0, abs_tol=1e-5), "no-buffer weights do not sum to 1.0")
    expect(math.isclose(sum(w_with_buffer), 1.0, abs_tol=1e-5), "with-buffer weights do not sum to 1.0")

    turnover_no_buf = 0.5 * sum(abs(w_no_buffer[i] - current_w[i]) for i in range(n))
    turnover_with_buf = 0.5 * sum(abs(w_with_buffer[i] - current_w[i]) for i in range(n))

    expect(
        turnover_with_buf < turnover_no_buf,
        f"buffer failed to reduce turnover: with={turnover_with_buf:.4f}, without={turnover_no_buf:.4f}",
    )
    # The drifted asset at idx_14 should still be held under buffered hysteresis
    expect(w_with_buffer[idx_14] > 1e-4, "buffered portfolio evicted asset whose rank was inside the hold band")


def test_input_validation_and_exceptions() -> None:
    """Verify that invalid inputs raise ValueError with informative messages."""
    w_init = list(INST["w_initial"])
    w_tgt = list(INST["w_target"])
    adv = list(INST["adv"])
    sigma = list(INST["sigma"])

    # Bad AUM <= 0
    with pytest.raises(ValueError):
        sol.compute_trade_lists(w_init, w_tgt, aum=-1000.0, prices=INST["prices"])

    # Bad gross_alpha <= 0
    with pytest.raises(ValueError):
        sol.find_capacity_limits(w_init, w_tgt, adv, sigma, gross_alpha=-0.05)

    # Negative ADV
    bad_adv = list(adv)
    bad_adv[0] = -500.0
    with pytest.raises(ValueError):
        sol.find_capacity_limits(w_init, w_tgt, bad_adv, sigma, gross_alpha=0.10)

    # Mismatched length
    with pytest.raises(ValueError):
        sol.find_capacity_limits(w_init[:-1], w_tgt, adv, sigma, gross_alpha=0.10)

    # Invalid buffer ratio < 1.0
    with pytest.raises(ValueError):
        sol.mitigate_costs(INST["ranks"], w_init, target_n_assets=15, buffer_ratio=0.8)
