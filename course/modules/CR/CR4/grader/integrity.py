"""Input validation helpers for the CR4 recovery waterfall and fulcrum engine.

Validates input types, dimensions, bounded domains, and mathematical consistency.
Raises ValueError on invalid numerical domains or lengths, and TypeError on bad types.
"""

from __future__ import annotations

import math
from typing import Any


def validate_tranches(tranches: list[dict[str, Any]]) -> None:
    """Validate capital structure tranche definitions."""
    if not isinstance(tranches, list):
        raise TypeError("tranches must be a list of dictionaries")
    if len(tranches) < 2:
        raise ValueError(f"tranches must contain at least 2 tranches, got {len(tranches)}")

    names: set[str] = set()
    prev_seniority = 0
    for idx, t in enumerate(tranches):
        if not isinstance(t, dict):
            raise TypeError(f"tranche[{idx}] must be a dictionary")
        for req in ["name", "claim", "seniority"]:
            if req not in t:
                raise ValueError(f"tranche[{idx}] missing required key '{req}'")

        name = t["name"]
        if not isinstance(name, str) or not name.strip():
            raise TypeError(f"tranche[{idx}]['name'] must be a non-empty string")
        if name in names:
            raise ValueError(f"Duplicate tranche name: '{name}'")
        names.add(name)

        claim = t["claim"]
        if not isinstance(claim, (int, float)):
            raise TypeError(f"tranche[{idx}]['claim'] must be a float or int")
        if not math.isfinite(claim) or claim < 0.0:
            raise ValueError(f"tranche[{idx}]['claim'] must be a non-negative finite number, got {claim}")

        sen = t["seniority"]
        if not isinstance(sen, int):
            raise TypeError(f"tranche[{idx}]['seniority'] must be an integer")
        if sen <= prev_seniority:
            raise ValueError(
                f"Seniority must be strictly increasing: tranche[{idx}] has {sen} <= previous {prev_seniority}"
            )
        prev_seniority = sen


def validate_scenarios(scenarios: list[dict[str, Any]]) -> None:
    """Validate enterprise value valuation scenarios."""
    if not isinstance(scenarios, list):
        raise TypeError("scenarios must be a list of dictionaries")
    if len(scenarios) < 2:
        raise ValueError(f"scenarios must contain at least 2 scenarios, got {len(scenarios)}")

    names: set[str] = set()
    total_prob = 0.0
    for idx, s in enumerate(scenarios):
        if not isinstance(s, dict):
            raise TypeError(f"scenario[{idx}] must be a dictionary")
        for req in ["name", "ev", "prob"]:
            if req not in s:
                raise ValueError(f"scenario[{idx}] missing required key '{req}'")

        name = s["name"]
        if not isinstance(name, str) or not name.strip():
            raise TypeError(f"scenario[{idx}]['name'] must be a non-empty string")
        if name in names:
            raise ValueError(f"Duplicate scenario name: '{name}'")
        names.add(name)

        ev = s["ev"]
        if not isinstance(ev, (int, float)):
            raise TypeError(f"scenario[{idx}]['ev'] must be a float or int")
        if not math.isfinite(ev) or ev < 0.0:
            raise ValueError(f"scenario[{idx}]['ev'] must be a non-negative finite number, got {ev}")

        prob = s["prob"]
        if not isinstance(prob, (int, float)):
            raise TypeError(f"scenario[{idx}]['prob'] must be a float or int")
        if not math.isfinite(prob) or prob < 0.0 or prob > 1.0:
            raise ValueError(f"scenario[{idx}]['prob'] must be in [0, 1], got {prob}")
        total_prob += float(prob)

    if abs(total_prob - 1.0) > 1e-5:
        raise ValueError(f"Scenario probabilities must sum to 1.0, got {total_prob:.6f}")


def validate_carveout(carveout: dict[str, Any], tranche_names: list[str]) -> None:
    """Validate consensual plan carve-out / APR violation settings."""
    if not isinstance(carveout, dict):
        raise TypeError("carveout must be a dictionary")
    for req in ["source_tranche", "target_tranche", "carveout_pct"]:
        if req not in carveout:
            raise ValueError(f"carveout missing required key '{req}'")

    src = carveout["source_tranche"]
    tgt = carveout["target_tranche"]
    pct = carveout["carveout_pct"]

    if src not in tranche_names:
        raise ValueError(f"Source tranche '{src}' not found in tranches")
    if tgt not in tranche_names:
        raise ValueError(f"Target tranche '{tgt}' not found in tranches")
    if src == tgt:
        raise ValueError("Source and target tranches must be different")

    if not isinstance(pct, (int, float)):
        raise TypeError("carveout_pct must be a float")
    if not math.isfinite(pct) or pct < 0.0 or pct > 1.0:
        raise ValueError(f"carveout_pct must be in [0, 1], got {pct}")


def validate_por_params(ev: float, new_debt: float, cash_dist: float) -> None:
    """Validate Plan of Reorganization (POR) distribution parameters."""
    for val, name in [(ev, "ev"), (new_debt, "new_debt"), (cash_dist, "cash_dist")]:
        if not isinstance(val, (int, float)):
            raise TypeError(f"{name} must be a float or int")
        if not math.isfinite(val) or val < 0.0:
            raise ValueError(f"{name} must be a non-negative finite number, got {val}")

    if (new_debt + cash_dist) > ev + 1e-9:
        raise ValueError(
            f"New debt ({new_debt}) + cash ({cash_dist}) = {new_debt + cash_dist} exceeds enterprise value ({ev})"
        )


def validate_returns_params(purchase_prices: dict[str, float], holding_period: float) -> None:
    """Validate investor purchase prices and holding period."""
    if not isinstance(purchase_prices, dict):
        raise TypeError("purchase_prices must be a dictionary")
    for name, price in purchase_prices.items():
        if not isinstance(name, str):
            raise TypeError("purchase_prices keys must be strings")
        if not isinstance(price, (int, float)):
            raise TypeError(f"purchase_prices['{name}'] must be a float")
        if not math.isfinite(price) or price <= 0.0:
            raise ValueError(f"purchase_prices['{name}'] must be strictly positive, got {price}")

    if not isinstance(holding_period, (int, float)):
        raise TypeError("holding_period must be a float or int")
    if not math.isfinite(holding_period) or holding_period <= 0.0:
        raise ValueError(f"holding_period must be strictly positive, got {holding_period}")
