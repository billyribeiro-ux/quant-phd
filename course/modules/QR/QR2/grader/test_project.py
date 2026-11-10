"""Acceptance suite for Atlas A9 (atlas.backtest), the QR2 project.

Dual-mode: runs identically in the browser (Pyodide) and locally:
    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py
"""

from __future__ import annotations

import importlib
import math
import os
from collections.abc import Callable
from typing import Any

import numpy as np
import pytest
from instance import make_instance

a9: Any
try:
    a9 = importlib.import_module("atlas.backtest")
except ImportError:
    a9 = importlib.import_module("reference")

Order = a9.Order
OrderSide = a9.OrderSide
OrderType = a9.OrderType
BacktestEngine = a9.BacktestEngine
CostModel = a9.CostModel

pytestmark = pytest.mark.filterwarnings("error")

SEED = int(os.environ.get("QF_SEED", "0"))
INST = make_instance(SEED)
INST2 = make_instance(SEED + 9973)


def expect(condition: bool, hint: str) -> None:
    """Fail with a descriptive hint if condition is false."""
    __tracebackhide__ = True
    if not condition:
        pytest.fail(hint, pytrace=False)


def must_raise(call: Callable[[], object], condition: str) -> None:
    """Check that call() raises ValueError."""
    __tracebackhide__ = True
    try:
        call()
    except ValueError:
        return
    except Exception as exc:
        pytest.fail(f"{condition}: expected ValueError, got {type(exc).__name__}: {exc}", pytrace=False)
    pytest.fail(f"{condition}: expected ValueError, none was raised", pytrace=False)


# -----------------------------------------------------------------------------
# 1. Discrete-Event Data Structures & Cost Models
# -----------------------------------------------------------------------------


def test_order_and_fill_validation() -> None:

    # Valid order
    o = Order(asset="SPY", side=OrderSide.BUY, quantity=100.0, order_type=OrderType.MARKET, submitted_bar=5)
    expect(o.quantity == 100.0, "Order quantity mismatch")
    expect(o.submitted_bar == 5, "Order submitted_bar mismatch")

    # Invariants
    must_raise(
        lambda: Order(asset="SPY", side=OrderSide.BUY, quantity=0.0),
        "Zero quantity order must raise ValueError",
    )
    must_raise(
        lambda: Order(asset="SPY", side=OrderSide.BUY, quantity=-10.0),
        "Negative quantity order must raise ValueError",
    )
    must_raise(
        lambda: Order(asset="SPY", side=OrderSide.BUY, quantity=100.0, submitted_bar=-1),
        "Negative submitted_bar must raise ValueError",
    )
    must_raise(
        lambda: Order(asset="SPY", side=OrderSide.BUY, quantity=100.0, limit_price=-50.0),
        "Negative limit_price must raise ValueError",
    )


def test_cost_model_calculation() -> None:
    cm = CostModel(commission_bps=10.0, half_spread_bps=5.0, impact_coeff=0.5)

    comm, spread, impact = cm.calculate_cost(quantity=1000.0, price=100.0, volume=1_000_000.0, volatility=0.02)
    # Notional = 100,000
    # Commission = 10 bps * 100,000 = 100.0
    expect(abs(comm - 100.0) < 1e-6, f"Expected commission 100.0, got {comm}")
    # Spread = 5 bps * 100,000 = 50.0
    expect(abs(spread - 50.0) < 1e-6, f"Expected spread 50.0, got {spread}")

    # Impact = 1000 * (0.5 * 0.02 * 100.0 * sqrt(1000 / 1e6))
    # = 1000 * (1.0 * sqrt(0.001)) = 1000 * 0.0316227766 = 31.6227766
    expected_impact = 1000.0 * (0.5 * 0.02 * 100.0 * math.sqrt(1000.0 / 1e6))
    expect(abs(impact - expected_impact) < 1e-6, f"Impact calculation error: {impact} vs {expected_impact}")

    # Scaling with quantity (impact scales as q^1.5)
    _comm2, _spread2, impact2 = cm.calculate_cost(quantity=4000.0, price=100.0, volume=1_000_000.0, volatility=0.02)
    # When quantity increases 4x, sqrt(4) = 2, so impact cost increases by 4 * 2 = 8x
    expect(abs(impact2 / impact - 8.0) < 1e-4, f"Impact must scale as q^1.5; ratio was {impact2 / impact}")

    # Validation
    must_raise(lambda: cm.calculate_cost(quantity=-10.0, price=100.0), "Negative quantity must raise")
    must_raise(lambda: cm.calculate_cost(quantity=10.0, price=-100.0), "Negative price must raise")
    must_raise(lambda: cm.calculate_cost(quantity=10.0, price=100.0, volume=-100.0), "Negative volume must raise")


