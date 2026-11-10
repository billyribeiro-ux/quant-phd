"""Wrong sign mutant: computes negative permanent impact on buys and positive on sells."""

from __future__ import annotations

import math

import numpy as np


def square_root_impact(
    size: float,
    daily_volume: float,
    daily_volatility: float,
    y_coeff: float = 0.5,
) -> float:
    if not math.isfinite(size):
        raise ValueError("size must be a finite number")
    if not math.isfinite(daily_volume) or daily_volume <= 0.0:
        raise ValueError("daily_volume must be a finite positive number")
    if not math.isfinite(daily_volatility) or daily_volatility < 0.0:
        raise ValueError("daily_volatility must be a finite non-negative number")
    if not math.isfinite(y_coeff) or y_coeff <= 0.0:
        raise ValueError("y_coeff must be a finite positive number")
    if size == 0.0:
        return 0.0
    sign = 1.0 if size > 0.0 else -1.0
    return float(sign * y_coeff * daily_volatility * math.sqrt(abs(size) / daily_volume))


def temporary_impact(rate: float, eta: float, alpha: float = 1.0) -> float:
    if not math.isfinite(rate):
        raise ValueError("rate must be a finite number")
    if not math.isfinite(eta) or eta < 0.0:
        raise ValueError("eta must be a finite non-negative number")
    if not math.isfinite(alpha) or alpha <= 0.0:
        raise ValueError("alpha must be a finite positive number")
    if rate == 0.0 or eta == 0.0:
        return 0.0
    sign = 1.0 if rate > 0.0 else -1.0
    return float(sign * eta * (abs(rate) ** alpha))


def permanent_impact(size: float, gamma: float) -> float:
    if not math.isfinite(size):
        raise ValueError("size must be a finite number")
    if not math.isfinite(gamma) or gamma < 0.0:
        raise ValueError("gamma must be a finite non-negative number")
    # BUG: Wrong sign on permanent impact
    return float(-gamma * size)


def almgren_chriss_trajectory(
    total_shares: float,
    horizon: float,
    n_steps: int,
    volatility: float,
    gamma: float,
    eta: float,
    risk_aversion: float,
) -> np.ndarray:
    if not math.isfinite(total_shares) or horizon <= 0.0 or n_steps < 1:
        raise ValueError("invalid arguments")
    if volatility < 0.0 or gamma < 0.0 or eta <= 0.0 or risk_aversion < 0.0:
        raise ValueError("invalid arguments")
    tau = horizon / n_steps
    times = np.linspace(0.0, horizon, n_steps + 1, dtype=np.float64)
    if total_shares == 0.0:
        return np.zeros(n_steps + 1, dtype=np.float64)
    if risk_aversion == 0.0 or volatility == 0.0:
        return np.array([total_shares * (1.0 - k / n_steps) for k in range(n_steps + 1)], dtype=np.float64)
    arg = 1.0 + 0.5 * (risk_aversion * (volatility**2) * (tau**2)) / eta
    kappa = math.acosh(arg) / tau
    sinh_kt = math.sinh(kappa * horizon)
    if sinh_kt == 0.0:
        return np.array([total_shares * (1.0 - k / n_steps) for k in range(n_steps + 1)], dtype=np.float64)
    trajectory = np.zeros(n_steps + 1, dtype=np.float64)
    for k in range(n_steps + 1):
        trajectory[k] = total_shares * math.sinh(kappa * (horizon - times[k])) / sinh_kt
    trajectory[-1] = 0.0
    trajectory[0] = total_shares
    return trajectory


def almgren_chriss_expected_cost(
    total_shares: float,
    trajectory: np.ndarray,
    tau: float,
    gamma: float,
    eta: float,
) -> float:
    if not math.isfinite(total_shares) or len(trajectory) < 2 or tau <= 0.0 or gamma < 0.0 or eta < 0.0:
        raise ValueError("invalid arguments")
    trades = trajectory[:-1] - trajectory[1:]
    perm_cost = 0.5 * gamma * (total_shares**2)
    temp_cost = (eta / tau) * float(np.sum(trades**2))
    return float(perm_cost + temp_cost)


def almgren_chriss_variance(trajectory: np.ndarray, tau: float, volatility: float) -> float:
    if len(trajectory) < 2 or tau <= 0.0 or volatility < 0.0:
        raise ValueError("invalid arguments")
    holdings = trajectory[1:]
    return float((volatility**2) * tau * np.sum(holdings**2))


def efficient_frontier(
    total_shares: float,
    horizon: float,
    n_steps: int,
    volatility: float,
    gamma: float,
    eta: float,
    lambdas: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    tau = horizon / n_steps
    expected_costs = np.zeros(len(lambdas), dtype=np.float64)
    variances = np.zeros(len(lambdas), dtype=np.float64)
    for i, lam in enumerate(lambdas):
        traj = almgren_chriss_trajectory(total_shares, horizon, n_steps, volatility, gamma, eta, float(lam))
        expected_costs[i] = almgren_chriss_expected_cost(total_shares, traj, tau, gamma, eta)
        variances[i] = almgren_chriss_variance(traj, tau, volatility)
    return expected_costs, variances


def obizhaeva_wang_trajectory(
    total_shares: float,
    horizon: float,
    resilience: float,
) -> tuple[float, float, float]:
    if not math.isfinite(total_shares) or horizon <= 0.0 or resilience < 0.0:
        raise ValueError("invalid arguments")
    denom = 2.0 + resilience * horizon
    return float(total_shares / denom), float((resilience * total_shares) / denom), float(total_shares / denom)


def implementation_shortfall(
    decision_price: float,
    arrival_price: float,
    trades: list[tuple[float, float]],
    terminal_price: float,
    target_shares: float,
    fees: float = 0.0,
) -> dict[str, float]:
    if not math.isfinite(target_shares) or target_shares == 0.0:
        raise ValueError("target_shares must be non-zero")
    if decision_price <= 0.0 or arrival_price <= 0.0 or terminal_price <= 0.0 or fees < 0.0:
        raise ValueError("invalid price or fees")
    sign = 1.0 if target_shares > 0.0 else -1.0
    abs_target = abs(target_shares)
    executed_shares = 0.0
    gross_spend = 0.0
    for q, p in trades:
        if p <= 0.0:
            raise ValueError("trade price must be positive")
        executed_shares += abs(q)
        gross_spend += abs(q) * p
    if executed_shares > abs_target * (1.0 + 1e-9):
        raise ValueError("executed shares exceeds target")
    unexecuted_shares = max(0.0, abs_target - executed_shares)
    vwap = (gross_spend / executed_shares) if executed_shares > 0.0 else arrival_price
    delay_cost = float(sign * executed_shares * (arrival_price - decision_price))
    impact_cost = float(sign * (gross_spend - executed_shares * arrival_price))
    opportunity_cost = float(sign * unexecuted_shares * (terminal_price - decision_price))
    total_shortfall = float(delay_cost + impact_cost + opportunity_cost + fees)
    is_bps = float((total_shortfall / (abs_target * decision_price)) * 10_000.0)
    return {
        "total_shortfall": total_shortfall,
        "delay_cost": delay_cost,
        "impact_cost": impact_cost,
        "opportunity_cost": opportunity_cost,
        "fees": float(fees),
        "executed_shares": float(executed_shares * sign),
        "unexecuted_shares": float(unexecuted_shares * sign),
        "vwap": float(vwap),
        "is_bps": is_bps,
    }
