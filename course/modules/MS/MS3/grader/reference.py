"""Reference solution for Atlas A10: execution and cost models (atlas.execution).

Provides square-root impact, Almgren-Chriss scheduler, Obizhaeva-Wang dynamics,
and Perold implementation shortfall accounting.
"""

from __future__ import annotations

import math

import numpy as np


def square_root_impact(
    size: float,
    daily_volume: float,
    daily_volatility: float,
    y_coeff: float = 0.5,
) -> float:
    """Compute expected price impact via the square-root law.

    Delta p = sign(Q) * Y * sigma * sqrt(|Q| / V)
    """
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


def temporary_impact(
    rate: float,
    eta: float,
    alpha: float = 1.0,
) -> float:
    """Compute instantaneous temporary price impact h(v) = sign(v) * eta * |v|^alpha."""
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


def permanent_impact(
    size: float,
    gamma: float,
) -> float:
    """Compute permanent price impact g(Q) = gamma * Q."""
    if not math.isfinite(size):
        raise ValueError("size must be a finite number")
    if not math.isfinite(gamma) or gamma < 0.0:
        raise ValueError("gamma must be a finite non-negative number")

    return float(gamma * size)


def almgren_chriss_trajectory(
    total_shares: float,
    horizon: float,
    n_steps: int,
    volatility: float,
    gamma: float,
    eta: float,
    risk_aversion: float,
) -> np.ndarray:
    """Compute the Almgren-Chriss optimal holdings trajectory x_0, ..., x_N.

    x_0 = total_shares, x_N = 0.
    """
    if not math.isfinite(total_shares):
        raise ValueError("total_shares must be a finite number")
    if not math.isfinite(horizon) or horizon <= 0.0:
        raise ValueError("horizon must be a finite positive number")
    if n_steps < 1:
        raise ValueError("n_steps must be at least 1")
    if not math.isfinite(volatility) or volatility < 0.0:
        raise ValueError("volatility must be a finite non-negative number")
    if not math.isfinite(gamma) or gamma < 0.0:
        raise ValueError("gamma must be a finite non-negative number")
    if not math.isfinite(eta) or eta <= 0.0:
        raise ValueError("eta must be a finite positive number")
    if not math.isfinite(risk_aversion) or risk_aversion < 0.0:
        raise ValueError("risk_aversion must be a finite non-negative number")

    tau = horizon / n_steps
    times = np.linspace(0.0, horizon, n_steps + 1, dtype=np.float64)

    if total_shares == 0.0:
        return np.zeros(n_steps + 1, dtype=np.float64)

    if risk_aversion == 0.0 or volatility == 0.0:
        # Linear TWAP trajectory
        return np.array([total_shares * (1.0 - k / n_steps) for k in range(n_steps + 1)], dtype=np.float64)

    # Exact discrete Almgren-Chriss formulation:
    # 2*(cosh(kappa*tau) - 1) = lambda * sigma^2 * tau^2 / eta
    arg = 1.0 + 0.5 * (risk_aversion * (volatility**2) * (tau**2)) / eta
    kappa = math.acosh(arg) / tau

    sinh_kt = math.sinh(kappa * horizon)
    if sinh_kt == 0.0:
        return np.array([total_shares * (1.0 - k / n_steps) for k in range(n_steps + 1)], dtype=np.float64)

    trajectory = np.zeros(n_steps + 1, dtype=np.float64)
    for k in range(n_steps + 1):
        t_k = times[k]
        trajectory[k] = total_shares * math.sinh(kappa * (horizon - t_k)) / sinh_kt

    # Enforce exact boundary condition at terminal step
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
    """Compute total expected execution cost E[x] under linear impact."""
    if not math.isfinite(total_shares):
        raise ValueError("total_shares must be a finite number")
    if len(trajectory) < 2:
        raise ValueError("trajectory must have at least 2 points")
    if not math.isfinite(tau) or tau <= 0.0:
        raise ValueError("tau must be a finite positive number")
    if not math.isfinite(gamma) or gamma < 0.0:
        raise ValueError("gamma must be a finite non-negative number")
    if not math.isfinite(eta) or eta < 0.0:
        raise ValueError("eta must be a finite non-negative number")

    # Trades executed per interval: n_k = x_{k-1} - x_k
    trades = trajectory[:-1] - trajectory[1:]
    perm_cost = 0.5 * gamma * (total_shares**2)
    temp_cost = (eta / tau) * float(np.sum(trades**2))
    return float(perm_cost + temp_cost)


