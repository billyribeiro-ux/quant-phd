"""Deterministic problem instance generator for CF7: Financial Modeling.

Generates seeded company cases with historical balance sheet and income statement,
forward operating assumptions, debt parameters, and valuation inputs.
"""

from __future__ import annotations

import functools
import random
from typing import Any


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, self-consistent company modeling case from seed."""
    rng = random.Random(seed)

    company_prefixes = ["Apex", "Vertex", "Quantum", "Nexus", "Titan", "Solaris", "Vanguard", "Aero"]
    company_suffixes = ["Dynamics", "Systems", "Technologies", "Industries", "Holdings", "Robotics"]
    prefix = company_prefixes[seed % len(company_prefixes)]
    suffix = company_suffixes[(seed // len(company_prefixes)) % len(company_suffixes)]
    name = f"{prefix} {suffix} Corp"

    # Scale: Base revenue between $200M and $800M (in millions)
    base_rev = round(rng.uniform(250.0, 750.0), 2)
    base_gross_margin = round(rng.uniform(0.40, 0.55), 4)
    base_sga_pct = round(rng.uniform(0.18, 0.26), 4)
    base_depr_pct = round(rng.uniform(0.08, 0.12), 4)
    base_capex_pct = round(rng.uniform(0.05, 0.08), 4)

    tax_rate = round(rng.uniform(0.21, 0.28), 4)
    dso = round(rng.uniform(40.0, 55.0), 1)
    dio = round(rng.uniform(50.0, 70.0), 1)
    dpo = round(rng.uniform(35.0, 50.0), 1)

    # Historical Year 0 calculations
    cogs_0 = round(base_rev * (1.0 - base_gross_margin), 2)
    gross_profit_0 = round(base_rev - cogs_0, 2)
    sga_0 = round(base_rev * base_sga_pct, 2)
    ebitda_0 = round(gross_profit_0 - sga_0, 2)

    net_ppe_0 = round(base_rev * rng.uniform(0.40, 0.60), 2)
    depr_0 = round(net_ppe_0 * base_depr_pct, 2)
    ebit_0 = round(ebitda_0 - depr_0, 2)

    ar_0 = round(base_rev * (dso / 365.0), 2)
    inv_0 = round(cogs_0 * (dio / 365.0), 2)
    ap_0 = round(cogs_0 * (dpo / 365.0), 2)

    # Debt structure
    term_debt_0 = round(base_rev * rng.uniform(0.20, 0.35), 2)
    term_rate = round(rng.uniform(0.055, 0.075), 4)
    revolver_rate = round(term_rate + rng.uniform(0.01, 0.02), 4)
    cash_rate = round(rng.uniform(0.015, 0.025), 4)

    revolver_0 = round(rng.uniform(0.0, 25.0), 2)
    total_debt_0 = round(term_debt_0 + revolver_0, 2)

    min_cash = round(base_rev * rng.uniform(0.05, 0.08), 2)
    cash_0 = round(min_cash + rng.uniform(5.0, 20.0), 2)

    interest_exp_0 = round(term_debt_0 * term_rate + revolver_0 * revolver_rate, 2)
    interest_inc_0 = round(cash_0 * cash_rate, 2)
    ebt_0 = round(ebit_0 - interest_exp_0 + interest_inc_0, 2)
    tax_0 = round(max(0.0, ebt_0 * tax_rate), 2)
    net_income_0 = round(ebt_0 - tax_0, 2)

    total_assets_0 = round(cash_0 + ar_0 + inv_0 + net_ppe_0, 2)
    total_liab_0 = round(ap_0 + revolver_0 + term_debt_0, 2)
    total_equity_0 = round(total_assets_0 - total_liab_0, 2)
    common_stock_0 = round(total_equity_0 * rng.uniform(0.40, 0.60), 2)
    retained_earnings_0 = round(total_equity_0 - common_stock_0, 2)

    # 3-Year Projection Assumptions
    horizon = 3
    rev_growth = [
        round(rng.uniform(0.06, 0.12), 4),
        round(rng.uniform(0.05, 0.10), 4),
        round(rng.uniform(0.04, 0.08), 4),
    ]
    gross_margins = [
        round(base_gross_margin + rng.uniform(-0.01, 0.01), 4),
        round(base_gross_margin + rng.uniform(-0.01, 0.015), 4),
        round(base_gross_margin + rng.uniform(0.0, 0.02), 4),
    ]
    sga_pcts = [round(base_sga_pct - 0.002 * t, 4) for t in range(horizon)]
    depr_pcts = [base_depr_pct] * horizon
    capex_pcts = [round(base_capex_pct + rng.uniform(-0.005, 0.005), 4) for _ in range(horizon)]

    term_amort = round(term_debt_0 / 5.0, 2)
    term_amort_schedule = [term_amort] * horizon

    revolver_commitment = round(total_debt_0 * 1.5, 2)
    dividend_payout = round(rng.uniform(0.15, 0.30), 4)

    # Valuation parameters
    wacc = round(rng.uniform(0.085, 0.115), 4)
    terminal_g = round(rng.uniform(0.020, 0.030), 4)
    shares_outstanding = round(rng.uniform(15.0, 40.0), 2)

    return {
        "seed": seed,
        "company_name": name,
        "currency": "USD",
        "horizon": horizon,
        "historical_data": {
            "revenue": base_rev,
            "cogs": cogs_0,
            "gross_profit": gross_profit_0,
            "sga": sga_0,
            "ebitda": ebitda_0,
            "depreciation": depr_0,
            "ebit": ebit_0,
            "interest_expense": interest_exp_0,
            "interest_income": interest_inc_0,
            "ebt": ebt_0,
            "tax": tax_0,
            "net_income": net_income_0,
            "cash": cash_0,
            "accounts_receivable": ar_0,
            "inventory": inv_0,
            "net_ppe": net_ppe_0,
            "total_assets": total_assets_0,
            "accounts_payable": ap_0,
            "revolver_balance": revolver_0,
            "term_debt": term_debt_0,
            "total_debt": total_debt_0,
            "total_liabilities": total_liab_0,
            "common_stock": common_stock_0,
            "retained_earnings": retained_earnings_0,
            "total_equity": total_equity_0,
        },
        "operating_assumptions": {
            "revenue_growth": rev_growth,
            "gross_margin": gross_margins,
            "sga_pct_revenue": sga_pcts,
            "depreciation_pct_ppe": depr_pcts,
            "capex_pct_revenue": capex_pcts,
            "dso": dso,
            "dio": dio,
            "dpo": dpo,
            "tax_rate": tax_rate,
        },
        "debt_assumptions": {
            "term_debt_amortization": term_amort_schedule,
            "term_debt_interest_rate": term_rate,
            "revolver_commitment": revolver_commitment,
            "revolver_interest_rate": revolver_rate,
            "cash_interest_rate": cash_rate,
            "minimum_cash": min_cash,
            "dividend_payout_ratio": dividend_payout,
        },
        "valuation_assumptions": {
            "wacc": wacc,
            "terminal_growth_rate": terminal_g,
            "shares_outstanding": shares_outstanding,
        },
    }
