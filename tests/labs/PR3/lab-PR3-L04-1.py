"""Lab PR3-L04-1: Kelly Sizing Under Parameter Estimation Error.

SIMULATED: Monte Carlo evaluation of growth penalty under estimation error and recovery via shrinkage.
"""

from __future__ import annotations

import numpy as np


def evaluate_estimation_error(
    true_mu_e: float = 0.08,
    sigma: float = 0.20,
    r: float = 0.02,
    sample_sizes: list[int] | None = None,
    n_trials: int = 10000,
    seed: int = 42,
) -> dict[int, dict[str, float]]:
    """Compare realized growth rates of true Kelly, naive sample Kelly, and shrinkage Kelly."""
    if sample_sizes is None:
        sample_sizes = [20, 50, 100, 250, 1000]

    rng = np.random.default_rng(seed)
    f_star = true_mu_e / (sigma**2)
    max_excess_g = 0.5 * (true_mu_e**2) / (sigma**2)

    results: dict[int, dict[str, float]] = {}

    for t in sample_sizes:
        # Standard error of the sample mean
        se_mu = sigma / np.sqrt(t)
        # Sample excess means drawn from N(true_mu_e, se_mu^2)
        mu_hat_e = rng.normal(loc=true_mu_e, scale=se_mu, size=n_trials)

        # 1. Naive plug-in Kelly: f_hat = mu_hat_e / sigma^2
        f_naive = mu_hat_e / (sigma**2)

        # 2. Optimal shrinkage Kelly: alpha* = (t * SR_hat^2) / (t * SR_hat^2 + 1)
        sr_hat = np.maximum(0.0, mu_hat_e / sigma)
        t_sr2 = t * (sr_hat**2)
        alpha_star = np.where(mu_hat_e > 0, t_sr2 / (t_sr2 + 1.0), 0.0)
        f_shrunk = alpha_star * np.maximum(0.0, f_naive)

        # Realized continuous excess growth under true parameters: f * true_mu_e - 0.5 * f^2 * sigma^2
        g_naive = f_naive * true_mu_e - 0.5 * (f_naive**2) * (sigma**2)
        g_shrunk = f_shrunk * true_mu_e - 0.5 * (f_shrunk**2) * (sigma**2)

        mean_g_naive = float(np.mean(g_naive))
        mean_g_shrunk = float(np.mean(g_shrunk))
        theo_naive_g = float(max_excess_g - 1.0 / (2.0 * t))
        overbet_rate = float(np.mean(f_naive > 2.0 * f_star))

        results[t] = {
            "mean_g_naive": mean_g_naive,
            "theo_naive_g": theo_naive_g,
            "mean_g_shrunk": mean_g_shrunk,
            "mean_alpha": float(np.mean(alpha_star)),
            "overbet_rate": overbet_rate,
        }

    return results


def main() -> None:
    mu_e = 0.08
    sigma = 0.20
    r = 0.02
    f_star = mu_e / (sigma**2)
    max_excess_g = 0.5 * (mu_e**2) / (sigma**2)  # 0.0800
    sample_sizes = [20, 50, 100, 250, 1000]

    sim = evaluate_estimation_error(
        true_mu_e=mu_e, sigma=sigma, r=r, sample_sizes=sample_sizes, n_trials=10000, seed=42
    )

    print(f"Estimation Error Impact on Kelly Sizing (True excess mu={mu_e:.2f}, sigma={sigma:.2f}):")
    print(f"Optimal Kelly Leverage f*: {f_star:.2f} | Max Excess Growth g*: {max_excess_g:.4f}\n")
    print(
        f"{'Sample T':<10} {'Naive Emp g':<13} {'Naive Theo g':<14} "
        f"{'Shrunk Emp g':<14} {'Mean Alpha*':<13} {'P(Overbet>2f*)':<15}"
    )
    print("-" * 79)

    for t in sample_sizes:
        res = sim[t]
        print(
            f"{t:<10} {res['mean_g_naive']:<13.4f} {res['theo_naive_g']:<14.4f} "
            f"{res['mean_g_shrunk']:<14.4f} {res['mean_alpha']:<13.3f} {res['overbet_rate']:<15.4f}"
        )


main()
