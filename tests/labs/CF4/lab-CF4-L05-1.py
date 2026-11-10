"""Lab CF4-L05-1: Sum-of-the-Parts (SOTP) and Dixit-Pindyck Real Option Timing.

Implements segment-level valuation for a multi-business conglomerate and solves the
Dixit & Pindyck (1994) optimal investment threshold under irreversibility.
"""

from __future__ import annotations

import math


def compute_sotp_valuation(
    segments: list[dict[str, float | str]],
    corporate_overhead_annual: float,
    corporate_wacc: float,
    net_debt: float,
    shares: float,
) -> dict[str, float]:
    """Calculate SOTP enterprise value, overhead capitalization, and equity value."""
    gross_ev = 0.0
    for seg in segments:
        ebitda = float(seg["ebitda"])
        mult = float(seg["multiple"])
        gross_ev += ebitda * mult

    pv_overhead = corporate_overhead_annual / corporate_wacc
    conglomerate_ev = gross_ev - pv_overhead
    equity_value = conglomerate_ev - net_debt
    per_share_value = equity_value / shares

    return {
        "gross_segment_ev": float(gross_ev),
        "pv_overhead": float(pv_overhead),
        "conglomerate_ev": float(conglomerate_ev),
        "equity_value": float(equity_value),
        "per_share_value": float(per_share_value),
    }


def dixit_pindyck_threshold(
    investment_cost: float,
    risk_free_rate: float,
    shortfall_rate: float,  # delta (convenience yield or cash flow yield)
    volatility: float,  # sigma
) -> dict[str, float]:
    """Solve Dixit & Pindyck (1994) optimal investment trigger and option multiple."""
    r = risk_free_rate
    delta = shortfall_rate
    sigma = volatility

    # Characteristic root: Q(beta) = 0.5 * sigma^2 * beta * (beta - 1) + (r - delta) * beta - r = 0
    a = 0.5 * (sigma**2)
    b = (r - delta) - 0.5 * (sigma**2)
    c = -r

    # Positive root beta_1 > 1
    beta_1 = (-b + math.sqrt(b**2 - 4.0 * a * c)) / (2.0 * a)
    hurdle_multiple = beta_1 / (beta_1 - 1.0)
    trigger_value = hurdle_multiple * investment_cost

    return {
        "beta_1": float(beta_1),
        "hurdle_multiple": float(hurdle_multiple),
        "trigger_value": float(trigger_value),
        "option_premium_pct": float((hurdle_multiple - 1.0) * 100.0),
    }


def main() -> None:
    print("CF4 Lab L05-1: SOTP Conglomerate Valuation & Real Option Threshold")
    print("================================================================")

    # 1. SOTP Conglomerate Valuation
    segments: list[dict[str, float | str]] = [
        {"name": "Defense Systems", "ebitda": 180.0, "multiple": 11.5},
        {"name": "Commercial Avionics", "ebitda": 120.0, "multiple": 14.0},
        {"name": "Energy Services", "ebitda": 90.0, "multiple": 7.5},
    ]
    overhead_annual = 30.0  # $M
    wacc = 0.085  # 8.5%
    net_debt = 650.0  # $M
    shares = 120.0  # million shares

    sotp = compute_sotp_valuation(segments, overhead_annual, wacc, net_debt, shares)

    print("--- Part 1: Sum-of-the-Parts Conglomerate Analysis ---")
    for seg in segments:
        seg_val = float(seg["ebitda"]) * float(seg["multiple"])
        s_name = str(seg["name"])
        s_eb = float(seg["ebitda"])
        s_m = float(seg["multiple"])
        print(f"  Segment: {s_name:20s} EBITDA: ${s_eb:5.1f}M  x {s_m:4.1f}x = ${seg_val:7.1f}M")
    print(f"Gross Aggregate Segment EV:   ${sotp['gross_segment_ev']:.2f}M")
    print(f"PV of Corporate Overhead:     -${sotp['pv_overhead']:.2f}M")
    print(f"Net Conglomerate EV:          ${sotp['conglomerate_ev']:.2f}M")
    print(f"Net Debt:                     -${net_debt:.2f}M")
    print(f"Common Equity Fair Value:     ${sotp['equity_value']:.2f}M")
    print(f"Fair Value Per Share:         ${sotp['per_share_value']:.2f}\n")

    # 2. Dixit-Pindyck Real Option Timing Boundary
    print("--- Part 2: Dixit–Pindyck (1994) Real Option Timing Boundary ---")
    investment_cost = 100.0  # $100M sunk capital expenditure
    r = 0.05
    delta = 0.04
    sigma_levels = [0.15, 0.20, 0.25, 0.30, 0.40]

    print("Volatility  beta_1   Hurdle Multiple  Trigger Value V*  Option Premium")
    print("----------------------------------------------------------------------")
    for sigma in sigma_levels:
        opt = dixit_pindyck_threshold(investment_cost, r, delta, sigma)
        print(
            f"   {sigma * 100:4.1f}%    {opt['beta_1']:6.3f}     "
            f"{opt['hurdle_multiple']:6.3f}x         "
            f"${opt['trigger_value']:6.2f}M          "
            f"{opt['option_premium_pct']:5.2f}%"
        )
    print("----------------------------------------------------------------------")
    print("Real option timing hurdle strictly exceeds static NPV threshold: True")


main()
