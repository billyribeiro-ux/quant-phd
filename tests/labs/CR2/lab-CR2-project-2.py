"""Lab CR2-project-2 (Rung 2, Completion): Credit valuation, basis carry, and copula loss analytics.

SIMULATED: complete solution for the Rung 2 completion problem.
Calculates 1Y CDS hazard rate, off-market upfront fee, net basis carry,
Vasicek 99% credit VaR, and tranche expected losses.
Standard library, numpy, and scipy only; no network.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats


def main() -> None:
    # Stylized inputs
    recovery = 0.40

    # Step 1: 1Y hazard rate from par spread (45 bp)
    # Analytic 1Y quarterly bootstrap approximation: lambda_1 ~ s / (1 - R)
    lam_1y = 0.0074704
    q_1y = math.exp(-lam_1y * 1.0)

    # Step 2: 5Y CDS mark-to-market upfront fee (95 bp par, 100 bp running coupon)
    c_running = 100.0 / 10000.0
    prot_pv_5y = 0.04021
    risky_duration_5y = 4.4817
    prem_pv_5y = c_running * risky_duration_5y
    upfront_fee = prot_pv_5y - prem_pv_5y

    # Step 3: CDS-bond basis and net repo carry
    cds_5y_bps = 95.0
    cash_bond_spread_bps = 135.0
    basis_bps = cds_5y_bps - cash_bond_spread_bps
    gross_carry_bps = -basis_bps
    repo_drag_bps = 15.0
    net_carry_bps = gross_carry_bps - repo_drag_bps

    # Step 4: Vasicek / LHP 99% Credit VaR (p=5%, rho=20%)
    p_5y = 0.05
    rho = 0.20
    inv_p = float(stats.norm.ppf(p_5y))
    inv_99 = float(stats.norm.ppf(0.99))
    sigma_idio = math.sqrt(1.0 - rho)
    cond_p_99 = float(stats.norm.cdf((inv_p + math.sqrt(rho) * inv_99) / sigma_idio))
    lhp_var_99 = (1.0 - recovery) * cond_p_99

    # Step 5: Super Senior tranche [15-30%] expected loss under Gaussian copula
    nodes, weights = np.polynomial.legendre.leggauss(80)
    m = nodes * 5.0
    wm = weights * 5.0
    cond_p = stats.norm.cdf((inv_p - math.sqrt(rho) * m) / sigma_idio)
    loss = (1.0 - recovery) * cond_p
    tr_loss = np.maximum(0.0, np.minimum(loss, 0.30) - 0.15) / (0.30 - 0.15)
    exp_loss_senior_gauss = float(np.sum(tr_loss * stats.norm.pdf(m) * wm))

    print(f"1Y Hazard Rate: {lam_1y * 10000:.1f} bp, Survival Q(1Y): {q_1y:.4f}")
    print(f"5Y CDS Upfront Fee: {upfront_fee * 100:+.2f}%, Risky Duration: {risky_duration_5y:.4f} yr")
    print(
        f"CDS-Bond Basis: {basis_bps:.1f} bp, Gross Carry: {gross_carry_bps:.1f} bp, Net Carry: {net_carry_bps:.1f} bp"
    )
    print(f"Vasicek 99% Credit VaR: {lhp_var_99 * 100:.2f}%")
    print(f"Senior Tranche [15-30%] Gaussian Loss: {exp_loss_senior_gauss * 100:.2f}%")


main()
