"""Lab X1-L05-1: Purchasing power parity and half-life of real exchange rate deviations.

Estimates AR(1) persistence and half-life of deviations from purchasing power parity,
applying Kendall's small-sample bias correction to confirm the 3-5 year consensus (Rogoff 1996).
"""

from __future__ import annotations

import math
import random


def estimate_ppp_half_life(
    seed: int = 16,
    n_months: int = 360,
    true_monthly_rho: float = 0.985,  # implies half-life of ~45.8 months (~3.8 years)
) -> dict[str, float]:
    """Simulate real exchange rate deviations and estimate persistence and half-life.

    Real exchange rate: q_t = s_t + p_t^* - p_t.
    AR(1) specification: q_t = alpha + rho * q_{t-1} + e_t.
    Half-life H = ln(0.5) / ln(rho).
    Kendall small-sample bias correction: rho_unbiased = rho_hat + (1 + 3*rho_hat) / T.
    """
    rng = random.Random(seed)

    # Generate AR(1) real exchange rate process
    q: list[float] = [0.0]
    for _ in range(1, n_months):
        q_next = true_monthly_rho * q[-1] + rng.gauss(0.0, 0.02)
        q.append(q_next)

    # OLS estimation of q_t on q_{t-1}
    y = q[1:]
    x = q[:-1]
    t_obs = len(y)

    mean_x = sum(x) / t_obs
    mean_y = sum(y) / t_obs

    var_x = sum((xi - mean_x) ** 2 for xi in x)
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y, strict=True))

    rho_hat = cov_xy / var_x
    alpha_hat = mean_y - rho_hat * mean_x

    # Kendall small-sample bias correction for AR(1)
    bias = -(1.0 + 3.0 * rho_hat) / float(t_obs)
    rho_corrected = rho_hat - bias

    # Half-life in months
    half_life_raw_months = math.log(0.5) / math.log(rho_hat) if rho_hat < 1.0 else float("inf")
    half_life_corrected_months = math.log(0.5) / math.log(rho_corrected) if rho_corrected < 1.0 else float("inf")

    # True half-life in years
    true_hl_years = (math.log(0.5) / math.log(true_monthly_rho)) / 12.0

    return {
        "true_monthly_rho": true_monthly_rho,
        "true_half_life_years": round(true_hl_years, 2),
        "rho_hat": round(rho_hat, 4),
        "alpha_hat": round(alpha_hat, 6),
        "half_life_raw_years": round(half_life_raw_months / 12.0, 2),
        "rho_corrected": round(rho_corrected, 4),
        "half_life_corrected_years": round(half_life_corrected_months / 12.0, 2),
    }


def main() -> None:
    print("Lab X1-L05-1 | Purchasing Power Parity (PPP) Half-Life Estimation")
    print("-----------------------------------------------------------------")

    res = estimate_ppp_half_life(seed=16, n_months=360, true_monthly_rho=0.985)

    print("Data Generating Process (Monthly Frequency, T=360 months / 30 years):")
    print(f"  True AR(1) Persistence (rho):      {res['true_monthly_rho']:.4f}")
    print(f"  True Half-Life (years):           {res['true_half_life_years']:>6.2f} years")
    print("\nOLS Estimation Results:")
    print(f"  Estimated rho (uncorrected):      {res['rho_hat']:>6.4f}")
    print(f"  Raw Half-Life Estimate:           {res['half_life_raw_years']:>6.2f} years")
    print("\nKendall Small-Sample Bias Correction:")
    print(f"  Bias-Corrected rho:               {res['rho_corrected']:>6.4f}")
    print(f"  Bias-Corrected Half-Life:         {res['half_life_corrected_years']:>6.2f} years")
    print("\nConsensus Comparison (Rogoff 1996 consensus: 3 to 5 years):")
    in_consensus = 3.0 <= res["half_life_corrected_years"] <= 5.0
    print(f"  Matches 3-5 Year Consensus Range: {in_consensus}")


main()
