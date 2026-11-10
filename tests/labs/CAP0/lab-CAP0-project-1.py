"""Lab Project 1 (Worked Example): End-to-end corporate finance model and valuation."""

from __future__ import annotations

import numpy as np


def main() -> None:
    # 1. Three-statement articulation check on sample base
    rev = 1000.0
    cogs = 500.0
    opex = 250.0
    ebitda = rev - cogs - opex
    depr = 60.0
    ebit = ebitda - depr
    interest = 15.0
    ebt = ebit - interest
    tax = ebt * 0.25
    net_income = ebt - tax
    dividends = net_income * 0.30

    capex = 60.0
    delta_nwc = 20.0
    cfo = net_income + depr - delta_nwc
    cfi = -capex
    cff = -dividends
    delta_cash = cfo + cfi + cff

    delta_assets = delta_cash + delta_nwc + (capex - depr)
    delta_liab_eq = net_income - dividends
    gap = delta_assets - delta_liab_eq

    print(f"Net Income: {net_income:.2f}")
    print(f"CFO: {cfo:.2f}, CFI: {cfi:.2f}, CFF: {cff:.2f}")
    print(f"Delta Cash: {delta_cash:.2f}")
    print(f"Articulation Gap: {gap:.10f}")

    # 2. Minimum-variance hedge ratio
    r_spot = np.array([0.02, -0.01, 0.04, -0.03, 0.01])
    r_futures = np.array([0.018, -0.009, 0.038, -0.028, 0.011])
    cov_sf = float(np.cov(r_spot, r_futures)[0, 1])
    var_f = float(np.var(r_futures, ddof=1))
    h_star = cov_sf / var_f
    print(f"Optimal Hedge Ratio h*: {h_star:.4f}")


main()
