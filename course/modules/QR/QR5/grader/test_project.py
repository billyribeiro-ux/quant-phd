"""Acceptance test suite for QR5 project: Deep Hedging vs. Delta Hedging.

Tests mathematical invariants, Black-Scholes limits, Whalley-Wilmott asymptotic width,
convex risk measure properties (CVaR and Entropic risk), hedging P&L cash flow conservation,
and out-of-sample policy execution.
"""

from __future__ import annotations

import math
import os
from typing import Any

import numpy as np
import pytest
from instance import make_instance

try:
    from atlas.hedging import (
        DeepHedger,
        DeltaHedger,
        WhalleyWilmottHedger,
        black_scholes_call_delta,
        black_scholes_call_price,
        black_scholes_gamma,
        compute_hedging_pnl,
        cvar_loss,
        entropic_risk_measure,
        evaluate_hedging_strategies,
        simulate_gbm_paths,
        simulate_jump_diffusion_paths,
        whalley_wilmott_bandwidth,
    )
except ImportError:
    from reference import (
        DeepHedger,
        DeltaHedger,
        WhalleyWilmottHedger,
        black_scholes_call_delta,
        black_scholes_call_price,
        black_scholes_gamma,
        compute_hedging_pnl,
        cvar_loss,
        entropic_risk_measure,
        evaluate_hedging_strategies,
        simulate_gbm_paths,
        simulate_jump_diffusion_paths,
        whalley_wilmott_bandwidth,
    )


@pytest.fixture
def inst() -> dict[str, Any]:
    seed_str = os.environ.get("QF_SEED", os.environ.get("ATLAS_SEED", "0"))
    seed = int(seed_str)
    return make_instance(seed)


def test_simulation_invariants(inst: dict[str, Any]) -> None:
    """Verifies that simulated paths satisfy non-negativity, dimension, and initial value properties."""
    rng = np.random.default_rng(inst["seed"] + 100)
    paths_gbm = simulate_gbm_paths(inst["s0"], inst["mu"], inst["sigma"], inst["t_exp"], inst["n_steps"], 50, rng)
    assert paths_gbm.shape == (50, inst["n_steps"] + 1), "GBM path shape mismatch"
    assert np.all(paths_gbm > 0.0), "Asset prices under GBM must be strictly positive"
    assert np.allclose(paths_gbm[:, 0], inst["s0"]), "GBM paths must start at S0"

    paths_jd = simulate_jump_diffusion_paths(
        inst["s0"],
        inst["mu"],
        inst["sigma"],
        inst["lambda_j"],
        inst["mu_j"],
        inst["sigma_j"],
        inst["t_exp"],
        inst["n_steps"],
        50,
        rng,
    )
    assert paths_jd.shape == (50, inst["n_steps"] + 1), "Jump diffusion path shape mismatch"
    assert np.all(paths_jd > 0.0), "Asset prices under jump diffusion must be strictly positive"
    assert np.allclose(paths_jd[:, 0], inst["s0"]), "Jump diffusion paths must start at S0"


def test_black_scholes_properties(inst: dict[str, Any]) -> None:
    """Verifies Black-Scholes call pricing, delta bounds, and gamma convexity."""
    s_grid = np.linspace(0.85 * inst["strike"], 1.25 * inst["strike"], 30, dtype=np.float64)
    tau_vec = np.full_like(s_grid, inst["t_exp"])

    price = black_scholes_call_price(s_grid, inst["strike"], tau_vec, inst["sigma"], inst["r"])
    delta = black_scholes_call_delta(s_grid, inst["strike"], tau_vec, inst["sigma"], inst["r"])
    gamma = black_scholes_gamma(s_grid, inst["strike"], tau_vec, inst["sigma"], inst["r"])

    # Prices non-negative and monotonically increasing in spot
    assert np.all(price >= 0.0), "Call option prices must be non-negative"
    assert np.all(np.diff(price) > 0.0), "Call option price must be strictly increasing in spot"

    # Call delta strictly bounded in [0, 1] and monotonic
    assert np.all(delta >= 0.0) and np.all(delta <= 1.0), "Call delta must lie in [0, 1]"
    assert np.all(np.diff(delta) > 0.0), "Call delta must be strictly increasing in spot"

    # Gamma non-negative and peaks near at-the-money
    assert np.all(gamma >= 0.0), "Option gamma must be non-negative"
    atm_idx = int(np.argmin(np.abs(s_grid - inst["strike"])))
    peak_idx = int(np.argmax(gamma))
    assert abs(peak_idx - atm_idx) <= 4, "Gamma peak must be located near the strike price"


