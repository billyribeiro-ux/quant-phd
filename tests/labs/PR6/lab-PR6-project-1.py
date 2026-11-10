"""Lab PR6-project-1: Project Rung 1 Worked Example - Lifecycle Dynamic Solver.

SIMULATED: Fully solved numerical instance of dynamic lifecycle allocation with
labour income and return predictability compared against target-date glide paths.
"""

from __future__ import annotations

import math

import numpy as np


def compute_human_capital(wages: np.ndarray, r_discount: float) -> np.ndarray:
    """Compute backward-discounted present value of labour income at each age."""
    n = len(wages)
    hc = np.zeros(n)
    for t in range(n):
        discounts = (1.0 + r_discount) ** (-np.arange(n - t))
        hc[t] = float(np.sum(wages[t:] * discounts))
    return hc


def run_lifecycle_benchmark(
    initial_age: int = 25,
    retire_age: int = 65,
    initial_wealth: float = 25000.0,
    initial_wage: float = 50000.0,
    wage_growth: float = 0.02,
    savings_rate: float = 0.15,
    r_free: float = 0.02,
    equity_premium: float = 0.05,
    equity_vol: float = 0.18,
    phi: float = 0.85,
    sigma_eta: float = 0.10,
    rho: float = -0.75,
    wage_beta: float = 0.0,
    gamma: float = 4.0,
    n_paths: int = 10000,
    seed: int = 42,
) -> dict[str, float]:
    """Run full numerical lifecycle benchmark comparing dynamic optimal vs target-date glide paths."""
    rng = np.random.default_rng(seed)
    years = retire_age - initial_age

    # 1. Deterministic career wage profile
    wages = np.zeros(years + 1)
    for t in range(years + 1):
        wages[t] = initial_wage * math.exp(wage_growth * t - 0.0003 * t**2)

    # 2. Human capital trajectory
    hc = compute_human_capital(wages, r_discount=r_free)

    # 3. Simulate market environment with return predictability
    # Innovations for [return, state]
    cov_eps_eta = rho * equity_vol * sigma_eta
    cov_mat = np.array([[equity_vol**2, cov_eps_eta], [cov_eps_eta, sigma_eta**2]])
    chol = np.linalg.cholesky(cov_mat)

    z = rng.standard_normal((n_paths, years, 2))
    shocks = np.einsum("ij,nyj->nyi", chol, z)
    eps = shocks[:, :, 0]
    eta = shocks[:, :, 1]

    # Pre-compute state variable x_t and equity return r_t
    beta_pred = 0.06
    x = np.zeros((n_paths, years + 1))
    r_equity = np.zeros((n_paths, years))

    for t in range(years):
        r_equity[:, t] = r_free + equity_premium + beta_pred * x[:, t] + eps[:, t]
        x[:, t + 1] = phi * x[:, t] + eta[:, t]

    # 4. Compare Dynamic Optimal vs "To-Retirement" Glide Path
    wealth_opt = np.zeros((n_paths, years + 1))
    wealth_tdf = np.zeros((n_paths, years + 1))
    wealth_opt[:, 0] = initial_wealth
    wealth_tdf[:, 0] = initial_wealth

    for t in range(years):
        age = initial_age + t
        # Dynamic policy: adjusts for H_t / W_t and return predictability hedging
        # Effective financial wealth
        w_safe = np.maximum(wealth_opt[:, t], 1000.0)
        hc_ratio = hc[t] / w_safe
        # Myopic demand: (mu_t - r) / (gamma * sigma^2)
        myopic_t = (equity_premium + beta_pred * x[:, t]) / (gamma * equity_vol**2)
        # Hedging demand: Campbell-Viceira predictability factor with finite horizon attenuation
        tau = float(years - t)
        horizon_factor = (1.0 - (phi**tau)) / (1.0 - phi) if (1.0 - phi) > 1e-6 else tau
        hedge_t = (1.0 - 1.0 / gamma) * (-rho * sigma_eta / equity_vol) * horizon_factor * (beta_pred / equity_vol**2)
        # Optimal total wealth risky share: alpha_tot = myopic_t + hedge_t
        alpha_tot = myopic_t + hedge_t
        # Financial equity allocation: alpha_F = alpha_tot * (1 + H/W) - beta_H * (H/W)
        alpha_dynamic = alpha_tot + (alpha_tot - wage_beta) * hc_ratio
        # Realistic lifecycle constraint: clamp to [0.0, 1.0]
        alpha_dynamic = np.clip(alpha_dynamic, 0.0, 1.0)

        # TDF "To-Retirement" linear glide path (90% to 30%)
        alpha_tdf_t = 0.90 if age <= 40 else 0.90 - (0.90 - 0.30) * ((age - 40) / (65 - 40))

        # Evolve portfolios
        port_ret_opt = (1.0 - alpha_dynamic) * r_free + alpha_dynamic * r_equity[:, t]
        port_ret_tdf = (1.0 - alpha_tdf_t) * r_free + alpha_tdf_t * r_equity[:, t]

        savings = savings_rate * wages[t]
        wealth_opt[:, t + 1] = wealth_opt[:, t] * (1.0 + port_ret_opt) + savings
        wealth_tdf[:, t + 1] = wealth_tdf[:, t] * (1.0 + port_ret_tdf) + savings

    # Terminal outcomes
    w_term_opt = np.maximum(wealth_opt[:, -1], 1.0)
    w_term_tdf = np.maximum(wealth_tdf[:, -1], 1.0)

    u_opt = float(np.mean((w_term_opt ** (1.0 - gamma)) / (1.0 - gamma)))
    u_tdf = float(np.mean((w_term_tdf ** (1.0 - gamma)) / (1.0 - gamma)))

    ce_opt = float(((1.0 - gamma) * u_opt) ** (1.0 / (1.0 - gamma)))
    ce_tdf = float(((1.0 - gamma) * u_tdf) ** (1.0 / (1.0 - gamma)))

    return {
        "mean_wealth_opt": float(np.mean(w_term_opt)),
        "mean_wealth_tdf": float(np.mean(w_term_tdf)),
        "p5_wealth_opt": float(np.percentile(w_term_opt, 5)),
        "p5_wealth_tdf": float(np.percentile(w_term_tdf, 5)),
        "ce_wealth_opt": ce_opt,
        "ce_wealth_tdf": ce_tdf,
        "welfare_gain_pct": float((ce_opt / ce_tdf - 1.0) * 100.0),
    }


