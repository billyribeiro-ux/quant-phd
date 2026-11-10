"""Mutant 4: Planted lookahead audit fails to detect future information leakage."""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from enum import Enum
from typing import Any
import numpy as np


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
        n = len(prices)
        return BacktestResult(
            equity=np.full(n, 100_000.0),
            returns=np.zeros(n),
            positions=np.zeros(n),
            fills=[],
            total_cost=0.0,
            sharpe_ratio=0.0,
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
    indices = np.arange(n_samples, dtype=np.int64)
    fold_bounds = np.linspace(0, n_samples, n_splits + 1, dtype=np.int64)
    h_embargo = int(math.ceil(embargo_pct * n_samples))
    splits = []
    for k in range(n_splits):
        t_start, t_end = fold_bounds[k], fold_bounds[k + 1]
        mask = np.ones(n_samples, dtype=bool)
        mask[t_start:t_end] = False
        mask[max(0, t_start - label_lookahead + 1) : t_start] = False
        mask[t_end : min(n_samples, t_end + h_embargo)] = False
        splits.append((indices[mask], indices[t_start:t_end]))
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
    # BUG: Fails to detect planted lookahead lead correlation and returns passed_audit = False
    return {
        "zero_lag_blocked": True,
        "corr_legitimate": 0.0,
        "corr_planted": 0.0,
        "sharpe_legitimate": 0.0,
        "sharpe_planted": 0.0,
        "lookahead_detected": False,
        "passed_audit": False,
    }
