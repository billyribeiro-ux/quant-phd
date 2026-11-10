"""CF5 Lab L05-1: MOIC, IRR, and the Kaplan-Strömberg Value Creation Attribution.

Decomposes total LBO equity value creation into EBITDA growth, multiple expansion,
and deleveraging across alternative exit scenarios.
"""

from __future__ import annotations


def decompose_lbo_returns(
    entry_ebitda: float,
    exit_ebitda: float,
    entry_multiple: float,
    exit_multiple: float,
    entry_net_debt: float,
    exit_net_debt: float,
    sponsor_equity_0: float,
    holding_period_years: float,
) -> dict[str, float]:
    """Decompose dollar and percentage equity creation via Kaplan-Strömberg (2009) framework."""
    entry_ev = entry_ebitda * entry_multiple
    exit_ev = exit_ebitda * exit_multiple

    entry_equity = entry_ev - entry_net_debt
    exit_equity = exit_ev - exit_net_debt
    total_gain = exit_equity - entry_equity

    # Attribution components
    delta_ebitda = (exit_ebitda - entry_ebitda) * entry_multiple
    delta_multiple = exit_ebitda * (exit_multiple - entry_multiple)
    delta_deleveraging = entry_net_debt - exit_net_debt

    moic = exit_equity / sponsor_equity_0
    irr = (moic ** (1.0 / holding_period_years)) - 1.0

    return {
        "entry_ev": float(entry_ev),
        "exit_ev": float(exit_ev),
        "entry_equity": float(entry_equity),
        "exit_equity": float(exit_equity),
        "total_gain": float(total_gain),
        "delta_ebitda": float(delta_ebitda),
        "delta_multiple": float(delta_multiple),
        "delta_deleveraging": float(delta_deleveraging),
        "pct_ebitda": float(delta_ebitda / total_gain) if total_gain else 0.0,
        "pct_multiple": float(delta_multiple / total_gain) if total_gain else 0.0,
        "pct_deleveraging": float(delta_deleveraging / total_gain) if total_gain else 0.0,
        "moic": float(moic),
        "irr": float(irr),
    }


def main() -> None:
    print("CF5 Lab L05-1: MOIC, IRR, and Kaplan-Strömberg Attribution")
    print("=========================================================")

    # Baseline Case ($M)
    entry_eb = 100.0
    exit_eb = 145.0
    entry_m = 10.0
    exit_m = 11.5
    entry_nd = 475.0
    exit_nd = 120.0
    sponsor_eq = 525.0
    years = 5.0

    res = decompose_lbo_returns(
        entry_ebitda=entry_eb,
        exit_ebitda=exit_eb,
        entry_multiple=entry_m,
        exit_multiple=exit_m,
        entry_net_debt=entry_nd,
        exit_net_debt=exit_nd,
        sponsor_equity_0=sponsor_eq,
        holding_period_years=years,
    )

    print(f"Entry Enterprise Value:     ${res['entry_ev']:.2f}M")
    print(f"Exit Enterprise Value:      ${res['exit_ev']:.2f}M")
    print(f"Entry Common Equity:        ${res['entry_equity']:.2f}M")
    print(f"Exit Common Equity:         ${res['exit_equity']:.2f}M")
    print(f"Total Equity Created:       ${res['total_gain']:.2f}M")
    print(f"Sponsor MOIC:               {res['moic']:.3f}x")
    print(f"Sponsor Net IRR:            {res['irr']:.2%}")

    print("\nKaplan-Strömberg Value Creation Attribution:")
    print(f"  1. Operational EBITDA Gain: ${res['delta_ebitda']:.2f}M ({res['pct_ebitda']:.1%})")
    print(f"  2. Multiple Expansion:      ${res['delta_multiple']:.2f}M ({res['pct_multiple']:.1%})")
    print(f"  3. Deleveraging / Debt Pay: ${res['delta_deleveraging']:.2f}M ({res['pct_deleveraging']:.1%})")
    sum_attr = res["delta_ebitda"] + res["delta_multiple"] + res["delta_deleveraging"]
    diff_val = abs(sum_attr - res["total_gain"])
    print(f"  Sum of Components:          ${sum_attr:.2f}M (Identity Difference: ${diff_val:.4f}M)")

    # Multiple Contraction Downside Scenario (exit at 8.5x multiple)
    downside = decompose_lbo_returns(
        entry_ebitda=entry_eb,
        exit_ebitda=exit_eb,
        entry_multiple=entry_m,
        exit_multiple=8.5,
        entry_net_debt=entry_nd,
        exit_net_debt=exit_nd,
        sponsor_equity_0=sponsor_eq,
        holding_period_years=years,
    )
    print("\nDownside Scenario (Exit Multiple Contraction to 8.5x):")
    print(f"  Exit Equity:                ${downside['exit_equity']:.2f}M")
    print(f"  Total Equity Created:       ${downside['total_gain']:.2f}M")
    print(f"  Sponsor MOIC:               {downside['moic']:.3f}x")
    print(f"  Sponsor Net IRR:            {downside['irr']:.2%}")
    print(f"  Multiple Expansion Loss:    ${downside['delta_multiple']:.2f}M")
    print(f"  EBITDA + Deleveraging Gain: ${downside['delta_ebitda'] + downside['delta_deleveraging']:.2f}M")


main()
