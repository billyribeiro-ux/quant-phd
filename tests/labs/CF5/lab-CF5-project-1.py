"""CF5 Project Completion: Core LBO Modeling and Returns Attribution.

Executes transaction Sources & Uses, multi-tranche debt schedule with cash sweeps,
and Kaplan-Strömberg value creation attribution.
"""

from __future__ import annotations


def build_sources_and_uses(
    ebitda_0: float,
    entry_multiple: float,
    existing_debt: float,
    min_cash: float,
    target_cash: float,
    txn_fee_rate: float,
    financing_fee_rate: float,
    tla_leverage: float,
    tlb_leverage: float,
    rollover_equity: float = 0.0,
) -> dict[str, float]:
    """Construct Sources and Uses of funds for the buyout transaction."""
    purchase_ev = ebitda_0 * entry_multiple
    equity_purchase_price = purchase_ev - existing_debt + target_cash
    tla_debt = ebitda_0 * tla_leverage
    tlb_debt = ebitda_0 * tlb_leverage
    total_debt = tla_debt + tlb_debt

    txn_fees = purchase_ev * txn_fee_rate
    financing_fees = total_debt * financing_fee_rate
    total_fees = txn_fees + financing_fees

    total_uses = equity_purchase_price + existing_debt + total_fees + min_cash
    sponsor_equity = total_uses - (total_debt + target_cash + rollover_equity)

    return {
        "purchase_ev": float(purchase_ev),
        "equity_purchase_price": float(equity_purchase_price),
        "total_debt": float(total_debt),
        "total_fees": float(total_fees),
        "total_uses": float(total_uses),
        "sponsor_equity": float(sponsor_equity),
        "total_sources": float(total_debt + target_cash + rollover_equity + sponsor_equity),
    }


def calculate_cash_sweep(
    cash_before_sweep: float,
    min_cash: float,
    sweep_pct: float,
    tla_balance: float,
    tlb_balance: float,
) -> tuple[float, float, float]:
    """Compute priority cash sweep across senior and subordinated debt tranches."""
    excess_cash = max(0.0, cash_before_sweep - min_cash)
    sweep_pool = excess_cash * sweep_pct

    tla_sweep = min(tla_balance, sweep_pool)
    remaining_pool = sweep_pool - tla_sweep
    tlb_sweep = min(tlb_balance, remaining_pool)
    end_cash = cash_before_sweep - (tla_sweep + tlb_sweep)

    return float(tla_sweep), float(tlb_sweep), float(end_cash)


def attribute_value_creation(
    entry_ebitda: float,
    exit_ebitda: float,
    entry_multiple: float,
    exit_multiple: float,
    entry_net_debt: float,
    exit_net_debt: float,
) -> dict[str, float]:
    """Decompose total equity value creation into EBITDA growth, multiple expansion, and deleveraging."""
    entry_ev = entry_ebitda * entry_multiple
    exit_ev = exit_ebitda * exit_multiple

    total_gain = (exit_ev - exit_net_debt) - (entry_ev - entry_net_debt)
    delta_ebitda = (exit_ebitda - entry_ebitda) * entry_multiple
    delta_multiple = exit_ebitda * (exit_multiple - entry_multiple)
    delta_deleveraging = entry_net_debt - exit_net_debt

    return {
        "total_gain": float(total_gain),
        "delta_ebitda": float(delta_ebitda),
        "delta_multiple": float(delta_multiple),
        "delta_deleveraging": float(delta_deleveraging),
        "pct_ebitda": float(delta_ebitda / total_gain) if total_gain else 0.0,
        "pct_multiple": float(delta_multiple / total_gain) if total_gain else 0.0,
        "pct_deleveraging": float(delta_deleveraging / total_gain) if total_gain else 0.0,
    }


def main() -> None:
    print("CF5 Project Completion: Core LBO Modeling Pipeline")
    print("==================================================")

    # 1. Sources & Uses ($M)
    ebitda_0 = 100.0
    entry_mult = 10.0
    su = build_sources_and_uses(
        ebitda_0=ebitda_0,
        entry_multiple=entry_mult,
        existing_debt=200.0,
        min_cash=25.0,
        target_cash=50.0,
        txn_fee_rate=0.02,
        financing_fee_rate=0.03,
        tla_leverage=3.0,
        tlb_leverage=2.0,
        rollover_equity=0.0,
    )
    print(f"Purchase Enterprise Value: ${su['purchase_ev']:.2f}M")
    print(f"Total Uses of Funds:       ${su['total_uses']:.2f}M")
    print(f"Sponsor Equity Funded:     ${su['sponsor_equity']:.2f}M")
    print(f"Total Sources of Funds:    ${su['total_sources']:.2f}M")

    # 2. Priority Cash Sweep ($M)
    cash_avail = 60.0
    min_cash = 25.0
    tla_bal = 180.0
    tlb_bal = 120.0
    tla_sw, tlb_sw, end_c = calculate_cash_sweep(
        cash_before_sweep=cash_avail,
        min_cash=min_cash,
        sweep_pct=1.0,
        tla_balance=tla_bal,
        tlb_balance=tlb_bal,
    )
    print(f"TLA Cash Sweep:            ${tla_sw:.2f}M")
    print(f"TLB Cash Sweep:            ${tlb_sw:.2f}M")
    print(f"Ending Operating Cash:     ${end_c:.2f}M")

    # 3. Kaplan-Strömberg Value Creation Attribution ($M)
    exit_ebitda = 145.0
    exit_mult = 11.5
    entry_net_debt = 475.0
    exit_net_debt = 120.0
    attr = attribute_value_creation(
        entry_ebitda=ebitda_0,
        exit_ebitda=exit_ebitda,
        entry_multiple=entry_mult,
        exit_multiple=exit_mult,
        entry_net_debt=entry_net_debt,
        exit_net_debt=exit_net_debt,
    )
    print(f"Total Equity Value Gain:   ${attr['total_gain']:.2f}M")
    print(f"  Operational EBITDA Gain: ${attr['delta_ebitda']:.2f}M ({attr['pct_ebitda']:.1%})")
    print(f"  Multiple Expansion Gain: ${attr['delta_multiple']:.2f}M ({attr['pct_multiple']:.1%})")
    print(f"  Deleveraging Gain:       ${attr['delta_deleveraging']:.2f}M ({attr['pct_deleveraging']:.1%})")


main()
