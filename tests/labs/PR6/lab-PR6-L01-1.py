"""Lab PR6-L01-1: The Time Diversification Fallacy and Samuelson's Equivalence.

SIMULATED: Monte Carlo evaluation of terminal wealth dispersion, annualized vs
cumulative variance, and constant CRRA optimal allocation across investment horizons.
"""

from __future__ import annotations

import math

import numpy as np


def evaluate_time_diversification(
    horizons: list[int],
    mu: float = 0.08,
    r: float = 0.02,
    sigma: float = 0.20,
    gamma: float = 3.0,
    w0: float = 100.0,
    n_paths: int = 10000,
    seed: int = 42,
) -> dict[int, dict[str, float]]:
    """Evaluate annualized variance, cumulative variance, terminal wealth dispersion, and optimal CRRA fraction."""
    rng = np.random.default_rng(seed)
    results: dict[int, dict[str, float]] = {}

    # Merton / Samuelson continuous-time optimal fraction for CRRA utility under i.i.d. returns
    alpha_star = (mu - r) / (gamma * sigma**2)

    for horizon in horizons:
        # Standard normal random shocks for cumulative horizon return
        z = rng.standard_normal(n_paths)
        # Log return on optimal portfolio: mean and variance scale linearly with horizon
        port_drift = r + alpha_star * (mu - r)
        port_vol = alpha_star * sigma
        log_ret = (port_drift - 0.5 * port_vol**2) * horizon + port_vol * math.sqrt(horizon) * z
        terminal_wealth = w0 * np.exp(log_ret)

        annualized_var = float(np.var(log_ret / horizon))
        cumulative_var = float(np.var(log_ret))
        mean_terminal = float(np.mean(terminal_wealth))
        std_terminal = float(np.std(terminal_wealth))

        # Shortfall metrics relative to initial capital
        shortfall_mask = terminal_wealth < w0
        p_shortfall = float(np.mean(shortfall_mask))
        worst_loss = float(np.max(w0 - terminal_wealth)) if np.any(shortfall_mask) else 0.0
        expected_shortfall = float(np.mean(w0 - terminal_wealth[shortfall_mask])) if np.any(shortfall_mask) else 0.0

        # Theoretical terminal wealth variance: W0^2 * exp(2 * port_drift * T) * (exp(port_vol^2 * T) - 1)
        theo_var = (w0**2) * math.exp(2.0 * port_drift * horizon) * (math.exp((port_vol**2) * horizon) - 1.0)
        theo_std = math.sqrt(theo_var)

        results[horizon] = {
            "alpha_star": alpha_star,
            "annualized_var": annualized_var,
            "cumulative_var": cumulative_var,
            "mean_terminal": mean_terminal,
            "std_terminal": std_terminal,
            "theo_std": theo_std,
            "p_shortfall": p_shortfall,
            "expected_shortfall": expected_shortfall,
            "worst_loss": worst_loss,
        }

    return results


def main() -> None:
    horizons = [1, 5, 10, 20, 30]
    mu = 0.08
    r = 0.02
    sigma = 0.20
    gamma = 3.0
    w0 = 100.0

    res = evaluate_time_diversification(
        horizons=horizons,
        mu=mu,
        r=r,
        sigma=sigma,
        gamma=gamma,
        w0=w0,
        n_paths=20000,
        seed=42,
    )

    print("Samuelson (1969, 1979) Time Diversification & Horizon Invariance Analysis:")
    print(f"Parameters: mu={mu:.2f}, r={r:.2f}, sigma={sigma:.2f}, gamma={gamma:.1f}, W0={w0:.1f}")
    print("=" * 86)
    print(
        f"{'Horizon (yr)':<14} {'Opt Alpha':<11} {'Ann LogVar':<13} {'Cum LogVar':<13} "
        f"{'E[W_T] ($)':<12} {'Std[W_T] ($)':<13} {'P(W_T<W0)':<10}"
    )
    print("-" * 86)

    for h in horizons:
        d = res[h]
        print(
            f"{h:<14d} {d['alpha_star']:<11.4f} {d['annualized_var']:<13.5f} {d['cumulative_var']:<13.4f} "
            f"{d['mean_terminal']:<12.2f} {d['std_terminal']:<13.2f} {d['p_shortfall']:<10.4f}"
        )

    print("=" * 86)
    print("Key Invariance: Optimal CRRA portfolio weight is strictly constant across all horizons.")
    print("Fallacy Proof: Ann LogVar -> 0 as 1/T, but Cumulative LogVar and Std[W_T] explode with T.")


main()