def test_whalley_wilmott_bandwidth(inst: dict[str, Any]) -> None:
    """Verifies asymptotic scaling of Whalley & Wilmott (1997) no-trade band with eps^(1/3)."""
    s_grid = np.array([inst["s0"]], dtype=np.float64)
    tau_vec = np.array([inst["t_exp"]], dtype=np.float64)

    eps1 = inst["cost_rate"]
    eps2 = 8.0 * eps1  # (8)^(1/3) = 2.0

    bw1 = whalley_wilmott_bandwidth(
        s_grid, inst["strike"], tau_vec, inst["sigma"], inst["r"], eps1, inst["risk_aversion"]
    )
    bw2 = whalley_wilmott_bandwidth(
        s_grid, inst["strike"], tau_vec, inst["sigma"], inst["r"], eps2, inst["risk_aversion"]
    )

    assert bw1[0] > 0.0, "Whalley-Wilmott bandwidth must be strictly positive for positive cost"
    ratio = bw2[0] / bw1[0]
    assert math.isclose(ratio, 2.0, rel_tol=1e-4), f"Bandwidth must scale as eps^(1/3): expected 2.0, got {ratio:.4f}"

    # As tau -> 0, bandwidth must shrink to 0
    bw_zero_tau = whalley_wilmott_bandwidth(
        s_grid, inst["strike"], np.array([0.0]), inst["sigma"], inst["r"], eps1, inst["risk_aversion"]
    )
    assert math.isclose(bw_zero_tau[0], 0.0, abs_tol=1e-6), "Bandwidth must vanish at expiration"


def test_hedging_pnl_accounting(inst: dict[str, Any]) -> None:
    """Verifies cash flow conservation, non-negative transaction costs, and payoff consistency."""
    paths = inst["test_paths"][:30]
    n_paths, n_steps_plus_1 = paths.shape
    n_steps = n_steps_plus_1 - 1

    # Zero hedge holding: delta = 0
    deltas_zero = np.zeros((n_paths, n_steps), dtype=np.float64)
    total_pnl, trading_gains, costs = compute_hedging_pnl(paths, deltas_zero, inst["strike"], inst["cost_rate"])

    assert np.allclose(trading_gains, 0.0), "Zero holding must produce zero trading gains"
    assert np.allclose(costs, 0.0), "Zero holding must incur zero transaction costs"
    expected_payoff = np.maximum(paths[:, -1] - inst["strike"], 0.0)
    assert np.allclose(total_pnl, -expected_payoff), "Zero hedge must yield exactly -payoff"

    # Constant hedge holding: delta = 1.0
    deltas_one = np.ones((n_paths, n_steps), dtype=np.float64)
    _total_pnl_1, trading_gains_1, costs_1 = compute_hedging_pnl(paths, deltas_one, inst["strike"], inst["cost_rate"])

    # Trading gains must equal terminal stock return: S_T - S_0
    assert np.allclose(trading_gains_1, paths[:, -1] - paths[:, 0]), "Delta=1 must replicate underlying stock return"
    # Initiation cost at S_0 and liquidation cost at S_T
    expected_costs = inst["cost_rate"] * paths[:, 0] + inst["cost_rate"] * paths[:, -1]
    assert np.allclose(costs_1, expected_costs), "Transaction costs for buy-and-hold must match S0 and ST friction"


def test_convex_risk_measures() -> None:
    """Verifies monotonicity, translation invariance, and subadditivity of CVaR and Entropic risk."""
    rng = np.random.default_rng(12345)
    losses = rng.normal(5.0, 2.0, size=500)

    # Monotonicity: L2 >= L1 implies rho(L2) >= rho(L1)
    losses_higher = losses + np.abs(rng.normal(1.0, 0.5, size=500))
    cvar_1 = cvar_loss(losses, alpha=0.95)
    cvar_2 = cvar_loss(losses_higher, alpha=0.95)
    assert cvar_2 > cvar_1, "CVaR must be strictly monotonic"

    ent_1 = entropic_risk_measure(losses, risk_aversion=1.0)
    ent_2 = entropic_risk_measure(losses_higher, risk_aversion=1.0)
    assert ent_2 > ent_1, "Entropic risk measure must be strictly monotonic"

    # Translation invariance: rho(L + c) = rho(L) + c
    c = 3.5
    assert math.isclose(cvar_loss(losses + c, alpha=0.95), cvar_1 + c, rel_tol=1e-5), (
        "CVaR must be translation invariant"
    )
    assert math.isclose(entropic_risk_measure(losses + c, risk_aversion=1.0), ent_1 + c, rel_tol=1e-5), (
        "Entropic risk must be translation invariant"
    )

    # CVaR exceeds mean loss and matches tail expectation on discrete spike
    assert cvar_1 >= float(np.mean(losses)) + 1.5, "CVaR must significantly exceed mean loss for positive tail variance"
    test_spike = np.array([1.0, 2.0, 3.0, 20.0], dtype=np.float64)
    assert math.isclose(cvar_loss(test_spike, alpha=0.75), 20.0, rel_tol=1e-5), "CVaR must isolate upper tail quantile"


