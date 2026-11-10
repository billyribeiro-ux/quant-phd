"""Mutant 1: Omits financing fees from Uses of funds, causing Sources and Uses to misarticulate."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


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
) -> dict[str, Any]:
    """Construct Sources and Uses of funds for the buyout transaction.

    Validates inputs and enforces the fundamental identity: Total Sources == Total Uses.
    """
    if ebitda_0 <= 0.0:
        raise ValueError(f"ebitda_0 must be strictly positive, got {ebitda_0}")
    if entry_multiple <= 0.0:
        raise ValueError(f"entry_multiple must be strictly positive, got {entry_multiple}")
    if txn_fee_rate < 0.0 or txn_fee_rate >= 1.0:
        raise ValueError(f"txn_fee_rate must be in [0, 1), got {txn_fee_rate}")
    if financing_fee_rate < 0.0 or financing_fee_rate >= 1.0:
        raise ValueError(f"financing_fee_rate must be in [0, 1), got {financing_fee_rate}")
    if tla_leverage < 0.0 or tlb_leverage < 0.0:
        raise ValueError("Leverage multiples cannot be negative")
    if min_cash < 0.0:
        raise ValueError("min_cash cannot be negative")
    if rollover_equity < 0.0:
        raise ValueError("rollover_equity cannot be negative")

    # Enterprise and Equity values
    purchase_enterprise_value = round(ebitda_0 * entry_multiple, 4)
    # Target equity purchase price = Enterprise Value - Existing Debt + Target Cash
    # Target equity holders receive purchase price
    equity_purchase_price = round(purchase_enterprise_value - existing_debt + target_cash, 4)

    # Debt tranches issued
    tla_debt = round(ebitda_0 * tla_leverage, 4)
    tlb_debt = round(ebitda_0 * tlb_leverage, 4)
    total_debt_issued = round(tla_debt + tlb_debt, 4)

    # Transaction and financing fees
    txn_fees = round(purchase_enterprise_value * txn_fee_rate, 4)
    financing_fees = round(total_debt_issued * financing_fee_rate, 4)
    total_fees = round(txn_fees + financing_fees, 4)

    # Uses of Funds
    # Refinance existing debt: debt is retired at closing
    refinance_debt = round(existing_debt, 4)
    # MUTATION 1: omits financing fees
    total_uses = round(equity_purchase_price + refinance_debt + txn_fees + min_cash, 4)

    # Sources of Funds
    target_cash_used = round(min(target_cash, target_cash), 4)
    funded_debt = round(total_debt_issued, 4)
    non_sponsor_sources = round(funded_debt + target_cash_used + rollover_equity, 4)

    sponsor_equity = round(total_uses - non_sponsor_sources, 4)
    if sponsor_equity < 0.0:
        raise ValueError(f"Debt and rollover exceed total uses: sponsor equity would be negative ({sponsor_equity})")

    total_sources = round(funded_debt + target_cash_used + rollover_equity + sponsor_equity, 4)

    # Enforce exact identity
    identity_diff = abs(total_sources - total_uses)
    if identity_diff > 1e-4:
        raise AssertionError(f"Sources and Uses do not balance: diff = {identity_diff}")

    total_equity_0 = round(sponsor_equity + rollover_equity, 4)
    opening_cash = round(min_cash, 4)
    opening_net_debt = round(total_debt_issued - opening_cash, 4)

    return {
        "purchase_enterprise_value": purchase_enterprise_value,
        "equity_purchase_price": equity_purchase_price,
        "refinance_debt": refinance_debt,
        "txn_fees": txn_fees,
        "financing_fees": financing_fees,
        "total_fees": total_fees,
        "min_cash_funded": min_cash,
        "total_uses": total_uses,
        "tla_debt": tla_debt,
        "tlb_debt": tlb_debt,
        "total_debt_issued": total_debt_issued,
        "target_cash_used": target_cash_used,
        "rollover_equity": rollover_equity,
        "sponsor_equity": sponsor_equity,
        "total_sources": total_sources,
        "total_equity_0": total_equity_0,
        "opening_cash": opening_cash,
        "opening_net_debt": opening_net_debt,
    }


def forecast_operations(
    revenue_0: float,
    growth_rates: Sequence[float],
    ebitda_margins: Sequence[float],
    capex_pcts: Sequence[float],
    da_pcts: Sequence[float],
    nwc_pcts: Sequence[float],
    tax_rate: float,
) -> dict[str, list[float]]:
    """Generate multi-year operating forecast for revenues, EBITDA, EBIT, and unlevered cash flows."""
    if revenue_0 <= 0.0:
        raise ValueError(f"revenue_0 must be strictly positive, got {revenue_0}")
    if tax_rate < 0.0 or tax_rate >= 1.0:
        raise ValueError(f"tax_rate must be in [0, 1), got {tax_rate}")

    n = len(growth_rates)
    if not (len(ebitda_margins) == len(capex_pcts) == len(da_pcts) == len(nwc_pcts) == n):
        raise ValueError("All forecast sequences must have the same length")
    if n == 0:
        raise ValueError("Forecast period cannot be empty")

    revenues: list[float] = []
    ebitdas: list[float] = []
    das: list[float] = []
    ebits: list[float] = []
    capexs: list[float] = []
    delta_nwcs: list[float] = []
    unlevered_taxes: list[float] = []
    unlevered_fcfs: list[float] = []

    prev_rev = revenue_0
    for i in range(n):
        g = float(growth_rates[i])
        m = float(ebitda_margins[i])
        c_pct = float(capex_pcts[i])
        da_pct = float(da_pcts[i])
        nwc_pct = float(nwc_pcts[i])

        rev = round(prev_rev * (1.0 + g), 4)
        revenues.append(rev)

        ebitda = round(rev * m, 4)
        ebitdas.append(ebitda)

        da = round(rev * da_pct, 4)
        das.append(da)

        ebit = round(ebitda - da, 4)
        ebits.append(ebit)

        capex = round(rev * c_pct, 4)
        capexs.append(capex)

        delta_nwc = round((rev - prev_rev) * nwc_pct, 4)
        delta_nwcs.append(delta_nwc)

        tax = round(max(0.0, ebit * tax_rate), 4)
        unlevered_taxes.append(tax)

        ufcf = round(ebitda - capex - delta_nwc - tax, 4)
        unlevered_fcfs.append(ufcf)

        prev_rev = rev

    return {
        "revenues": revenues,
        "ebitdas": ebitdas,
        "das": das,
        "ebits": ebits,
        "capexs": capexs,
        "delta_nwcs": delta_nwcs,
        "unlevered_taxes": unlevered_taxes,
        "unlevered_fcfs": unlevered_fcfs,
    }


def run_debt_schedule(
    ebitda_forecast: Sequence[float],
    capex_forecast: Sequence[float],
    da_forecast: Sequence[float],
    delta_nwc_forecast: Sequence[float],
    tax_rate: float,
    tla_initial: float,
    tla_rate: float,
    tla_amort_rate: float,
    tlb_initial: float,
    tlb_rate: float,
    tlb_amort_rate: float,
    min_cash: float,
    initial_cash: float,
    sweep_pct: float = 1.0,
    interest_method: str = "beginning",
) -> dict[str, Any]:
    """Execute multi-tranche debt schedule with mandatory amortization and priority cash sweeps."""
    n = len(ebitda_forecast)
    if not (len(capex_forecast) == len(da_forecast) == len(delta_nwc_forecast) == n):
        raise ValueError("Forecast lengths must match")
    if tla_initial < 0.0 or tlb_initial < 0.0:
        raise ValueError("Initial debt balances cannot be negative")
    if tla_rate < 0.0 or tlb_rate < 0.0:
        raise ValueError("Interest rates cannot be negative")
    if min_cash < 0.0:
        raise ValueError("min_cash cannot be negative")
    if sweep_pct < 0.0 or sweep_pct > 1.0:
        raise ValueError(f"sweep_pct must be in [0, 1], got {sweep_pct}")
    if interest_method not in ("beginning", "average"):
        raise ValueError("interest_method must be 'beginning' or 'average'")

    beg_tla_list: list[float] = []
    end_tla_list: list[float] = []
    beg_tlb_list: list[float] = []
    end_tlb_list: list[float] = []
    tla_interest_list: list[float] = []
    tlb_interest_list: list[float] = []
    total_interest_list: list[float] = []
    tax_list: list[float] = []
    cfads_list: list[float] = []
    tla_mand_amort_list: list[float] = []
    tlb_mand_amort_list: list[float] = []
    total_mand_amort_list: list[float] = []
    tla_sweep_list: list[float] = []
    tlb_sweep_list: list[float] = []
    total_sweep_list: list[float] = []
    beg_cash_list: list[float] = []
    end_cash_list: list[float] = []
    total_debt_list: list[float] = []
    net_debt_list: list[float] = []

    curr_tla = float(tla_initial)
    curr_tlb = float(tlb_initial)
    curr_cash = float(initial_cash)

    for i in range(n):
        ebitda = float(ebitda_forecast[i])
        capex = float(capex_forecast[i])
        da = float(da_forecast[i])
        delta_nwc = float(delta_nwc_forecast[i])
        ebit = ebitda - da

        beg_tla_list.append(round(curr_tla, 4))
        beg_tlb_list.append(round(curr_tlb, 4))
        beg_cash_list.append(round(curr_cash, 4))

        # Interest calculation
        if interest_method == "beginning":
            int_tla = curr_tla * tla_rate
            int_tlb = curr_tlb * tlb_rate
        else:
            # First-order estimate using beginning balance for average
            int_tla = curr_tla * tla_rate
            int_tlb = curr_tlb * tlb_rate

        total_int = int_tla + int_tlb
        tla_interest_list.append(round(int_tla, 4))
        tlb_interest_list.append(round(int_tlb, 4))
        total_interest_list.append(round(total_int, 4))

        # Taxes with interest deductibility
        ebt = ebit - total_int
        tax = max(0.0, ebt * tax_rate)
        tax_list.append(round(tax, 4))

        # Cash flow available for debt service (CFADS)
        cfads = ebitda - capex - delta_nwc - total_int - tax
        cfads_list.append(round(cfads, 4))

        # Mandatory Amortization
        mand_tla = min(curr_tla, tla_initial * tla_amort_rate)
        mand_tlb = min(curr_tlb, tlb_initial * tlb_amort_rate)
        total_mand = mand_tla + mand_tlb
        tla_mand_amort_list.append(round(mand_tla, 4))
        tlb_mand_amort_list.append(round(mand_tlb, 4))
        total_mand_amort_list.append(round(total_mand, 4))

        # Cash balance prior to sweep
        cash_avail = curr_cash + cfads - total_mand
        excess_cash = max(0.0, cash_avail - min_cash)
        sweep_pool = excess_cash * sweep_pct

        # Apply sweep: TLA first, then TLB
        rem_tla = curr_tla - mand_tla
        sweep_tla = min(rem_tla, sweep_pool)
        rem_pool = sweep_pool - sweep_tla

        rem_tlb = curr_tlb - mand_tlb
        sweep_tlb = min(rem_tlb, rem_pool)
        total_sweep = sweep_tla + sweep_tlb

        tla_sweep_list.append(round(sweep_tla, 4))
        tlb_sweep_list.append(round(sweep_tlb, 4))
        total_sweep_list.append(round(total_sweep, 4))

        # Ending balances
        curr_tla = round(rem_tla - sweep_tla, 4)
        curr_tlb = round(rem_tlb - sweep_tlb, 4)
        curr_cash = round(cash_avail - total_sweep, 4)
        end_total_debt = round(curr_tla + curr_tlb, 4)
        end_net_debt = round(end_total_debt - curr_cash, 4)

        end_tla_list.append(curr_tla)
        end_tlb_list.append(curr_tlb)
        end_cash_list.append(curr_cash)
        total_debt_list.append(end_total_debt)
        net_debt_list.append(end_net_debt)

    return {
        "beg_tla": beg_tla_list,
        "end_tla": end_tla_list,
        "beg_tlb": beg_tlb_list,
        "end_tlb": end_tlb_list,
        "tla_interest": tla_interest_list,
        "tlb_interest": tlb_interest_list,
        "total_interest": total_interest_list,
        "taxes": tax_list,
        "cfads": cfads_list,
        "tla_mand_amort": tla_mand_amort_list,
        "tlb_mand_amort": tlb_mand_amort_list,
        "total_mand_amort": total_mand_amort_list,
        "tla_sweep": tla_sweep_list,
        "tlb_sweep": tlb_sweep_list,
        "total_sweep": total_sweep_list,
        "beg_cash": beg_cash_list,
        "end_cash": end_cash_list,
        "total_debt": total_debt_list,
        "net_debt": net_debt_list,
    }


def evaluate_covenants(
    total_debt: Sequence[float],
    cash: Sequence[float],
    interest: Sequence[float],
    ebitda: Sequence[float],
    max_leverage_schedule: Sequence[float],
    min_coverage: float,
) -> dict[str, Any]:
    """Evaluate financial covenants across forecast periods."""
    n = len(total_debt)
    if not (len(cash) == len(interest) == len(ebitda) == len(max_leverage_schedule) == n):
        raise ValueError("All sequences must have identical lengths")

    leverage_ratios: list[float] = []
    interest_coverages: list[float] = []
    leverage_breaches: list[bool] = []
    coverage_breaches: list[bool] = []

    for i in range(n):
        d = float(total_debt[i])
        eb = float(ebitda[i])
        intr = float(interest[i])
        max_lev = float(max_leverage_schedule[i])

        lev = round(d / eb, 4) if eb > 0 else float("inf")
        leverage_ratios.append(lev)
        lev_breach = lev > max_lev
        leverage_breaches.append(lev_breach)

        cov = round(eb / intr, 4) if intr > 0 else float("inf")
        interest_coverages.append(cov)
        cov_breach = cov < min_coverage
        coverage_breaches.append(cov_breach)

    is_compliant = not (any(leverage_breaches) or any(coverage_breaches))

    return {
        "leverage_ratios": leverage_ratios,
        "interest_coverages": interest_coverages,
        "leverage_breaches": leverage_breaches,
        "coverage_breaches": coverage_breaches,
        "is_compliant": is_compliant,
    }


def calculate_returns_and_attribution(
    entry_ebitda: float,
    exit_ebitda: float,
    entry_multiple: float,
    exit_multiple: float,
    sponsor_equity_0: float,
    exit_net_debt: float,
    holding_period_years: float,
    rollover_equity_0: float = 0.0,
) -> dict[str, Any]:
    """Compute exit equity value, MOIC, IRR, and Kaplan-Strömberg value creation attribution.

    Decomposes total equity gain into:
      1. EBITDA growth (operational improvement)
      2. Multiple expansion (market re-rating)
      3. Deleveraging / debt paydown (financial leverage)
    """
    if entry_ebitda <= 0.0 or exit_ebitda <= 0.0:
        raise ValueError("EBITDA values must be strictly positive")
    if entry_multiple <= 0.0 or exit_multiple <= 0.0:
        raise ValueError("Multiples must be strictly positive")
    if sponsor_equity_0 <= 0.0:
        raise ValueError("sponsor_equity_0 must be strictly positive")
    if holding_period_years <= 0.0:
        raise ValueError("holding_period_years must be strictly positive")

    entry_ev = round(entry_ebitda * entry_multiple, 4)
    exit_ev = round(exit_ebitda * exit_multiple, 4)
    exit_equity_total = round(exit_ev - exit_net_debt, 4)

    total_equity_0 = round(sponsor_equity_0 + rollover_equity_0, 4)
    sponsor_share = round(sponsor_equity_0 / total_equity_0, 6)

    sponsor_exit_equity = round(exit_equity_total * sponsor_share, 4)
    sponsor_gain = round(sponsor_exit_equity - sponsor_equity_0, 4)

    moic = round(sponsor_exit_equity / sponsor_equity_0, 4)
    irr = round((moic ** (1.0 / holding_period_years)) - 1.0, 4)

    # Total equity bridge & Kaplan-Strömberg attribution
    # Entry net debt implied by bridge: Entry Net Debt = Entry EV - Total Entry Equity
    entry_net_debt = round(entry_ev - total_equity_0, 4)
    total_equity_gain = round(exit_equity_total - total_equity_0, 4)

    # Attribution components:
    # 1. Operational Improvement (EBITDA growth at entry multiple)
    delta_ebitda_growth = round((exit_ebitda - entry_ebitda) * entry_multiple, 4)
    # 2. Multiple Expansion (exit EBITDA at change in multiple)
    delta_multiple_expansion = round(exit_ebitda * (exit_multiple - entry_multiple), 4)
    # 3. Deleveraging / Debt Paydown (reduction in net debt)
    delta_deleveraging = round(entry_net_debt - exit_net_debt, 4)

    # Check exact sum identity
    sum_components = round(delta_ebitda_growth + delta_multiple_expansion + delta_deleveraging, 4)
    diff = abs(sum_components - total_equity_gain)
    if diff > 1e-3:
        raise AssertionError(f"Attribution does not articulate: sum={sum_components}, total={total_equity_gain}")

    # Percentage breakdown of equity creation
    if abs(total_equity_gain) > 1e-6:
        pct_ebitda = round(delta_ebitda_growth / total_equity_gain, 4)
        pct_multiple = round(delta_multiple_expansion / total_equity_gain, 4)
        pct_deleveraging = round(delta_deleveraging / total_equity_gain, 4)
    else:
        pct_ebitda = 0.0
        pct_multiple = 0.0
        pct_deleveraging = 0.0

    return {
        "entry_ev": entry_ev,
        "exit_ev": exit_ev,
        "exit_equity_total": exit_equity_total,
        "sponsor_share": sponsor_share,
        "sponsor_exit_equity": sponsor_exit_equity,
        "sponsor_gain": sponsor_gain,
        "moic": moic,
        "irr": irr,
        "total_equity_0": total_equity_0,
        "entry_net_debt": entry_net_debt,
        "exit_net_debt": exit_net_debt,
        "total_equity_gain": total_equity_gain,
        "delta_ebitda_growth": delta_ebitda_growth,
        "delta_multiple_expansion": delta_multiple_expansion,
        "delta_deleveraging": delta_deleveraging,
        "pct_ebitda_growth": pct_ebitda,
        "pct_multiple_expansion": pct_multiple,
        "pct_deleveraging": pct_deleveraging,
    }


def run_lbo_model(params: dict[str, Any]) -> dict[str, Any]:
    """Execute the complete end-to-end LBO model pipeline."""
    # 1. Sources and Uses
    su = build_sources_and_uses(
        ebitda_0=float(params["ebitda_0"]),
        entry_multiple=float(params["entry_multiple"]),
        existing_debt=float(params["existing_debt"]),
        min_cash=float(params["min_cash"]),
        target_cash=float(params["target_cash"]),
        txn_fee_rate=float(params["txn_fee_rate"]),
        financing_fee_rate=float(params["financing_fee_rate"]),
        tla_leverage=float(params["tla_leverage"]),
        tlb_leverage=float(params["tlb_leverage"]),
        rollover_equity=float(params.get("rollover_equity", 0.0)),
    )

    # 2. Operating Forecast
    ops = forecast_operations(
        revenue_0=float(params["revenue_0"]),
        growth_rates=params["growth_rates"],
        ebitda_margins=params["ebitda_margins"],
        capex_pcts=params["capex_pcts"],
        da_pcts=params["da_pcts"],
        nwc_pcts=params["nwc_pcts"],
        tax_rate=float(params["tax_rate"]),
    )

    # 3. Debt Schedule & Cash Sweep
    debt = run_debt_schedule(
        ebitda_forecast=ops["ebitdas"],
        capex_forecast=ops["capexs"],
        da_forecast=ops["das"],
        delta_nwc_forecast=ops["delta_nwcs"],
        tax_rate=float(params["tax_rate"]),
        tla_initial=float(su["tla_debt"]),
        tla_rate=float(params["tla_rate"]),
        tla_amort_rate=float(params["tla_amort_rate"]),
        tlb_initial=float(su["tlb_debt"]),
        tlb_rate=float(params["tlb_rate"]),
        tlb_amort_rate=float(params["tlb_amort_rate"]),
        min_cash=float(params["min_cash"]),
        initial_cash=float(su["opening_cash"]),
        sweep_pct=float(params.get("sweep_pct", 1.0)),
    )

    # 4. Covenant Checks
    covs = evaluate_covenants(
        total_debt=debt["total_debt"],
        cash=debt["end_cash"],
        interest=debt["total_interest"],
        ebitda=ops["ebitdas"],
        max_leverage_schedule=params["max_leverage_schedule"],
        min_coverage=float(params["min_coverage"]),
    )

    # 5. Exit Valuation and Value Creation Attribution
    exit_ebitda = ops["ebitdas"][-1]
    exit_net_debt = debt["net_debt"][-1]
    returns = calculate_returns_and_attribution(
        entry_ebitda=float(params["ebitda_0"]),
        exit_ebitda=exit_ebitda,
        entry_multiple=float(params["entry_multiple"]),
        exit_multiple=float(params["exit_multiple"]),
        sponsor_equity_0=float(su["sponsor_equity"]),
        exit_net_debt=exit_net_debt,
        holding_period_years=float(params["holding_period_years"]),
        rollover_equity_0=float(su["rollover_equity"]),
    )

    return {
        "sources_and_uses": su,
        "operating_forecast": ops,
        "debt_schedule": debt,
        "covenants": covs,
        "returns": returns,
    }
