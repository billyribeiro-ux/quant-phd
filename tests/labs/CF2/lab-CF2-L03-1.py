"""CF2 lab L03-1: Estimation error in WACC, delta method, and second-order term.

SIMULATED: Beta, equity risk premium, and debt spreads are drawn from a seeded
multivariate distribution. No real market data is used.
Demonstrates the delta-method linearisation of WACC variance, compares it to
20,000 Monte Carlo draws, and verifies the exact analytical formula for the
omitted second-order interaction term.
"""

from __future__ import annotations

import math
import random

SEED = 20261110


def main() -> None:
    print("CF2 Lab L03-1: WACC Estimation Error Propagation (SIMULATED)")
    print("----------------------------------------------------------")

    rng = random.Random(SEED)
    n_sims = 20_000

    # Capital weights and tax rate (treated as fixed per Assumption A8)
    w_e = 0.60
    w_d = 0.40
    tau_c = 0.25
    r_f = 0.040

    # Parameter point estimates (means)
    mu_beta = 1.20
    mu_erp = 0.055
    mu_spread = 0.020

    # Parameter estimation uncertainties (variances and covariance)
    var_beta = 0.0400  # se(beta) = 0.20
    var_erp = 0.000400  # se(erp) = 0.020 (2.0%)
    cov_beta_erp = 0.001000  # positive covariance between beta and ERP estimates
    var_spread = 0.000049  # se(spread) = 0.007 (70 bps)

    # 1. Delta-method linearised variance
    # r_WACC = w_E * (r_f + beta * ERP) + w_D * (r_f + spread) * (1 - tau_c)
    # Gradient w.r.t [beta, ERP, spread]:
    # dWACC/dbeta = w_E * ERP, dWACC/dERP = w_E * beta, dWACC/dspread = w_D * (1 - tau_c)
    v_delta_equity = (w_e**2) * (
        (mu_erp**2) * var_beta + (mu_beta**2) * var_erp + 2.0 * mu_beta * mu_erp * cov_beta_erp
    )
    v_delta_debt = (w_d * (1.0 - tau_c)) ** 2 * var_spread
    v_delta = v_delta_equity + v_delta_debt
    se_delta = math.sqrt(v_delta)

    # 2. Exact theoretical moment for product of bivariate normals
    # Var(beta * ERP) = mu_beta^2 * var_erp + mu_erp^2 * var_beta + 2*mu_beta*mu_erp*cov
    #                   + var_beta * var_erp + cov^2
    second_order_term = (w_e**2) * (var_beta * var_erp + cov_beta_erp**2)
    v_exact = v_delta + second_order_term
    se_exact = math.sqrt(v_exact)

    # 3. Monte Carlo simulation (20,000 draws)
    # Cholesky factor for bivariate normal (beta, ERP)
    sigma_b = math.sqrt(var_beta)
    sigma_erp = math.sqrt(var_erp)
    rho = cov_beta_erp / (sigma_b * sigma_erp)
    sigma_spread = math.sqrt(var_spread)

    sim_wacc: list[float] = []
    for _ in range(n_sims):
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        z3 = rng.gauss(0.0, 1.0)

        b_sim = mu_beta + sigma_b * z1
        erp_sim = mu_erp + sigma_erp * (rho * z1 + math.sqrt(1.0 - rho**2) * z2)
        spread_sim = mu_spread + sigma_spread * z3

        re_sim = r_f + b_sim * erp_sim
        rd_sim = r_f + spread_sim
        w_sim = w_e * re_sim + w_d * rd_sim * (1.0 - tau_c)
        sim_wacc.append(w_sim)

    mc_mean = sum(sim_wacc) / n_sims
    mc_var = sum((w - mc_mean) ** 2 for w in sim_wacc) / (n_sims - 1)
    mc_se = math.sqrt(mc_var)

    print(f"Base WACC estimate: {w_e * (r_f + mu_beta * mu_erp) + w_d * (r_f + mu_spread) * (1 - tau_c):.4%}")
    print(f"\n1. Delta-method variance:   {v_delta:.8f} (SE = {se_delta:.4%})")
    print(f"2. Exact theoretical var:   {v_exact:.8f} (SE = {se_exact:.4%})")
    print(f"3. Monte Carlo (20k draws): {mc_var:.8f} (SE = {mc_se:.4%})")

    print(f"\nAnalytical second-order gap (v_exact - v_delta): {second_order_term:.8f}")
    print(f"Observed gap in theory:                          {v_exact - v_delta:.8f}")
    print(f"Monte Carlo vs. exact theory difference:         {abs(mc_var - v_exact):.8f}")
    mc_error_bound = 4.0 * math.sqrt(2.0 / n_sims) * v_exact
    print(f"Within 4 MC standard errors ({mc_error_bound:.8f}): {abs(mc_var - v_exact) <= mc_error_bound}")


main()
