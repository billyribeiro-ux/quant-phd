"""Student error: returns N(d1) for put delta instead of N(d1) - 1."""

from __future__ import annotations

import math
import random
from typing import Any


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bs_price(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    is_call: bool = True,
) -> float:
    """Analytical Black-Scholes price for European options."""
    if spot <= 0.0:
        raise ValueError("Spot price must be strictly positive.")
    if strike <= 0.0:
        raise ValueError("Strike price must be strictly positive.")
    if vol <= 0.0:
        raise ValueError("Volatility must be strictly positive.")
    if maturity < 0.0:
        raise ValueError("Maturity cannot be negative.")

    if maturity <= 1e-12:
        return max(spot - strike, 0.0) if is_call else max(strike - spot, 0.0)

    sq_tau = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol**2) * maturity) / (vol * sq_tau)
    d2 = d1 - vol * sq_tau
    df = math.exp(-rate * maturity)

    if is_call:
        return spot * norm_cdf(d1) - strike * df * norm_cdf(d2)
    return strike * df * norm_cdf(-d2) - spot * norm_cdf(-d1)


def bs_delta(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    is_call: bool = True,
) -> float:
    """Analytical Black-Scholes Delta sensitivity."""
    if spot <= 0.0 or strike <= 0.0 or vol <= 0.0 or maturity < 0.0:
        raise ValueError("Invalid parameters for Delta.")

    if maturity <= 1e-12:
        if is_call:
            return 1.0 if spot > strike else 0.0
        return -1.0 if spot < strike else 0.0

    sq_tau = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol**2) * maturity) / (vol * sq_tau)
    if is_call:
        return norm_cdf(d1)
    return norm_cdf(d1)


def bs_gamma(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
) -> float:
    """Analytical Black-Scholes Gamma sensitivity."""
    if spot <= 0.0 or strike <= 0.0 or vol <= 0.0 or maturity < 0.0:
        raise ValueError("Invalid parameters for Gamma.")

    if maturity <= 1e-12:
        return 0.0

    sq_tau = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol**2) * maturity) / (vol * sq_tau)
    return norm_pdf(d1) / (spot * vol * sq_tau)


def bs_theta(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    is_call: bool = True,
) -> float:
    """Analytical Black-Scholes Theta sensitivity (calendar time derivative d_t V)."""
    if spot <= 0.0 or strike <= 0.0 or vol <= 0.0 or maturity < 0.0:
        raise ValueError("Invalid parameters for Theta.")

    if maturity <= 1e-12:
        return 0.0

    sq_tau = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol**2) * maturity) / (vol * sq_tau)
    d2 = d1 - vol * sq_tau
    pdf_d1 = norm_pdf(d1)
    df = math.exp(-rate * maturity)

    term1 = -(spot * pdf_d1 * vol) / (2.0 * sq_tau)
    if is_call:
        return term1 - rate * strike * df * norm_cdf(d2)
    return term1 + rate * strike * df * norm_cdf(-d2)


def simulate_paths(
    spot: float,
    rate: float,
    vol: float,
    maturity: float,
    steps: int,
    n_paths: int,
    seed: int,
) -> list[list[float]]:
    """Simulate geometric Brownian motion price paths under the risk-neutral measure Q."""
    if spot <= 0.0 or vol <= 0.0 or maturity <= 0.0 or steps <= 0 or n_paths <= 0:
        raise ValueError("Invalid simulation arguments.")

    dt = maturity / steps
    drift = (rate - 0.5 * vol**2) * dt
    vol_step = vol * math.sqrt(dt)

    rng = random.Random(seed)
    paths: list[list[float]] = []

    for _ in range(n_paths):
        path = [spot]
        s = spot
        for _ in range(steps):
            z = rng.gauss(0.0, 1.0)
            s = s * math.exp(drift + vol_step * z)
            path.append(s)
        paths.append(path)

    return paths


def delta_hedging_pnl(
    paths: list[list[float]],
    strike: float,
    rate: float,
    vol_implied: float,
    maturity: float,
    cost_rate: float = 0.0,
    is_call: bool = True,
) -> dict[str, Any]:
    """Simulate discrete delta-hedged short option book along given price paths."""
    if not paths or len(paths[0]) < 2:
        raise ValueError("Paths must contain at least 2 points.")
    if strike <= 0.0 or vol_implied <= 0.0 or maturity <= 0.0 or cost_rate < 0.0:
        raise ValueError("Invalid hedging parameters.")

    n_paths = len(paths)
    steps = len(paths[0]) - 1
    dt = maturity / steps
    df_step = math.exp(rate * dt)

    s0 = paths[0][0]
    c0 = bs_price(s0, strike, rate, vol_implied, maturity, is_call)

    pnls: list[float] = []
    costs: list[float] = []

    for path in paths:
        s = path[0]
        delta = bs_delta(s, strike, rate, vol_implied, maturity, is_call)
        cash = c0 - delta * s
        tot_cost = 0.0

        for step in range(1, steps):
            s_next = path[step]
            cash = cash * df_step

            tau_rem = max(maturity - step * dt, 1e-12)
            delta_new = bs_delta(s_next, strike, rate, vol_implied, tau_rem, is_call)

            trade_shares = abs(delta_new - delta)
            tc = cost_rate * trade_shares * s_next
            tot_cost += tc

            cash -= (delta_new - delta) * s_next + tc
            delta = delta_new
            s = s_next

        s_t = path[-1]
        cash = cash * df_step

        payoff = max(s_t - strike, 0.0) if is_call else max(strike - s_t, 0.0)
        terminal_pnl = delta * s_t + cash - payoff

        pnls.append(terminal_pnl)
        costs.append(tot_cost)

    mean_pnl = sum(pnls) / n_paths
    var_pnl = sum((x - mean_pnl) ** 2 for x in pnls) / max(n_paths - 1, 1)
    std_pnl = math.sqrt(var_pnl)
    mean_cost = sum(costs) / n_paths

    return {
        "mean_pnl": mean_pnl,
        "std_pnl": std_pnl,
        "mean_costs": mean_cost,
        "errors": pnls,
    }


