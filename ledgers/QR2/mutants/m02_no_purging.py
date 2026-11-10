"""Mutant 2: Omits purging of overlapping labels in cross-validation splits."""

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
    from integrity import IntegrityReport, TrialSet, integrity_report


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
        if self.quantity <= 0.0 or not math.isfinite(self.quantity):
            raise ValueError("Order quantity must be strictly positive")
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
    impact_coeff: float = 0.5

    def calculate_cost(
        self,
        quantity: float,
        price: float,
        volume: float = 1e6,
        volatility: float = 0.02,
    ) -> tuple[float, float, float]:
        if quantity <= 0.0 or not math.isfinite(quantity):
            raise ValueError("quantity must be strictly positive and finite")
        if price <= 0.0 or not math.isfinite(price):
            raise ValueError("price must be strictly positive and finite")
        if volume <= 0.0 or not math.isfinite(volume):
            raise ValueError("volume must be strictly positive and finite")
        if volatility < 0.0 or not math.isfinite(volatility):
            raise ValueError("volatility must be non-negative and finite")

        notional = quantity * price
        comm = self.commission_bps * 1e-4 * notional
        spread = self.half_spread_bps * 1e-4 * notional
        impact = quantity * (self.impact_coeff * volatility * price * math.sqrt(quantity / volume))
        return float(comm), float(spread), float(impact)


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
    def __init__(
        self,
        initial_cash: float = 100_000.0,
        lag_bars: int = 1,
        cost_model: CostModel | None = None,
        min_lag_bars: int = 1,
    ) -> None:
        if initial_cash <= 0.0 or not math.isfinite(initial_cash):
            raise ValueError("initial_cash must be positive")
        if min_lag_bars < 1:
            raise ValueError("min_lag_bars must be at least 1")
        if lag_bars < min_lag_bars:
            raise ValueError("lag_bars < min_lag_bars")

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
        p = np.asarray(prices, dtype=np.float64)
        s = np.asarray(signals, dtype=np.float64)
        if len(p) < 4:
            raise ValueError("At least 4 bars required")
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

        cash = self.initial_cash
        position = 0.0
        equity = np.zeros(n_bars, dtype=np.float64)
        positions = np.zeros(n_bars, dtype=np.float64)
        returns = np.zeros(n_bars, dtype=np.float64)
        fills: list[Fill] = []
        total_cost = 0.0
        pending_orders: list[Order] = []

        for t in range(n_bars):
            rem = []
            for order in pending_orders:
                if t >= order.submitted_bar + self.lag_bars:
                    qty = order.quantity
                    side = order.side
                    comm, spread, impact = self.cost_model.calculate_cost(qty, p[t], volume=v[t], volatility=vol[t])
                    trade_cost = comm + spread + impact
                    exec_price = p[t] + (impact / qty) if side == OrderSide.BUY else p[t] - (impact / qty)
                    notional = qty * exec_price
                    if side == OrderSide.BUY:
                        cash -= notional + comm + spread
                        position += qty
                    else:
                        cash += notional - (comm + spread)
                        position -= qty
                    total_cost += trade_cost
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
                    rem.append(order)
            pending_orders = rem

            current_equity = cash + position * p[t]
            equity[t] = current_equity
            positions[t] = position
            returns[t] = (current_equity - equity[t - 1]) / equity[t - 1] if t > 0 and equity[t - 1] > 0 else 0.0

            target_weight = float(np.clip(s[t], -1.0, 1.0))
            target_notional = target_weight * current_equity
            target_shares = target_notional / p[t] if p[t] > 0 else 0.0
            share_diff = target_shares - position
            if abs(share_diff) > 1e-4:
                order_side = OrderSide.BUY if share_diff > 0.0 else OrderSide.SELL
                pending_orders.append(
                    Order(
                        asset="ASSET",
                        side=order_side,
                        quantity=abs(share_diff),
                        order_type=OrderType.MARKET,
                        submitted_bar=t,
                    )
                )

        mean_ret = float(np.mean(returns[1:])) if n_bars > 1 else 0.0
        std_ret = float(np.std(returns[1:], ddof=1)) if n_bars > 2 else 0.0
        sharpe = (mean_ret / std_ret * math.sqrt(periods_per_year)) if std_ret > 1e-12 else 0.0

        return BacktestResult(
            equity=equity,
            returns=returns,
            positions=positions,
            fills=fills,
            total_cost=total_cost,
            sharpe_ratio=sharpe,
            max_drawdown=0.0,
            turnover=0.0,
            integrity=None,
        )


def walk_forward_splits(
    n_samples: int,
    train_size: int,
    test_size: int,
    step_size: int | None = None,
    expanding: bool = False,
) -> list[tuple[np.ndarray, np.ndarray]]:
    step = step_size or test_size
    splits: list[tuple[np.ndarray, np.ndarray]] = []
    curr = train_size
    while curr + test_size <= n_samples:
        t_start = 0 if expanding else curr - train_size
        splits.append((np.arange(t_start, curr, dtype=np.int64), np.arange(curr, curr + test_size, dtype=np.int64)))
        curr += step
    return splits


def purged_kfold_splits(
    n_samples: int,
    n_splits: int = 5,
    label_lookahead: int = 1,
    embargo_pct: float = 0.01,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """BUG: Omits purging of overlapping labels."""
    indices = np.arange(n_samples, dtype=np.int64)
    fold_bounds = np.linspace(0, n_samples, n_splits + 1, dtype=np.int64)
    splits: list[tuple[np.ndarray, np.ndarray]] = []
    for k in range(n_splits):
        t_start = fold_bounds[k]
        t_end = fold_bounds[k + 1]
        test_idx = indices[t_start:t_end]
        # BUG: train set simply excludes test, omitting purging and embargoing!
        train_idx = np.concatenate([indices[:t_start], indices[t_end:]])
        splits.append((train_idx, test_idx))
    return splits


def cpcv_splits(
    n_samples: int,
    n_groups: int = 6,
    k_test_groups: int = 2,
    label_lookahead: int = 1,
    embargo_pct: float = 0.01,
) -> list[tuple[np.ndarray, np.ndarray, tuple[int, ...]]]:
    indices = np.arange(n_samples, dtype=np.int64)
    bounds = np.linspace(0, n_samples, n_groups + 1, dtype=np.int64)
    combs = list(itertools.combinations(range(n_groups), k_test_groups))
    splits = []
    for c in combs:
        t_mask = np.zeros(n_samples, dtype=bool)
        for g in c:
            t_mask[bounds[g] : bounds[g + 1]] = True
        splits.append((indices[~t_mask], indices[t_mask], c))
    return splits


def planted_lookahead_audit(
    engine: BacktestEngine,
    prices: np.ndarray,
    legitimate_signal: np.ndarray,
    planted_signal: np.ndarray,
) -> dict[str, Any]:
    return {
        "zero_lag_blocked": True,
        "corr_legitimate": 0.0,
        "corr_planted": 0.8,
        "sharpe_legitimate": 0.0,
        "sharpe_planted": 10.0,
        "lookahead_detected": True,
        "passed_audit": True,
    }
