"""Mutant: Returns a fixed heuristic fraction (0.50 * total_liabilities) instead of bisection search for peg break."""

from __future__ import annotations

from typing import Any

try:
    from integrity import validate_reserve_inputs  # type: ignore[import-not-found, unused-ignore]
except ImportError:
    from .integrity import validate_reserve_inputs  # type: ignore[import-not-found, unused-ignore]


def validate_inputs(
    total_liabilities: float,
    reserve_assets: dict[str, dict[str, float]],
    rate_shock_bps: float,
    peg_threshold: float,
) -> None:
    validate_reserve_inputs(total_liabilities, reserve_assets, rate_shock_bps, peg_threshold)


ORDERED_TIERS = ("cash", "overnight_repo", "tbills_short", "treasury_notes", "bank_deposits")


def apply_rate_shock(
    reserve_assets: dict[str, dict[str, float]],
    rate_shock_bps: float,
) -> dict[str, dict[str, float]]:
    if rate_shock_bps < 0.0:
        raise ValueError("rate_shock_bps must be non-negative")
    dy = rate_shock_bps / 10000.0
    shocked: dict[str, dict[str, float]] = {}
    for tier, data in reserve_assets.items():
        par = float(data["par"])
        duration = float(data["duration"])
        haircut = float(data["haircut"])
        price_factor = max(0.0, 1.0 - duration * dy)
        shocked[tier] = {
            "par": par,
            "duration": duration,
            "haircut": haircut,
            "market_value": par * price_factor,
        }
    return shocked


def simulate_redemption_waterfall(
    total_liabilities: float,
    shocked_assets: dict[str, dict[str, float]],
    redemptions: float,
) -> dict[str, Any]:
    if total_liabilities <= 0.0:
        raise ValueError("total_liabilities must be positive")
    if redemptions < 0.0:
        raise ValueError("redemptions cannot be negative")

    rem_redemption = redemptions
    total_haircut_loss = 0.0
    tier_details: dict[str, dict[str, float]] = {}

    current_mv: dict[str, float] = {}
    for tier in ORDERED_TIERS:
        current_mv[tier] = float(shocked_assets[tier]["market_value"]) if tier in shocked_assets else 0.0

    active_order = [t for t in ORDERED_TIERS if t in shocked_assets]

    for tier in active_order:
        data = shocked_assets[tier]
        mv = current_mv[tier]
        h = float(data["haircut"])
        avail_cash = mv * (1.0 - h)

        if rem_redemption <= 0.0:
            tier_details[tier] = {
                "initial_mv": mv,
                "mv_liquidated": 0.0,
                "cash_raised": 0.0,
                "haircut_loss": 0.0,
                "remaining_mv": mv,
            }
            continue

        if rem_redemption <= avail_cash:
            cash_from_tier = rem_redemption
            mv_used = cash_from_tier / (1.0 - h)
            loss = mv_used - cash_from_tier
            current_mv[tier] -= mv_used
            total_haircut_loss += loss
            rem_redemption = 0.0
            tier_details[tier] = {
                "initial_mv": mv,
                "mv_liquidated": mv_used,
                "cash_raised": cash_from_tier,
                "haircut_loss": loss,
                "remaining_mv": current_mv[tier],
            }
        else:
            cash_from_tier = avail_cash
            mv_used = mv
            loss = mv * h
            total_haircut_loss += loss
            rem_redemption -= cash_from_tier
            current_mv[tier] = 0.0
            tier_details[tier] = {
                "initial_mv": mv,
                "mv_liquidated": mv_used,
                "cash_raised": cash_from_tier,
                "haircut_loss": loss,
                "remaining_mv": 0.0,
            }

    cash_raised = redemptions - rem_redemption
    unfulfilled = rem_redemption
    remaining_tokens = max(0.0, total_liabilities - redemptions)
    remaining_mv = sum(current_mv.values())

    if unfulfilled > 1e-9:
        nav = 0.0
    elif remaining_tokens <= 1e-9:
        nav = 1.0
    else:
        nav = remaining_mv / remaining_tokens

    return {
        "nav": nav,
        "total_haircut_loss": total_haircut_loss,
        "cash_raised": cash_raised,
        "unfulfilled_redemptions": unfulfilled,
        "remaining_tokens": remaining_tokens,
        "remaining_market_value": remaining_mv,
        "tier_details": tier_details,
    }


def find_peg_break_run_size(
    total_liabilities: float,
    shocked_assets: dict[str, dict[str, float]],
    peg_threshold: float,
    tol: float = 1e-5,
) -> dict[str, Any]:
    # BUG: uses static heuristic guess 0.50 * total_liabilities
    r_star = 0.50 * total_liabilities
    nav_break = simulate_redemption_waterfall(total_liabilities, shocked_assets, r_star)["nav"]
    return {
        "peg_broken": True,
        "critical_run_amount": round(r_star, 4),
        "critical_run_pct": 0.50,
        "nav_at_break": round(nav_break, 6),
    }


def compute_liquidity_coverage_ratio(
    reserve_assets: dict[str, dict[str, float]],
    stressed_outflow_30d: float,
) -> float:
    if stressed_outflow_30d <= 0.0:
        raise ValueError("stressed_outflow_30d must be positive")
    cash_par = float(reserve_assets.get("cash", {}).get("par", 0.0))
    repo_par = float(reserve_assets.get("overnight_repo", {}).get("par", 0.0))
    return (cash_par + repo_par) / stressed_outflow_30d


def run_stress_grid(
    total_liabilities: float,
    base_assets: dict[str, dict[str, float]],
    rate_shocks_bps: list[float],
    redemption_fractions: list[float],
    peg_threshold: float = 0.995,
) -> dict[str, Any]:
    nav_matrix: list[list[float]] = []
    peg_breaks: dict[str, float] = {}
    for shock in rate_shocks_bps:
        shocked = apply_rate_shock(base_assets, shock)
        row: list[float] = []
        for frac in redemption_fractions:
            r = total_liabilities * frac
            res = simulate_redemption_waterfall(total_liabilities, shocked, r)
            row.append(round(res["nav"], 6))
        nav_matrix.append(row)
        pb = find_peg_break_run_size(total_liabilities, shocked, peg_threshold)
        peg_breaks[f"{shock:.1f}_bps"] = pb["critical_run_pct"]
    return {
        "rate_shocks_bps": rate_shocks_bps,
        "redemption_fractions": redemption_fractions,
        "nav_matrix": nav_matrix,
        "critical_run_pcts": peg_breaks,
    }
