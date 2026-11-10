"""Instance generator for the CF5 LBO Model project.

Deterministic from seed. Exposes make_instance(seed: int) -> dict.
Standard library only.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid LBO project instance for the given seed.

    Provides target historical financials, operating forecast parameters,
    transaction structuring inputs (entry multiple, existing debt, fees, debt tranches),
    debt financing terms (TLA, TLB, amortization, interest rates), cash sweep policy,
    covenant schedules, and exit valuation assumptions.
    """
    rng = random.Random(seed)
    n_years = 5

    # 1. Base Target Financials (LTM / Year 0)
    revenue_0 = round(rng.uniform(300.0, 1200.0), 2)
    ebitda_margin_0 = round(rng.uniform(0.16, 0.25), 4)
    ebitda_0 = round(revenue_0 * ebitda_margin_0, 2)
    existing_debt = round(ebitda_0 * rng.uniform(1.0, 2.5), 2)
    target_cash = round(ebitda_0 * rng.uniform(0.3, 0.6), 2)
    min_cash = round(ebitda_0 * rng.uniform(0.15, 0.25), 2)

    # 2. Transaction Structuring Inputs
    entry_multiple = round(rng.uniform(9.5, 12.5), 2)
    txn_fee_rate = round(rng.uniform(0.015, 0.025), 4)  # % of Enterprise Value
    financing_fee_rate = round(rng.uniform(0.020, 0.030), 4)  # % of total funded debt
    rollover_equity = round(rng.uniform(10.0, 50.0), 2)

    # Leverage tranches (multiples of LTM EBITDA)
    tla_leverage = round(rng.uniform(2.5, 3.5), 2)
    tlb_leverage = round(rng.uniform(1.5, 2.5), 2)
    total_leverage = tla_leverage + tlb_leverage

    # 3. Debt Financing Terms
    tla_rate = round(rng.uniform(0.065, 0.085), 4)  # e.g., SOFR + 275 bps
    tlb_rate = round(rng.uniform(0.090, 0.115), 4)  # e.g., SOFR + 500 bps
    tla_amort_rate = round(rng.uniform(0.025, 0.050), 4)  # 2.5% - 5.0% annual mandatory amortization
    tlb_amort_rate = 0.0100  # 1.0% annual 1% amortization (standard Term Loan B)
    sweep_pct = 1.00  # 100% mandatory cash sweep of available excess cash

    # 4. Operating Forecast Assumptions (Years 1 to 5)
    tax_rate = round(rng.uniform(0.21, 0.25), 4)
    growth_rates = [round(rng.uniform(0.04, 0.09), 4) for _ in range(n_years)]
    ebitda_margins = [round(ebitda_margin_0 + (i + 1) * rng.uniform(0.004, 0.008), 4) for i in range(n_years)]
    capex_pcts = [round(rng.uniform(0.035, 0.050), 4) for _ in range(n_years)]
    da_pcts = [round(rng.uniform(0.025, 0.038), 4) for _ in range(n_years)]
    nwc_pcts = [round(rng.uniform(0.080, 0.120), 4) for _ in range(n_years)]  # % of delta revenue

    # 5. Exit Assumptions (Year 5)
    holding_period_years = 5.0
    exit_multiple = round(entry_multiple + rng.uniform(-1.0, 1.5), 2)

    # 6. Covenant Schedule
    # Decreasing max leverage covenant schedule
    max_leverage_schedule = [round(total_leverage + 0.50 - i * 0.40, 2) for i in range(n_years)]
    min_coverage = round(rng.uniform(2.0, 2.5), 2)

    return {
        "revenue_0": revenue_0,
        "ebitda_0": ebitda_0,
        "ebitda_margin_0": ebitda_margin_0,
        "existing_debt": existing_debt,
        "target_cash": target_cash,
        "min_cash": min_cash,
        "entry_multiple": entry_multiple,
        "txn_fee_rate": txn_fee_rate,
        "financing_fee_rate": financing_fee_rate,
        "rollover_equity": rollover_equity,
        "tla_leverage": tla_leverage,
        "tlb_leverage": tlb_leverage,
        "tla_rate": tla_rate,
        "tlb_rate": tlb_rate,
        "tla_amort_rate": tla_amort_rate,
        "tlb_amort_rate": tlb_amort_rate,
        "sweep_pct": sweep_pct,
        "tax_rate": tax_rate,
        "growth_rates": growth_rates,
        "ebitda_margins": ebitda_margins,
        "capex_pcts": capex_pcts,
        "da_pcts": da_pcts,
        "nwc_pcts": nwc_pcts,
        "holding_period_years": holding_period_years,
        "exit_multiple": exit_multiple,
        "max_leverage_schedule": max_leverage_schedule,
        "min_coverage": min_coverage,
    }
