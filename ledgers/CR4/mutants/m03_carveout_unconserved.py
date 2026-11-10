"""Mutant 3: Deducts carveout from source tranche but only credits 80% to target tranche violating conservation."""

from __future__ import annotations

import copy
import math
from typing import Any

from integrity import (  # type: ignore[import-not-found, unused-ignore]
    validate_carveout,
    validate_tranches,
)


def calculate_waterfall_strict(
    tranches: list[dict[str, Any]],
    ev: float,
) -> list[dict[str, Any]]:
    validate_tranches(tranches)
    if not isinstance(ev, (int, float)) or not math.isfinite(ev) or ev < 0.0:
        raise ValueError(f"Enterprise value must be non-negative and finite, got {ev}")

    remaining_ev = float(ev)
    results: list[dict[str, Any]] = []
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
            if remaining_ev > 0:
                allocated = remaining_ev
                remaining_ev = 0.0
                recovery_pct = 1.0
                deficiency = 0.0
            else:
                allocated = 0.0
                recovery_pct = 0.0
                deficiency = 0.0

        results.append({
            "name": name,
            "claim": claim,
            "seniority": sen,
            "allocated": round(allocated, 6),
            "recovery_pct": round(recovery_pct, 6),
            "deficiency": round(deficiency, 6),
            "is_fulcrum": False,
        })

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
                if 0.0 < r["allocated"] < r["claim"] or (abs(r["allocated"] - r["claim"]) < 1e-6 and abs(cum_claim - ev) < 1e-6):
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

    # Bug: Only credits 80% to target, leaking 20% of carve-out
    tgt_item["allocated"] = round(tgt_item["allocated"] + carveout_amount * 0.8, 6)
    return adjusted


def reorganization_equity_distribution(
    tranches: list[dict[str, Any]],
    ev: float,
    new_debt_issued: float,
    cash_dist: float,
) -> dict[str, Any]:
    reorg_equity_val = round(max(0.0, ev - new_debt_issued - cash_dist), 6)
    return {
        "reorg_equity_value": reorg_equity_val,
        "cash_distributed": round(cash_dist, 6),
        "new_debt_distributed": round(new_debt_issued, 6),
        "tranche_distributions": [],
    }


def evaluate_expected_returns(
    tranches: list[dict[str, Any]],
    scenarios: list[dict[str, Any]],
    purchase_prices: dict[str, float],
    holding_period_years: float,
) -> dict[str, Any]:
    return {
        "holding_period_years": holding_period_years,
        "total_capital_invested": 0.0,
        "total_expected_recovery": 0.0,
        "portfolio_moic": 0.0,
        "portfolio_irr": -1.0,
        "tranche_returns": [],
    }


def run_waterfall_engine(instance: dict[str, Any]) -> dict[str, Any]:
    return {}
