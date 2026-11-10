"""Reference implementation of PR3 Growth-Optimal Sizing library.

Provides discrete and continuous Kelly sizing, multi-asset GOP weights,
drawdown probability, shrinkage under parameter estimation error,
and executive sizing policies.
"""

from __future__ import annotations

import math

import numpy as np


def binary_kelly(p: float, b: float = 1.0) -> float:
    """Calculate the Kelly fraction for a discrete binary bet.

    f* = max(0, (b * p - (1 - p)) / b)

    Parameters
    ----------
    p : float
        Win probability in [0, 1].
    b : float
        Net odds / payoff ratio (net profit per dollar wagered upon win).

    Returns
    -------
    float
        Optimal fraction of capital to bet.
    """
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"Win probability p must be in [0, 1], got {p}")
    if b <= 0.0:
        raise ValueError(f"Payoff ratio b must be strictly positive, got {b}")

    q = 1.0 - p
    edge = b * p - q
    if edge <= 0.0:
        return 0.0
    return float(edge / b)


def continuous_kelly(mu: float, r: float, sigma: float) -> float:
    """Calculate unconstrained continuous-time log-optimal leverage.

    f* = (mu - r) / sigma^2

    Parameters
    ----------
    mu : float
        Expected annualized return of the asset.
    r : float
        Annualized risk-free rate.
    sigma : float
        Annualized volatility of the asset (must be > 0).

    Returns
    -------
    float
        Unconstrained log-optimal leverage fraction.
    """
    if sigma <= 0.0:
        raise ValueError(f"Volatility sigma must be strictly positive, got {sigma}")
    return float((mu - r) / (sigma**2))


def multivariate_kelly(mu: np.ndarray, r: float, cov: np.ndarray) -> np.ndarray:
    """Calculate unconstrained multi-asset Growth-Optimal Portfolio weights.

    w* = Sigma^{-1} (mu - r * 1)

    Parameters
    ----------
    mu : np.ndarray
        1D array of expected asset returns of shape (N,).
    r : float
        Risk-free rate.
    cov : np.ndarray
        2D covariance matrix of asset returns of shape (N, N).

    Returns
    -------
    np.ndarray
        1D array of portfolio weights of length N.
    """
    mu_arr = np.asarray(mu, dtype=np.float64)
    cov_arr = np.asarray(cov, dtype=np.float64)

    if mu_arr.ndim != 1:
        raise ValueError(f"mu must be 1-dimensional, got shape {mu_arr.shape}")
    n = len(mu_arr)
    if cov_arr.shape != (n, n):
        raise ValueError(f"cov shape {cov_arr.shape} does not match mu length {n}")

    excess_mu = mu_arr - r
    weights = np.linalg.solve(cov_arr, excess_mu)
    return np.asarray(weights, dtype=np.float64)


def growth_rate(f: float, mu: float, r: float, sigma: float) -> float:
    """Calculate expected continuous geometric compounding growth rate.

    g(f) = r + f * (mu - r) - 0.5 * f^2 * sigma^2

    Parameters
    ----------
    f : float
        Portfolio leverage / fraction allocated to risky asset.
    mu : float
        Expected annualized return of risky asset.
    r : float
        Annualized risk-free rate.
    sigma : float
        Annualized volatility of risky asset.

    Returns
    -------
    float
        Instantaneous asymptotic capital growth rate.
    """
    return float(r + f * (mu - r) - 0.5 * (f**2) * (sigma**2))


def drawdown_probability(c: float, d: float) -> float:
    """Calculate the asymptotic probability of ever suffering a drawdown of fraction d.

    For fractional Kelly multiplier c in (0, 2):
        P(drawdown >= d) = (1 - d)^(2/c - 1)
    For c <= 0: returns 0.0.
    For c >= 2: returns 1.0 (almost sure ruin/total loss).

    Parameters
    ----------
    c : float
        Fraction of full Kelly leverage (e.g. 0.5 for half-Kelly).
    d : float
        Drawdown threshold fraction in (0, 1) (e.g. 0.20 for 20% drawdown).

    Returns
    -------
    float
        Probability in [0, 1].
    """
    if not (0.0 < d < 1.0):
        raise ValueError(f"Drawdown fraction d must be in (0, 1), got {d}")
    if c <= 0.0:
        return 0.0
    if c >= 2.0:
        return 1.0

    exponent = (2.0 / c) - 1.0
    return float((1.0 - d) ** exponent)


