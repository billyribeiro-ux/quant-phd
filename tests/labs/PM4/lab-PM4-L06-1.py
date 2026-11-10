"""Lab PM4-L06-1: The 2000s Housing Boom and Bust — Subprime Credit Expansion and Default Contagion.

SIMULATED: Replicates the empirical design of Mian & Sufi (2009) evaluating cross-sectional
mortgage credit growth, income growth, and subsequent mortgage default rates across zip-code deciles.
"""

from __future__ import annotations

import numpy as np


def simulate_mian_sufi_panel(
    n_zipcodes: int = 1000,
    seed: int = 101,
) -> dict[str, np.ndarray]:
    """Simulate a cross-section of zip codes reflecting 2002-2005 boom and 2006-2009 bust.

    Parameters
    ----------
    n_zipcodes : int
        Number of simulated zip-code observations.
    seed : int
        RNG seed for reproducibility.

    Returns
    -------
    dict[str, np.ndarray]
        Arrays of subprime share, credit growth, income growth, price appreciation, and default rate.
    """
    rng = np.random.default_rng(seed)

    # 1996 Baseline subprime share (fraction with credit score < 660)
    subprime_share = rng.beta(2.0, 5.0, size=n_zipcodes)

    # Income growth 2002-2005: driven by fundamental economic productivity, uncorrelated with subprime
    income_growth = rng.normal(0.08, 0.04, size=n_zipcodes)

    # Credit supply shock: securitization drove mortgage credit into high-subprime zip codes
    # Independent of local income growth (Mian & Sufi 2009 identification)
    credit_growth = 0.10 + 0.85 * subprime_share - 0.15 * income_growth + rng.normal(0.0, 0.03, size=n_zipcodes)

    # House price appreciation 2002-2005: fueled by credit expansion
    hpa_boom = 0.05 + 0.65 * credit_growth + rng.normal(0.0, 0.04, size=n_zipcodes)

    # Default rate 2006-2009: catastrophic default clustered in high-subprime credit-boom areas
    noise = rng.normal(0.0, 0.015, size=n_zipcodes)
    base_def = 0.02 + 0.28 * subprime_share + 0.18 * credit_growth - 0.20 * hpa_boom * 0.1
    default_rate = np.clip(base_def + noise, 0.005, 0.35)

    return {
        "subprime_share": subprime_share,
        "income_growth": income_growth,
        "credit_growth": credit_growth,
        "hpa_boom": hpa_boom,
        "default_rate": default_rate,
    }


def compute_decile_averages(
    sorting_variable: np.ndarray,
    target_variables: dict[str, np.ndarray],
    n_bins: int = 4,
) -> dict[str, list[float]]:
    """Sort zip codes into quartiles and compute conditional group means."""
    quantiles = np.quantile(sorting_variable, np.linspace(0, 1, n_bins + 1))
    results: dict[str, list[float]] = {name: [] for name in target_variables}

    for b in range(n_bins):
        q_low, q_high = quantiles[b], quantiles[b + 1]
        mask = (sorting_variable >= q_low) & (sorting_variable <= q_high)
        for name, series in target_variables.items():
            results[name].append(float(np.mean(series[mask])))

    return results


def main() -> None:
    data = simulate_mian_sufi_panel(n_zipcodes=2000, seed=101)

    targets = {
        "Subprime Share": data["subprime_share"],
        "Credit Growth 02-05": data["credit_growth"],
        "Income Growth 02-05": data["income_growth"],
        "Price Apprec 02-05": data["hpa_boom"],
        "Default Rate 06-09": data["default_rate"],
    }

    quartile_stats = compute_decile_averages(data["subprime_share"], targets, n_bins=4)

    print("Mian-Sufi (2009) Cross-Sectional Zip-Code Quartile Stratification:")
    print("Quartile | Subprime Share | Credit Growth | Income Growth | Price Apprec | Default Rate")
    for q in range(4):
        s_sh = quartile_stats["Subprime Share"][q] * 100
        c_gr = quartile_stats["Credit Growth 02-05"][q] * 100
        i_gr = quartile_stats["Income Growth 02-05"][q] * 100
        p_ap = quartile_stats["Price Apprec 02-05"][q] * 100
        d_rt = quartile_stats["Default Rate 06-09"][q] * 100
        print(f"    Q{q + 1}   | {s_sh:13.2f}% | {c_gr:12.2f}% | {i_gr:12.2f}% | {p_ap:11.2f}% | {d_rt:11.2f}%")

    # Econometric correlation checks (Mian & Sufi core empirical results)
    corr_credit_subprime = float(np.corrcoef(data["credit_growth"], data["subprime_share"])[0, 1])
    corr_credit_income = float(np.corrcoef(data["credit_growth"], data["income_growth"])[0, 1])
    corr_default_credit = float(np.corrcoef(data["default_rate"], data["credit_growth"])[0, 1])

    print("\nEmpirical Correlation Matrix:")
    print(f"Corr(Credit Growth, Subprime Share): {corr_credit_subprime:7.4f}")
    print(f"Corr(Credit Growth, Income Growth):   {corr_credit_income:7.4f}")
    print(f"Corr(Default Rate, Credit Growth):   {corr_default_credit:7.4f}")

    # Assertions validating the Mian-Sufi mechanism:
    # 1. Credit growth is strongly positively correlated with latent subprime share
    assert corr_credit_subprime > 0.85
    # 2. Credit growth is disconnected or negatively related to income growth
    assert corr_credit_income < 0.0
    # 3. Subsequent defaults are concentrated in the areas with highest credit growth
    assert corr_default_credit > 0.85


main()
