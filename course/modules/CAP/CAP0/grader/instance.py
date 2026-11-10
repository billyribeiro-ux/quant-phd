"""Instance generator for CAP0: Integrated Corporate Finance and Equity Case."""

from __future__ import annotations

import hashlib
from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, realistic flat instance for CAP0 capstone project."""
    rng = np.random.default_rng(seed)

    # 1. Base Operations & Growth Parameters
    rev_base = float(np.round(rng.uniform(800.0, 1500.0), 1))
    gross_margin = float(np.round(rng.uniform(0.40, 0.55), 3))
    ebitda_margin = float(np.round(rng.uniform(0.20, 0.28), 3))
    raw_growth = rng.uniform(0.04, 0.10, size=5)
    growth_rates = np.array(sorted(raw_growth, reverse=True), dtype=np.float64)

    capex_ratio = float(np.round(rng.uniform(0.04, 0.08), 3))
    depr_rate = float(np.round(rng.uniform(0.12, 0.18), 3))
    tax_rate = 0.25
    interest_rate = float(np.round(rng.uniform(0.045, 0.065), 4))
    dividend_payout = float(np.round(rng.uniform(0.20, 0.35), 2))

    # Working capital metrics (days)
    dso = float(np.round(rng.uniform(40.0, 55.0), 1))
    dio = float(np.round(rng.uniform(45.0, 65.0), 1))
    dpo = float(np.round(rng.uniform(35.0, 50.0), 1))

    # Initial Balance sheet at t=0
    cogs_0 = rev_base * (1.0 - gross_margin)
    ar_0 = float(np.round(rev_base * (dso / 365.0), 2))
    inv_0 = float(np.round(cogs_0 * (dio / 365.0), 2))
    ap_0 = float(np.round(cogs_0 * (dpo / 365.0), 2))
    cash_0 = float(np.round(rng.uniform(80.0, 150.0), 2))
    nppe_0 = float(np.round(rng.uniform(350.0, 600.0), 2))
    total_assets_0 = cash_0 + ar_0 + inv_0 + nppe_0

    debt_0 = float(np.round(rng.uniform(200.0, 400.0), 2))
    equity_0 = float(np.round(total_assets_0 - ap_0 - debt_0, 2))

    # 2. Market and Cost of Capital Parameters
    rf = float(np.round(rng.uniform(0.035, 0.045), 4))
    erp = float(np.round(rng.uniform(0.050, 0.060), 4))
    beta_u = float(np.round(rng.uniform(0.85, 1.15), 3))
    rd = float(np.round(interest_rate, 4))
    terminal_growth = float(np.round(rng.uniform(0.020, 0.030), 4))
    shares_outstanding = float(np.round(rng.uniform(40.0, 80.0), 2))
    current_share_price = float(np.round(rng.uniform(25.0, 45.0), 2))
    non_operating_assets = float(np.round(rng.uniform(10.0, 30.0), 2))

    # 3. Forensic Accounting Audit Parameters (Year 1 and Year 2)
    ta_f2 = float(np.round(total_assets_0 / 0.88, 2))
    ta_f1 = float(np.round(ta_f2 * rng.uniform(0.90, 0.96), 2))
    rev_f1 = float(np.round(rev_base * rng.uniform(0.90, 0.96), 2))
    rev_f2 = rev_base
    gp_f1 = float(np.round(rev_f1 * (gross_margin + rng.uniform(-0.015, 0.015)), 2))
    gp_f2 = float(np.round(rev_f2 * gross_margin, 2))
    ar_f1 = float(np.round(rev_f1 * (rng.uniform(40.0, 48.0) / 365.0), 2))
    ar_f2 = ar_0
    ca_f1 = float(np.round(ta_f1 * 0.38, 2))
    ca_f2 = cash_0 + ar_0 + inv_0
    cash_f1 = float(np.round(cash_0 * 0.92, 2))
    cash_f2 = cash_0
    cl_f1 = float(np.round(ta_f1 * 0.16, 2))
    cl_f2 = ap_0 + (debt_0 * 0.10)
    std_f1 = float(np.round(debt_0 * 0.09, 2))
    std_f2 = float(np.round(debt_0 * 0.10, 2))
    ltd_f1 = float(np.round(debt_0 * 0.85, 2))
    ltd_f2 = float(np.round(debt_0 * 0.90, 2))
    depr_f1 = float(np.round(nppe_0 * 0.14, 2))
    depr_f2 = float(np.round(nppe_0 * depr_rate, 2))
    ppe_f1 = float(np.round(ta_f1 * 0.50, 2))
    ppe_f2 = nppe_0
    sga_f1 = float(np.round(rev_f1 * 0.155, 2))
    sga_f2 = float(np.round(rev_f2 * 0.15, 2))
    ni_f2 = float(np.round(rev_f2 * ebitda_margin * 0.45, 2))
    delta_wc_f2 = (ca_f2 - ca_f1 - (cash_f2 - cash_f1)) - (cl_f2 - cl_f1 - (std_f2 - std_f1))
    cfo_f2 = float(np.round(ni_f2 + depr_f2 - delta_wc_f2, 2))

    # 4. Capital Structure Trade-off & Liquidity Parameters
    distress_prob_k = 12.0
    distress_prob_d0 = 0.55
    distress_cost_fraction = 0.25
    covenant_min_icr = float(np.round(rng.uniform(2.5, 3.5), 2))
    covenant_max_leverage = float(np.round(rng.uniform(3.5, 4.5), 2))
    fixed_overhead_monthly = float(np.round(rev_base * 0.035, 2))
    runway_months = 6.0

    # 5. Hedging Time Series (T=36 monthly FX/Commodity returns)
    rho = float(np.round(rng.uniform(0.85, 0.95), 3))
    sigma_s = float(np.round(rng.uniform(0.04, 0.06), 4))
    sigma_f = float(np.round(rng.uniform(0.04, 0.06), 4))

    cov_matrix = np.array(
        [
            [sigma_s**2, rho * sigma_s * sigma_f],
            [rho * sigma_s * sigma_f, sigma_f**2],
        ]
    )
    shocks = rng.multivariate_normal([0.0, 0.0], cov_matrix, size=36)
    r_spot = np.array([float(np.round(x, 5)) for x in shocks[:, 0]], dtype=np.float64)
    r_hedge = np.array([float(np.round(x, 5)) for x in shocks[:, 1]], dtype=np.float64)
    fx_exposure_amount = float(np.round(rev_base * 0.25, 2))

    token = hashlib.sha256(f"{seed}-{rev_base}-{gross_margin}".encode()).hexdigest()[:12]

    return {
        "seed": seed,
        "token": token,
        "rev_base": rev_base,
        "gross_margin": gross_margin,
        "ebitda_margin": ebitda_margin,
        "growth_rates": growth_rates,
        "capex_ratio": capex_ratio,
        "depr_rate": depr_rate,
        "tax_rate": tax_rate,
        "interest_rate": interest_rate,
        "dividend_payout": dividend_payout,
        "dso": dso,
        "dio": dio,
        "dpo": dpo,
        "cash_0": cash_0,
        "ar_0": ar_0,
        "inv_0": inv_0,
        "nppe_0": nppe_0,
        "total_assets_0": total_assets_0,
        "ap_0": ap_0,
        "debt_0": debt_0,
        "equity_0": equity_0,
        "rf": rf,
        "erp": erp,
        "beta_u": beta_u,
        "rd": rd,
        "terminal_growth": terminal_growth,
        "shares_outstanding": shares_outstanding,
        "current_share_price": current_share_price,
        "non_operating_assets": non_operating_assets,
        "ta_1": ta_f1,
        "ta_2": ta_f2,
        "rev_1": rev_f1,
        "rev_2": rev_f2,
        "gp_1": gp_f1,
        "gp_2": gp_f2,
        "ar_1": ar_f1,
        "ar_2": ar_f2,
        "ca_1": ca_f1,
        "ca_2": ca_f2,
        "cash_1": cash_f1,
        "cash_2": cash_f2,
        "cl_1": cl_f1,
        "cl_2": cl_f2,
        "std_1": std_f1,
        "std_2": std_f2,
        "ltd_1": ltd_f1,
        "ltd_2": ltd_f2,
        "depr_1": depr_f1,
        "depr_2": depr_f2,
        "ppe_1": ppe_f1,
        "ppe_2": ppe_f2,
        "sga_1": sga_f1,
        "sga_2": sga_f2,
        "ni_2": ni_f2,
        "cfo_2": cfo_f2,
        "distress_prob_k": distress_prob_k,
        "distress_prob_d0": distress_prob_d0,
        "distress_cost_fraction": distress_cost_fraction,
        "covenant_min_icr": covenant_min_icr,
        "covenant_max_leverage": covenant_max_leverage,
        "fixed_overhead_monthly": fixed_overhead_monthly,
        "runway_months": runway_months,
        "r_spot": r_spot,
        "r_hedge": r_hedge,
        "fx_exposure_amount": fx_exposure_amount,
    }