# -----------------------------------------------------------------------------
# 2. Strict Lag Enforcement & Event-Driven Engine
# -----------------------------------------------------------------------------


def test_lag_enforcement_invariants() -> None:

    # Zero lag must be rejected
    must_raise(
        lambda: BacktestEngine(lag_bars=0, min_lag_bars=1),
        "BacktestEngine must reject lag_bars < min_lag_bars (zero lag)",
    )
    must_raise(
        lambda: BacktestEngine(lag_bars=1, min_lag_bars=2),
        "BacktestEngine must reject lag_bars < min_lag_bars",
    )
    must_raise(
        lambda: BacktestEngine(min_lag_bars=0),
        "BacktestEngine must reject min_lag_bars < 1",
    )
    must_raise(
        lambda: BacktestEngine(initial_cash=-1000.0),
        "BacktestEngine must reject non-positive initial_cash",
    )


def test_engine_execution_lag_timing() -> None:
    engine = BacktestEngine(initial_cash=100_000.0, lag_bars=1)

    prices = np.array([100.0, 105.0, 110.0, 115.0, 120.0])
    # Signal appears at bar 0
    signals = np.array([1.0, 1.0, 1.0, 1.0, 1.0])

    res = engine.run(prices, signals)
    expect(len(res.fills) > 0, "Engine must execute orders")
    first_fill = res.fills[0]

    # With lag_bars = 1, order submitted at bar 0 cannot execute before bar 1
    expect(
        first_fill.bar >= 1,
        f"Order submitted at bar 0 must execute at bar >= 1 with lag 1; executed at {first_fill.bar}",
    )
    expect(res.positions[0] == 0.0, "Position at bar 0 must be 0 because lag enforces execution at bar >= 1")


def test_engine_multi_bar_lag() -> None:
    engine = BacktestEngine(initial_cash=100_000.0, lag_bars=2)

    prices = np.array([100.0, 102.0, 104.0, 106.0, 108.0, 110.0])
    signals = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    res = engine.run(prices, signals)
    first_fill = res.fills[0]
    expect(
        first_fill.bar >= 2,
        f"With lag_bars = 2, order submitted at bar 0 cannot execute before bar 2; executed at {first_fill.bar}",
    )
    expect(res.positions[0] == 0.0 and res.positions[1] == 0.0, "Positions at bar 0 and 1 must be 0 with lag 2")


def test_conservation_of_equity_and_cost_deduction() -> None:

    cm = CostModel(commission_bps=0.0, half_spread_bps=0.0, impact_coeff=0.0)
    engine_frictionless = BacktestEngine(initial_cash=100_000.0, lag_bars=1, cost_model=cm)

    prices = np.array([100.0, 100.0, 100.0, 100.0])
    signals = np.array([1.0, 1.0, 1.0, 1.0])

    res = engine_frictionless.run(prices, signals)
    # In frictionless constant price market, equity must remain exactly initial_cash
    expect(
        bool(np.all(np.abs(res.equity - 100_000.0) < 1e-4)),
        "Equity must be conserved in constant price zero friction market",
    )
    expect(res.total_cost == 0.0, "Frictionless run must incur 0 total cost")

    # With costs
    cm_cost = CostModel(commission_bps=10.0, half_spread_bps=5.0, impact_coeff=0.2)
    engine_cost = BacktestEngine(initial_cash=100_000.0, lag_bars=1, cost_model=cm_cost)
    res_cost = engine_cost.run(prices, signals)
    expect(res_cost.total_cost > 0.0, "Cost model must accumulate positive total cost")
    expect(res_cost.equity[-1] < 100_000.0, "Equity must decrease by transaction cost on entry")


