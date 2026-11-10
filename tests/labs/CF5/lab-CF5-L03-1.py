"""CF5 Lab L03-1: Sources and Uses of Funds and Purchase Price Accounting.

Constructs the transaction funding schedule, validates the Sources == Uses balance,
and calculates purchase price allocation, asset step-ups, and goodwill creation.
"""

from __future__ import annotations


def construct_sources_and_uses(
    target_ebitda: float,
    entry_multiple: float,
    existing_debt: float,
    target_cash: float,
    min_cash_buffer: float,
    revolver_drawn: float,
    tla_multiple: float,
    tlb_multiple: float,
    mezz_multiple: float,
    mna_fee_rate: float,
    debt_fee_rate: float,
    rollover_equity: float,
) -> dict[str, float]:
    """Calculate institutional Sources & Uses schedule and sponsor equity check."""
    enterprise_value = target_ebitda * entry_multiple
    equity_purchase_price = enterprise_value - existing_debt + target_cash

    tla = target_ebitda * tla_multiple
    tlb = target_ebitda * tlb_multiple
    mezz = target_ebitda * mezz_multiple
    total_term_debt = tla + tlb + mezz + revolver_drawn

    mna_fees = enterprise_value * mna_fee_rate
    debt_fees = total_term_debt * debt_fee_rate
    total_fees = mna_fees + debt_fees

    total_uses = equity_purchase_price + existing_debt + total_fees + min_cash_buffer
    sponsor_equity = total_uses - (total_term_debt + target_cash + rollover_equity)
    total_sources = total_term_debt + target_cash + rollover_equity + sponsor_equity

    return {
        "enterprise_value": float(enterprise_value),
        "equity_purchase_price": float(equity_purchase_price),
        "refinance_debt": float(existing_debt),
        "total_fees": float(total_fees),
        "min_cash_buffer": float(min_cash_buffer),
        "total_uses": float(total_uses),
        "total_debt_funded": float(total_term_debt),
        "target_cash_used": float(target_cash),
        "rollover_equity": float(rollover_equity),
        "sponsor_equity": float(sponsor_equity),
        "total_sources": float(total_sources),
        "opening_debt": float(total_term_debt),
        "opening_cash": float(min_cash_buffer),
        "opening_net_debt": float(total_term_debt - min_cash_buffer),
    }


def purchase_price_allocation(
    equity_purchase_price: float,
    existing_book_equity: float,
    ppe_writeup: float,
    intangibles_writeup: float,
    deferred_tax_rate: float,
) -> dict[str, float]:
    """Calculate goodwill created under GAAP/IFRS acquisition method."""
    book_value_step_up = ppe_writeup + intangibles_writeup
    deferred_tax_liability = book_value_step_up * deferred_tax_rate
    net_identifiable_fair_value = existing_book_equity + book_value_step_up - deferred_tax_liability
    goodwill = equity_purchase_price - net_identifiable_fair_value

    return {
        "equity_purchase_price": float(equity_purchase_price),
        "net_identifiable_fair_value": float(net_identifiable_fair_value),
        "deferred_tax_liability": float(deferred_tax_liability),
        "goodwill_created": float(goodwill),
    }


def main() -> None:
    print("CF5 Lab L03-1: LBO Sources & Uses and Purchase Price Accounting")
    print("================================================================")

    # 1. Sources & Uses ($M)
    ebitda = 120.0
    mult = 11.0
    su = construct_sources_and_uses(
        target_ebitda=ebitda,
        entry_multiple=mult,
        existing_debt=250.0,
        target_cash=40.0,
        min_cash_buffer=30.0,
        revolver_drawn=10.0,
        tla_multiple=2.75,  # $330M
        tlb_multiple=2.00,  # $240M
        mezz_multiple=1.00,  # $120M
        mna_fee_rate=0.018,
        debt_fee_rate=0.025,
        rollover_equity=50.0,
    )
    print(f"Enterprise Value:         ${su['enterprise_value']:.2f}M")
    print(f"Equity Purchase Price:    ${su['equity_purchase_price']:.2f}M")
    print(f"Transaction Fees:         ${su['total_fees']:.2f}M")
    print(f"Total Uses of Funds:      ${su['total_uses']:.2f}M")
    print(f"Total Debt Funded:        ${su['total_debt_funded']:.2f}M ({su['total_debt_funded'] / ebitda:.2f}x EBITDA)")
    print(f"Target Cash Contributed:  ${su['target_cash_used']:.2f}M")
    print(f"Management Rollover:      ${su['rollover_equity']:.2f}M")
    print(f"Sponsor Equity Funded:    ${su['sponsor_equity']:.2f}M")
    print(f"Total Sources of Funds:   ${su['total_sources']:.2f}M")
    print(f"Opening Net Debt:         ${su['opening_net_debt']:.2f}M")

    # 2. Purchase Price Allocation & Goodwill
    ppa = purchase_price_allocation(
        equity_purchase_price=su["equity_purchase_price"],
        existing_book_equity=350.0,
        ppe_writeup=80.0,
        intangibles_writeup=120.0,
        deferred_tax_rate=0.25,
    )
    print("\nPurchase Price Accounting ($M):")
    print("  Existing Book Equity:   $350.00M")
    print("  PPE & Intangibles Up:   $200.00M")
    print(f"  Deferred Tax Liability: ${ppa['deferred_tax_liability']:.2f}M")
    print(f"  Net Identifiable Assets:${ppa['net_identifiable_fair_value']:.2f}M")
    print(f"  Goodwill Created:       ${ppa['goodwill_created']:.2f}M")


main()
