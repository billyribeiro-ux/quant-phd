"""Instance generator for the CF4 Valuation engine project (Atlas A16).

Deterministic from seed. Exposes make_instance(seed: int) -> dict.
Standard library only.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid project instance for the given seed.

    Provides multi-year financial forecasts, capital structure parameters,
    WACC, cost of equity, terminal assumptions, bridge items, Ohlson RI inputs,
    and scenario grids.
    """
    rng = random.Random(seed)
    n_years = 5

    # Base operating scale
    rev_0 = round(rng.uniform(500.0, 2500.0), 2)
    ebit_margin = round(rng.uniform(0.12, 0.24), 4)
    tax_rate = round(rng.uniform(0.20, 0.28), 4)

    # 5-year forecasts
    growth_rates = [round(rng.uniform(0.04, 0.12), 4) for _ in range(n_years)]
    revenues: list[float] = []
    ebits: list[float] = []
    depreciations: list[float] = []
    capexs: list[float] = []
    delta_nwcs: list[float] = []
    fcffs: list[float] = []

    curr_rev = rev_0
    for g in growth_rates:
        curr_rev = round(curr_rev * (1.0 + g), 2)
        revenues.append(curr_rev)
        ebit = round(curr_rev * ebit_margin, 2)
        ebits.append(ebit)
        depr = round(curr_rev * rng.uniform(0.03, 0.05), 2)
        depreciations.append(depr)
        capex = round(curr_rev * rng.uniform(0.04, 0.07), 2)
        capexs.append(capex)
        dnwc = round(curr_rev * g * rng.uniform(0.08, 0.15), 2)
        delta_nwcs.append(dnwc)
        nopat = round(ebit * (1.0 - tax_rate), 4)
        fcff = round(nopat + depr - capex - dnwc, 4)
        fcffs.append(fcff)

    # Discount rates
    rf = round(rng.uniform(0.03, 0.045), 4)
    beta = round(rng.uniform(0.85, 1.35), 3)
    erp = round(rng.uniform(0.05, 0.065), 4)
    cost_of_equity = round(rf + beta * erp, 4)

    debt_weight = round(rng.uniform(0.20, 0.40), 2)
    equity_weight = round(1.0 - debt_weight, 2)
    pretax_debt_cost = round(rf + rng.uniform(0.015, 0.035), 4)
    aftertax_debt_cost = round(pretax_debt_cost * (1.0 - tax_rate), 4)
    wacc = round(equity_weight * cost_of_equity + debt_weight * aftertax_debt_cost, 4)

    # Terminal parameters (ensure wacc - terminal_growth >= 0.035)
    terminal_growth = round(rng.uniform(0.018, min(0.028, wacc - 0.035)), 4)
    exit_multiple = round(rng.uniform(9.0, 14.0), 2)
    terminal_ebitda = round(ebits[-1] + depreciations[-1], 2)

    # Capital claims and bridge items
    total_debt = round(rng.uniform(200.0, 800.0), 2)
    cash = round(rng.uniform(50.0, 300.0), 2)
    minority_interest = round(rng.uniform(0.0, 50.0), 2)
    preferred_stock = round(rng.uniform(0.0, 30.0), 2)
    non_operating_assets = round(rng.uniform(10.0, 80.0), 2)
    shares_outstanding = round(rng.uniform(50.0, 150.0), 2)

    # Ohlson Residual income inputs
    initial_book_equity = round(rng.uniform(400.0, 1200.0), 2)
    net_incomes: list[float] = []
    dividends: list[float] = []
    payout_ratio = round(rng.uniform(0.30, 0.50), 2)
    for ebit in ebits:
        interest_exp = round(total_debt * pretax_debt_cost, 2)
        ebt = max(10.0, ebit - interest_exp)
        ni = round(ebt * (1.0 - tax_rate), 2)
        net_incomes.append(ni)
        div = round(ni * payout_ratio, 2)
        dividends.append(div)
    omega = round(rng.uniform(0.40, 0.70), 3)

    # Peer multiples
    ebitda_peer_multiple = round(rng.uniform(10.0, 13.0), 2)
    pe_peer_multiple = round(rng.uniform(15.0, 22.0), 2)

    # Sensitivity ranges
    wacc_center = wacc
    wacc_range = [round(wacc_center + delta, 4) for delta in [-0.010, -0.005, 0.0, 0.005, 0.010]]
    growth_center = terminal_growth
    growth_range = [round(growth_center + delta, 4) for delta in [-0.006, -0.003, 0.0, 0.003, 0.006]]

    # Scenarios: Bear, Base, Bull
    bear_fcff = [round(f * 0.80, 4) for f in fcffs]
    bull_fcff = [round(f * 1.25, 4) for f in fcffs]
    scenario_weights = [0.25, 0.50, 0.25]
    scenario_waccs = [round(wacc + 0.01, 4), wacc, max(0.05, round(wacc - 0.008, 4))]
    scenario_growths = [
        max(0.01, round(terminal_growth - 0.005, 4)),
        terminal_growth,
        round(terminal_growth + 0.005, 4),
    ]

    return {
        "seed": seed,
        "n_years": n_years,
        "revenues": revenues,
        "ebits": ebits,
        "tax_rate": tax_rate,
        "depreciations": depreciations,
        "capexs": capexs,
        "delta_nwcs": delta_nwcs,
        "fcffs": fcffs,
        "cost_of_equity": cost_of_equity,
        "wacc": wacc,
        "terminal_growth": terminal_growth,
        "exit_multiple": exit_multiple,
        "terminal_ebitda": terminal_ebitda,
        "total_debt": total_debt,
        "cash": cash,
        "minority_interest": minority_interest,
        "preferred_stock": preferred_stock,
        "non_operating_assets": non_operating_assets,
        "shares_outstanding": shares_outstanding,
        "initial_book_equity": initial_book_equity,
        "net_incomes": net_incomes,
        "dividends": dividends,
        "omega": omega,
        "ebitda_peer_multiple": ebitda_peer_multiple,
        "pe_peer_multiple": pe_peer_multiple,
        "wacc_range": wacc_range,
        "growth_range": growth_range,
        "scenario_weights": scenario_weights,
        "scenario_waccs": scenario_waccs,
        "scenario_growths": scenario_growths,
        "bear_fcff": bear_fcff,
        "bull_fcff": bull_fcff,
    }
