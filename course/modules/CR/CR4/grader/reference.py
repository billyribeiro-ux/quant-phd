"""Reference solution for CR4 Capital Structure Recovery Waterfall & Fulcrum Engine.

Implements strict waterfall allocation, consensual plan carve-outs, Plan of Reorganization
consideration distribution (cash, take-back paper, equity), and distressed debt investor returns.
"""

from __future__ import annotations

import copy
import math
from typing import Any

try:
    from integrity import (  # type: ignore[import-not-found, unused-ignore]
        validate_carveout,
        validate_por_params,
        validate_returns_params,
        validate_scenarios,
        validate_tranches,
    )
except ImportError:
    from .integrity import (  # type: ignore[import-not-found, no-redef, unused-ignore]
        validate_carveout,
        validate_por_params,
        validate_returns_params,
        validate_scenarios,
        validate_tranches,
    )


def calculate_waterfall_strict(
    tranches: list[dict[str, Any]],
    ev: float,
) -> list[dict[str, Any]]:
    """Allocate enterprise value down the capital structure according to strict Absolute Priority Rule.

    Identifies the unique fulcrum security tranche.
    """
    validate_tranches(tranches)
    if not isinstance(ev, (int, float)) or not math.isfinite(ev) or ev < 0.0:
        raise ValueError(f"Enterprise value must be non-negative and finite, got {ev}")

    remaining_ev = float(ev)
    results: list[dict[str, Any]] = []

    # Check total debt claims
    total_debt_claims = sum(float(t["claim"]) for t in tranches if t["claim"] > 0)

    for t in tranches:
        claim = float(t["claim"])
        name = str(t["name"])
        sen = int(t["seniority"])

        if claim > 0:
            allocated = min(remaining_ev, claim)
            remaining_ev -= allocated
            recovery_pct = allocated / claim
            deficiency = claim - allocated
        else:
            # Equity or zero-claim residual
            if remaining_ev > 0 and abs(remaining_ev) > 1e-9:
                allocated = remaining_ev
                remaining_ev = 0.0
                recovery_pct = 1.0
                deficiency = 0.0
            else:
                allocated = 0.0
                recovery_pct = 0.0
                deficiency = 0.0

        results.append(
            {
                "name": name,
                "claim": claim,
                "seniority": sen,
                "allocated": round(allocated, 6),
                "recovery_pct": round(recovery_pct, 6),
                "deficiency": round(deficiency, 6),
                "is_fulcrum": False,
            }
        )

    # Fulcrum identification:
    # 1. Any debt tranche with partial recovery (0 < allocated < claim) is the fulcrum.
    # 2. If ev == 0, the first tranche with claim > 0 is fulcrum.
    # 3. If ev exactly matches cumulative claims up to tranche k and k < debt tranches, tranche k is fulcrum.
    # 4. If all debt claims are 100% satisfied (ev >= total_debt_claims), no debt tranche is fulcrum.
    fulcrum_idx: int | None = None

    if ev == 0.0:
        for idx, r in enumerate(results):
            if r["claim"] > 0:
                fulcrum_idx = idx
                break
    elif ev < total_debt_claims:
        cum_claim = 0.0
        for idx, r in enumerate(results):
            if r["claim"] > 0:
                cum_claim += r["claim"]
                is_partial = 0.0 < r["allocated"] < r["claim"]
                is_exact_match = abs(r["allocated"] - r["claim"]) < 1e-6 and abs(cum_claim - ev) < 1e-6
                if is_partial or is_exact_match:
                    fulcrum_idx = idx
                    break

    if fulcrum_idx is not None:
        results[fulcrum_idx]["is_fulcrum"] = True

    return results


