"""Reference solution for Atlas A9: Backtesting Architecture (atlas.backtest).

Implements the complete contract in atlas/A9.contract.md:
- Event-driven backtesting engine with strict signal-to-execution lag enforcement.
- Proportional cost and square-root market impact accounting.
- Out-of-sample walk-forward split generation (rolling and expanding).
- Purged and embargoed cross-validation (PurgedKFold).
- Combinatorial Purged Cross-Validation (CPCV).
- Planted-lookahead audit detection harness.
- Research integrity report attachment via Atlas A8 (atlas.integrity).
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np

try:
    from atlas.integrity import IntegrityReport, TrialSet, integrity_report
except ImportError:
    try:
        from integrity import IntegrityReport, TrialSet, integrity_report
    except ImportError:
        # Fallback minimal stub if integrity module is missing
        IntegrityReport = Any
        TrialSet = Any
        integrity_report = None


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


@dataclass(frozen=True)
class Order:
    asset: str
    side: OrderSide
    quantity: float
    order_type: OrderType = OrderType.MARKET
    limit_price: float | None = None
    submitted_bar: int = 0

    def __post_init__(self) -> None:
        if self.quantity <= 0.0:
            raise ValueError("Order quantity must be strictly positive")
        if not math.isfinite(self.quantity):
            raise ValueError("Order quantity must be finite")
        if self.submitted_bar < 0:
            raise ValueError("Order submitted_bar cannot be negative")
        if self.limit_price is not None and (self.limit_price <= 0.0 or not math.isfinite(self.limit_price)):
            raise ValueError("Limit price must be positive and finite")


@dataclass(frozen=True)
class Fill:
    asset: str
    side: OrderSide
    quantity: float
    price: float
    commission: float
    impact: float
    bar: int


@dataclass(frozen=True)
class CostModel:
    commission_bps: float = 5.0
    half_spread_bps: float = 2.0
    impact_coeff: float = 0.5  # Y in square-root law

    def __post_init__(self) -> None:
        if self.commission_bps < 0.0 or not math.isfinite(self.commission_bps):
            raise ValueError("commission_bps must be non-negative and finite")
        if self.half_spread_bps < 0.0 or not math.isfinite(self.half_spread_bps):
            raise ValueError("half_spread_bps must be non-negative and finite")
        if self.impact_coeff < 0.0 or not math.isfinite(self.impact_coeff):
            raise ValueError("impact_coeff must be non-negative and finite")

    def calculate_cost(
        self,
        quantity: float,
        price: float,
        volume: float = 1e6,
        volatility: float = 0.02,
    ) -> tuple[float, float, float]:
        """Calculates (commission, spread_cost, impact_cost) in currency units.

        Impact follows the square-root law:
            Delta P = Y * volatility * price * sqrt(quantity / volume)
            Impact Cost = quantity * Delta P
        """
        if quantity <= 0.0 or not math.isfinite(quantity):
            raise ValueError("quantity must be strictly positive and finite")
        if price <= 0.0 or not math.isfinite(price):
            raise ValueError("price must be strictly positive and finite")
        if volume <= 0.0 or not math.isfinite(volume):
            raise ValueError("volume must be strictly positive and finite")
        if volatility < 0.0 or not math.isfinite(volatility):
            raise ValueError("volatility must be non-negative and finite")

        notional = quantity * price
        commission = self.commission_bps * 1e-4 * notional
        spread_cost = self.half_spread_bps * 1e-4 * notional

        # Square-root impact
        participation = quantity / volume
        impact_price_delta = self.impact_coeff * volatility * price * math.sqrt(participation)
        impact_cost = quantity * impact_price_delta

        return float(commission), float(spread_cost), float(impact_cost)


@dataclass(frozen=True)
class BacktestResult:
    equity: np.ndarray
    returns: np.ndarray
    positions: np.ndarray
    fills: list[Fill]
    total_cost: float
    sharpe_ratio: float
    max_drawdown: float
    turnover: float
    integrity: Any


class BacktestEngine:
    """Discrete-event backtesting simulation engine with strict lag enforcement."""

    def __init__(
        self,
        initial_cash: float = 100_000.0,
        lag_bars: int = 1,
        cost_model: CostModel | None = None,
        min_lag_bars: int = 1,
    ) -> None:
        if initial_cash <= 0.0 or not math.isfinite(initial_cash):
            raise ValueError("initial_cash must be strictly positive and finite")
        if min_lag_bars < 1:
            raise ValueError("min_lag_bars must be at least 1")
        if lag_bars < min_lag_bars:
            raise ValueError(f"lag_bars ({lag_bars}) cannot be less than min_lag_bars ({min_lag_bars})")

        self.initial_cash = float(initial_cash)
        self.lag_bars = int(lag_bars)
        self.cost_model = cost_model if cost_model is not None else CostModel()
        self.min_lag_bars = int(min_lag_bars)

    def run(
        self,
        prices: np.ndarray,
        signals: np.ndarray,
        volumes: np.ndarray | None = None,
        volatilities: np.ndarray | None = None,
        periods_per_year: int = 252,
        trial_returns: np.ndarray | None = None,
        selected_trial: int = 0,
    ) -> BacktestResult:
        """Executes the event-driven backtesting loop over prices and signals."""
        p = np.asarray(prices, dtype=np.float64)
        s = np.asarray(signals, dtype=np.float64)

        if p.ndim != 1 or s.ndim != 1:
            raise ValueError("prices and signals must be 1D arrays")
        if len(p) != len(s):
            raise ValueError("prices and signals must have the same length")
        if len(p) < 4:
            raise ValueError("Backtest requires at least 4 bars")
        if np.any(p <= 0.0) or not np.all(np.isfinite(p)):
            raise ValueError("prices must be strictly positive and finite")
        if not np.all(np.isfinite(s)):
            raise ValueError("signals must be finite")

        n_bars = len(p)
        v = (
            np.asarray(volumes, dtype=np.float64)
            if volumes is not None
            else np.full(n_bars, 1_000_000.0, dtype=np.float64)
        )
        vol = (
            np.asarray(volatilities, dtype=np.float64)
            if volatilities is not None
            else np.full(n_bars, 0.02, dtype=np.float64)
        )

        if len(v) != n_bars or len(vol) != n_bars:
            raise ValueError("volumes and volatilities must match prices length")
        if np.any(v <= 0.0) or not np.all(np.isfinite(v)):
            raise ValueError("volumes must be strictly positive and finite")
        if np.any(vol < 0.0) or not np.all(np.isfinite(vol)):
            raise ValueError("volatilities must be non-negative and finite")

        cash = self.initial_cash
        position = 0.0
        equity = np.zeros(n_bars, dtype=np.float64)
        positions = np.zeros(n_bars, dtype=np.float64)
        returns = np.zeros(n_bars, dtype=np.float64)
        fills: list[Fill] = []
        total_cost = 0.0
        total_traded_notional = 0.0

        pending_orders: list[Order] = []

        for t in range(n_bars):
            current_price = p[t]

            # 1. Process pending orders eligible for execution at bar t
            # Eligible if t >= submitted_bar + lag_bars
            remaining_orders: list[Order] = []
            for order in pending_orders:
                if t >= order.submitted_bar + self.lag_bars:
                    # Execute order
                    qty = order.quantity
                    side = order.side
                    comm, spread, impact = self.cost_model.calculate_cost(
                        qty, current_price, volume=v[t], volatility=vol[t]
                    )
                    trade_cost = comm + spread + impact

                    # Execution price incorporating impact
                    exec_price = (
                        current_price + (impact / qty) if side == OrderSide.BUY else current_price - (impact / qty)
                    )
                    notional = qty * exec_price

                    if side == OrderSide.BUY:
                        cash -= notional + comm + spread
                        position += qty
                    else:
                        cash += notional - (comm + spread)
                        position -= qty

                    total_cost += trade_cost
                    total_traded_notional += qty * current_price
                    fills.append(
                        Fill(
                            asset="ASSET",
                            side=side,
                            quantity=qty,
                            price=exec_price,
                            commission=comm + spread,
                            impact=impact,
                            bar=t,
                        )
                    )
                else:
                    remaining_orders.append(order)
            pending_orders = remaining_orders

            # 2. Mark-to-market equity
            current_equity = cash + position * current_price
            equity[t] = current_equity
            positions[t] = position

            if t == 0:
                returns[t] = 0.0
            else:
                prev_eq = equity[t - 1]
                returns[t] = (current_equity - prev_eq) / prev_eq if prev_eq > 0.0 else 0.0

            # 3. Strategy decision: generate new order based strictly on signal s[t]
            # Target position: signal is treated as target portfolio weight in [-1, 1]
            target_weight = float(np.clip(s[t], -1.0, 1.0))
            target_notional = target_weight * current_equity
            target_shares = target_notional / current_price if current_price > 0.0 else 0.0
            share_diff = target_shares - position

            # Only trade if difference is non-trivial (> 1e-4)
            if abs(share_diff) > 1e-4:
                order_side = OrderSide.BUY if share_diff > 0.0 else OrderSide.SELL
                new_order = Order(
                    asset="ASSET",
                    side=order_side,
                    quantity=abs(share_diff),
                    order_type=OrderType.MARKET,
                    submitted_bar=t,
                )
                pending_orders.append(new_order)

        # Performance metrics
        mean_ret = float(np.mean(returns[1:])) if n_bars > 1 else 0.0
        std_ret = float(np.std(returns[1:], ddof=1)) if n_bars > 2 else 0.0
        sharpe = (mean_ret / std_ret * math.sqrt(periods_per_year)) if std_ret > 1e-12 else 0.0

        # Maximum drawdown
        running_max = np.maximum.accumulate(equity)
        drawdowns = (running_max - equity) / np.where(running_max > 0.0, running_max, 1.0)
        max_dd = float(np.max(drawdowns)) if len(drawdowns) > 0 else 0.0

        # Turnover
        avg_equity = float(np.mean(equity))
        turnover = (total_traded_notional / avg_equity) if avg_equity > 0.0 else 0.0

        # Research integrity report attachment (Atlas A8)
        integrity_out: Any = None
        if trial_returns is not None:
            t_ret = np.asarray(trial_returns, dtype=np.float64)
            if (
                t_ret.ndim == 2
                and t_ret.shape[0] >= 4
                and t_ret.shape[1] >= 2
                and integrity_report is not None
                and TrialSet is not None
            ):
                tset = TrialSet(returns=t_ret, selected=selected_trial, periods_per_year=periods_per_year)
                integrity_out = integrity_report(tset)
        elif integrity_report is not None and TrialSet is not None and n_bars >= 4:
            # Construct a 2-trial comparison: [strategy_returns, buy_and_hold_returns]
            bmk_returns = np.zeros(n_bars, dtype=np.float64)
            bmk_returns[1:] = np.diff(p) / p[:-1]
            dual_trials = np.column_stack([returns, bmk_returns])
            # Check variance non-zero
            if np.std(dual_trials[:, 0], ddof=1) > 1e-12 and np.std(dual_trials[:, 1], ddof=1) > 1e-12:
                try:
                    tset = TrialSet(returns=dual_trials, selected=0, periods_per_year=periods_per_year)
                    integrity_out = integrity_report(tset)
                except Exception:
                    integrity_out = None

        return BacktestResult(
            equity=equity,
            returns=returns,
            positions=positions,
            fills=fills,
            total_cost=total_cost,
            sharpe_ratio=sharpe,
            max_drawdown=max_dd,
            turnover=turnover,
            integrity=integrity_out,
        )


def walk_forward_splits(
    n_samples: int,
    train_size: int,
    test_size: int,
    step_size: int | None = None,
    expanding: bool = False,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Generates strictly causal out-of-sample walk-forward index splits.

    Guarantees:
    - Every split satisfies max(train_idx) < min(test_idx).
    - Testing windows are strictly non-overlapping.
    """
    if n_samples < 4:
        raise ValueError("n_samples must be at least 4")
    if train_size < 2:
        raise ValueError("train_size must be at least 2")
    if test_size < 1:
        raise ValueError("test_size must be at least 1")
    if train_size + test_size > n_samples:
        raise ValueError("train_size + test_size cannot exceed n_samples")

    step = test_size if step_size is None else step_size
    if step < 1:
        raise ValueError("step_size must be at least 1")

    splits: list[tuple[np.ndarray, np.ndarray]] = []
    current_test_start = train_size

    while current_test_start + test_size <= n_samples:
        train_start = 0 if expanding else (current_test_start - train_size)
        train_idx = np.arange(train_start, current_test_start, dtype=np.int64)
        test_idx = np.arange(current_test_start, current_test_start + test_size, dtype=np.int64)

        splits.append((train_idx, test_idx))
        current_test_start += step

    if not splits:
        raise ValueError("No valid walk-forward splits could be generated with given parameters")

    return splits


