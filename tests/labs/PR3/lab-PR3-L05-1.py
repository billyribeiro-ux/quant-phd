"""Lab PR3-L05-1: Samuelson's Critique and CRRA Utility Evaluation.

SIMULATED: Verification of Samuelson's critique: expected utility of full Kelly vs fractional Merton sizing.
"""

from __future__ import annotations

import numpy as np


def evaluate_samuelson_utility(
    gamma_levels: list[float],
    fractions: list[float],
    mu: float = 0.10,
    r: float = 0.02,
    sigma: float = 0.20,
    t_years: float = 5.0,
    n_paths: int = 15000,
    seed: int = 42,
) -> dict[float, dict[float, dict[str, float]]]:
    """Calculate empirical and analytical certainty equivalent growth rates for CRRA investors."""
    rng = np.random.default_rng(seed)
    f_kelly = (mu - r) / (sigma**2)  # 2.00
    z = rng.standard_normal(n_paths)

    results: dict[float, dict[float, dict[str, float]]] = {}

    for gamma in gamma_levels:
        results[gamma] = {}
        for c in fractions:
            f = c * f_kelly

            # Analytical Certainty Equivalent Growth Rate: CEGR = r + f*(mu-r) - 0.5 * gamma * f^2 * sigma^2
            theo_cegr = r + f * (mu - r) - 0.5 * gamma * (f**2) * (sigma**2)

            # Simulated terminal wealth
            drift = (r + f * (mu - r) - 0.5 * (f**2) * (sigma**2)) * t_years
            diffusion = f * sigma * np.sqrt(t_years) * z
            log_w = drift + diffusion
            wealth = np.exp(log_w)

            # CRRA Certainty Equivalent: (E[W^(1-gamma)])^(1 / (1-gamma)) / t_years
            if abs(gamma - 1.0) < 1e-4:
                emp_cegr = float(np.mean(log_w) / t_years)
            else:
                power_w = np.power(wealth, 1.0 - gamma)
                mean_power = np.mean(power_w)
                if mean_power > 0:
                    ce_wealth = float(np.power(mean_power, 1.0 / (1.0 - gamma)))
                    emp_cegr = float(np.log(ce_wealth) / t_years)
                else:
                    emp_cegr = -np.inf

            results[gamma][c] = {
                "f": float(f),
                "theo_cegr": float(theo_cegr),
                "emp_cegr": float(emp_cegr),
            }

    return results


def main() -> None:
    mu = 0.10
    r = 0.02
    sigma = 0.20
    f_kelly = (mu - r) / (sigma**2)  # 2.00
    gamma_levels = [1.0, 2.0, 4.0, 10.0]
    # Sizing fractions: full Kelly (1.0), half (0.50), quarter (0.25), tenth (0.10)
    fractions = [1.0, 0.50, 0.25, 0.10]

    sim = evaluate_samuelson_utility(
        gamma_levels, fractions, mu=mu, r=r, sigma=sigma, t_years=5.0, n_paths=15000, seed=42
    )

    print(f"Samuelson Critique: Certainty Equivalent Growth Rates (mu={mu:.2f}, r={r:.2f}, sigma={sigma:.2f}):")
    print(f"Full Kelly Leverage f* = {f_kelly:.2f}\n")
    print(f"{'CRRA Gamma':<12} {'Policy':<18} {'Fraction c':<12} {'Lev f':<8} {'Theo CEGR':<12} {'Emp CEGR':<12}")
    print("-" * 74)

    for gamma in gamma_levels:
        opt_c = 1.0 / gamma
        for c in fractions:
            d = sim[gamma][c]
            is_opt = abs(c - opt_c) < 1e-4
            policy_label = "Merton Optimal" if is_opt else ("Full Kelly" if c == 1.0 else f"{c:.2f}-Kelly")
            print(
                f"{gamma:<12.1f} {policy_label:<18} {c:<12.2f} {d['f']:<8.2f} "
                f"{d['theo_cegr']:<12.4f} {d['emp_cegr']:<12.4f}"
            )
        print("-" * 74)


main()