def calculate_waterfall_with_carveout(
    tranches: list[dict[str, Any]],
    ev: float,
    carveout: dict[str, Any],
) -> list[dict[str, Any]]:
    """Apply consensual plan carve-out / APR violation adjustments to strict waterfall.

    Transfers a percentage of the source tranche's allocated recovery to the target tranche.
    Preserves exact conservation of distributed value.
    """
    tranche_names = [str(t["name"]) for t in tranches]
    validate_carveout(carveout, tranche_names)

    strict_results = calculate_waterfall_strict(tranches, ev)
    adjusted = copy.deepcopy(strict_results)

    src_name = carveout["source_tranche"]
    tgt_name = carveout["target_tranche"]
    pct = float(carveout["carveout_pct"])

    src_item = next(item for item in adjusted if item["name"] == src_name)
    tgt_item = next(item for item in adjusted if item["name"] == tgt_name)

    carveout_amount = round(src_item["allocated"] * pct, 6)

    src_item["allocated"] = round(src_item["allocated"] - carveout_amount, 6)
    if src_item["claim"] > 0:
        src_item["recovery_pct"] = round(src_item["allocated"] / src_item["claim"], 6)
        src_item["deficiency"] = round(src_item["claim"] - src_item["allocated"], 6)

    tgt_item["allocated"] = round(tgt_item["allocated"] + carveout_amount, 6)
    if tgt_item["claim"] > 0:
        tgt_item["recovery_pct"] = round(tgt_item["allocated"] / tgt_item["claim"], 6)
        tgt_item["deficiency"] = round(max(0.0, tgt_item["claim"] - tgt_item["allocated"]), 6)
    else:
        tgt_item["recovery_pct"] = 1.0 if tgt_item["allocated"] > 0 else 0.0
        tgt_item["deficiency"] = 0.0

    return adjusted


def reorganization_equity_distribution(
    tranches: list[dict[str, Any]],
    ev: float,
    new_debt_issued: float,
    cash_dist: float,
) -> dict[str, Any]:
    """Distribute Plan of Reorganization (POR) consideration: cash, take-back debt, and reorganized equity."""
    validate_tranches(tranches)
    validate_por_params(ev, new_debt_issued, cash_dist)

    reorg_equity_val = round(max(0.0, ev - new_debt_issued - cash_dist), 6)

    rem_cash = float(cash_dist)
    rem_debt = float(new_debt_issued)
    rem_equity = float(reorg_equity_val)

    tranche_dists: list[dict[str, Any]] = []

    for t in tranches:
        claim = float(t["claim"])
        name = str(t["name"])
        sen = int(t["seniority"])

        if claim > 0:
            unmet = claim

            cash_alloc = min(rem_cash, unmet)
            rem_cash -= cash_alloc
            unmet -= cash_alloc

            debt_alloc = min(rem_debt, unmet)
            rem_debt -= debt_alloc
            unmet -= debt_alloc

            equity_alloc = min(rem_equity, unmet)
            rem_equity -= equity_alloc
            unmet -= equity_alloc
        else:
            # Common equity gets any residual reorganized equity
            cash_alloc = 0.0
            debt_alloc = 0.0
            equity_alloc = rem_equity
            rem_equity = 0.0

        total_alloc = cash_alloc + debt_alloc + equity_alloc
        equity_pct = (equity_alloc / reorg_equity_val) if reorg_equity_val > 0 else 0.0

        tranche_dists.append(
            {
                "name": name,
                "seniority": sen,
                "claim": claim,
                "cash_allocated": round(cash_alloc, 6),
                "debt_allocated": round(debt_alloc, 6),
                "equity_allocated": round(equity_alloc, 6),
                "total_allocated": round(total_alloc, 6),
                "equity_ownership_pct": round(equity_pct, 6),
            }
        )

    return {
        "reorg_equity_value": reorg_equity_val,
        "cash_distributed": round(cash_dist, 6),
        "new_debt_distributed": round(new_debt_issued, 6),
        "tranche_distributions": tranche_dists,
    }