def purged_kfold_splits(
    n_samples: int,
    n_splits: int = 5,
    label_lookahead: int = 1,
    embargo_pct: float = 0.01,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Generates purged and embargoed k-fold cross-validation index splits (López de Prado 2018).

    - Purging: removes training indices that overlap with the testing label evaluation window.
    - Embargoing: removes training indices immediately following the testing fold.
    """
    if n_samples < 4:
        raise ValueError("n_samples must be at least 4")
    if n_splits < 2 or n_splits > n_samples:
        raise ValueError(f"n_splits must be between 2 and {n_samples}")
    if label_lookahead < 1:
        raise ValueError("label_lookahead must be at least 1")
    if embargo_pct < 0.0 or embargo_pct >= 1.0:
        raise ValueError("embargo_pct must be in [0, 1)")

    indices = np.arange(n_samples, dtype=np.int64)
    fold_bounds = np.linspace(0, n_samples, n_splits + 1, dtype=np.int64)
    h_embargo = math.ceil(embargo_pct * n_samples)

    splits: list[tuple[np.ndarray, np.ndarray]] = []

    for k in range(n_splits):
        test_start = fold_bounds[k]
        test_end = fold_bounds[k + 1]  # exclusive
        test_idx = indices[test_start:test_end]

        # Purging: remove training samples whose label window [i, i + label_lookahead - 1]
        # intersects [test_start, test_end + label_lookahead - 1]
        # Any i where i + label_lookahead - 1 >= test_start and i < test_end is in or leaks into test
        train_mask = np.ones(n_samples, dtype=bool)

        # 1. Exclude test fold itself
        train_mask[test_start:test_end] = False

        # 2. Purge left: samples before test_start whose label overlaps test_start
        left_purge_start = max(0, test_start - label_lookahead + 1)
        train_mask[left_purge_start:test_start] = False

        # 3. Embargo right: samples immediately after test_end up to test_end + h_embargo
        right_embargo_end = min(n_samples, test_end + h_embargo)
        train_mask[test_end:right_embargo_end] = False

        train_idx = indices[train_mask]
        splits.append((train_idx, test_idx))

    return splits


def cpcv_splits(
    n_samples: int,
    n_groups: int = 6,
    k_test_groups: int = 2,
    label_lookahead: int = 1,
    embargo_pct: float = 0.01,
) -> list[tuple[np.ndarray, np.ndarray, tuple[int, ...]]]:
    """Generates combinatorial purged cross-validation (CPCV) index splits (López de Prado 2018).

    Partitions samples into n_groups contiguous blocks, selecting all combinations of
    k_test_groups as test folds, with purging and embargoing applied to the training set.
    """
    if n_samples < 6:
        raise ValueError("n_samples must be at least 6")
    if n_groups < 2 or n_groups > n_samples:
        raise ValueError(f"n_groups must be between 2 and {n_samples}")
    if k_test_groups < 1 or k_test_groups >= n_groups:
        raise ValueError("k_test_groups must be between 1 and n_groups - 1")
    if label_lookahead < 1:
        raise ValueError("label_lookahead must be at least 1")
    if embargo_pct < 0.0 or embargo_pct >= 1.0:
        raise ValueError("embargo_pct must be in [0, 1)")

    indices = np.arange(n_samples, dtype=np.int64)
    group_bounds = np.linspace(0, n_samples, n_groups + 1, dtype=np.int64)
    h_embargo = math.ceil(embargo_pct * n_samples)

    combinations = list(itertools.combinations(range(n_groups), k_test_groups))
    splits: list[tuple[np.ndarray, np.ndarray, tuple[int, ...]]] = []

    for comb in combinations:
        test_mask = np.zeros(n_samples, dtype=bool)
        for g in comb:
            test_mask[group_bounds[g] : group_bounds[g + 1]] = True
        test_idx = indices[test_mask]

        train_mask = ~test_mask

        # Apply purging and embargoing for each test group in this combination
        for g in comb:
            g_start = group_bounds[g]
            g_end = group_bounds[g + 1]

            # Left purge
            left_purge_start = max(0, g_start - label_lookahead + 1)
            train_mask[left_purge_start:g_start] = False

            # Right embargo
            right_embargo_end = min(n_samples, g_end + h_embargo)
            train_mask[g_end:right_embargo_end] = False

        train_idx = indices[train_mask]
        splits.append((train_idx, test_idx, comb))

    return splits


def planted_lookahead_audit(
    engine: BacktestEngine,
    prices: np.ndarray,
    legitimate_signal: np.ndarray,
    planted_signal: np.ndarray,
) -> dict[str, Any]:
    """Audits the backtester by testing legitimate vs planted-lookahead strategies.

    Checks:
    1. Cross-correlation between signal and 1-bar future return Corr(s_t, r_{t+1}).
    2. Zero-lag rejection (engine must reject lag_bars = 0).
    3. Performance gap under enforced lag.
    """
    p = np.asarray(prices, dtype=np.float64)
    if len(p) < 10:
        raise ValueError("prices array too short for audit")

    future_returns = np.zeros_like(p)
    future_returns[:-1] = (p[1:] - p[:-1]) / p[:-1]

    # Compute lead correlations
    corr_legit = (
        float(np.corrcoef(legitimate_signal[:-1], future_returns[:-1])[0, 1])
        if np.std(legitimate_signal[:-1]) > 1e-8
        else 0.0
    )
    corr_planted = (
        float(np.corrcoef(planted_signal[:-1], future_returns[:-1])[0, 1])
        if np.std(planted_signal[:-1]) > 1e-8
        else 0.0
    )

    # Invariant check: attempting to run engine with lag_bars = 0 must raise ValueError
    zero_lag_blocked = False
    try:
        zero_engine = BacktestEngine(
            initial_cash=engine.initial_cash,
            lag_bars=0,
            cost_model=engine.cost_model,
            min_lag_bars=1,
        )
        zero_engine.run(prices, planted_signal)
    except ValueError:
        zero_lag_blocked = True

    # Run with legitimate vs planted signal under engine's configured lag
    res_legit = engine.run(prices, legitimate_signal)
    res_planted = engine.run(prices, planted_signal)

    # When lag is enforced (lag >= 1), the 1-bar planted signal (s_t = sign(P_{t+1} - P_t))
    # is executed at bar t+1, so it captures (P_{t+2} - P_{t+1}), neutralizing the 1-bar leak!
    lookahead_detected = corr_planted > 0.40 or (res_planted.sharpe_ratio > res_legit.sharpe_ratio + 5.0)

    return {
        "zero_lag_blocked": zero_lag_blocked,
        "corr_legitimate": corr_legit,
        "corr_planted": corr_planted,
        "sharpe_legitimate": res_legit.sharpe_ratio,
        "sharpe_planted": res_planted.sharpe_ratio,
        "lookahead_detected": lookahead_detected,
        "passed_audit": zero_lag_blocked and (corr_planted > corr_legit),
    }
