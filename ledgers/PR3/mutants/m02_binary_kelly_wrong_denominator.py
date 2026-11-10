"""Binary Kelly divides by b + 1 instead of net odds b in the optimal fraction denominator."""

from __future__ import annotations

import math

import numpy as np


def binary_kelly(p: float, b: float = 1.0) -> float:
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"Win probability p must be in [0, 1], got {p}")
    if b <= 0.0:
        raise ValueError(f"Payoff ratio b must be strictly positive, got {b}")
    q = 1.0 - p
    edge = b * p - q
    if edge <= 0.0:
        return 0.0
    # BUG: divides by (b + 1) instead of b
    return float(edge / (b + 1.0))


def continuous_kelly(mu: float, r: float, sigma: float) -> float:
    if sigma <= 0.0:
        raise ValueError(f"Volatility sigma must be strictly positive, got {sigma}")
    return float((mu - r) / (sigma**2))


def multivariate_kelly(mu: np.ndarray, r: float, cov: np.ndarray) -> np.ndarray:
    mu_arr = np.asarray(mu, dtype=np.float64)
    cov_arr = np.asarray(cov, dtype=np.float64)
    if mu_arr.ndim != 1 or cov_arr.shape != (len(mu_arr), len(mu_arr)):
        raise ValueError("Shape mismatch")
    excess_mu = mu_arr - r
    weights = np.linalg.solve(cov_arr, excess_mu)
    return np.asarray(weights, dtype=np.float64)


def growth_rate(f: float, mu: float, r: float, sigma: float) -> float:
    return float(r + f * (mu - r) - 0.5 * (f**2) * (sigma**2))


def drawdown_probability(c: float, d: float) -> float:
    if not (0.0 < d < 1.0):
        raise ValueError("d must be in (0, 1)")
    if c <= 0.0:
        return 0.0
    if c >= 2.0:
        return 1.0
    exponent = (2.0 / c) - 1.0
    return float((1.0 - d) ** exponent)


def optimal_shrinkage_factor(sharpe: float, t_obs: int) -> float:
    if t_obs <= 0:
        raise ValueError("t_obs must be strictly positive")
    if sharpe <= 0.0:
        return 0.0
    t_s2 = float(t_obs) * (sharpe**2)
    return float(t_s2 / (t_s2 + 1.0))


def drawdown_constrained_multiplier(max_drawdown: float, max_prob: float) -> float:
    if not (0.0 < max_drawdown < 1.0) or not (0.0 < max_prob < 1.0):
        raise ValueError("inputs must be in (0, 1)")
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
    dt = t_years / float(n_steps)
    rng = np.random.default_rng(seed)
    z = rng.standard_normal((n_paths, n_steps))
    step_drift = (r + f * (mu - r) - 0.5 * (f**2) * (sigma**2)) * dt
    step_diff = f * sigma * math.sqrt(dt) * z
    log_paths = np.cumsum(step_drift + step_diff, axis=1)
    log_terminal = log_paths[:, -1]
    terminal_wealth = np.exp(log_terminal)
    return {
        "mean_terminal_wealth": float(np.mean(terminal_wealth)),
        "median_terminal_wealth": float(np.median(terminal_wealth)),
        "prob_loss": float(np.mean(terminal_wealth < 1.0)),
        "empirical_growth_rate": float(np.median(log_terminal) / t_years),
    }