def test_delta_vs_whalley_wilmott(inst: dict[str, Any]) -> None:
    """Verifies that Whalley-Wilmott significantly reduces trading turnover and transaction costs."""
    paths = inst["test_paths"]
    delta_hedger = DeltaHedger(inst["strike"], inst["t_exp"], inst["sigma"], inst["r"])
    ww_hedger = WhalleyWilmottHedger(
        inst["strike"], inst["t_exp"], inst["sigma"], inst["r"], inst["cost_rate"], inst["risk_aversion"]
    )

    deltas_bs = delta_hedger.compute_deltas(paths)
    deltas_ww = ww_hedger.compute_deltas(paths)

    _, _, costs_bs = compute_hedging_pnl(paths, deltas_bs, inst["strike"], inst["cost_rate"])
    _, _, costs_ww = compute_hedging_pnl(paths, deltas_ww, inst["strike"], inst["cost_rate"])

    turnover_bs = np.mean(np.sum(np.abs(np.diff(deltas_bs, axis=1)), axis=1))
    turnover_ww = np.mean(np.sum(np.abs(np.diff(deltas_ww, axis=1)), axis=1))

    assert turnover_ww < turnover_bs, (
        f"Whalley-Wilmott turnover ({turnover_ww:.4f}) must be lower than Delta Hedging ({turnover_bs:.4f})"
    )
    assert np.mean(costs_ww) < np.mean(costs_bs), (
        f"Whalley-Wilmott costs ({np.mean(costs_ww):.4f}) must be less than Delta Hedging ({np.mean(costs_bs):.4f})"
    )


def test_deep_hedging_optimization(inst: dict[str, Any]) -> None:
    """Verifies that the DeepHedger policy produces bounded deltas and optimizes convex risk."""
    train_sub = inst["train_paths"][:120]
    dh = DeepHedger(
        inst["strike"],
        inst["t_exp"],
        inst["n_steps"],
        inst["sigma"],
        inst["r"],
        inst["cost_rate"],
        hidden_dim=12,
        seed=inst["seed"],
    )

    init_deltas = dh.compute_deltas(train_sub)
    assert np.all(init_deltas >= 0.0) and np.all(init_deltas <= 1.0), "DeepHedger deltas must be bounded in [0, 1]"

    learning_rate = 0.008 / max(inst["risk_aversion"], 1.0)
    history = dh.fit(train_sub, epochs=15, lr=learning_rate, risk_aversion=inst["risk_aversion"])
    assert len(history) == 15, "Optimization history must record each epoch"
    assert history[-1] < history[0], (
        f"Deep hedging training must reduce risk objective: initial={history[0]:.4f}, final={history[-1]:.4f}"
    )


def test_evaluation_pipeline(inst: dict[str, Any]) -> None:
    """Verifies that the multi-strategy evaluation pipeline produces coherent comparative metrics."""
    test_sub = inst["test_paths"][:80]
    dh = DeepHedger(
        inst["strike"],
        inst["t_exp"],
        inst["n_steps"],
        inst["sigma"],
        inst["r"],
        inst["cost_rate"],
        hidden_dim=12,
        seed=inst["seed"],
    )
    dh.fit(inst["train_paths"][:100], epochs=8, lr=0.03, risk_aversion=inst["risk_aversion"])

    eval_results = evaluate_hedging_strategies(
        test_sub,
        inst["strike"],
        inst["t_exp"],
        inst["sigma"],
        inst["r"],
        inst["cost_rate"],
        inst["risk_aversion"],
        dh,
        alpha=inst["alpha"],
    )

    for strategy in ("DeltaHedging", "WhalleyWilmott", "DeepHedging"):
        assert strategy in eval_results, f"Evaluation must include {strategy}"
        metrics = eval_results[strategy]
        for key in ("mean_pnl", "std_pnl", "cvar_95", "entropic_risk", "mean_costs", "total_turnover"):
            assert key in metrics, f"Metric {key} missing from {strategy}"
            assert math.isfinite(metrics[key]), f"Metric {key} in {strategy} must be finite"