def hedging_error_scaling(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    step_list: list[int],
    n_paths: int,
    seed: int,
) -> dict[str, Any]:
    """Evaluate discrete hedging error standard deviation across rebalancing steps.

    Verifies the theoretical scaling Std(eps_N) ~ O(1 / sqrt(N)).
    """
    if not step_list:
        raise ValueError("step_list must be non-empty.")

    results: dict[str, Any] = {}
    log_n: list[float] = []
    log_std: list[float] = []

    for steps in step_list:
        paths = simulate_paths(spot, rate, vol, maturity, steps, n_paths, seed + steps)
        out = delta_hedging_pnl(paths, strike, rate, vol, maturity, cost_rate=0.0, is_call=True)

        std_err = float(out["std_pnl"])
        mean_err = float(out["mean_pnl"])
        norm_std = std_err * math.sqrt(steps)

        results[str(steps)] = {
            "std_error": std_err,
            "mean_error": mean_err,
            "norm_std": norm_std,
        }
        log_n.append(math.log(steps))
        log_std.append(math.log(std_err))

    # Compute empirical slope
    mean_ln = sum(log_n) / len(log_n)
    mean_ls = sum(log_std) / len(log_std)
    numerator = sum((x - mean_ln) * (y - mean_ls) for x, y in zip(log_n, log_std, strict=True))
    denominator = sum((x - mean_ln) ** 2 for x in log_n)
    slope = numerator / denominator if denominator > 1e-12 else -0.5

    results["slope"] = slope
    return results


def gamma_theta_attribution(
    path: list[float],
    strike: float,
    rate: float,
    vol_implied: float,
    maturity: float,
    is_call: bool = True,
) -> dict[str, float]:
    """Single-path P&L attribution verifying the gamma-theta identity."""
    if len(path) < 2:
        raise ValueError("Path must contain at least 2 points.")

    steps = len(path) - 1
    dt = maturity / steps

    s = path[0]
    v = bs_price(s, strike, rate, vol_implied, maturity, is_call)
    delta = bs_delta(s, strike, rate, vol_implied, maturity, is_call)

    actual_hedged_pnl = 0.0
    delta_pnl = 0.0
    theta_decay = 0.0
    gamma_pnl = 0.0
    vol_spread_pnl = 0.0

    for step in range(steps):
        tau = maturity - step * dt
        delta = bs_delta(s, strike, rate, vol_implied, tau, is_call)
        gamma = bs_gamma(s, strike, rate, vol_implied, tau)
        theta = bs_theta(s, strike, rate, vol_implied, tau, is_call)

        s_next = path[step + 1]
        ds = s_next - s
        tau_next = max(maturity - (step + 1) * dt, 1e-12)
        v_next = bs_price(s_next, strike, rate, vol_implied, tau_next, is_call)

        # Actual discrete hedged increment: (v_next - v) - delta * ds - r*(v - delta*s)*dt
        inc_hedged = (v_next - v) - delta * ds - rate * (v - delta * s) * dt
        actual_hedged_pnl += inc_hedged

        delta_pnl += delta * ds
        theta_inc = theta * dt - rate * (v - delta * s) * dt
        gamma_inc = 0.5 * gamma * (ds**2)
        theta_decay += theta_inc
        gamma_pnl += gamma_inc

        # Volatility spread representation: 0.5 * S^2 * Gamma * ((dS/S)^2 - sigma_imp^2 * dt)
        vol_spread_pnl += 0.5 * (s**2) * gamma * ((ds / s) ** 2 - (vol_implied**2) * dt)

        s = s_next
        v = v_next

    taylor_pnl = theta_decay + gamma_pnl
    discrepancy = actual_hedged_pnl - taylor_pnl

    return {
        "actual_hedged_pnl": actual_hedged_pnl,
        "delta_pnl": delta_pnl,
        "theta_decay": theta_decay,
        "gamma_pnl": gamma_pnl,
        "vol_spread_pnl": vol_spread_pnl,
        "taylor_pnl": taylor_pnl,
        "discrepancy": discrepancy,
    }