def almgren_chriss_variance(
    trajectory: np.ndarray,
    tau: float,
    volatility: float,
) -> float:
    """Compute total variance of execution cost V[x] = sigma^2 * tau * sum(x_k^2)."""
    if len(trajectory) < 2:
        raise ValueError("trajectory must have at least 2 points")
    if not math.isfinite(tau) or tau <= 0.0:
        raise ValueError("tau must be a finite positive number")
    if not math.isfinite(volatility) or volatility < 0.0:
        raise ValueError("volatility must be a finite non-negative number")

    # Holdings at end of intervals 1 .. N
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
    """Compute efficient execution frontier (expected_costs, variances) across risk aversion array."""
    if len(lambdas) == 0:
        raise ValueError("lambdas array cannot be empty")
    if any(lam < 0.0 for lam in lambdas):
        raise ValueError("risk aversion values must be non-negative")

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
    """Compute Obizhaeva-Wang (2013) optimal execution decomposition (x_0, v_star, x_T).

    Initial block trade: x_0 = X / (2 + rho * T)
    Continuous trading rate: v^* = rho * X / (2 + rho * T)
    Terminal block trade: x_T = X / (2 + rho * T)
    """
    if not math.isfinite(total_shares):
        raise ValueError("total_shares must be a finite number")
    if not math.isfinite(horizon) or horizon <= 0.0:
        raise ValueError("horizon must be a finite positive number")
    if not math.isfinite(resilience) or resilience < 0.0:
        raise ValueError("resilience must be a finite non-negative number")

    denom = 2.0 + resilience * horizon
    x_0 = total_shares / denom
    v_star = (resilience * total_shares) / denom
    x_t = total_shares / denom
    return float(x_0), float(v_star), float(x_t)


def implementation_shortfall(
    decision_price: float,
    arrival_price: float,
    trades: list[tuple[float, float]],
    terminal_price: float,
    target_shares: float,
    fees: float = 0.0,
) -> dict[str, float]:
    """Calculate Perold (1988) implementation shortfall and attribution components.

    Decomposes total shortfall into delay cost, price appreciation (impact),
    opportunity cost of unexecuted shares, and explicit fees.
    """
    if not math.isfinite(target_shares) or target_shares == 0.0:
        raise ValueError("target_shares must be a finite non-zero number")
    if not math.isfinite(decision_price) or decision_price <= 0.0:
        raise ValueError("decision_price must be a finite positive number")
    if not math.isfinite(arrival_price) or arrival_price <= 0.0:
        raise ValueError("arrival_price must be a finite positive number")
    if not math.isfinite(terminal_price) or terminal_price <= 0.0:
        raise ValueError("terminal_price must be a finite positive number")
    if not math.isfinite(fees) or fees < 0.0:
        raise ValueError("fees must be a finite non-negative number")

    sign = 1.0 if target_shares > 0.0 else -1.0
    abs_target = abs(target_shares)

    executed_shares = 0.0
    gross_spend = 0.0
    for q, p in trades:
        if not math.isfinite(q) or not math.isfinite(p):
            raise ValueError("trade shares and prices must be finite numbers")
        if (target_shares > 0.0 and q < 0.0) or (target_shares < 0.0 and q > 0.0):
            raise ValueError("trade share direction must match target_shares")
        if p <= 0.0:
            raise ValueError("trade prices must be positive")
        executed_shares += abs(q)
        gross_spend += abs(q) * p

    if executed_shares > abs_target * (1.0 + 1e-9):
        raise ValueError("executed shares cannot exceed target shares")

    unexecuted_shares = max(0.0, abs_target - executed_shares)
    vwap = (gross_spend / executed_shares) if executed_shares > 0.0 else arrival_price

    # Delay cost: difference between arrival price and decision price on executed volume
    delay_cost = float(sign * executed_shares * (arrival_price - decision_price))

    # Impact cost (trading cost): execution slippage relative to arrival price
    impact_cost = float(sign * (gross_spend - executed_shares * arrival_price))

    # Opportunity cost: unexecuted volume evaluated at terminal price vs decision price
    opportunity_cost = float(sign * unexecuted_shares * (terminal_price - decision_price))

    # Total shortfall
    total_shortfall = float(delay_cost + impact_cost + opportunity_cost + fees)

    # Shortfall in basis points relative to paper decision value
    paper_notional = abs_target * decision_price
    is_bps = float((total_shortfall / paper_notional) * 10_000.0)

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
