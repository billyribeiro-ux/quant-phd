"""Lab L03-1: Dynamic valuation and path-dependent WACC discounting."""

from __future__ import annotations

import math


def main() -> None:
    # 5-year explicit forecast metrics
    ebit = [220.0, 245.0, 270.0, 295.0, 315.0]
    depr = [65.0, 70.0, 75.0, 80.0, 85.0]
    capex = [75.0, 80.0, 85.0, 90.0, 95.0]
    delta_nwc = [18.0, 20.0, 22.0, 24.0, 25.0]
    tax_rate = 0.25

    debt = [320.0, 300.0, 280.0, 260.0, 240.0]
    equity = [650.0, 740.0, 840.0, 950.0, 1070.0]

    rf = 0.040
    erp = 0.055
    beta_u = 0.95
    rd = 0.052
    terminal_g = 0.025
    shares = 50.0
    net_debt_0 = 200.0  # Debt 320 - Cash 120

    print("Year | FCFF ($M) | Beta_L | WACC (%) | Mid-Year DF | PV(FCFF) ($M)")
    print("-" * 65)

    cum_compounding = 1.0
    pv_fcff_total = 0.0

    for t in range(5):
        nopat = ebit[t] * (1.0 - tax_rate)
        fcff = nopat + depr[t] - capex[t] - delta_nwc[t]

        de = debt[t] / equity[t]
        beta_l = beta_u * (1.0 + (1.0 - tax_rate) * de)
        re = rf + beta_l * erp
        v = debt[t] + equity[t]
        wacc = (equity[t] / v) * re + (debt[t] / v) * rd * (1.0 - tax_rate)

        cum_compounding *= 1.0 + wacc
        df_mid = (1.0 / cum_compounding) * math.sqrt(1.0 + wacc)
        pv = fcff * df_mid
        pv_fcff_total += pv

        print(f"{t + 1:4d} | {fcff:9.2f} | {beta_l:6.3f} | {wacc * 100:8.3f} | {df_mid:11.4f} | {pv:13.2f}")

    # Terminal value at year 5
    terminal_fcff = fcff * (1.0 + terminal_g)
    terminal_value = terminal_fcff / (wacc - terminal_g)
    df_terminal = 1.0 / cum_compounding
    pv_tv = terminal_value * df_terminal
    ev = pv_fcff_total + pv_tv
    eq_val = ev - net_debt_0
    share_price = eq_val / shares

    print("\nValuation Summary:")
    print(f"  PV of Explicit Forecast (5 yrs): ${pv_fcff_total:,.2f}M")
    print(f"  Terminal Value at Year 5:       ${terminal_value:,.2f}M")
    print(f"  PV of Terminal Value:            ${pv_tv:,.2f}M")
    print(f"  Enterprise Value (EV):           ${ev:,.2f}M")
    print(f"  Equity Value:                    ${eq_val:,.2f}M")
    print(f"  Target Share Price:              ${share_price:.2f}")


main()