# -----------------------------------------------------------------------------
# 3. Walk-Forward Cross-Validation
# -----------------------------------------------------------------------------


def test_walk_forward_splits_properties() -> None:
    wf = a9.walk_forward_splits

    n_samples = 100
    train_size = 40
    test_size = 15
    splits = wf(n_samples=n_samples, train_size=train_size, test_size=test_size, step_size=15)

    expect(len(splits) >= 3, f"Expected at least 3 splits, got {len(splits)}")

    for k, (train_idx, test_idx) in enumerate(splits):
        expect(len(train_idx) == train_size, f"Fold {k}: train size must equal {train_size}")
        expect(len(test_idx) == test_size, f"Fold {k}: test size must equal {test_size}")
        # Strict temporal order: train must precede test
        expect(
            int(train_idx.max()) < int(test_idx.min()),
            f"Fold {k}: max train index ({train_idx.max()}) must be < min test index ({test_idx.min()})",
        )

    # Expanding window
    splits_exp = wf(n_samples=n_samples, train_size=train_size, test_size=test_size, step_size=15, expanding=True)
    for k, (train_idx, test_idx) in enumerate(splits_exp):
        expect(train_idx[0] == 0, f"Expanding window fold {k} must start at index 0")
        expect(
            int(train_idx.max()) < int(test_idx.min()),
            f"Expanding fold {k} must maintain train < test invariant",
        )

    # Invariant validations
    must_raise(lambda: wf(n_samples=50, train_size=40, test_size=20), "train + test > n_samples must raise")
    must_raise(lambda: wf(n_samples=10, train_size=1, test_size=5), "train_size < 2 must raise")
    must_raise(lambda: wf(n_samples=10, train_size=5, test_size=0), "test_size < 1 must raise")


# -----------------------------------------------------------------------------
# 4. Purged and Embargoed Cross-Validation (López de Prado 2018)
# -----------------------------------------------------------------------------


def test_purged_kfold_splits_properties() -> None:
    pkf = a9.purged_kfold_splits

    n_samples = 200
    n_splits = 5
    label_lookahead = 5
    embargo_pct = 0.02  # 4 samples

    splits = pkf(
        n_samples=n_samples,
        n_splits=n_splits,
        label_lookahead=label_lookahead,
        embargo_pct=embargo_pct,
    )
    expect(len(splits) == n_splits, f"Expected {n_splits} splits, got {len(splits)}")

    for k, (train_idx, test_idx) in enumerate(splits):
        test_start = int(test_idx.min())
        test_end = int(test_idx.max()) + 1

        # Check no overlap between train and test
        overlap = np.intersect1d(train_idx, test_idx)
        expect(len(overlap) == 0, f"Fold {k}: train and test must be disjoint")

        # Purge check: no train sample in [test_start - label_lookahead + 1, test_start)
        purged_zone = np.arange(max(0, test_start - label_lookahead + 1), test_start)
        purged_leak = np.intersect1d(train_idx, purged_zone)
        expect(
            len(purged_leak) == 0,
            f"Fold {k}: Purged zone {purged_zone} leaked into training indices!",
        )

        # Embargo check: no train sample in [test_end, test_end + h_embargo)
        h_embargo = math.ceil(embargo_pct * n_samples)
        embargo_zone = np.arange(test_end, min(n_samples, test_end + h_embargo))
        embargo_leak = np.intersect1d(train_idx, embargo_zone)
        expect(
            len(embargo_leak) == 0,
            f"Fold {k}: Embargo zone {embargo_zone} leaked into training indices!",
        )

    # Invariants
    must_raise(lambda: pkf(n_samples=10, n_splits=1), "n_splits < 2 must raise")
    must_raise(lambda: pkf(n_samples=10, label_lookahead=0), "label_lookahead < 1 must raise")
    must_raise(lambda: pkf(n_samples=10, embargo_pct=-0.1), "negative embargo_pct must raise")


