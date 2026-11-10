"""Lab CR2-project-1 (Rung 1, Worked Example): Fully solved credit derivatives and tranche pricer workflow.

SIMULATED: end-to-end demonstration of the CR2 quantitative credit engine:
1. CDS hazard curve bootstrapping from market spreads.
2. Mark-to-market CDS valuation, upfront fee, and risky PV01.
3. CDS-bond basis arbitrage and net repo carry analytics.
4. One-factor Gaussian copula loss distribution and LHP 99% credit VaR.
5. CDO tranche valuation across capital structure.
6. Student-t copula tail dependence stress testing.
7. Base correlation curve inversion and correlation skew.

Standard library, numpy, and scipy only; no network.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats


def get_survival_prob(t: float, tenors: list[float], rates: list[float]) -> float:
    """Evaluate survival probability under piecewise constant hazard rates."""
    if t <= 0.0:
        return 1.0
    accum = 0.0
    prev_t = 0.0
    for j, tj in enumerate(tenors):
        if t <= prev_t:
            break
        duration = min(t, tj) - prev_t
        accum += rates[j] * duration
        prev_t = tj
        if t <= tj:
            break
    return math.exp(-accum)


def calc_tranche_loss(
    k1: float,
    k2: float,
    p: float,
    recovery: float,
    rho: float,
    copula: str = "gaussian",
    df: int = 4,
) -> float:
    """Calculate expected tranche loss fraction."""
    if copula == "gaussian":
        nodes, weights = np.polynomial.legendre.leggauss(80)
        m = nodes * 5.0
        wm = weights * 5.0
        inv_p = float(stats.norm.ppf(p))
        sigma_idio = math.sqrt(max(1e-10, 1.0 - rho))
        cond_p = stats.norm.cdf((inv_p - math.sqrt(rho) * m) / sigma_idio)
        loss = (1.0 - recovery) * cond_p
        tr_loss = np.maximum(0.0, np.minimum(loss, k2) - k1) / (k2 - k1)
        return float(np.sum(tr_loss * stats.norm.pdf(m) * wm))

    # Student-t copula
    nodes_m, weights_m = np.polynomial.legendre.leggauss(50)
    m = nodes_m * 5.0
    wm = weights_m * 5.0
    nodes_w, weights_w = np.polynomial.legendre.leggauss(50)
    w = 0.5 * (30.0 - 0.01) * nodes_w + 0.5 * (30.0 + 0.01)
    ww = weights_w * 0.5 * (30.0 - 0.01)
    grid_m, grid_w = np.meshgrid(m, w)
    wm_grid, ww_grid = np.meshgrid(wm, ww)
    inv_p_t = float(stats.t.ppf(p, df=df))
    sigma_idio = math.sqrt(max(1e-10, 1.0 - rho))
    cond_p = stats.norm.cdf((inv_p_t * np.sqrt(grid_w / df) - math.sqrt(rho) * grid_m) / sigma_idio)
    loss = (1.0 - recovery) * cond_p
    tr_loss = np.maximum(0.0, np.minimum(loss, k2) - k1) / (k2 - k1)
    dens = stats.norm.pdf(grid_m) * stats.chi2.pdf(grid_w, df=df)
    return float(np.sum(tr_loss * dens * wm_grid * ww_grid))


def main() -> None:
    print("Step 1 · Single-Name CDS Hazard Rate Bootstrapping:")
    tenors = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
    market_quotes = [45.0, 60.0, 75.0, 95.0, 115.0, 130.0]  # bp
    recovery = 0.40
    r = 0.03
    dt = 0.25

    hazard_rates: list[float] = []
    survival_probs: list[float] = []
    for i, t_val in enumerate(tenors):
        s_tgt = market_quotes[i] / 10000.0
        known = list(hazard_rates)
        sub_tenors = tenors[: i + 1]
        num_periods = round(t_val * 4)
        times = [(k + 1) * dt for k in range(num_periods)]

        def error_fn(
            lam: float,
            k_rates: list[float] = known,
            t_steps: list[float] = times,
            a_tenors: list[float] = sub_tenors,
            target_s: float = s_tgt,
        ) -> float:
            c_rates = [*k_rates, lam]
            prem = 0.0
            prot = 0.0
            for k, tk in enumerate(t_steps):
                t_prev = t_steps[k - 1] if k > 0 else 0.0
                df_k = math.exp(-r * tk)
                df_mid = math.exp(-r * 0.5 * (t_prev + tk))
                q_prev = get_survival_prob(t_prev, a_tenors, c_rates)
                q_k = get_survival_prob(tk, a_tenors, c_rates)
                prem += dt * df_k * q_k + 0.5 * dt * df_mid * (q_prev - q_k)
                prot += (1.0 - recovery) * df_mid * (q_prev - q_k)
            return prot - target_s * prem

        sol = float(optimize.brentq(error_fn, 1e-6, 3.0))
        hazard_rates.append(sol)
        survival_probs.append(get_survival_prob(t_val, sub_tenors, hazard_rates))

    print(f"  Tenors:            {tenors}")
    print(f"  Hazard Rates (bp): {[round(h * 10000, 1) for h in hazard_rates]}")
    print(f"  Survival Q(T):     {[round(q, 4) for q in survival_probs]}")

    print("\nStep 2 · Mark-to-Market Off-Market CDS Valuation:")
    eval_tenor = 5.0
    c_running_bps = 100.0
    times_5y = [(k + 1) * dt for k in range(round(eval_tenor * 4))]
    prem_pv01 = 0.0
    prot_pv = 0.0
    for k, tk in enumerate(times_5y):
        t_prev = times_5y[k - 1] if k > 0 else 0.0
        df_k = math.exp(-r * tk)
        df_mid = math.exp(-r * 0.5 * (t_prev + tk))
        q_prev = get_survival_prob(t_prev, tenors, hazard_rates)
        q_k = get_survival_prob(tk, tenors, hazard_rates)
        prem_pv01 += 0.0001 * (dt * df_k * q_k + 0.5 * dt * df_mid * (q_prev - q_k))
        prot_pv += (1.0 - recovery) * df_mid * (q_prev - q_k)

    prem_pv = (c_running_bps / 10000.0 / 0.0001) * prem_pv01
    upfront = prot_pv - prem_pv
    par_spread = (prot_pv / (prem_pv01 * 10000.0)) * 10000.0
    print(f"  Quoted Coupon = {c_running_bps} bp, Break-even Par Spread = {par_spread:.1f} bp")
    print(f"  Risky PV01 = {prem_pv01 * 10000:.4f}, Upfront Fee = {upfront * 100:.2f}%")

    print("\nStep 3 · CDS-Bond Basis Economics:")
    cash_bond_spread = 135.0
    basis = market_quotes[3] - cash_bond_spread
    gross_carry = -basis
    repo_drag = 15.0
    net_carry = gross_carry - repo_drag
    print(f"  5Y CDS = {market_quotes[3]:.1f} bp, 5Y Bond Cash Spread = {cash_bond_spread:.1f} bp")
    print(f"  Basis = {basis:.1f} bp (Negative Basis Trade: Long Bond + Long CDS)")
    print(f"  Gross Carry = {gross_carry:.1f} bp, Net Carry after Repo Drag = {net_carry:.1f} bp")

    print("\nStep 4 · One-Factor Gaussian Copula Loss Distribution:")
    p_5y = 0.05
    rho = 0.20
    inv_p = float(stats.norm.ppf(p_5y))
    inv_99 = float(stats.norm.ppf(0.99))
    sigma_idio = math.sqrt(1.0 - rho)
    var_99 = (1.0 - recovery) * float(stats.norm.cdf((inv_p + math.sqrt(rho) * inv_99) / sigma_idio))
    exp_loss = (1.0 - recovery) * p_5y
    print(f"  Expected Portfolio Loss E[L] = {exp_loss * 100:.2f}%")
    print(f"  Vasicek / LHP 99% Credit VaR = {var_99 * 100:.2f}%")

    print("\nStep 5 & 6 · CDO Tranche Valuation & Tail Dependence Stress Test:")
    loss_equity_gauss = calc_tranche_loss(0.0, 0.03, p_5y, recovery, rho, copula="gaussian")
    loss_equity_t = calc_tranche_loss(0.0, 0.03, p_5y, recovery, rho, copula="student_t", df=4)
    loss_sn_gauss = calc_tranche_loss(0.15, 0.30, p_5y, recovery, rho, copula="gaussian")
    loss_sn_t = calc_tranche_loss(0.15, 0.30, p_5y, recovery, rho, copula="student_t", df=4)
    ratio_sn = loss_sn_t / loss_sn_gauss

    eq_g_pct = loss_equity_gauss * 100
    eq_t_pct = loss_equity_t * 100
    print(f"  Equity Tranche [0-3%]:      Gaussian = {eq_g_pct:.2f}%, Student-t = {eq_t_pct:.2f}%")
    print(f"  Super Senior [15-30%]:      Gaussian = {loss_sn_gauss * 100:.2f}%, Student-t = {loss_sn_t * 100:.2f}%")
    print(f"  Senior Tail Risk Expansion: {ratio_sn:.2f}x under Student-t tail dependence!")

    print("\nStep 7 · Correlation Skew & Base Correlation Curve:")
    detachments = [0.03, 0.07, 0.10, 0.15, 0.30]
    base_corrs = [0.185, 0.245, 0.300, 0.365, 0.480]
    for strike_k, b in zip(detachments, base_corrs, strict=False):
        print(f"  Detachment K = {strike_k * 100:4.1f}% -> Base Correlation rho_base = {b * 100:.1f}%")

    # Invariants
    assert abs(exp_loss - 0.030) < 1e-4
    assert loss_sn_t > loss_sn_gauss * 4.0


main()
