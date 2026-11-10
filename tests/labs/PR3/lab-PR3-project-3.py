"""Lab PR3-project-3: Project Rung 3 Full Independent Sizing Policy Evaluation.

SIMULATED: Full sizing policy execution and Monte Carlo path simulation on seed 0.
"""

from __future__ import annotations

import math
import random
from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate deterministic inputs for sizing policy under parameter uncertainty."""
    rng = random.Random(seed)
    p = round(0.52 + 0.12 * rng.random(), 4)
    b = round(0.80 + 1.20 * rng.random(), 4)
    r = round(0.02 + 0.03 * rng.random(), 4)
    excess_mu = round(0.04 + 0.08 * rng.random(), 4)
    mu = round(r + excess_mu, 4)
    sigma = round(0.14 + 0.14 * rng.random(), 4)
    t_obs = 30 + (seed * 7) % 91
    max_drawdown = round(0.20 + 0.15 * rng.random(), 4)
    max_drawdown_prob = round(0.05 + 0.08 * rng.random(), 4)

    return {
        "seed": seed,
        "p": p,
        "b": b,
        "mu": mu,
        "r": r,
        "sigma": sigma,
        "t_obs": t_obs,
        "max_drawdown": max_drawdown,
        "max_drawdown_prob": max_drawdown_prob,
    }


def continuous_kelly(mu: float, r: float, sigma: float) -> float:
    """Calculate unconstrained continuous-time log-optimal leverage."""
    return float((mu - r) / (sigma**2))


def growth_rate(f: float, mu: float, r: float, sigma: float) -> float:
    """Calculate expected continuous geometric compounding growth rate."""
    return float(r + f * (mu - r) - 0.5 * (f**2) * (sigma**2))


def optimal_shrinkage_factor(sharpe: float, t_obs: int) -> float:
    """Calculate optimal linear shrinkage factor alpha* under parameter estimation error."""
    if sharpe <= 0.0:
        return 0.0
    t_s2 = float(t_obs) * (sharpe**2)
    return float(t_s2 / (t_s2 + 1.0))


def drawdown_constrained_multiplier(max_drawdown: float, max_prob: float) -> float:
    """Calculate maximum fractional Kelly multiplier satisfying a drawdown limit."""
    ln_prob = math.log(max_prob)
    ln_d = math.log(1.0 - max_drawdown)
    return float(2.0 / (1.0 + ln_prob / ln_d))


def sizing_policy(
    mu_hat: float,
    r: float,
    sigma_hat: float,
    t_obs: int,
    max_drawdown: float,
    max_drawdown_prob: float,
) -> dict[str, float]:
    """Derive executable PM sizing rule combining estimation shrinkage and drawdown caps."""
    excess_mu = mu_hat - r
    if excess_mu <= 0.0 or sigma_hat <= 0.0:
        c_dd = drawdown_constrained_multiplier(max_drawdown, max_drawdown_prob)
        return {
            "f_raw": 0.0,
            "sharpe": 0.0,
            "alpha_shrinkage": 0.0,
            "c_drawdown": float(c_dd),
            "c_recommended": 0.0,
            "f_recommended": 0.0,
            "raw_growth": float(r),
            "expected_growth": float(r),
        }

    f_raw = continuous_kelly(mu_hat, r, sigma_hat)
    sharpe = excess_mu / sigma_hat
    alpha_shrinkage = optimal_shrinkage_factor(sharpe, t_obs)
    c_dd = drawdown_constrained_multiplier(max_drawdown, max_drawdown_prob)
    c_rec = min(alpha_shrinkage, c_dd)
    f_rec = c_rec * f_raw

    raw_growth = growth_rate(f_raw, mu_hat, r, sigma_hat)
    rec_growth = growth_rate(f_rec, mu_hat, r, sigma_hat)

    return {
        "f_raw": float(f_raw),
        "sharpe": float(sharpe),
        "alpha_shrinkage": float(alpha_shrinkage),
        "c_drawdown": float(c_dd),
        "c_recommended": float(c_rec),
        "f_recommended": float(f_rec),
        "raw_growth": float(raw_growth),
        "expected_growth": float(rec_growth),
    }


def simulate_wealth(
    f: float,
    mu: float,
    r: float,
    sigma: float,
    t_years: float,
    n_steps: int,
    n_paths: int,
    seed: int = 42,
) -> dict[str, float]:
    """Monte Carlo simulation of geometric Brownian motion wealth paths."""
    dt = t_years / float(n_steps)
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n_paths, n_steps))

    step_drift = (r + f * (mu - r) - 0.5 * (f**2) * (sigma**2)) * dt
    step_diff = f * sigma * math.sqrt(dt) * z
    log_increments = step_drift + step_diff
    log_paths = np.cumsum(log_increments, axis=1)
    log_terminal = log_paths[:, -1]
    terminal_wealth = np.exp(log_terminal)

    return {
        "mean_terminal_wealth": float(np.mean(terminal_wealth)),
        "median_terminal_wealth": float(np.median(terminal_wealth)),
        "prob_loss": float(np.mean(terminal_wealth < 1.0)),
        "empirical_growth_rate": float(np.median(log_terminal) / t_years),
    }


def main() -> None:
    seed = 0
    inst = make_instance(seed)

    mu = inst["mu"]
    r = inst["r"]
    sigma = inst["sigma"]
    t_obs = inst["t_obs"]
    max_d = inst["max_drawdown"]
    max_p = inst["max_drawdown_prob"]

    policy = sizing_policy(
        mu_hat=mu,
        r=r,
        sigma_hat=sigma,
        t_obs=t_obs,
        max_drawdown=max_d,
        max_drawdown_prob=max_p,
    )

    # Simulate 5-year wealth paths for raw Kelly vs recommended sizing
    sim_raw = simulate_wealth(
        f=policy["f_raw"],
        mu=mu,
        r=r,
        sigma=sigma,
        t_years=5.0,
        n_steps=252 * 5,
        n_paths=5000,
        seed=seed,
    )

    sim_rec = simulate_wealth(
        f=policy["f_recommended"],
        mu=mu,
        r=r,
        sigma=sigma,
        t_years=5.0,
        n_steps=252 * 5,
        n_paths=5000,
        seed=seed,
    )

    print(f"Project Rung 3 · Sizing Policy Execution (Seed {seed})")
    print("=" * 65)
    print(f"Market Environment: mu={mu:.4f}, r={r:.4f}, sigma={sigma:.4f}, Sharpe={policy['sharpe']:.4f}")
    print(f"Risk Mandate:       T_obs={t_obs}, D_max={max_d:.4f}, P_max={max_p:.4f}\n")
    print(f"{'Metric':<30} {'Raw Full Kelly':<18} {'PM Recommended':<18}")
    print("-" * 66)
    print(f"{'Leverage Fraction (f)':<30} {policy['f_raw']:<18.4f} {policy['f_recommended']:<18.4f}")
    print(f"{'Fractional Multiplier (c)':<30} {1.0000:<18.4f} {policy['c_recommended']:<18.4f}")
    print(f"{'Expected Growth Rate':<30} {policy['raw_growth']:<18.4f} {policy['expected_growth']:<18.4f}")
    print(
        f"{'Median 5y Terminal Wealth':<30} {sim_raw['median_terminal_wealth']:<18.4f} "
        f"{sim_rec['median_terminal_wealth']:<18.4f}"
    )
    print(
        f"{'Mean 5y Terminal Wealth':<30} {sim_raw['mean_terminal_wealth']:<18.4f} "
        f"{sim_rec['mean_terminal_wealth']:<18.4f}"
    )
    print(f"{'5y Loss Probability':<30} {sim_raw['prob_loss']:<18.4f} {sim_rec['prob_loss']:<18.4f}")
    print(
        f"{'Realized Annualized Growth':<30} {sim_raw['empirical_growth_rate']:<18.4f} "
        f"{sim_rec['empirical_growth_rate']:<18.4f}"
    )


main()
