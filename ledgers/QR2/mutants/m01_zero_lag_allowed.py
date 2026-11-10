"""Mutant 1: Allows execution on the same bar as signal generation (zero lag allowed)."""

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
        IntegrityReport = Any  # type: ignore[misc, assignment]
        TrialSet = Any  # type: ignore[misc, assignment]
        integrity_report = None  # type: ignore[assignment]


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
        lag_bars: int = 0,
        cost_model: CostModel | None = None,
        min_lag_bars: int = 0,
    ) -> None:
        # BUG: does not enforce min_lag_bars >= 1, allows lag_bars = 0
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

        for t in range(n_bars):
            # BUG: executes orders generated at bar t immediately on bar t!
            target_weight = float(np.clip(s[t], -1.0, 1.0))
            current_equity = cash + position * p[t]
            target_shares = (target_weight * current_equity) / p[t]
            share_diff = target_shares - position

            if abs(share_diff) > 1e-4:
                side = OrderSide.BUY if share_diff > 0.0 else OrderSide.SELL
                qty = abs(share_diff)
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

            current_equity = cash + position * p[t]
            equity[t] = current_equity
            positions[t] = position
            returns[t] = (current_equity - equity[t - 1]) / equity[t - 1] if t > 0 and equity[t - 1] > 0 else 0.0

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
    from reference import walk_forward_splits as ref_wf

    return ref_wf(n_samples, train_size, test_size, step_size, expanding)


def purged_kfold_splits(
    n_samples: int,
    n_splits: int = 5,
    label_lookahead: int = 1,
    embargo_pct: float = 0.01,
) -> list[tuple[np.ndarray, np.ndarray]]:
    from reference import purged_kfold_splits as ref_pkf

    return ref_pkf(n_samples, n_splits, label_lookahead, embargo_pct)


def cpcv_splits(
    n_samples: int,
    n_groups: int = 6,
    k_test_groups: int = 2,
    label_lookahead: int = 1,
    embargo_pct: float = 0.01,
) -> list[tuple[np.ndarray, np.ndarray, tuple[int, ...]]]:
    from reference import cpcv_splits as ref_cpcv

    return ref_cpcv(n_samples, n_groups, k_test_groups, label_lookahead, embargo_pct)


def planted_lookahead_audit(
    engine: BacktestEngine,
    prices: np.ndarray,
    legitimate_signal: np.ndarray,
    planted_signal: np.ndarray,
) -> dict[str, Any]:
    from reference import planted_lookahead_audit as ref_audit

    return ref_audit(engine, prices, legitimate_signal, planted_signal)