def evaluate_expected_returns(
    tranches: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    purchase_prices: dict[str, float],
    holding_period_years: float,
) -> dict[str, Any]:
    """Evaluate scenario-weighted expected recovery, MOIC, and annualized IRR across tranches."""
    validate_tranches(tranches)
    validate_scenarios(scenarios)
    validate_returns_params(purchase_prices, holding_period_years)

    # Compute strict allocations for each scenario
    scenario_allocations: dict[str, list[dict[str, Any]]] = {}
    for s in scenarios:
        s_name = s["name"]
        ev = float(s["ev"])
        scenario_allocations[s_name] = calculate_waterfall_strict(tranches, ev)

    tranche_returns: list[dict[str, Any]] = []
    total_cost = 0.0
    total_expected_recovery = 0.0

    for t in tranches:
        name = str(t["name"])
        claim = float(t["claim"])

        # Expected recovery in dollars
        exp_rec_dollars = sum(
            float(s["prob"])
            * next(item["allocated"] for item in scenario_allocations[s["name"]] if item["name"] == name)
            for s in scenarios
        )
        exp_rec_dollars = round(exp_rec_dollars, 6)
        exp_rec_pct = round(exp_rec_dollars / claim, 6) if claim > 0 else 0.0

        entry_price = purchase_prices.get(name)
        if entry_price is not None and claim > 0:
            invested = round(entry_price * claim, 6)
            total_cost += invested
            total_expected_recovery += exp_rec_dollars

            moic = round(exp_rec_dollars / invested, 6) if invested > 0 else 0.0
            irr = round((moic ** (1.0 / holding_period_years)) - 1.0, 6) if moic > 0.0 else -1.0
        else:
            invested = None
            moic = None
            irr = None

        tranche_returns.append(
            {
                "name": name,
                "claim": claim,
                "expected_recovery_dollars": exp_rec_dollars,
                "expected_recovery_pct": exp_rec_pct,
                "purchase_price": entry_price,
                "capital_invested": invested,
                "moic": moic,
                "irr": irr,
            }
        )

    portfolio_moic = round(total_expected_recovery / total_cost, 6) if total_cost > 0 else 0.0
    portfolio_irr = round((portfolio_moic ** (1.0 / holding_period_years)) - 1.0, 6) if portfolio_moic > 0.0 else -1.0

    return {
        "holding_period_years": holding_period_years,
        "total_capital_invested": round(total_cost, 6),
        "total_expected_recovery": round(total_expected_recovery, 6),
        "portfolio_moic": portfolio_moic,
        "portfolio_irr": portfolio_irr,
        "tranche_returns": tranche_returns,
    }


def run_waterfall_engine(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute end-to-end recovery waterfall analysis on instance."""
    tranches = instance["tranches"]
    scenarios = instance["scenarios"]
    carveout = instance["carveout"]
    por = instance["por"]
    purchase_prices = instance["purchase_prices"]
    holding_period = instance["holding_period_years"]

    scenario_results: list[dict[str, Any]] = []
    for s in scenarios:
        s_res = calculate_waterfall_strict(tranches, float(s["ev"]))
        scenario_results.append(
            {
                "scenario_name": s["name"],
                "ev": s["ev"],
                "prob": s["prob"],
                "waterfall": s_res,
            }
        )

    # Carveout for base scenario
    base_ev = next(s["ev"] for s in scenarios if s["name"] == por["scenario_name"])
    carveout_results = calculate_waterfall_with_carveout(tranches, float(base_ev), carveout)

    # POR distribution for base scenario
    por_results = reorganization_equity_distribution(
        tranches,
        float(base_ev),
        float(por["new_debt_issued"]),
        float(por["cash_dist"]),
    )

    # Expected returns
    returns_results = evaluate_expected_returns(
        tranches,
        scenarios,
        purchase_prices,
        float(holding_period),
    )

    return {
        "company_name": instance["company_name"],
        "scenarios": scenario_results,
        "carveout_results": carveout_results,
        "por_distribution": por_results,
        "expected_returns": returns_results,
    }
