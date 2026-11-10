"""Lab AP2-L05-1: The Security Market Line (SML) on exact and SIMULATED cross-sections.

Note on data: The curriculum names French portfolios for this lab, but the library's
distribution terms are not cleared. No equity-return series is embedded.
The lab demonstrates the SML on the exact equilibrium economy from L04,
followed by a 10-asset cross-section labelled SIMULATED.
"""

from __future__ import annotations

import random
from fractions import Fraction


def main() -> None:
    # 1. Exact SML check on L04 economy
    betas_exact = [Fraction(262, 543), Fraction(524, 543), Fraction(655, 543)]
    mu_excess_exact = [Fraction(4, 100), Fraction(8, 100), Fraction(10, 100)]
    erp_exact = Fraction(543, 6550)

    # Cross-sectional regression: mu_excess = gamma_0 + gamma_1 * beta
    n_exact = len(betas_exact)
    mean_b = sum(betas_exact, Fraction(0, 1)) / Fraction(n_exact, 1)
    mean_y = sum(mu_excess_exact, Fraction(0, 1)) / Fraction(n_exact, 1)
    s_bb = sum(((b - mean_b) ** 2 for b in betas_exact), Fraction(0, 1))
    s_by = sum(((betas_exact[i] - mean_b) * (mu_excess_exact[i] - mean_y) for i in range(n_exact)), Fraction(0, 1))
    gamma_1_exact = s_by / s_bb
    gamma_0_exact = mean_y - gamma_1_exact * mean_b

    print("--- Part 1: Exact Equilibrium Economy (L04) ---")
    print(f"SML Intercept gamma_0: {gamma_0_exact}")
    print(f"SML Slope gamma_1:     {gamma_1_exact}")
    print(f"Theoretical ERP:       {erp_exact}")
    print(f"Exact match with ERP:  {gamma_1_exact == erp_exact}")

    alphas_exact = [mu_excess_exact[i] - betas_exact[i] * erp_exact for i in range(n_exact)]
    print(f"Pricing errors (alphas): [{alphas_exact[0]}, {alphas_exact[1]}, {alphas_exact[2]}]")

    # 2. Seeded 10-asset SIMULATED cross-section
    print("\n--- Part 2: 10-Asset SIMULATED Cross-Section ---")
    rng = random.Random(42)
    n_sim = 10
    sim_betas: list[float] = []
    sim_excess: list[float] = []
    true_erp = 0.06  # 6% annual / periodic risk premium

    for i in range(n_sim):
        b = round(0.5 + 0.1 * i + rng.uniform(-0.05, 0.05), 4)
        alpha_err = round(rng.gauss(0.0, 0.005), 4)  # idiosyncratic deviation
        ret = round(b * true_erp + alpha_err, 4)
        sim_betas.append(b)
        sim_excess.append(ret)

    # OLS fit on simulated sample
    mean_sb = sum(sim_betas) / float(n_sim)
    mean_sy = sum(sim_excess) / float(n_sim)
    s_sbb = sum((b - mean_sb) ** 2 for b in sim_betas)
    s_sby = sum((sim_betas[i] - mean_sb) * (sim_excess[i] - mean_sy) for i in range(n_sim))
    gamma_1_sim = s_sby / s_sbb
    gamma_0_sim = mean_sy - gamma_1_sim * mean_sb

    print(f"SIMULATED SML Intercept gamma_0: {gamma_0_sim:.6f}")
    print(f"SIMULATED SML Slope gamma_1:     {gamma_1_sim:.6f}")
    print("Asset | Beta   | Mean Excess | SML Fitted | Mispricing (alpha)")
    print("---------------------------------------------------------------")
    for i in range(n_sim):
        fitted = gamma_0_sim + gamma_1_sim * sim_betas[i]
        alpha_i = sim_excess[i] - fitted
        print(f"{i + 1:5d} | {sim_betas[i]:6.4f} | {sim_excess[i]:11.4f} | {fitted:10.4f} | {alpha_i:10.4f}")


main()
