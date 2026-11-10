"""Lab CF4-L03-1: Terminal-Value Share of DCF Value Across Growth Assumptions.

Evaluates terminal value and its proportion of total enterprise value across a grid
of sustainable growth rates and return on new invested capital (RONIC) levels.
Demonstrates the value-neutrality of growth when RONIC == WACC.
"""

from __future__ import annotations


def evaluate_terminal_value(
    nopat_h1: float,
    pv_explicit: float,
    wacc: float,
    g: float,
    ronic: float,
    h: int = 5,
) -> dict[str, float]:
    """Calculate terminal value and TV share under fundamental reinvestment articulation."""
    # Reinvestment rate required to sustain growth g at return ronic: b = g / RONIC
    reinvestment_rate = g / ronic
    fcff_terminal = nopat_h1 * (1.0 - reinvestment_rate)

    # Gordon perpetuity: TV_H = FCFF_{H+1} / (WACC - g)
    tv = fcff_terminal / (wacc - g)
    pv_tv = tv / ((1.0 + wacc) ** h)
    enterprise_value = pv_explicit + pv_tv
    tv_share = pv_tv / enterprise_value

    return {
        "reinvestment_rate": float(reinvestment_rate),
        "fcff_terminal": float(fcff_terminal),
        "tv": float(tv),
        "pv_tv": float(pv_tv),
        "enterprise_value": float(enterprise_value),
        "tv_share": float(tv_share),
    }


def main() -> None:
    print("CF4 Lab L03-1: Terminal-Value Share & Value Driver Convergence")
    print("=============================================================")

    nopat_h1 = 250.0  # Year 6 NOPAT ($M)
    pv_explicit = 523.81  # 5-year explicit PV ($M)
    wacc = 0.090  # 9.0%
    h = 5

    growth_rates = [0.010, 0.015, 0.020, 0.025, 0.030]
    ronic_levels = [0.060, 0.090, 0.150]  # Value-destroying, neutral, creating

    print(f"Base Parameters: NOPAT_6 = ${nopat_h1:.1f}M, WACC = {wacc * 100:.1f}%, Explicit PV = ${pv_explicit:.2f}M\n")

    for ronic in ronic_levels:
        label = (
            "Value-Destroying (RONIC < WACC)"
            if ronic < wacc
            else ("Value-Neutral (RONIC == WACC)" if abs(ronic - wacc) < 1e-6 else "Value-Accretive (RONIC > WACC)")
        )
        print(f"--- RONIC = {ronic * 100:4.1f}% [{label}] ---")
        print("  g (%)   Reinv Rate    TV ($M)     PV(TV) ($M)    EV ($M)    TV Share")
        for g in growth_rates:
            res = evaluate_terminal_value(nopat_h1, pv_explicit, wacc, g, ronic, h)
            print(
                f"  {g * 100:4.1f}%     {res['reinvestment_rate'] * 100:5.1f}%    "
                f"${res['tv']:8.2f}M   ${res['pv_tv']:8.2f}M   "
                f"${res['enterprise_value']:8.2f}M    {res['tv_share'] * 100:5.2f}%"
            )

            # When RONIC == WACC, TV must identically equal NOPAT_6 / WACC
            if abs(ronic - wacc) < 1e-6:
                neutral_tv = nopat_h1 / wacc
                assert abs(res["tv"] - neutral_tv) < 1e-6
        print()

    print("Fundamental identity verified: when RONIC == WACC, TV is invariant to growth: True")


main()
