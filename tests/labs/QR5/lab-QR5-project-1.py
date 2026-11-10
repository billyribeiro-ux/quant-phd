"""Lab QR5-project-1: Rung 2 Completion Problem Reference Solution.

Implements the three core algorithmic building blocks of the deep hedging framework:
1. Whalley-Wilmott asymptotic cubic no-trade bandwidth calculation.
2. Rockafellar-Uryasev Expected Shortfall (CVaR_alpha) tail loss computation.
3. Entropic risk measure via numerically stable log-sum-exp.
"""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray
from scipy.special import erf


def _std_norm_cdf(x: NDArray[np.float64]) -> NDArray[np.float64]:
    res: NDArray[np.float64] = np.asarray(0.5 * (1.0 + erf(x / math.sqrt(2.0))), dtype=np.float64)
    return res


def _std_norm_pdf(x: NDArray[np.float64]) -> NDArray[np.float64]:
    res: NDArray[np.float64] = np.asarray(np.exp(-0.5 * (x**2)) / math.sqrt(2.0 * math.pi), dtype=np.float64)
    return res


def compute_whalley_wilmott_half_width(
    s: float,
    k: float,
    tau: float,
    sigma: float,
    r: float,
    cost_rate: float,
    risk_aversion: float,
) -> float:
    """Compute Whalley & Wilmott (1997) asymptotic half-bandwidth h(S, t)."""
    if tau <= 1e-8:
        return 0.0
    vol_sqrt = sigma * math.sqrt(tau)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / vol_sqrt
    gamma = float(math.exp(-0.5 * d1**2) / (math.sqrt(2.0 * math.pi) * s * vol_sqrt))

    inner = (1.5 * cost_rate * math.exp(-r * tau) * s * (gamma**2)) / risk_aversion
    return float(np.cbrt(max(inner, 0.0)))


def compute_cvar(loss_distribution: NDArray[np.float64], alpha: float = 0.95) -> float:
    """Compute Expected Shortfall at confidence level alpha."""
    sorted_losses = np.sort(loss_distribution)
    cutoff = math.ceil(alpha * len(sorted_losses))
    cutoff = min(cutoff, len(sorted_losses) - 1)
    return float(np.mean(sorted_losses[cutoff:]))


def compute_entropic_risk(loss_distribution: NDArray[np.float64], gamma: float = 1.0) -> float:
    """Compute Entropic Risk Measure: (1/gamma) * ln E[exp(gamma * L)]."""
    scaled = gamma * loss_distribution
    max_val = float(np.max(scaled))
    log_mean_exp = max_val + math.log(float(np.mean(np.exp(scaled - max_val))))
    return float(log_mean_exp / gamma)


def main() -> None:
    s0 = 100.0
    k = 100.0
    tau = 0.20
    sigma = 0.25
    r = 0.03
    cost_rate = 0.005
    risk_aversion = 1.0

    h_width = compute_whalley_wilmott_half_width(s0, k, tau, sigma, r, cost_rate, risk_aversion)

    rng = np.random.default_rng(42)
    simulated_losses = rng.normal(4.0, 2.5, size=1000)

    cvar_val = compute_cvar(simulated_losses, alpha=0.95)
    entropic_val = compute_entropic_risk(simulated_losses, gamma=1.0)

    print(f"Whalley-Wilmott half-width h(S0, tau): {h_width:.6f}")
    print(f"CVaR 95% loss: {cvar_val:.6f}")
    print(f"Entropic risk (gamma=1.0): {entropic_val:.6f}")


main()
