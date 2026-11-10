"""Starter template for Atlas A9: Backtesting Architecture (atlas.backtest).

Students implement this module to build the event-driven backtesting engine,
lag enforcement, transaction cost models, and cross-validation splits.
"""

from __future__ import annotations

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
        raise NotImplementedError("Implement CostModel.calculate_cost")


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
        raise NotImplementedError("Implement BacktestEngine.__init__")

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
        raise NotImplementedError("Implement BacktestEngine.run")


def walk_forward_splits(
    n_samples: int,
    train_size: int,
    test_size: int,
    step_size: int | None = None,
    expanding: bool = False,
) -> list[tuple[np.ndarray, np.ndarray]]:
    raise NotImplementedError("Implement walk_forward_splits")


def purged_kfold_splits(
    n_samples: int,
    n_splits: int = 5,
    label_lookahead: int = 1,
    embargo_pct: float = 0.01,
) -> list[tuple[np.ndarray, np.ndarray]]:
    raise NotImplementedError("Implement purged_kfold_splits")


def cpcv_splits(
    n_samples: int,
    n_groups: int = 6,
    k_test_groups: int = 2,
    label_lookahead: int = 1,
    embargo_pct: float = 0.01,
) -> list[tuple[np.ndarray, np.ndarray, tuple[int, ...]]]:
    raise NotImplementedError("Implement cpcv_splits")


def planted_lookahead_audit(
    engine: BacktestEngine,
    prices: np.ndarray,
    legitimate_signal: np.ndarray,
    planted_signal: np.ndarray,
) -> dict[str, Any]:
    raise NotImplementedError("Implement planted_lookahead_audit")