def main() -> None:
    res = run_lifecycle_benchmark(
        initial_age=25,
        retire_age=65,
        initial_wealth=25000.0,
        initial_wage=50000.0,
        wage_growth=0.02,
        savings_rate=0.15,
        r_free=0.02,
        equity_premium=0.05,
        equity_vol=0.18,
        phi=0.85,
        sigma_eta=0.10,
        rho=-0.75,
        wage_beta=0.0,
        gamma=4.0,
        n_paths=15000,
        seed=42,
    )

    print("Project Rung 1: Dynamic Lifecycle Allocation Benchmark Results:")
    print("=" * 76)
    print(f"{'Metric':<36} {'Dynamic Policy':<20} {'Target-Date Fund':<18}")
    print("-" * 76)
    print(f"{'Expected Terminal Wealth ($)':<36} {res['mean_wealth_opt']:<20.1f} {res['mean_wealth_tdf']:<18.1f}")
    print(f"{'5th Percentile Wealth ($)':<36} {res['p5_wealth_opt']:<20.1f} {res['p5_wealth_tdf']:<18.1f}")
    print(f"{'Certainty Equivalent Wealth ($)':<36} {res['ce_wealth_opt']:<20.1f} {res['ce_wealth_tdf']:<18.1f}")
    print("-" * 76)
    print(f"Dynamic Policy Certainty Equivalent Premium: {res['welfare_gain_pct']:+.2f}%")
    print("=" * 76)


main()
