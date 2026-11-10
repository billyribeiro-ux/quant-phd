"""Lab CF4-L06-1: Valuation Error Decomposition and Ohlson (1995) Clean-Surplus Equivalence.

Quantifies the dominant variance contributors to valuation error and demonstrates the
exact mathematical equivalence of DCF and Ohlson (1995) Residual Income valuation.
"""

from __future__ import annotations

import numpy as np


def ohlson_vs_dcf_equivalence(
    b0: float,
    earnings: np.ndarray,
    dividends: np.ndarray,
    cost_of_equity: float,
    terminal_growth: float,
) -> dict[str, float]:
    """Demonstrate exact equivalence between Dividend Discount / FCFE and Ohlson RI."""
    r_e = cost_of_equity
    g = terminal_growth
    h = len(earnings)

    # 1. Clean surplus balance sheet progression: B_t = B_{t-1} + NI_t - Div_t
    b = np.zeros(h + 1, dtype=np.float64)
    b[0] = b0
    for t in range(h):
        b[t + 1] = b[t] + earnings[t] - dividends[t]

    # 2. Residual income sequence: RI_t = NI_t - r_e * B_{t-1}
    ri = np.zeros(h, dtype=np.float64)
    for t in range(h):
        ri[t] = earnings[t] - r_e * b[t]

    # 3. Discount explicit periods
    periods = np.arange(1, h + 1, dtype=np.float64)
    dfs = 1.0 / np.power(1.0 + r_e, periods)

    pv_divs_explicit = np.sum(dividends * dfs)
    pv_ri_explicit = np.sum(ri * dfs)

    # 4. Terminal values under clean-surplus long-run growth g:
    # In terminal state, book equity grows at g: B_{H+1} = B_H * (1 + g)
    # NI_{H+1} = NI_H * (1 + g)
    # Articulated terminal dividend: Div_{H+1} = NI_{H+1} - g * B_H
    # Articulated terminal residual income: RI_{H+1} = NI_{H+1} - r_e * B_H
    ni_next = earnings[-1] * (1.0 + g)
    div_next = ni_next - g * b[-1]
    ri_next = ni_next - r_e * b[-1]

    tv_div = div_next / (r_e - g)
    tv_ri = ri_next / (r_e - g)

    pv_div_terminal = tv_div / ((1.0 + r_e) ** h)
    pv_ri_terminal = tv_ri / ((1.0 + r_e) ** h)

    v_dividend_dcf = pv_divs_explicit + pv_div_terminal
    v_ohlson = b0 + pv_ri_explicit + pv_ri_terminal

    return {
        "v_dcf": float(v_dividend_dcf),
        "v_ohlson": float(v_ohlson),
        "b0": float(b0),
        "b_h": float(b[-1]),
        "pv_ri_explicit": float(pv_ri_explicit),
        "pv_ri_terminal": float(pv_ri_terminal),
        "absolute_difference": float(abs(v_ohlson - v_dividend_dcf)),
    }


def valuation_error_variance_breakdown(
    base_cf: float,
    base_wacc: float,
    base_g: float,
    sigma_cf_pct: float = 0.10,
    sigma_wacc_bps: float = 75.0,  # 75 bps
    sigma_g_bps: float = 40.0,  # 40 bps
) -> dict[str, float]:
    """Decompose valuation variance into cash flow, WACC, and growth components."""
    # V = CF / (WACC - g)
    v0 = base_cf / (base_wacc - base_g)

    # Sensitivities (Jacobians)
    j_cf = 1.0 / (base_wacc - base_g)
    j_wacc = -base_cf / ((base_wacc - base_g) ** 2)
    j_g = base_cf / ((base_wacc - base_g) ** 2)

    var_cf = (base_cf * sigma_cf_pct) ** 2
    var_wacc = (sigma_wacc_bps / 10000.0) ** 2
    var_g = (sigma_g_bps / 10000.0) ** 2

    contr_cf = (j_cf**2) * var_cf
    contr_wacc = (j_wacc**2) * var_wacc
    contr_g = (j_g**2) * var_g
    total_var = contr_cf + contr_wacc + contr_g

    return {
        "v0": float(v0),
        "pct_cashflow_error": float(contr_cf / total_var * 100.0),
        "pct_wacc_error": float(contr_wacc / total_var * 100.0),
        "pct_growth_error": float(contr_g / total_var * 100.0),
        "total_standard_error": float(np.sqrt(total_var)),
    }


def main() -> None:
    print("CF4 Lab L06-1: Valuation Error Sources & Ohlson Equivalence")
    print("==========================================================")

    # Part 1: Valuation Error Variance Breakdown
    print("--- Part 1: Dominant Sources of Valuation Error ---")
    err = valuation_error_variance_breakdown(
        base_cf=100.0,
        base_wacc=0.085,
        base_g=0.025,
        sigma_cf_pct=0.12,  # 12% cash flow uncertainty
        sigma_wacc_bps=80.0,  # 80 bps discount rate uncertainty
        sigma_g_bps=50.0,  # 50 bps terminal growth uncertainty
    )
    print(f"Base Capitalized Value:        ${err['v0']:.2f}M")
    print(f"Estimated Standard Error:      ${err['total_standard_error']:.2f}M")
    print(f"Contribution of Cash Flow Error:    {err['pct_cashflow_error']:.2f}%")
    print(f"Contribution of WACC Error:         {err['pct_wacc_error']:.2f}%")
    print(f"Contribution of Terminal Growth:    {err['pct_growth_error']:.2f}%\n")

    # Part 2: Ohlson (1995) Clean-Surplus Equivalence
    print("--- Part 2: Ohlson Clean-Surplus Residual Income Equivalence ---")
    b0 = 400.0
    earnings = np.array([60.0, 68.0, 76.0, 85.0, 95.0])
    dividends = np.array([20.0, 24.0, 28.0, 32.0, 38.0])
    r_e = 0.10
    g = 0.03

    res = ohlson_vs_dcf_equivalence(b0, earnings, dividends, r_e, g)
    print(f"Initial Book Equity (B0):      ${res['b0']:.2f}M")
    print(f"Terminal Book Equity (B5):     ${res['b_h']:.2f}M")
    print(f"PV of Explicit Residual Income:${res['pv_ri_explicit']:.2f}M")
    print(f"PV of Terminal Residual Income:${res['pv_ri_terminal']:.2f}M")
    print(f"Total Ohlson Equity Value:     ${res['v_ohlson']:.4f}M")
    print(f"Total Dividend DCF Value:      ${res['v_dcf']:.4f}M")
    print(f"Absolute Difference:           {res['absolute_difference']:.2e}")
    assert res["absolute_difference"] < 1e-10
    print("Exact algebraic and numerical equivalence verified: True")


main()
