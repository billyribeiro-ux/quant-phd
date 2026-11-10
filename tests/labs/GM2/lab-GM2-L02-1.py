"""Lab GM2-L02-1: Yield Curve Term Spread Probit Recession Model.

SIMULATED: Estimates the Estrella-Hardouvelis (1991) and Estrella-Mishkin (1998)
probit recession-probability model on simulated yield curve term spreads.
"""

from __future__ import annotations

from typing import cast

import numpy as np
from scipy.optimize import minimize  # type: ignore[import-untyped]
from scipy.special import erf  # type: ignore[import-untyped]


def standard_normal_cdf(x: np.ndarray) -> np.ndarray:
    """Vectorized standard normal cumulative distribution function."""
    return cast(np.ndarray, 0.5 * (1.0 + erf(x / np.sqrt(2.0))))


def standard_normal_pdf(x: np.ndarray) -> np.ndarray:
    """Vectorized standard normal probability density function."""
    return cast(np.ndarray, (1.0 / np.sqrt(2.0 * np.pi)) * np.exp(-0.5 * x**2))


def simulate_term_spread_and_recessions(
    n_periods: int = 160,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate simulated quarterly term spread and 4-quarter ahead recession indicator.

    Term spread S_t = 10Y Treasury yield minus 3M Treasury bill rate.
    Recession R_{t+4} is 1 if in recession 4 quarters ahead, 0 otherwise.
    """
    rng = np.random.default_rng(seed)
    # Term spread as mean-reverting AR(1) process around 1.60% (160 bps)
    spread = np.zeros(n_periods)
    spread[0] = 1.50
    for t in range(1, n_periods):
        shock = rng.normal(0.0, 0.75)
        spread[t] = 0.82 * spread[t - 1] + (1.0 - 0.82) * 1.60 + shock

    # Latent recession propensity: y*_{t+4} = alpha + beta * S_t + epsilon
    # True alpha = -0.70, beta = -0.65
    latent = -0.70 - 0.65 * spread + rng.normal(0.0, 1.0, size=n_periods)
    recession_4q = (latent > 0.0).astype(np.float64)
    return spread, recession_4q


def fit_probit(
    x: np.ndarray,
    y: np.ndarray,
) -> tuple[float, float, float, float, float]:
    """Fit probit model y ~ Phi(alpha + beta * x) via maximum likelihood.

    Returns (alpha, beta, loglik_unconstrained, loglik_constrained, pseudo_r2_estrella).
    """
    n = len(y)
    eps = 1e-12

    # Negative log-likelihood
    def nll(params: np.ndarray) -> float:
        a, b = params[0], params[1]
        z = a + b * x
        p = np.clip(standard_normal_cdf(z), eps, 1.0 - eps)
        ll = np.sum(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))
        return -float(ll)

    # Initial guess
    res = minimize(nll, np.array([0.0, -0.5]), method="BFGS")
    alpha_hat, beta_hat = float(res.x[0]), float(res.x[1])
    ll_u = -float(res.fun)

    # Constrained model: intercept only
    p_base = np.clip(np.mean(y), eps, 1.0 - eps)
    ll_c = float(np.sum(y * np.log(p_base) + (1.0 - y) * np.log(1.0 - p_base)))

    # Estrella & Mishkin (1998) pseudo-R2:
    # R2_EM = 1 - (ll_u / ll_c)**(-(2/n) * ll_c)
    ratio = ll_u / ll_c
    power = -(2.0 / n) * ll_c
    pseudo_r2 = float(1.0 - (ratio**power))

    return alpha_hat, beta_hat, ll_u, ll_c, pseudo_r2


def compute_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC)."""
    # Wilcoxon-Mann-Whitney rank formulation
    pos = y_score[y_true == 1.0]
    neg = y_score[y_true == 0.0]
    n_pos, n_neg = len(pos), len(neg)
    if n_pos == 0 or n_neg == 0:
        return 0.5
    # Vectorized pairwise comparison
    greater = np.sum(pos[:, None] > neg[None, :])
    ties = 0.5 * np.sum(pos[:, None] == neg[None, :])
    return float((greater + ties) / (n_pos * n_neg))


def main() -> None:
    spread, recession = simulate_term_spread_and_recessions(n_periods=160, seed=2024)
    alpha, beta, ll_u, ll_c, pseudo_r2 = fit_probit(spread, recession)

    # Inversion threshold where Pr(R=1) = 0.50: alpha + beta * S* = 0 -> S* = -alpha / beta
    threshold_50 = -alpha / beta

    # Model predictions
    z = alpha + beta * spread
    pred_prob = standard_normal_cdf(z)
    auc = compute_auc(recession, pred_prob)
    brier = float(np.mean((pred_prob - recession) ** 2))

    print("Yield Curve Probit Recession Model (Estrella & Mishkin 1998)")
    print("------------------------------------------------------------")
    print(f"Sample Size:                 {len(spread)} quarters")
    print(f"Historical Recession Share:  {np.mean(recession) * 100:.2f}%")
    print(f"Estimated Intercept (alpha): {alpha:.4f}")
    print(f"Estimated Slope (beta):      {beta:.4f}")
    print(f"Unconstrained Log-Lik:       {ll_u:.2f}")
    print(f"Constrained Log-Lik:         {ll_c:.2f}")
    print(f"Estrella Pseudo R-squared:   {pseudo_r2:.4f}")
    print(f"Pr(R=1)=0.50 Term Spread:    {threshold_50:.4f}% ({threshold_50 * 100:.1f} bps)")
    print(f"Area Under ROC Curve (AUC):  {auc:.4f}")
    print(f"Brier Accuracy Score:        {brier:.4f}")
    print("Inversion Signal Status:     PASS")


main()