# -----------------------------------------------------------------------------
# 5. Combinatorial Purged Cross-Validation (CPCV)
# -----------------------------------------------------------------------------


def test_cpcv_splits_properties() -> None:
    cpcv = a9.cpcv_splits

    n_samples = 120
    n_groups = 6
    k_test_groups = 2
    label_lookahead = 3
    embargo_pct = 0.01

    splits = cpcv(
        n_samples=n_samples,
        n_groups=n_groups,
        k_test_groups=k_test_groups,
        label_lookahead=label_lookahead,
        embargo_pct=embargo_pct,
    )

    expected_combinations = math.comb(n_groups, k_test_groups)  # comb(6, 2) = 15
    expect(
        len(splits) == expected_combinations,
        f"CPCV must yield exactly {expected_combinations} splits, got {len(splits)}",
    )

    for i, (train_idx, test_idx, comb) in enumerate(splits):
        expect(len(comb) == k_test_groups, f"Split {i} combination length mismatch")
        # Ensure disjoint
        expect(len(np.intersect1d(train_idx, test_idx)) == 0, f"Split {i}: train and test must be disjoint")
        # Ensure both are non-empty
        expect(len(train_idx) > 0 and len(test_idx) > 0, f"Split {i}: partitions cannot be empty")


# -----------------------------------------------------------------------------
# 6. Planted-Lookahead Test & Verification
# -----------------------------------------------------------------------------


def test_planted_lookahead_detection() -> None:
    audit_fn = a9.planted_lookahead_audit

    engine = BacktestEngine(initial_cash=INST["initial_cash"], lag_bars=1)
    audit = audit_fn(
        engine=engine,
        prices=INST["prices"],
        legitimate_signal=INST["legitimate_signals"],
        planted_signal=INST["planted_signals"],
    )

    expect(audit["zero_lag_blocked"] is True, "Audit must confirm zero-lag backtesting is strictly blocked")
    expect(
        audit["corr_planted"] > audit["corr_legitimate"],
        (
            f"Planted lookahead correlation ({audit['corr_planted']:.3f}) "
            f"must exceed legitimate ({audit['corr_legitimate']:.3f})"
        ),
    )
    expect(audit["passed_audit"] is True, "Backtest system must pass the planted lookahead audit verification")


# -----------------------------------------------------------------------------
# 7. Seeded Verification & A8 Integrity Attachment
# -----------------------------------------------------------------------------


def test_seeded_backtest_with_integrity_report() -> None:

    cm = CostModel(
        commission_bps=INST["commission_bps"],
        half_spread_bps=INST["half_spread_bps"],
        impact_coeff=INST["impact_coeff"],
    )
    engine = BacktestEngine(initial_cash=INST["initial_cash"], lag_bars=1, cost_model=cm)

    res = engine.run(
        prices=INST["prices"],
        signals=INST["legitimate_signals"],
        volumes=INST["volumes"],
        volatilities=INST["volatilities"],
        trial_returns=INST["trial_returns"],
        selected_trial=INST["selected_trial"],
    )

    expect(len(res.equity) == INST["n_bars"], "Equity curve length must match number of bars")
    expect(len(res.returns) == INST["n_bars"], "Returns array length must match number of bars")
    expect(math.isfinite(res.sharpe_ratio), "Sharpe ratio must be finite")
    expect(res.max_drawdown >= 0.0 and res.max_drawdown <= 1.0, "Max drawdown must lie in [0, 1]")
    expect(res.total_cost >= 0.0, "Total cost must be non-negative")

    # A8 Research integrity report must be attached
    expect(res.integrity is not None, "BacktestResult must attach research integrity report")
    if hasattr(res.integrity, "psr"):
        expect(math.isfinite(res.integrity.psr), "Integrity report PSR must be finite")
        expect(math.isfinite(res.integrity.dsr), "Integrity report DSR must be finite")
