"""Mutant 1: Allocates residual value pro-rata across remaining tranches violating strict absolute priority."""

from __future__ import annotations

import math
from typing import Any

from integrity import (  # type: ignore[import-not-found, unused-ignore]
    validate_tranches,
)


def calculate_waterfall_strict(
    tranches: list[dict[str, Any]],
    ev: float,
) -> list[dict[str, Any]]:
    """Allocate EV with pro-rata leakage across tranches."""
    validate_tranches(tranches)
    if not isinstance(ev, (int, float)) or not math.isfinite(ev) or ev < 0.0:
        raise ValueError(f"Enterprise value must be non-negative and finite, got {ev}")

    remaining_ev = float(ev)
    results: list[dict[str, Any]] = []

    # Bug: split remaining EV pro-rata among all debt tranches
    total_claims = sum(float(t["claim"]) for t in tranches if t["claim"] > 0)
    for t in tranches:
        claim = float(t["claim"])
        name = str(t["name"])
        sen = int(t["seniority"])

        if total_claims > 0 and claim > 0:
            allocated = min(claim, (claim / total_claims) * ev)
            recovery_pct = allocated / claim
            deficiency = claim - allocated
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

    return results


def calculate_waterfall_with_carveout(
    tranches: list[dict[str, Any]],
    ev: float,
    carveout: dict[str, Any],
) -> list[dict[str, Any]]:
    strict_results = calculate_waterfall_strict(tranches, ev)
    return strict_results


def reorganization_equity_distribution(
    tranches: list[dict[str, Any]],
    ev: float,
    new_debt_issued: float,
    cash_dist: float,
) -> dict[str, Any]:
    return {
        "reorg_equity_value": ev,
        "cash_distributed": cash_dist,
        "new_debt_distributed": new_debt_issued,
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