def optimal_shrinkage_factor(sharpe: float, t_obs: int) -> float:
    """Calculate optimal linear shrinkage factor alpha* under parameter estimation error.

    alpha* = (t_obs * Sharpe^2) / (t_obs * Sharpe^2 + 1)

    Parameters
    ----------
    sharpe : float
        Estimated annualized Sharpe ratio of the trading strategy.
    t_obs : int
        Number of historical sample observations used to estimate the drift.

    Returns
    -------
    float
        Shrinkage coefficient in [0, 1).
    """
    if t_obs <= 0:
        raise ValueError(f"Observation count t_obs must be strictly positive, got {t_obs}")
    if sharpe <= 0.0:
        return 0.0

    t_s2 = float(t_obs) * (sharpe**2)
    return float(t_s2 / (t_s2 + 1.0))


def drawdown_constrained_multiplier(max_drawdown: float, max_prob: float) -> float:
    """Calculate the maximum fractional Kelly multiplier satisfying a drawdown limit.

    Solves: (1 - max_drawdown)^(2/c - 1) <= max_prob
    Yields: c_dd = 2 / (1 + ln(max_prob) / ln(1 - max_drawdown))

    Parameters
    ----------
    max_drawdown : float
        Maximum allowable peak-to-trough loss in (0, 1).
    max_prob : float
        Maximum acceptable probability of hitting max_drawdown in (0, 1).

    Returns
    -------
    float
        Upper bound on fractional Kelly multiplier c.
    """
    if not (0.0 < max_drawdown < 1.0):
        raise ValueError(f"max_drawdown must be in (0, 1), got {max_drawdown}")
    if not (0.0 < max_prob < 1.0):
        raise ValueError(f"max_prob must be in (0, 1), got {max_prob}")

    ln_prob = math.log(max_prob)
    ln_d = math.log(1.0 - max_drawdown)
    ratio = ln_prob / ln_d
    c_dd = 2.0 / (1.0 + ratio)
    return float(c_dd)


def sizing_policy(
    mu_hat: float,
    r: float,
    sigma_hat: float,
    t_obs: int,
    max_drawdown: float,
    max_drawdown_prob: float,
) -> dict[str, float]:
    """Derive an executable PM sizing rule combining estimation shrinkage and drawdown caps.

    Parameters
    ----------
    mu_hat : float
        Estimated asset annualized return.
    r : float
        Annualized risk-free rate.
    sigma_hat : float
        Estimated asset annualized volatility.
    t_obs : int
        Estimation sample observation count.
    max_drawdown : float
        Maximum tolerable drawdown fraction.
    max_drawdown_prob : float
        Maximum acceptable probability of experiencing max_drawdown.

    Returns
    -------
    dict[str, float]
        Dictionary with policy metrics:
        - f_raw: raw continuous Kelly fraction
        - sharpe: estimated Sharpe ratio
        - alpha_shrinkage: optimal shrinkage multiplier alpha*
        - c_drawdown: drawdown-constrained multiplier c_dd
        - c_recommended: min(alpha_shrinkage, c_drawdown)
        - f_recommended: c_recommended * f_raw
        - raw_growth: expected growth rate under unconstrained full Kelly
        - expected_growth: expected growth rate under recommended sizing
    """
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
    """Monte Carlo simulation of geometric Brownian motion wealth paths under constant leverage f.

    Parameters
    ----------
    f : float
        Leverage fraction.
    mu : float
        Annualized expected asset return.
    r : float
        Risk-free rate.
    sigma : float
        Annualized asset volatility.
    t_years : float
        Investment horizon in years.
    n_steps : int
        Number of discrete simulation steps.
    n_paths : int
        Number of independent paths.
    seed : int
        Random seed.

    Returns
    -------
    dict[str, float]
        Dictionary with terminal wealth statistics:
        - mean_terminal_wealth
        - median_terminal_wealth
        - prob_loss (fraction of paths ending below initial wealth 1.0)
        - empirical_growth_rate (median annualized log return)
    """
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
